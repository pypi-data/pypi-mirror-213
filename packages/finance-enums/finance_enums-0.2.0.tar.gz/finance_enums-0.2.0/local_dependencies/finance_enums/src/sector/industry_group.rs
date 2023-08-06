use super::{Industry, Sector};
use serde::{Deserialize, Serialize};

#[derive(Clone, Debug, Deserialize, Display, EnumIter, EnumString, Eq, PartialEq, Serialize)]
#[strum(serialize_all = "PascalCase")]
pub enum IndustryGroup {
    // Energy
    Energy,
    // Materials
    Materials,
    // Industrials
    CapitalGoods,
    CommercialAndProfessionalServices,
    Transportation,
    // Consumer Discretionary
    AutomobilesAndComponents,
    ConsumerDurablesAndApparel,
    ConsumerServices,
    ConsumerDiscretionaryDistributionAndRetail,
    // Consumer Staples
    ConsumerStaplesDistributionAndRetail,
    FoodBeverageAndTobacco,
    HouseholdAndPersonalProducts,
    // Health Care
    HealthCareEquipmentAndServices,
    PharmaceuticalsBiotechnologyAndLifeSciences,
    // Financials
    Banks,
    FinancialServices,
    Insurance,
    // Information Technology
    SoftwareAndServices,
    TechnologyHardwareAndEquipment,
    SemiconductorsAndSemiconductorEquipment,
    // Communication Services
    TelecommunicationServices,
    MediaAndEntertainment,
    // Utilities
    Utilities,
    // Real Estate
    EquityRealEstateInvestmentTrusts,
    RealEstateManagementAndDevelopment,
}

impl IndustryGroup {
    pub fn sector(&self) -> Sector {
        match self {
            IndustryGroup::Energy => Sector::Energy,
            IndustryGroup::Materials => Sector::Materials,
            IndustryGroup::CapitalGoods => Sector::Industrials,
            IndustryGroup::CommercialAndProfessionalServices => Sector::Industrials,
            IndustryGroup::Transportation => Sector::Industrials,
            IndustryGroup::AutomobilesAndComponents => Sector::ConsumerDiscretionary,
            IndustryGroup::ConsumerDurablesAndApparel => Sector::ConsumerDiscretionary,
            IndustryGroup::ConsumerServices => Sector::ConsumerDiscretionary,
            IndustryGroup::ConsumerDiscretionaryDistributionAndRetail => {
                Sector::ConsumerDiscretionary
            }
            IndustryGroup::ConsumerStaplesDistributionAndRetail => Sector::ConsumerStaples,
            IndustryGroup::FoodBeverageAndTobacco => Sector::ConsumerStaples,
            IndustryGroup::HouseholdAndPersonalProducts => Sector::ConsumerStaples,
            IndustryGroup::HealthCareEquipmentAndServices => Sector::HealthCare,
            IndustryGroup::PharmaceuticalsBiotechnologyAndLifeSciences => Sector::HealthCare,
            IndustryGroup::Banks => Sector::Financials,
            IndustryGroup::FinancialServices => Sector::Financials,
            IndustryGroup::Insurance => Sector::Financials,
            IndustryGroup::SoftwareAndServices => Sector::InformationTechnology,
            IndustryGroup::TechnologyHardwareAndEquipment => Sector::InformationTechnology,
            IndustryGroup::SemiconductorsAndSemiconductorEquipment => Sector::InformationTechnology,
            IndustryGroup::TelecommunicationServices => Sector::CommunicationServices,
            IndustryGroup::MediaAndEntertainment => Sector::CommunicationServices,
            IndustryGroup::Utilities => Sector::Utilities,
            IndustryGroup::EquityRealEstateInvestmentTrusts => Sector::RealEstate,
            IndustryGroup::RealEstateManagementAndDevelopment => Sector::RealEstate,
        }
    }

