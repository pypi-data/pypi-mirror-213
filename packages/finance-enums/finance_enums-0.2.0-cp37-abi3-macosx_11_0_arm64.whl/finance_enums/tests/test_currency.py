from finance_enums import Currency


class TestCurrency:
    def test_currency_basic(self):
        assert len(Currency.members()) == 180
        assert str(Currency.USD) == "USD"
        assert Currency.USD.name == "United States dollar"
