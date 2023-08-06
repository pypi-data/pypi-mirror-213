use pyo3::prelude::*;
use pyo3::types::PyType;
use strum::IntoEnumIterator;
use std::str::FromStr;

use finance_enums::{Industry as BaseIndustry};
use super::{IndustryGroup, SubIndustry};

#[pyclass]
pub struct Industry {
    pub typ: BaseIndustry,
}

#[pymethods]
impl Industry {
    #[new]
    fn py_new(value: String) -> PyResult<Self> {
        Ok(
            Industry {
                typ: BaseIndustry::from_str(value.as_str()).unwrap()
            }
        )

    }

    fn __str__(&self) -> PyResult<String>   {
        Ok(format!("{}", self.typ.to_string()))
    }

    fn __repr__(&self) -> PyResult<String>   {
        Ok(format!("Industry<{}>", self.typ.to_string()))
    }

    fn __eq__(&self, other: &Self) -> bool   {
        self.typ == other.typ
    }

    fn industry_group(&self) -> IndustryGroup {
        IndustryGroup {
            typ: self.typ.industry_group()
        }
    }

    fn subindustries(&self) -> Vec<SubIndustry> {
        self.typ.subindustries().iter().map(|item| SubIndustry{typ: item.clone()} ).collect()
    }

    #[classmethod]
    fn __len__(_cls: &PyType) -> PyResult<usize> {
        Ok(BaseIndustry::iter().count())
    }

    // TODO figure out how to make a class iterator,
    // is way too complicated in pyo3 rn
    #[staticmethod]
    fn members() -> Vec<Industry> {
        BaseIndustry::iter().map(|item: BaseIndustry| Industry{typ: item} ).collect()
    }