    pub fn industries(&self) -> Vec<Industry> {
        match self {
            IndustryGroup::Energy => vec![
                Industry::EnergyEquipmentAndServices,
                Industry::OilGasAndConsumeableFules,
            ],
            IndustryGroup::Materials => vec![
                Industry::Chemicals,
                Industry::ConstructionMaterials,
                Industry::ContainersAndPackaging,
                Industry::MetalsAndMining,
                Industry::PaperAndForestProducts,
            ],
            IndustryGroup::CapitalGoods => vec![
                Industry::AerospaceAndDefense,
                Industry::BuildingProducts,
                Industry::ConstructionAndEngineering,
                Industry::ElectricalEquipment,
                Industry::IndustrialConglomerates,
                Industry::Machinery,
                Industry::TradingCompaniesAndDistributors,
            ],
            IndustryGroup::CommercialAndProfessionalServices => vec![
                Industry::CommercialServicesAndSupplies,
                Industry::ProfessionalServices,
            ],
            IndustryGroup::Transportation => vec![
                Industry::AirFreightAndLogistics,
                Industry::PassengerAirlines,
                Industry::MarineTransportation,
                Industry::GroundTransportation,
                Industry::TransportationInfrastructure,
            ],
            IndustryGroup::AutomobilesAndComponents => {
                vec![Industry::AutomobileComponents, Industry::Automobiles]
            }
            IndustryGroup::ConsumerDurablesAndApparel => vec![
                Industry::HouseholdDurables,
                Industry::LeisureProducts,
                Industry::TextilesApparelAndLuxuryGoods,
            ],
            IndustryGroup::ConsumerServices => vec![
                Industry::HotelsRestaurantsAndLeisure,
                Industry::DiversifiedConsumerServices,
            ],
            IndustryGroup::ConsumerDiscretionaryDistributionAndRetail => vec![
                Industry::Distributors,
                Industry::BroadlineRetail,
                Industry::SpecialtyRetail,
            ],
            IndustryGroup::ConsumerStaplesDistributionAndRetail => {
                vec![Industry::ConsumerStaplesDistributionAndRetail]
            }
            IndustryGroup::FoodBeverageAndTobacco => vec![
                Industry::Beverages,
                Industry::FoodProducts,
                Industry::Tobacco,
            ],
            IndustryGroup::HouseholdAndPersonalProducts => {
                vec![Industry::HouseholdProducts, Industry::PersonalCareProducts]
            }
            IndustryGroup::HealthCareEquipmentAndServices => vec![
                Industry::HealthCareEquipmentAndSupplies,
                Industry::HealthCareProvidersAndServices,
                Industry::HealthCareTechnology,
            ],
            IndustryGroup::PharmaceuticalsBiotechnologyAndLifeSciences => vec![
                Industry::Biotechnology,
                Industry::Pharmaceuticals,
                Industry::LifeSciencesToolsAndServices,
            ],
            IndustryGroup::Banks => vec![Industry::Banks],
            IndustryGroup::FinancialServices => vec![
                Industry::FinancialServices,
                Industry::ConsumerFinance,
                Industry::CapitalMarkets,
                Industry::MortgageRealEstateInvestmentTrusts,
            ],
            IndustryGroup::Insurance => vec![Industry::Insurance],
            IndustryGroup::SoftwareAndServices => vec![Industry::ITServices, Industry::Software],
            IndustryGroup::TechnologyHardwareAndEquipment => vec![
                Industry::CommunicationsEquipment,
                Industry::TechnologyHardwareStorageAndPeripherals,
                Industry::ElectronicEquipmentInstrumentsAndComponents,
            ],
            IndustryGroup::SemiconductorsAndSemiconductorEquipment => {
                vec![Industry::SemiconductorsAndSemiconductorEquipment]
            }
            IndustryGroup::TelecommunicationServices => vec![
                Industry::DiversifiedTelecommunicationServices,
                Industry::WirelessTelecommunicationServices,
            ],
            IndustryGroup::MediaAndEntertainment => vec![
                Industry::Media,
                Industry::Entertainment,
                Industry::InteractiveMediaAndServices,
            ],
            IndustryGroup::Utilities => vec![
                Industry::ElectricUtilities,
                Industry::GasUtilities,
                Industry::MultiUtilities,
                Industry::WaterUtilities,
                Industry::IndependentPowerAndRenewableElectricityProducers,
            ],
            IndustryGroup::EquityRealEstateInvestmentTrusts => vec![
                Industry::DiversifiedREITs,
                Industry::IndustrialREITs,
                Industry::HotelAndResortREITs,
                Industry::OfficeREITs,
                Industry::HealthCareREITs,
                Industry::ResidentialREITs,
                Industry::RetailREITs,
                Industry::SpecializedREITs,
            ],
            IndustryGroup::RealEstateManagementAndDevelopment => {
                vec![Industry::RealEstateManagementAndDevelopment]
            }
        }
    }
}

/**********************************/
#[cfg(test)]
mod industry_group_tests {
    use super::*;
    use std::str::FromStr;
    use strum::IntoEnumIterator;

    #[test]
    fn test_from_str() {
        let ig = IndustryGroup::from_str("EquityRealEstateInvestmentTrusts").unwrap();
        assert_eq!(IndustryGroup::EquityRealEstateInvestmentTrusts, ig);
    }
    #[test]
    fn test_to_str() {
        let ig: String = IndustryGroup::EquityRealEstateInvestmentTrusts.to_string();
        assert_eq!("EquityRealEstateInvestmentTrusts", ig);
    }
    #[test]
    fn test_iter() {
        let igs: Vec<IndustryGroup> = IndustryGroup::iter().collect();
        assert_eq!(
            vec![
                IndustryGroup::Energy,
                IndustryGroup::Materials,
                IndustryGroup::CapitalGoods,
                IndustryGroup::CommercialAndProfessionalServices,
                IndustryGroup::Transportation,
                IndustryGroup::AutomobilesAndComponents,
                IndustryGroup::ConsumerDurablesAndApparel,
                IndustryGroup::ConsumerServices,
                IndustryGroup::ConsumerDiscretionaryDistributionAndRetail,
                IndustryGroup::ConsumerStaplesDistributionAndRetail,
                IndustryGroup::FoodBeverageAndTobacco,
                IndustryGroup::HouseholdAndPersonalProducts,
                IndustryGroup::HealthCareEquipmentAndServices,
                IndustryGroup::PharmaceuticalsBiotechnologyAndLifeSciences,
                IndustryGroup::Banks,
                IndustryGroup::FinancialServices,
                IndustryGroup::Insurance,
                IndustryGroup::SoftwareAndServices,
                IndustryGroup::TechnologyHardwareAndEquipment,
                IndustryGroup::SemiconductorsAndSemiconductorEquipment,
                IndustryGroup::TelecommunicationServices,
                IndustryGroup::MediaAndEntertainment,
                IndustryGroup::Utilities,
                IndustryGroup::EquityRealEstateInvestmentTrusts,
                IndustryGroup::RealEstateManagementAndDevelopment,
            ],
            igs
        );
    }
}
