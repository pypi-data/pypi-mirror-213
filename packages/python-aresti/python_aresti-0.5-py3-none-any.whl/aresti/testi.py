import functools


class SisempiLuokka:
  def __init__(self, sisempi_luokka):
    self.sisempi_luokka = sisempi_luokka

  def __get__(self, instance, cls=None):
    #if isinstance(
    #  self.sisempi_luokka, RajapinnanTyyppi
    #):
    #  # pylint: disable=invalid-name
    #  _Meta = type(self.sisempi_luokka)
    #else:
    #  class _Meta(
    #    RajapinnanTyyppi,
    #    type(self.sisempi_luokka)
    #  ):
    #    pass
    @functools.wraps(
      self.sisempi_luokka,
      updated=()
    )
    class _SisempiLuokka(
      self.sisempi_luokka,
      #metaclass=_Meta,
    ):
      def __init__(self2, *args, **kwargs):
        # pylint: disable=no-self-argument
        super().__init__(
          instance,
          *args,
          **kwargs
        )
    return _SisempiLuokka
    # def __get__

  # class SisempiLuokka


class RajapinnanTyyppi(type):

  def __new__(mcs, name, bases, attrs, **kwargs):
    return super().__new__(
      mcs,
      name,
      bases,
      {
        avain: (
          SisempiLuokka(arvo)
          if isinstance(arvo, type)
          else arvo
        )
        for avain, arvo in attrs.items()
      },
      **kwargs
    )
    # def __new__

  # class RajapinnanTyyppi


if __name__ == '__main__':
  class A(metaclass=RajapinnanTyyppi):
    class B:
      def __init__(self, rajapinta):
        print('B.__init__', rajapinta)
        self.rajapinta = rajapinta
        # def __init__
      #class C:
      #  def __init__(self, *args, **kwargs):
      #    print('C.__init__', self, args, kwargs)
  a = A()
  b = a.B()
  #c = b.C()
