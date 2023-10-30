from enum import StrEnum

from pydantic import BaseModel


class ThreeLetterIsoCode(StrEnum):
    DEU = "DEU"
    GBR = "GBR"
    USA = "USA"


class EnergyDataRecord(BaseModel):
    iso_code: ThreeLetterIsoCode = ThreeLetterIsoCode.DEU
    renewables_consumption: float = 0
