use pyo3::prelude::*;
use pyo3::types::PyType;
use strum::IntoEnumIterator;
use std::str::FromStr;

use finance_enums::{SubIndustry as BaseSubIndustry};
use super::Industry;

#[pyclass]
pub struct SubIndustry {
    pub typ: BaseSubIndustry,
}

#[pymethods]
impl SubIndustry {
    #[new]
    fn py_new(value: String) -> PyResult<Self> {
        Ok(
            SubIndustry {
                typ: BaseSubIndustry::from_str(value.as_str()).unwrap()
            }
        )

    }

    fn __str__(&self) -> PyResult<String>   {
        Ok(format!("{}", self.typ.to_string()))
    }

    fn __repr__(&self) -> PyResult<String>   {
        Ok(format!("SubIndustry<{}>", self.typ.to_string()))
    }

    fn __eq__(&self, other: &Self) -> bool   {
        self.typ == other.typ
    }

    fn industry(&self) -> Industry {
        Industry {
            typ: self.typ.industry()
        }
    }

    #[classmethod]
    fn __len__(_cls: &PyType) -> PyResult<usize> {
        Ok(BaseSubIndustry::iter().count())
    }

    // TODO figure out how to make a class iterator,
    // is way too complicated in pyo3 rn
    #[staticmethod]
    fn members() -> Vec<SubIndustry> {
        BaseSubIndustry::iter().map(|item: BaseSubIndustry| SubIndustry{typ: item} ).collect()
    }

