"""The dataset adapters, by source id."""

from __future__ import annotations

from collections.abc import Callable

from canary.adapters.base import Adapter
from canary.adapters.cline import ClineCoups
from canary.adapters.ewp import EwpSra
from canary.adapters.owid import SERIES, OurWorldInData
from canary.adapters.reference import GeoNames, NaturalEarth, Wikidata
from canary.adapters.ucdp import UcdpCandidate, UcdpGed, UcdpPrioAcd
from canary.adapters.vdem import VdemCountryYear, VdemErt
from canary.adapters.worldbank import WorldBank

ADAPTERS: dict[str, Callable[[], Adapter]] = {
    "vdem-country-year": VdemCountryYear,
    "vdem-ert": VdemErt,
    "ucdp-candidate": UcdpCandidate,
    "ucdp-ged": UcdpGed,
    "ucdp-prio-acd": UcdpPrioAcd,
    "world-bank-indicators": WorldBank,
    "our-world-in-data": lambda: OurWorldInData(SERIES),
    "ewp-sra": EwpSra,
    "cline-coups": ClineCoups,
    "geonames": GeoNames,
    "wikidata": Wikidata,
    "natural-earth": NaturalEarth,
}
