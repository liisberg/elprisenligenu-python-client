from dataclasses import dataclass


@dataclass
class ElectricityPrice:
    dkk_per_kwh: float
    eur_per_kwh: float
    exchange_rate: float
    start: str
    end: str

    @property
    def dkk_per_kwh_incl_vat(self) -> float:
        """Price in DKK per kWh including 25% VAT."""
        return round(self.dkk_per_kwh * 1.25, 5)
