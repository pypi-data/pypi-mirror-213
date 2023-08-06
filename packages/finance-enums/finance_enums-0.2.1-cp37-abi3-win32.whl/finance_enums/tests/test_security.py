from finance_enums import (
    SecurityType,
    EquityType,
    OptionType,
    BondType,
    CommodityType,
    FundType,
    OptionExerciseType,
    FundSubType,
    MutualFundEndedness,
)


class TestSecurityType:
    def test_security_type_basic(self):
        assert len(SecurityType.members()) == 12

    def test_equity_type_basic(self):
        assert len(EquityType.members()) == 5

    def test_option_type_basic(self):
        assert len(OptionType.members()) == 2

    def test_bond_type_basic(self):
        assert len(BondType.members()) == 3

    def test_commodity_type_basic(self):
        assert len(CommodityType.members()) == 3

    def test_fund_type_basic(self):
        assert len(FundType.members()) == 3

    def test_option_exercise_type_basic(self):
        assert len(OptionExerciseType.members()) == 3

    def test_fund_subtype_basic(self):
        assert len(FundSubType.members()) == 4

    def test_mutual_fund_endedness_basic(self):
        assert len(MutualFundEndedness.members()) == 2
