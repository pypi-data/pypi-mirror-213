use super::{IndustryGroup, SubIndustry};
use serde::{Deserialize, Serialize};

#[derive(Clone, Debug, Deserialize, Display, EnumIter, EnumString, Eq, PartialEq, Serialize)]
#[strum(serialize_all = "PascalCase")]
pub enum Industry {
    // Energy
    EnergyEquipmentAndServices,
    OilGasAndConsumeableFules,
    // Materials,
    Chemicals,
    ConstructionMaterials,
    ContainersAndPackaging,
    MetalsAndMining,
    PaperAndForestProducts,
    // Industrials -> Capital Goods
    AerospaceAndDefense,
    BuildingProducts,
    ConstructionAndEngineering,
    ElectricalEquipment,
    IndustrialConglomerates,
    Machinery,
    TradingCompaniesAndDistributors,
    // Industrials -> Commercial and Professional Services
    CommercialServicesAndSupplies,
    ProfessionalServices,
    // Industrials -> Transportation
    AirFreightAndLogistics,
    PassengerAirlines,
    MarineTransportation,
    GroundTransportation,
    TransportationInfrastructure,
    // Consumer Discretionary -> Automobiles and Components
    AutomobileComponents,
    Automobiles,
    // Consumer Discretionary -> Consumer Durables and Apparel
    HouseholdDurables,
    LeisureProducts,
    TextilesApparelAndLuxuryGoods,
    // Consumer Discretionary -> Consumer Services
    HotelsRestaurantsAndLeisure,
    DiversifiedConsumerServices,
    // Consumer Discretionary -> Consumer Discretionary Distribution and Retail
    Distributors,
    BroadlineRetail,
    SpecialtyRetail,
    // Consumer Staples -> Consumer Staples Distribution And Retail
    ConsumerStaplesDistributionAndRetail,
    // Consumer Staples -> Food, Beverage, and Tobacco
    Beverages,
    FoodProducts,
    Tobacco,
    // Consumer Staples -> Household and Personal Products
    HouseholdProducts,
    PersonalCareProducts,
    // Health Care -> Health Care Equipment and Services
    HealthCareEquipmentAndSupplies,
    HealthCareProvidersAndServices,
    HealthCareTechnology,
    // Health Care -> Pharmaceuticals, Biotechnology, and Life Sciences
    Biotechnology,
    Pharmaceuticals,
    LifeSciencesToolsAndServices,
    // Financials -> Banks
    Banks,
    // Financials -> Financial Services
    FinancialServices,
    ConsumerFinance,
    CapitalMarkets,
    MortgageRealEstateInvestmentTrusts,
    // Financials -> Insurance
    Insurance,
    // Information Technology -> Software and Services
    ITServices,
    Software,
    // Information Technology -> Technology Equipment and Hardware
    CommunicationsEquipment,
    TechnologyHardwareStorageAndPeripherals,
    ElectronicEquipmentInstrumentsAndComponents,
    // Information Technology -> Semiconductors and Semiconductor Equipment
    SemiconductorsAndSemiconductorEquipment,
    // Communication Services -> Telecommunication Services
    DiversifiedTelecommunicationServices,
    WirelessTelecommunicationServices,
    // Communication Services -> Media and Entertainment
    Media,
    Entertainment,
    InteractiveMediaAndServices,
    // Utilities
    ElectricUtilities,
    GasUtilities,
    MultiUtilities,
    WaterUtilities,
    IndependentPowerAndRenewableElectricityProducers,
    // Real Estate -> Equity REITs
    DiversifiedREITs,
    IndustrialREITs,
    HotelAndResortREITs,
    OfficeREITs,
    HealthCareREITs,
    ResidentialREITs,
    RetailREITs,
    SpecializedREITs,
    // Real Estate -> Real Estate Management and Development
    RealEstateManagementAndDevelopment,
}