    #[classattr]
    #[allow(non_snake_case)]
    fn OilAndGasDrilling() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::OilAndGasDrilling
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn OilAndGasEquipmentAndServices() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::OilAndGasEquipmentAndServices
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn IntegratedOilAndGas() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::IntegratedOilAndGas
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn OilAndGasExplorationAndProduction() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::OilAndGasExplorationAndProduction
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn OilAndGasRefiningAndMarketing() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::OilAndGasRefiningAndMarketing
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn OilAndGasStorageAndTransportation() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::OilAndGasStorageAndTransportation
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn CoalAndConsumeableFuels() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::CoalAndConsumeableFuels
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn CommodityChemicals() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::CommodityChemicals
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn DiversifiedChemicals() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::DiversifiedChemicals
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn FertilizersAndAgriculturalChemicals() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::FertilizersAndAgriculturalChemicals
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn IndustrialGases() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::IndustrialGases
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn SpecialtyChemicals() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::SpecialtyChemicals
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn ConstructionMaterials() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::ConstructionMaterials
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn MetalGlassAndPlasticContainers() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::MetalGlassAndPlasticContainers
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn PaperAndPlasticPackagingProductsAndMaterials() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::PaperAndPlasticPackagingProductsAndMaterials
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn Aluminum() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::Aluminum
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn DiversifiedMetalsAndMining() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::DiversifiedMetalsAndMining
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn Copper() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::Copper
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn Gold() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::Gold
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn PreciousMetalsAndMinerals() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::PreciousMetalsAndMinerals
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn Silver() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::Silver
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn Steel() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::Steel
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn ForestProducts() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::ForestProducts
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn PaperProducts() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::PaperProducts
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn AerospaceAndDefense() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::AerospaceAndDefense
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn BuildingProducts() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::BuildingProducts
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn ConstructionAndEngineering() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::ConstructionAndEngineering
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn ElectricalComponentsAndEquipment() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::ElectricalComponentsAndEquipment
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn HeavyElectricalEquipment() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::HeavyElectricalEquipment
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn IndustrialConglomerates() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::IndustrialConglomerates
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn ConstructionMachineryAndHeavyTransportationEquipment() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::ConstructionMachineryAndHeavyTransportationEquipment
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn AgriculturalAndFarmMachinery() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::AgriculturalAndFarmMachinery
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn IndustrialMachinerySuppliesAndComponents() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::IndustrialMachinerySuppliesAndComponents
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn TradingCompaniesAndDistributors() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::TradingCompaniesAndDistributors
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn CommercialPrinting() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::CommercialPrinting
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn EnvironmentalAndFacilitiesServices() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::EnvironmentalAndFacilitiesServices
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn OfficeServicesAndSupplies() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::OfficeServicesAndSupplies
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn DiviersifiedSupportServices() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::DiviersifiedSupportServices
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn SecurityAndAlarmServices() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::SecurityAndAlarmServices
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn HumanResourcesAndEmploymentServices() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::HumanResourcesAndEmploymentServices
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn ResearchAndConsultingServices() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::ResearchAndConsultingServices
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn DataProcessingAndOutsourcedServices() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::DataProcessingAndOutsourcedServices
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn AirFreightAndLogistics() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::AirFreightAndLogistics
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn PassengerAirlines() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::PassengerAirlines
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn MarineTransportation() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::MarineTransportation
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn RailTransportation() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::RailTransportation
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn CargoGroundTransportation() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::CargoGroundTransportation
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn PassengerGroundTransportation() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::PassengerGroundTransportation
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn AirportServices() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::AirportServices
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn HighwaysAndRailtracks() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::HighwaysAndRailtracks
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn MarinePortsAndServices() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::MarinePortsAndServices
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn AutomotivePartsAndEquipment() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::AutomotivePartsAndEquipment
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn TiresAndRubber() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::TiresAndRubber
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn AutomobileManufacturers() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::AutomobileManufacturers
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn MotorcycleManufacturers() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::MotorcycleManufacturers
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn ConsumerElectronics() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::ConsumerElectronics
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn HomeFurnishings() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::HomeFurnishings
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn Homebuilding() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::Homebuilding
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn HouseholdAppliances() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::HouseholdAppliances
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn HousewaresAndSpecialties() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::HousewaresAndSpecialties
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn LeisureProducts() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::LeisureProducts
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn ApparelAccessoriesAndLuxuryGoods() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::ApparelAccessoriesAndLuxuryGoods
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn Footwear() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::Footwear
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn Textiles() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::Textiles
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn CasinosAndGaming() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::CasinosAndGaming
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn HotelsResortsAndCruiseLines() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::HotelsResortsAndCruiseLines
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn LeisureFacilities() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::LeisureFacilities
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn Restaurants() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::Restaurants
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn EducationServices() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::EducationServices
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn SpecializedConsumerServices() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::SpecializedConsumerServices
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn Distributors() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::Distributors
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn BroadlineRetail() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::BroadlineRetail
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn ApparelRetail() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::ApparelRetail
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn ComputerAndElectronicsretail() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::ComputerAndElectronicsretail
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn HomeImprovementRetail() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::HomeImprovementRetail
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn OtherSpecialtyRetail() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::OtherSpecialtyRetail
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn AutomotiveRetail() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::AutomotiveRetail
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn HomefurnishingRetail() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::HomefurnishingRetail
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn DrugRetail() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::DrugRetail
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn FoodDistributors() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::FoodDistributors
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn FoodRetail() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::FoodRetail
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn ConsumerStaplesMerchandiseRetail() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::ConsumerStaplesMerchandiseRetail
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn Brewers() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::Brewers
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn DistillersAndVintners() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::DistillersAndVintners
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn SoftDrinksAndNonAlcoholicBeverages() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::SoftDrinksAndNonAlcoholicBeverages
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn AgriculturalProductsAndServices() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::AgriculturalProductsAndServices
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn PackagedFoodsAndMeats() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::PackagedFoodsAndMeats
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn Tobacco() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::Tobacco
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn HouseholdProducts() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::HouseholdProducts
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn PersonalCareProducts() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::PersonalCareProducts
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn HealthCareEquipment() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::HealthCareEquipment
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn HealthCareSupplies() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::HealthCareSupplies
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn HealthCareDistributors() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::HealthCareDistributors
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn HealthCareServices() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::HealthCareServices
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn HealthCareFacilities() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::HealthCareFacilities
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn ManagedHealthCare() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::ManagedHealthCare
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn HealthCareTechnology() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::HealthCareTechnology
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn Biotechnology() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::Biotechnology
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn Pharmaceuticals() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::Pharmaceuticals
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn LifeSciencesToolsAndServices() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::LifeSciencesToolsAndServices
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn DiversifiedBanks() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::DiversifiedBanks
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn RegionalBanks() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::RegionalBanks
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn DiversifiedFinancialServices() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::DiversifiedFinancialServices
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn MultiSectorHoldings() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::MultiSectorHoldings
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn SpecializedFinance() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::SpecializedFinance
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn CommercialAndResidentialMortgageFinance() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::CommercialAndResidentialMortgageFinance
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn TransactionAndPaymentProcessingServices() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::TransactionAndPaymentProcessingServices
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn ConsumerFinance() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::ConsumerFinance
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn AssetManagementAndCustodyBanks() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::AssetManagementAndCustodyBanks
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn InvestmentBankingAndBrokerage() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::InvestmentBankingAndBrokerage
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn DiversifiedCapitalMarkets() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::DiversifiedCapitalMarkets
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn FinancialExchangesAndData() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::FinancialExchangesAndData
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn MortgageRealEstateInvestmentTrusts() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::MortgageRealEstateInvestmentTrusts
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn InsuranceBrokers() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::InsuranceBrokers
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn LifeAndHealthInsurance() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::LifeAndHealthInsurance
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn MultilineInsurance() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::MultilineInsurance
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn PropertyAndCasualtyInsurance() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::PropertyAndCasualtyInsurance
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn Reinsurance() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::Reinsurance
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn ITConsultingAndOtherServices() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::ITConsultingAndOtherServices
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn InternetServicesAndInfrastructure() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::InternetServicesAndInfrastructure
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn ApplicationSoftware() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::ApplicationSoftware
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn SystemsSoftware() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::SystemsSoftware
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn CommunicationsEquipment() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::CommunicationsEquipment
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn TechnologyHardwareStorageAndPeripherals() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::TechnologyHardwareStorageAndPeripherals
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn ElectronicEquipmentAndInstruments() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::ElectronicEquipmentAndInstruments
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn ElectronicComponents() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::ElectronicComponents
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn ElectronicManufacturingServices() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::ElectronicManufacturingServices
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn TechnologyDistributors() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::TechnologyDistributors
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn SemiconductorMaterialsAndEquipment() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::SemiconductorMaterialsAndEquipment
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn Semiconductors() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::Semiconductors
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn AlternativeCarriers() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::AlternativeCarriers
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn IntegratedTelecommunicationServices() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::IntegratedTelecommunicationServices
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn WirelessTelecommunicationServices() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::WirelessTelecommunicationServices
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn Advertising() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::Advertising
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn Broadcasting() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::Broadcasting
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn CableAndSatellite() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::CableAndSatellite
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn Publishing() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::Publishing
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn MoviesAndEntertainment() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::MoviesAndEntertainment
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn InteractiveHomeEntertainment() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::InteractiveHomeEntertainment
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn InteractiveMediaAndServices() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::InteractiveMediaAndServices
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn ElectricUtilities() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::ElectricUtilities
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn GasUtilities() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::GasUtilities
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn MultiUtilities() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::MultiUtilities
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn WaterUtilities() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::WaterUtilities
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn IndependentPowerProducersAndEnergyTraders() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::IndependentPowerProducersAndEnergyTraders
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn RenewableElectricity() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::RenewableElectricity
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn DiversifiedREITs() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::DiversifiedREITs
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn IndustrialREITs() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::IndustrialREITs
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn HotelAndResortREITs() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::HotelAndResortREITs
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn OfficeREITs() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::OfficeREITs
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn HealthCareREITs() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::HealthCareREITs
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn MultiFamilyResidentialREITs() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::MultiFamilyResidentialREITs
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn SingleFamilyResidentialREITs() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::SingleFamilyResidentialREITs
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn RetailREITs() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::RetailREITs
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn OtherSpecializedREITs() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::OtherSpecializedREITs
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn SelfStorageREITs() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::SelfStorageREITs
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn TelecomTowerREITs() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::TelecomTowerREITs
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn TimberREITs() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::TimberREITs
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn DataCenterREITs() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::DataCenterREITs
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn DiversifiedRealEstateActivities() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::DiversifiedRealEstateActivities
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn RealEstateOperatingCompanies() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::RealEstateOperatingCompanies
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn RealEstateDevelopment() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::RealEstateDevelopment
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn RealEstateServices() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::RealEstateServices
        }
    }

}
