from finance_enums import OrderType, Side, TimeInForce, OrderFlag


class TestCurrency:
    def test_order_type_basic(self):
        assert len(OrderType.members()) == 3

    def test_side_basic(self):
        assert len(Side.members()) == 2

    def test_time_in_force_basic(self):
        assert len(TimeInForce.members()) == 2

    def test_order_flag_basic(self):
        assert len(OrderFlag.members()) == 4