impl Industry {
    pub fn subindustries(&self) -> Vec<SubIndustry> {
        match self {
            Industry::EnergyEquipmentAndServices => vec![
                SubIndustry::OilAndGasDrilling,
                SubIndustry::OilAndGasEquipmentAndServices,
            ],
            Industry::OilGasAndConsumeableFules => vec![
                SubIndustry::IntegratedOilAndGas,
                SubIndustry::OilAndGasExplorationAndProduction,
                SubIndustry::OilAndGasRefiningAndMarketing,
                SubIndustry::OilAndGasStorageAndTransportation,
                SubIndustry::CoalAndConsumeableFuels,
            ],
            Industry::Chemicals => vec![
                SubIndustry::CommodityChemicals,
                SubIndustry::DiversifiedChemicals,
                SubIndustry::FertilizersAndAgriculturalChemicals,
                SubIndustry::IndustrialGases,
                SubIndustry::SpecialtyChemicals,
            ],
            Industry::ConstructionMaterials => vec![SubIndustry::ConstructionMaterials],
            Industry::ContainersAndPackaging => vec![
                SubIndustry::MetalGlassAndPlasticContainers,
                SubIndustry::PaperAndPlasticPackagingProductsAndMaterials,
            ],
            Industry::MetalsAndMining => vec![
                SubIndustry::Aluminum,
                SubIndustry::DiversifiedMetalsAndMining,
                SubIndustry::Copper,
                SubIndustry::Gold,
                SubIndustry::PreciousMetalsAndMinerals,
                SubIndustry::Silver,
                SubIndustry::Steel,
            ],
            Industry::PaperAndForestProducts => {
                vec![SubIndustry::ForestProducts, SubIndustry::PaperProducts]
            }
            Industry::AerospaceAndDefense => vec![SubIndustry::AerospaceAndDefense],
            Industry::BuildingProducts => vec![SubIndustry::BuildingProducts],
            Industry::ConstructionAndEngineering => vec![SubIndustry::ConstructionAndEngineering],
            Industry::ElectricalEquipment => vec![
                SubIndustry::ElectricalComponentsAndEquipment,
                SubIndustry::HeavyElectricalEquipment,
            ],
            Industry::IndustrialConglomerates => vec![SubIndustry::IndustrialConglomerates],
            Industry::Machinery => vec![
                SubIndustry::ConstructionMachineryAndHeavyTransportationEquipment,
                SubIndustry::AgriculturalAndFarmMachinery,
                SubIndustry::IndustrialMachinerySuppliesAndComponents,
            ],
            Industry::TradingCompaniesAndDistributors => {
                vec![SubIndustry::TradingCompaniesAndDistributors]
            }
            Industry::CommercialServicesAndSupplies => vec![
                SubIndustry::CommercialPrinting,
                SubIndustry::EnvironmentalAndFacilitiesServices,
                SubIndustry::OfficeServicesAndSupplies,
                SubIndustry::DiviersifiedSupportServices,
                SubIndustry::SecurityAndAlarmServices,
            ],
            Industry::ProfessionalServices => vec![
                SubIndustry::HumanResourcesAndEmploymentServices,
                SubIndustry::ResearchAndConsultingServices,
                SubIndustry::DataProcessingAndOutsourcedServices,
            ],
            Industry::AirFreightAndLogistics => vec![SubIndustry::AirFreightAndLogistics],
            Industry::PassengerAirlines => vec![SubIndustry::PassengerAirlines],
            Industry::MarineTransportation => vec![SubIndustry::MarineTransportation],
            Industry::GroundTransportation => vec![
                SubIndustry::RailTransportation,
                SubIndustry::CargoGroundTransportation,
                SubIndustry::PassengerGroundTransportation,
            ],
            Industry::TransportationInfrastructure => vec![
                SubIndustry::AirportServices,
                SubIndustry::HighwaysAndRailtracks,
                SubIndustry::MarinePortsAndServices,
            ],
            Industry::AutomobileComponents => vec![
                SubIndustry::AutomotivePartsAndEquipment,
                SubIndustry::TiresAndRubber,
            ],
            Industry::Automobiles => vec![
                SubIndustry::AutomobileManufacturers,
                SubIndustry::MotorcycleManufacturers,
            ],
            Industry::HouseholdDurables => vec![
                SubIndustry::ConsumerElectronics,
                SubIndustry::HomeFurnishings,
                SubIndustry::Homebuilding,
                SubIndustry::HouseholdAppliances,
                SubIndustry::HousewaresAndSpecialties,
            ],
            Industry::LeisureProducts => vec![SubIndustry::LeisureProducts],
            Industry::TextilesApparelAndLuxuryGoods => vec![
                SubIndustry::ApparelAccessoriesAndLuxuryGoods,
                SubIndustry::Footwear,
                SubIndustry::Textiles,
            ],
            Industry::HotelsRestaurantsAndLeisure => vec![
                SubIndustry::CasinosAndGaming,
                SubIndustry::HotelsResortsAndCruiseLines,
                SubIndustry::LeisureFacilities,
                SubIndustry::Restaurants,
            ],
            Industry::DiversifiedConsumerServices => vec![
                SubIndustry::EducationServices,
                SubIndustry::SpecializedConsumerServices,
            ],
            Industry::Distributors => vec![SubIndustry::Distributors],
            Industry::BroadlineRetail => vec![SubIndustry::BroadlineRetail],
            Industry::SpecialtyRetail => vec![
                SubIndustry::ApparelRetail,
                SubIndustry::ComputerAndElectronicsretail,
                SubIndustry::HomeImprovementRetail,
                SubIndustry::OtherSpecialtyRetail,
                SubIndustry::AutomotiveRetail,
                SubIndustry::HomefurnishingRetail,
            ],
            Industry::ConsumerStaplesDistributionAndRetail => vec![
                SubIndustry::DrugRetail,
                SubIndustry::FoodDistributors,
                SubIndustry::FoodRetail,
                SubIndustry::ConsumerStaplesMerchandiseRetail,
            ],
            Industry::Beverages => vec![
                SubIndustry::Brewers,
                SubIndustry::DistillersAndVintners,
                SubIndustry::SoftDrinksAndNonAlcoholicBeverages,
            ],
            Industry::FoodProducts => vec![
                SubIndustry::AgriculturalProductsAndServices,
                SubIndustry::PackagedFoodsAndMeats,
            ],
            Industry::Tobacco => vec![SubIndustry::Tobacco],
            Industry::HouseholdProducts => vec![SubIndustry::HouseholdProducts],
            Industry::PersonalCareProducts => vec![SubIndustry::PersonalCareProducts],
            Industry::HealthCareEquipmentAndSupplies => vec![
                SubIndustry::HealthCareEquipment,
                SubIndustry::HealthCareSupplies,
            ],
            Industry::HealthCareProvidersAndServices => vec![
                SubIndustry::HealthCareDistributors,
                SubIndustry::HealthCareServices,
                SubIndustry::HealthCareFacilities,
                SubIndustry::ManagedHealthCare,
            ],
            Industry::HealthCareTechnology => vec![SubIndustry::HealthCareTechnology],
            Industry::Biotechnology => vec![SubIndustry::Biotechnology],
            Industry::Pharmaceuticals => vec![SubIndustry::Pharmaceuticals],
            Industry::LifeSciencesToolsAndServices => {
                vec![SubIndustry::LifeSciencesToolsAndServices]
            }
            Industry::Banks => vec![SubIndustry::DiversifiedBanks, SubIndustry::RegionalBanks],
            Industry::FinancialServices => vec![
                SubIndustry::DiversifiedFinancialServices,
                SubIndustry::MultiSectorHoldings,
                SubIndustry::SpecializedFinance,
                SubIndustry::CommercialAndResidentialMortgageFinance,
                SubIndustry::TransactionAndPaymentProcessingServices,
            ],
            Industry::ConsumerFinance => vec![SubIndustry::ConsumerFinance],
            Industry::CapitalMarkets => vec![
                SubIndustry::AssetManagementAndCustodyBanks,
                SubIndustry::InvestmentBankingAndBrokerage,
                SubIndustry::DiversifiedCapitalMarkets,
                SubIndustry::FinancialExchangesAndData,
            ],
            Industry::MortgageRealEstateInvestmentTrusts => {
                vec![SubIndustry::MortgageRealEstateInvestmentTrusts]
            }
            Industry::Insurance => vec![
                SubIndustry::InsuranceBrokers,
                SubIndustry::LifeAndHealthInsurance,
                SubIndustry::MultilineInsurance,
                SubIndustry::PropertyAndCasualtyInsurance,
                SubIndustry::Reinsurance,
            ],
            Industry::ITServices => vec![
                SubIndustry::ITConsultingAndOtherServices,
                SubIndustry::InternetServicesAndInfrastructure,
            ],
            Industry::Software => vec![
                SubIndustry::ApplicationSoftware,
                SubIndustry::SystemsSoftware,
            ],
            Industry::CommunicationsEquipment => vec![SubIndustry::CommunicationsEquipment],
            Industry::TechnologyHardwareStorageAndPeripherals => {
                vec![SubIndustry::TechnologyHardwareStorageAndPeripherals]
            }
            Industry::ElectronicEquipmentInstrumentsAndComponents => vec![
                SubIndustry::ElectronicEquipmentAndInstruments,
                SubIndustry::ElectronicComponents,
                SubIndustry::ElectronicManufacturingServices,
                SubIndustry::TechnologyDistributors,
            ],
            Industry::SemiconductorsAndSemiconductorEquipment => vec![
                SubIndustry::SemiconductorMaterialsAndEquipment,
                SubIndustry::Semiconductors,
            ],
            Industry::DiversifiedTelecommunicationServices => vec![
                SubIndustry::AlternativeCarriers,
                SubIndustry::IntegratedTelecommunicationServices,
            ],
            Industry::WirelessTelecommunicationServices => {
                vec![SubIndustry::WirelessTelecommunicationServices]
            }
            Industry::Media => vec![
                SubIndustry::Advertising,
                SubIndustry::Broadcasting,
                SubIndustry::CableAndSatellite,
                SubIndustry::Publishing,
            ],
            Industry::Entertainment => vec![
                SubIndustry::MoviesAndEntertainment,
                SubIndustry::InteractiveHomeEntertainment,
            ],
            Industry::InteractiveMediaAndServices => vec![SubIndustry::InteractiveMediaAndServices],
            Industry::ElectricUtilities => vec![SubIndustry::ElectricUtilities],
            Industry::GasUtilities => vec![SubIndustry::GasUtilities],
            Industry::MultiUtilities => vec![SubIndustry::MultiUtilities],
            Industry::WaterUtilities => vec![SubIndustry::WaterUtilities],
            Industry::IndependentPowerAndRenewableElectricityProducers => vec![
                SubIndustry::IndependentPowerProducersAndEnergyTraders,
                SubIndustry::RenewableElectricity,
            ],
            Industry::DiversifiedREITs => vec![SubIndustry::DiversifiedREITs],
            Industry::IndustrialREITs => vec![SubIndustry::IndustrialREITs],
            Industry::HotelAndResortREITs => vec![SubIndustry::HotelAndResortREITs],
            Industry::OfficeREITs => vec![SubIndustry::OfficeREITs],
            Industry::HealthCareREITs => vec![SubIndustry::HealthCareREITs],
            Industry::ResidentialREITs => vec![
                SubIndustry::MultiFamilyResidentialREITs,
                SubIndustry::SingleFamilyResidentialREITs,
            ],
            Industry::RetailREITs => vec![SubIndustry::RetailREITs],
            Industry::SpecializedREITs => vec![
                SubIndustry::OtherSpecializedREITs,
                SubIndustry::SelfStorageREITs,
                SubIndustry::TelecomTowerREITs,
                SubIndustry::TimberREITs,
                SubIndustry::DataCenterREITs,
            ],
            Industry::RealEstateManagementAndDevelopment => vec![
                SubIndustry::DiversifiedRealEstateActivities,
                SubIndustry::RealEstateOperatingCompanies,
                SubIndustry::RealEstateDevelopment,
                SubIndustry::RealEstateServices,
            ],
        }
    }

