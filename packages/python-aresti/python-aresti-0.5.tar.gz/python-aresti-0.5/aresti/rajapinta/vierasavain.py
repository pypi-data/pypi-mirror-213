from dataclasses import dataclass, is_dataclass

from aresti.sanoma import RestSanoma


@dataclass
class Vierasavain(RestSanoma):
  class Meta:
    rajapinta: 'aresti.rajapinta.Rajapinta'

  nakyma: str
  vierasavain: str = 'id'

  @type.__call__
  class _nakyma:
    def __get__(self, instance, cls=None):
      cls = cls or type(instance)
      nakyma = getattr(
        cls.Meta.rajapinta,
        cls.nakyma
      )
      if instance is not None:
        instance.__dict__['_nakyma'] = nakyma
      return nakyma
      # def __get__
    # class _nakyma

  def lahteva(self, sanoma):
    return {
      self.vierasavain: getattr(sanoma, self._nakyma.Meta.primaariavain),
      #self.vierasavain: self._nakyma.lahteva(sanoma)[
      #  self._nakyma.Meta.primaariavain
      #]
    }

  @classmethod
  def saapuva(cls, sanoma):
    return cls._nakyma(**{
      cls._nakyma.Meta.primaariavain: sanoma[cls.vierasavain]
    })
    #return cls._nakyma.saapuva({
    #  cls._nakyma.Meta.primaariavain: sanoma[self.vierasavain]
    #})

  # class Vierasavain


@dataclass
class SisempiNakyma(RestSanoma):
  class Meta:
    rajapinta: 'aresti.rajapinta.Rajapinta'

  nakyma: str

  @type.__call__
  class _nakyma:
    def __get__(self, instance, cls=None):
      cls = cls or type(instance)
      nakyma = getattr(
        cls.Meta.rajapinta,
        cls.nakyma
      )
      if instance is not None:
        instance.__dict__['_nakyma'] = nakyma
      return nakyma
      # def __get__
    # class _nakyma

  def lahteva(self, sanoma):
    return self._nakyma.lahteva(sanoma)
    # def lahteva

  @classmethod
  def saapuva(cls, sanoma):
    return cls._nakyma.saapuva(sanoma)
    # def saapuva

  # class SisempiNakyma
