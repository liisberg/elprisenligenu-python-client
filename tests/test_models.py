import unittest

from elprisenligenu.models import ElectricityPrice


class ElectricityPriceTests(unittest.TestCase):
    def test_dkk_per_kwh_incl_vat_rounds_to_five_decimals(self):
        price = ElectricityPrice(
            dkk_per_kwh=0.1234567,
            eur_per_kwh=0.0,
            exchange_rate=7.5,
            start="",
            end="",
        )

        self.assertEqual(price.dkk_per_kwh_incl_vat, 0.15432)


if __name__ == "__main__":
    unittest.main()