    pub fn industry_group(&self) -> IndustryGroup {
        match self {
            Industry::EnergyEquipmentAndServices => IndustryGroup::Energy,
            Industry::OilGasAndConsumeableFules => IndustryGroup::Energy,
            Industry::Chemicals => IndustryGroup::Materials,
            Industry::ConstructionMaterials => IndustryGroup::Materials,
            Industry::ContainersAndPackaging => IndustryGroup::Materials,
            Industry::MetalsAndMining => IndustryGroup::Materials,
            Industry::PaperAndForestProducts => IndustryGroup::Materials,
            Industry::AerospaceAndDefense => IndustryGroup::CapitalGoods,
            Industry::BuildingProducts => IndustryGroup::CapitalGoods,
            Industry::ConstructionAndEngineering => IndustryGroup::CapitalGoods,
            Industry::ElectricalEquipment => IndustryGroup::CapitalGoods,
            Industry::IndustrialConglomerates => IndustryGroup::CapitalGoods,
            Industry::Machinery => IndustryGroup::CapitalGoods,
            Industry::TradingCompaniesAndDistributors => IndustryGroup::CapitalGoods,
            Industry::CommercialServicesAndSupplies => {
                IndustryGroup::CommercialAndProfessionalServices
            }
            Industry::ProfessionalServices => IndustryGroup::CommercialAndProfessionalServices,
            Industry::AirFreightAndLogistics => IndustryGroup::Transportation,
            Industry::PassengerAirlines => IndustryGroup::Transportation,
            Industry::MarineTransportation => IndustryGroup::Transportation,
            Industry::GroundTransportation => IndustryGroup::Transportation,
            Industry::TransportationInfrastructure => IndustryGroup::Transportation,
            Industry::AutomobileComponents => IndustryGroup::AutomobilesAndComponents,
            Industry::Automobiles => IndustryGroup::AutomobilesAndComponents,
            Industry::HouseholdDurables => IndustryGroup::ConsumerDurablesAndApparel,
            Industry::LeisureProducts => IndustryGroup::ConsumerDurablesAndApparel,
            Industry::TextilesApparelAndLuxuryGoods => IndustryGroup::ConsumerDurablesAndApparel,
            Industry::HotelsRestaurantsAndLeisure => IndustryGroup::ConsumerServices,
            Industry::DiversifiedConsumerServices => IndustryGroup::ConsumerServices,
            Industry::Distributors => IndustryGroup::ConsumerDiscretionaryDistributionAndRetail,
            Industry::BroadlineRetail => IndustryGroup::ConsumerDiscretionaryDistributionAndRetail,
            Industry::SpecialtyRetail => IndustryGroup::ConsumerDiscretionaryDistributionAndRetail,
            Industry::ConsumerStaplesDistributionAndRetail => {
                IndustryGroup::ConsumerStaplesDistributionAndRetail
            }
            Industry::Beverages => IndustryGroup::FoodBeverageAndTobacco,
            Industry::FoodProducts => IndustryGroup::FoodBeverageAndTobacco,
            Industry::Tobacco => IndustryGroup::FoodBeverageAndTobacco,
            Industry::HouseholdProducts => IndustryGroup::HouseholdAndPersonalProducts,
            Industry::PersonalCareProducts => IndustryGroup::HouseholdAndPersonalProducts,
            Industry::HealthCareEquipmentAndSupplies => {
                IndustryGroup::HealthCareEquipmentAndServices
            }
            Industry::HealthCareProvidersAndServices => {
                IndustryGroup::HealthCareEquipmentAndServices
            }
            Industry::HealthCareTechnology => IndustryGroup::HealthCareEquipmentAndServices,
            Industry::Biotechnology => IndustryGroup::PharmaceuticalsBiotechnologyAndLifeSciences,
            Industry::Pharmaceuticals => IndustryGroup::PharmaceuticalsBiotechnologyAndLifeSciences,
            Industry::LifeSciencesToolsAndServices => {
                IndustryGroup::PharmaceuticalsBiotechnologyAndLifeSciences
            }
            Industry::Banks => IndustryGroup::Banks,
            Industry::FinancialServices => IndustryGroup::FinancialServices,
            Industry::ConsumerFinance => IndustryGroup::FinancialServices,
            Industry::CapitalMarkets => IndustryGroup::FinancialServices,
            Industry::MortgageRealEstateInvestmentTrusts => IndustryGroup::FinancialServices,
            Industry::Insurance => IndustryGroup::Insurance,
            Industry::ITServices => IndustryGroup::SoftwareAndServices,
            Industry::Software => IndustryGroup::SoftwareAndServices,
            Industry::CommunicationsEquipment => IndustryGroup::TechnologyHardwareAndEquipment,
            Industry::TechnologyHardwareStorageAndPeripherals => {
                IndustryGroup::TechnologyHardwareAndEquipment
            }
            Industry::ElectronicEquipmentInstrumentsAndComponents => {
                IndustryGroup::TechnologyHardwareAndEquipment
            }
            Industry::SemiconductorsAndSemiconductorEquipment => {
                IndustryGroup::SemiconductorsAndSemiconductorEquipment
            }
            Industry::DiversifiedTelecommunicationServices => {
                IndustryGroup::TelecommunicationServices
            }
            Industry::WirelessTelecommunicationServices => IndustryGroup::TelecommunicationServices,
            Industry::Media => IndustryGroup::MediaAndEntertainment,
            Industry::Entertainment => IndustryGroup::MediaAndEntertainment,
            Industry::InteractiveMediaAndServices => IndustryGroup::MediaAndEntertainment,
            Industry::ElectricUtilities => IndustryGroup::Utilities,
            Industry::GasUtilities => IndustryGroup::Utilities,
            Industry::MultiUtilities => IndustryGroup::Utilities,
            Industry::WaterUtilities => IndustryGroup::Utilities,
            Industry::IndependentPowerAndRenewableElectricityProducers => IndustryGroup::Utilities,
            Industry::DiversifiedREITs => IndustryGroup::EquityRealEstateInvestmentTrusts,
            Industry::IndustrialREITs => IndustryGroup::EquityRealEstateInvestmentTrusts,
            Industry::HotelAndResortREITs => IndustryGroup::EquityRealEstateInvestmentTrusts,
            Industry::OfficeREITs => IndustryGroup::EquityRealEstateInvestmentTrusts,
            Industry::HealthCareREITs => IndustryGroup::EquityRealEstateInvestmentTrusts,
            Industry::ResidentialREITs => IndustryGroup::EquityRealEstateInvestmentTrusts,
            Industry::RetailREITs => IndustryGroup::EquityRealEstateInvestmentTrusts,
            Industry::SpecializedREITs => IndustryGroup::EquityRealEstateInvestmentTrusts,
            Industry::RealEstateManagementAndDevelopment => {
                IndustryGroup::RealEstateManagementAndDevelopment
            }
        }
    }
}
