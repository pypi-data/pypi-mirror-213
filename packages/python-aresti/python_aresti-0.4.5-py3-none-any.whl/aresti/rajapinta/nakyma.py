from __future__ import annotations

from dataclasses import dataclass, fields, is_dataclass
import functools
from typing import get_type_hints

from aresti.sanoma import RestSanoma
from aresti.tyokalut import (
  luokka_tai_oliometodi,
  luokkamaare,
)
from aresti.rest import RestYhteys

from .meta import RajapinnanTyyppi


class NakymanTyyppi(type(RestSanoma)):

  def x__new__(mcs, name, bases, attrs, **kwargs):
    cls = super().__new__(mcs, name, bases, attrs, **kwargs)
    if hasattr(cls, '_avattu_rest_'):
      print('NT.new X', repr(cls))
      return cls
    cls._avattu_rest_ = True
    rest = dict(**cls._rest)
    print('NT.new 0', repr(rest))
    _rest = {**{
      avain: (
        rest.pop(avain, avain),
        nakyma.saapuva,
        nakyma.lahteva,
      )
      for avain, nakyma in get_type_hints(cls).items()
      if issubclass(nakyma, RestSanoma)
    }, **rest}
    cls._rest = _rest
    print('NT.new 1', repr(cls._rest))
    return cls
    # def __new__

  def __getattribute__(cls, avain):
    '''
    Asetetaan Näkymän määreinä määriteltyihin
    ``dataclass``-alaluokkiin (sisemmät näkymät)
    `Meta.rajapinta`-määre.
    '''
    print('NakymanTyyppi.__getattribute__', cls, avain)
    arvo = super().__getattribute__(avain)
    if isinstance(arvo, type) and is_dataclass(arvo):
      return cls.Meta.rajapinta.rajapintakohtainen_nakyma(arvo)
    return arvo
    # def __getattribute__

  # class NakymanTyyppi


class Nakyma(RestSanoma, metaclass=NakymanTyyppi):

  def __init__(self, rajapinta, *args, rest=None, **kwargs):
    super().__init__(*args, **kwargs)
    self.rajapinta = rajapinta
    # def __init__

  class Meta:
    rajapinta: 'Rajapinta'
    polku: str
    primaariavain: str = 'id'
    @luokkamaare
    def crud(cls) -> dict:
      # pylint: disable=no-self-argument
      return {
        'nouda_kaikki': f'{cls.polku}',
        'nouda': f'{cls.polku}/%(avain)s',
        'lisaa': f'{cls.polku}',
        'muuta': f'{cls.polku}/%(avain)s',
        'tuhoa': f'{cls.polku}/%(avain)s',
      }

  @luokka_tai_oliometodi
  async def nouda(cls, **haku) -> ['Nakyma']:
    # pylint: disable=no-self-argument
    async def _nouda(rajapinta, polku):
      osoite = rajapinta.palvelin + polku
      while True:
        sivullinen = await rajapinta.nouda_data(
          osoite,
          suhteellinen=False,
        )
        if 'results' in sivullinen:
          for tulos in sivullinen['results']:
            yield tulos
          osoite = sivullinen.get('next')
          if osoite is None:
            return
            # if osoite is None
        else:
          for tulos in sivullinen:
            yield tulos
          return
        # while True
      # async def _nouda
    async for tietue in _nouda(
      rajapinta=cls.Meta.rajapinta,
      polku='?'.join(filter(None, (
        cls.Meta.crud['nouda_kaikki'],
        cls.Meta.rajapinta.hakukriteerit(**haku),
      ))),
    ):
      try:
        #print(repr(tietue))
        print('nouda.tulos', repr(cls.saapuva(tietue)))
        print(fields(cls))
        print(__import__('inspect').getsource(cls.saapuva))
        yield cls.saapuva(tietue)
      except BaseException as exc:
        raise #RuntimeError(', '.join((repr(cls), repr(tietue), repr(exc))))
    # async def nouda

  @nouda.oliometodi
  async def nouda(self) -> 'Nakyma':
    ''' Päivitä ``self`` rajapinnasta. '''
    assert (avain := getattr(self, self.Meta.primaariavain, False))
    haettu = self.saapuva(
      await self.Meta.rajapinta.nouda_data(
        self.Meta.crud['nouda'] % {'avain': avain}
      )
    )
    self.__dict__.update(haettu.__dict__)
    return self
    # async def nouda

  async def lisaa(self):
    if getattr(self, self.Meta.primaariavain, False):
      return await self.muuta()
    await self.Meta.rajapinta.lisaa_data(
      self.Meta.crud['lisaa'],
      self.lahteva()
    )
    # async def lisaa

  async def muuta(self):
    assert (avain := getattr(self, self.Meta.primaariavain, False))
    await self.Meta.rajapinta.muuta_data(
      self.Meta.crud['muuta'] % {'avain': avain},
      self.lahteva()
    )
    # async def muuta

  async def tuhoa(self):
    assert (avain := getattr(self, self.Meta.primaariavain, False))
    await self.Meta.rajapinta.tuhoa_data(
      self.Meta.crud['tuhoa'] % {'avain': avain},
    )
    # async def tuhoa

  @staticmethod
  def yksio(cls):
    ''' Merkitse REST-näkymä yksittäiseen riviin rajoittuvaksi. '''
    @functools.wraps(cls, updated=())
    class Yksio(cls):
      class Meta(*(
        (cls.Meta, ) if hasattr(cls, 'Meta') else ()
      ), Nakyma.Meta):
        crud = {
          'nouda': f'{cls.Meta.polku}',
          'lisaa': f'{cls.Meta.polku}',
        }
      @luokka_tai_oliometodi
      async def nouda(cls) -> 'Yksio':
        # pylint: disable=no-member
        return cls.saapuva(await cls.Meta.rajapinta.nouda_data(
          cls.Meta.crud['nouda']
        ))
        # async def nouda

      @nouda.oliometodi
      async def nouda(self) -> 'Yksio':
        haettu = self.saapuva(
          await self.Meta.rajapinta.nouda_data(
            self.Meta.crud['nouda']
          )
        )
        self.__dict__.update(haettu.__dict__)
        return self
        # async def nouda

      async def muuta(self):
        await self.Meta.rajapinta.lisaa_data(
          self.Meta.crud['lisaa'],
          self.lahteva()
        )
        # async def muuta

      async def toimintoa_ei_ole(self):
        raise RuntimeError('Toiminto ei mahdollinen')

      lisaa = tuhoa = toimintoa_ei_ole
      # class Yksio
    return Yksio
    # def yksio

  def __getattribute__(self, avain):
    '''
    Asetetaan Näkymän määreinä määriteltyihin
    ``dataclass``-alaluokkiin (sisemmät näkymät)
    `Meta.rajapinta`-määre.
    '''
    print('Nakyma.__getattribute__', self, avain)
    arvo = super().__getattribute__(avain)
    if isinstance(arvo, type) and is_dataclass(arvo):
      return self.Meta.rajapinta.rajapintakohtainen_nakyma(arvo)
    return arvo
    # def __getattribute__

  # class Nakyma
