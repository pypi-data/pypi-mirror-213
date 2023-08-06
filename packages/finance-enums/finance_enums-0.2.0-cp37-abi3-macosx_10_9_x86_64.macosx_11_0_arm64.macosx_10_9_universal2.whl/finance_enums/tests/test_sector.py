from finance_enums import Sector, IndustryGroup, Industry, SubIndustry


class TestSector:
    def test_sector_basic(self):
        assert len(Sector.members()) == 11

    def test_industry_group_basic(self):
        assert len(IndustryGroup.members()) == 25

    def test_industry_basic(self):
        assert len(Industry.members()) == 74

    def test_subindustry_basic(self):
        assert len(SubIndustry.members()) == 163
