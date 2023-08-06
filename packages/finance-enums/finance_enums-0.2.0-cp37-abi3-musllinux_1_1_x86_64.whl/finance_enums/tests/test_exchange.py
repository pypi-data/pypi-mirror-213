from finance_enums import Exchange


class TestExchange:
    def test_exchange_basic(self):
        assert len(Exchange.members()) == 21
