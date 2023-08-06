from dataclasses import dataclass, is_dataclass
import functools
from typing import get_type_hints
from urllib.parse import urlencode

from aresti.rest import RestYhteys
from aresti.sanoma import RestSanoma

from .meta import RajapinnanTyyppi
from .nakyma import Nakyma
from .tyokalut import nested_dataclass
from .vierasavain import (
  SisempiNakyma,
  Vierasavain,
)


class Rajapinta(
  RestYhteys,
  metaclass=RajapinnanTyyppi,
):

  @classmethod
  def nakyma(cls, polku):
    def _nakyma(cls2):
      _polku = polku
      @dataclass
      @functools.wraps(cls2, updated=())
      class _Nakyma(cls2, Nakyma):
        class Meta(
          *((cls2.Meta, ) if hasattr(cls2, 'Meta') else ()),
          Nakyma.Meta
        ):
          polku = _polku

        @type.__call__
        class _rest:
          def __get__(self, instance, cls=None):
            cls = cls or type(instance)
            tyypit = get_type_hints(cls, localns=cls2.__dict__)
            rest = dict(**vars(cls).get('_rest', {}))
            print('NT.new 0', repr(rest), repr(tyypit))
            return {**{
              avain: (
                rest.pop(avain, avain),
                lambda lahteva: nakyma.lahteva(lahteva),
                lambda saapuva: nakyma.saapuva(saapuva),
              )
              for avain, nakyma in (
                (avain, nakyma())
                for avain, nakyma in tyypit.items()
                if issubclass(nakyma, RestSanoma)
              )
            }, **rest}

      return _Nakyma
    return _nakyma
    # def nakyma

  @classmethod
  def sanoma(cls):
    return dataclass(
      functools.wraps(cls, updated=())(
        type(cls.__name__, (cls, RestSanoma), {})
      )
    )
    # def sanoma

  @classmethod
  def hakukriteerit(cls, **haku):
    return urlencode(haku)

  @classmethod
  def yksio(cls):
    return Nakyma.yksio(cls)

  @classmethod
  def vierasavain(cls, *args, **kwargs):
    @type.__call__
    class _vierasavain:
      def __get__(self, instance, cls2=None):
        vierasavain = Vierasavain(*args, **kwargs)
        vierasavain.Meta.rajapinta = cls2.Meta.rajapinta
    return _vierasavain
    # def vierasavain

  @classmethod
  def sisempi_nakyma(cls, nakyma):
    class _sisempi_nakyma:
      def __get__(self, instance, cls2=None):
        return getattr(cls2.Meta.rajapinta, nakyma)
    return _sisempi_nakyma
    # def sisempi_nakyma

  def polku_oletus(self, nakyma):
    return nakyma.__name__.lower() + '/'

  def rajapintakohtainen_nakyma(self, nakyma):
    nakyma_meta = getattr(nakyma, 'Meta', None)
    @functools.wraps(nakyma, updated=())
    class _Nakyma(nakyma, Nakyma):
      class Meta(*((nakyma_meta, ) if nakyma_meta else ()), Nakyma.Meta):
        rajapinta = self
        if nakyma_meta is None or not hasattr(nakyma_meta, 'polku'):
          polku = self.polku_oletus(nakyma)
        # class Meta
      if nakyma_meta is not None:
        Meta = functools.wraps(nakyma_meta, updated=())(Meta)
      # class _Nakyma
    _Nakyma.__annotations__.setdefault(
      _Nakyma.Meta.primaariavain, str
    )
    return _Nakyma
    #return dataclass(_Nakyma)
    # def rajapintakohtainen_nakyma

  def __getattribute__(self, avain):
    '''
    Asetetaan Rajapinnan määreinä määriteltyihin
    ``dataclass``-alaluokkiin (näkymät) `Meta.rajapinta`-määre.
    '''
    arvo = super().__getattribute__(avain)
    if isinstance(arvo, type) and issubclass(arvo, Nakyma):
      return self.rajapintakohtainen_nakyma(arvo)
    return arvo
    # def __getattribute__

  # class Rajapinta