    #[classattr]
    #[allow(non_snake_case)]
    fn EnergyEquipmentAndServices() -> Industry {
        Industry {
            typ: BaseIndustry::EnergyEquipmentAndServices
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn OilGasAndConsumeableFules() -> Industry {
        Industry {
            typ: BaseIndustry::OilGasAndConsumeableFules
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn Chemicals() -> Industry {
        Industry {
            typ: BaseIndustry::Chemicals
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn ConstructionMaterials() -> Industry {
        Industry {
            typ: BaseIndustry::ConstructionMaterials
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn ContainersAndPackaging() -> Industry {
        Industry {
            typ: BaseIndustry::ContainersAndPackaging
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn MetalsAndMining() -> Industry {
        Industry {
            typ: BaseIndustry::MetalsAndMining
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn PaperAndForestProducts() -> Industry {
        Industry {
            typ: BaseIndustry::PaperAndForestProducts
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn AerospaceAndDefense() -> Industry {
        Industry {
            typ: BaseIndustry::AerospaceAndDefense
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn BuildingProducts() -> Industry {
        Industry {
            typ: BaseIndustry::BuildingProducts
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn ConstructionAndEngineering() -> Industry {
        Industry {
            typ: BaseIndustry::ConstructionAndEngineering
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn ElectricalEquipment() -> Industry {
        Industry {
            typ: BaseIndustry::ElectricalEquipment
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn IndustrialConglomerates() -> Industry {
        Industry {
            typ: BaseIndustry::IndustrialConglomerates
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn Machinery() -> Industry {
        Industry {
            typ: BaseIndustry::Machinery
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn TradingCompaniesAndDistributors() -> Industry {
        Industry {
            typ: BaseIndustry::TradingCompaniesAndDistributors
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn CommercialServicesAndSupplies() -> Industry {
        Industry {
            typ: BaseIndustry::CommercialServicesAndSupplies
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn ProfessionalServices() -> Industry {
        Industry {
            typ: BaseIndustry::ProfessionalServices
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn AirFreightAndLogistics() -> Industry {
        Industry {
            typ: BaseIndustry::AirFreightAndLogistics
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn PassengerAirlines() -> Industry {
        Industry {
            typ: BaseIndustry::PassengerAirlines
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn MarineTransportation() -> Industry {
        Industry {
            typ: BaseIndustry::MarineTransportation
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn GroundTransportation() -> Industry {
        Industry {
            typ: BaseIndustry::GroundTransportation
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn TransportationInfrastructure() -> Industry {
        Industry {
            typ: BaseIndustry::TransportationInfrastructure
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn AutomobileComponents() -> Industry {
        Industry {
            typ: BaseIndustry::AutomobileComponents
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn Automobiles() -> Industry {
        Industry {
            typ: BaseIndustry::Automobiles
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn HouseholdDurables() -> Industry {
        Industry {
            typ: BaseIndustry::HouseholdDurables
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn LeisureProducts() -> Industry {
        Industry {
            typ: BaseIndustry::LeisureProducts
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn TextilesApparelAndLuxuryGoods() -> Industry {
        Industry {
            typ: BaseIndustry::TextilesApparelAndLuxuryGoods
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn HotelsRestaurantsAndLeisure() -> Industry {
        Industry {
            typ: BaseIndustry::HotelsRestaurantsAndLeisure
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn DiversifiedConsumerServices() -> Industry {
        Industry {
            typ: BaseIndustry::DiversifiedConsumerServices
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn Distributors() -> Industry {
        Industry {
            typ: BaseIndustry::Distributors
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn BroadlineRetail() -> Industry {
        Industry {
            typ: BaseIndustry::BroadlineRetail
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn SpecialtyRetail() -> Industry {
        Industry {
            typ: BaseIndustry::SpecialtyRetail
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn ConsumerStaplesDistributionAndRetail() -> Industry {
        Industry {
            typ: BaseIndustry::ConsumerStaplesDistributionAndRetail
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn Beverages() -> Industry {
        Industry {
            typ: BaseIndustry::Beverages
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn FoodProducts() -> Industry {
        Industry {
            typ: BaseIndustry::FoodProducts
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn Tobacco() -> Industry {
        Industry {
            typ: BaseIndustry::Tobacco
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn HouseholdProducts() -> Industry {
        Industry {
            typ: BaseIndustry::HouseholdProducts
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn PersonalCareProducts() -> Industry {
        Industry {
            typ: BaseIndustry::PersonalCareProducts
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn HealthCareEquipmentAndSupplies() -> Industry {
        Industry {
            typ: BaseIndustry::HealthCareEquipmentAndSupplies
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn HealthCareProvidersAndServices() -> Industry {
        Industry {
            typ: BaseIndustry::HealthCareProvidersAndServices
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn HealthCareTechnology() -> Industry {
        Industry {
            typ: BaseIndustry::HealthCareTechnology
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn Biotechnology() -> Industry {
        Industry {
            typ: BaseIndustry::Biotechnology
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn Pharmaceuticals() -> Industry {
        Industry {
            typ: BaseIndustry::Pharmaceuticals
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn LifeSciencesToolsAndServices() -> Industry {
        Industry {
            typ: BaseIndustry::LifeSciencesToolsAndServices
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn Banks() -> Industry {
        Industry {
            typ: BaseIndustry::Banks
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn FinancialServices() -> Industry {
        Industry {
            typ: BaseIndustry::FinancialServices
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn ConsumerFinance() -> Industry {
        Industry {
            typ: BaseIndustry::ConsumerFinance
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn CapitalMarkets() -> Industry {
        Industry {
            typ: BaseIndustry::CapitalMarkets
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn MortgageRealEstateInvestmentTrusts() -> Industry {
        Industry {
            typ: BaseIndustry::MortgageRealEstateInvestmentTrusts
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn Insurance() -> Industry {
        Industry {
            typ: BaseIndustry::Insurance
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn ITServices() -> Industry {
        Industry {
            typ: BaseIndustry::ITServices
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn Software() -> Industry {
        Industry {
            typ: BaseIndustry::Software
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn CommunicationsEquipment() -> Industry {
        Industry {
            typ: BaseIndustry::CommunicationsEquipment
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn TechnologyHardwareStorageAndPeripherals() -> Industry {
        Industry {
            typ: BaseIndustry::TechnologyHardwareStorageAndPeripherals
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn ElectronicEquipmentInstrumentsAndComponents() -> Industry {
        Industry {
            typ: BaseIndustry::ElectronicEquipmentInstrumentsAndComponents
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn SemiconductorsAndSemiconductorEquipment() -> Industry {
        Industry {
            typ: BaseIndustry::SemiconductorsAndSemiconductorEquipment
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn DiversifiedTelecommunicationServices() -> Industry {
        Industry {
            typ: BaseIndustry::DiversifiedTelecommunicationServices
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn WirelessTelecommunicationServices() -> Industry {
        Industry {
            typ: BaseIndustry::WirelessTelecommunicationServices
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn Media() -> Industry {
        Industry {
            typ: BaseIndustry::Media
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn Entertainment() -> Industry {
        Industry {
            typ: BaseIndustry::Entertainment
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn InteractiveMediaAndServices() -> Industry {
        Industry {
            typ: BaseIndustry::InteractiveMediaAndServices
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn ElectricUtilities() -> Industry {
        Industry {
            typ: BaseIndustry::ElectricUtilities
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn GasUtilities() -> Industry {
        Industry {
            typ: BaseIndustry::GasUtilities
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn MultiUtilities() -> Industry {
        Industry {
            typ: BaseIndustry::MultiUtilities
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn WaterUtilities() -> Industry {
        Industry {
            typ: BaseIndustry::WaterUtilities
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn IndependentPowerAndRenewableElectricityProducers() -> Industry {
        Industry {
            typ: BaseIndustry::IndependentPowerAndRenewableElectricityProducers
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn DiversifiedREITs() -> Industry {
        Industry {
            typ: BaseIndustry::DiversifiedREITs
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn IndustrialREITs() -> Industry {
        Industry {
            typ: BaseIndustry::IndustrialREITs
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn HotelAndResortREITs() -> Industry {
        Industry {
            typ: BaseIndustry::HotelAndResortREITs
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn OfficeREITs() -> Industry {
        Industry {
            typ: BaseIndustry::OfficeREITs
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn HealthCareREITs() -> Industry {
        Industry {
            typ: BaseIndustry::HealthCareREITs
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn ResidentialREITs() -> Industry {
        Industry {
            typ: BaseIndustry::ResidentialREITs
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn RetailREITs() -> Industry {
        Industry {
            typ: BaseIndustry::RetailREITs
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn SpecializedREITs() -> Industry {
        Industry {
            typ: BaseIndustry::SpecializedREITs
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn RealEstateManagementAndDevelopment() -> Industry {
        Industry {
            typ: BaseIndustry::RealEstateManagementAndDevelopment
        }
    }
}
