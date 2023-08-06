# -*- coding: utf-8 -*-
# pylint: disable=protected-access, not-an-iterable

import os

import pkg_resources


def _jakelu_sisaltaa_tiedoston(jakelu):
  '''
  Palauttaa testifunktion, joka ottaa tiedostonimen ja palauttaa
  boolean-tyyppisen tiedon tiedoston sisältymisestä annettuun jakeluun.
  '''
  try:
    # Hae asennetun paketin (pip install) tiedostoluettelo.
    # Python-moduuli (esim. .../site-packages/x/y/z.py) sisältyy
    # pakettiin, mikäli se esiintyy tiedostoluettelossa.
    return [
      os.path.realpath(
        os.path.normpath(
          os.path.join(jakelu.location, r.split(',')[0])
        )
      )
      for r in jakelu.get_metadata_lines('RECORD')
    ].__contains__
  except FileNotFoundError:
    pass

  try:
    # Hae luettelon asennetun paketin sisältämistä
    # ylimmän tason moduuleista. Tutkitaan sisältyykö tiedosto
    # johonkin niistä.
    return lambda t: any(
      os.path.commonpath((
        os.path.realpath(os.path.normpath(t)),
        os.path.realpath(
          os.path.normpath(
            os.path.join(jakelu.location, toplevel)
          )
        )
      )) == os.path.realpath(
        os.path.normpath(
          os.path.join(jakelu.location, toplevel)
        )
      )
      for toplevel in jakelu.get_metadata_lines('top_level.txt')
    )
  except FileNotFoundError:
    pass

  # Kehitystilassa (pip install -e) oleva paketti.
  # Python-moduuli (esim. ~/git/a/x/y/z.py) sisältyy pakettiin,
  # mikäli se sijaitsee paketin sisällä (~/git/a/).
  return lambda t: os.path.commonpath((
    t, os.path.realpath(jakelu.location)
  )) == os.path.realpath(jakelu.location)

  # def _jakelu_sisaltaa_tiedoston


# Muodosta käännöksenaikaisesti luettelo paketeista
# ja testeistä moduulin sisältymisestä niihin.
# Vrt. https://stackoverflow.com/a/56032725
def _jakelut():
  # pylint: disable=no-method-argument
  for jakelu in pkg_resources.working_set:
    yield (jakelu, _jakelu_sisaltaa_tiedoston(jakelu))
_jakelut = list(_jakelut())


# Käytetään globaalia välimuistisanakirjaa:
# juurimoduulin nimi -> jakelu.
_valimuisti = {}

def _jakelu(moduuli):
  '''
  Hae se pip-paketti, johon annettu moduuli sisältyy.

  Raises:
    ValueError: moduuli ei sisälly mihinkään pip-pakettiin.

  Return:
    pkg_resources.Distribution
  '''
  # Tutkitaan vain moduulipolun ensimmäistä osaa.
  juurimoduuli = moduuli.__name__.split('.')[0]

  # Haetaan välimuistista.
  try: return _valimuisti[juurimoduuli]
  except KeyError: pass

  # Otetaan moduulin tiedostopolku.
  try: tiedosto = os.path.realpath(moduuli.__file__)
  except (AttributeError, KeyError): return None

  # Haetaan asennetuista paketeista, tallennetaan välimuistiin.
  try:
    jakelu = _valimuisti[juurimoduuli] = next(
      jakelu for jakelu, testi in _jakelut if testi(tiedosto)
    )
  except StopIteration:
    return None
  else:
    return jakelu
    # else
  # def _jakelu
