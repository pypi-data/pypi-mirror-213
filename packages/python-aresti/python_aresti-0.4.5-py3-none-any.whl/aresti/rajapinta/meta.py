import functools


class SisempiLuokka:
  def __init__(self, sisempi_luokka):
    self.sisempi_luokka = sisempi_luokka

  def __get__(self, instance, cls=None):
    @functools.wraps(
      self.sisempi_luokka,
      updated=()
    )
    class _SisempiLuokka(self.sisempi_luokka):
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

  def x___new__(mcs, name, bases, attrs, **kwargs):
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
