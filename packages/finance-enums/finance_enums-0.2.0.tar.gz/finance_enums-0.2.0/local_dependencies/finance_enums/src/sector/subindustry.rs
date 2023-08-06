use super::Industry;
use serde::{Deserialize, Serialize};

#[derive(Clone, Debug, Deserialize, Display, EnumIter, EnumString, Eq, PartialEq, Serialize)]
#[strum(serialize_all = "PascalCase")]
pub enum SubIndustry {
    // Energy -> Energy Equipment and Services
    OilAndGasDrilling,
    OilAndGasEquipmentAndServices,
    // Energy -> Oil, Gas, and Consumeable Fuels
    IntegratedOilAndGas,
    OilAndGasExplorationAndProduction,
    OilAndGasRefiningAndMarketing,
    OilAndGasStorageAndTransportation,
    CoalAndConsumeableFuels,
    // Materials -> Chemicals
    CommodityChemicals,
    DiversifiedChemicals,
    FertilizersAndAgriculturalChemicals,
    IndustrialGases,
    SpecialtyChemicals,
    // Materials -> Construction Materials
    ConstructionMaterials,
    // Materials -> Containers and Packaging
    MetalGlassAndPlasticContainers,
    PaperAndPlasticPackagingProductsAndMaterials,
    // Materials -> Metals and Mining
    Aluminum,
    DiversifiedMetalsAndMining,
    Copper,
    Gold,
    PreciousMetalsAndMinerals,
    Silver,
    Steel,
    // Materials -> Paper and Forest Products
    ForestProducts,
    PaperProducts,
    // Industrials -> Capital Goods -> AerospaceAndDefense
    AerospaceAndDefense,
    // Industrials -> Capital Goods -> BuildingProducts
    BuildingProducts,
    // Industrials -> Capital Goods -> ConstructionAndEngineering
    ConstructionAndEngineering,
    // Industrials -> Capital Goods -> ElectricalEquipment
    ElectricalComponentsAndEquipment,
    HeavyElectricalEquipment,
    // Industrials -> Capital Goods -> IndustrialConglomerates
    IndustrialConglomerates,
    // Industrials -> Capital Goods -> Machinery
    ConstructionMachineryAndHeavyTransportationEquipment,
    AgriculturalAndFarmMachinery,
    IndustrialMachinerySuppliesAndComponents,
    // Industrials -> Capital Goods -> TradingCompaniesAndDistributors
    TradingCompaniesAndDistributors,
    // Industrials -> Commercial and Professional Services -> CommercialServicesAndSupplies
    CommercialPrinting,
    EnvironmentalAndFacilitiesServices,
    OfficeServicesAndSupplies,
    DiviersifiedSupportServices,
    SecurityAndAlarmServices,
    // Industrials -> Commercial and Professional Services -> ProfessionalServices
    HumanResourcesAndEmploymentServices,
    ResearchAndConsultingServices,
    DataProcessingAndOutsourcedServices,
    // Industrials -> Transportation -> AirFreightAndLogistics
    AirFreightAndLogistics,
    // Industrials -> Transportation -> PassengerAirlines
    PassengerAirlines,
    // Industrials -> Transportation -> MarineTransportation
    MarineTransportation,
    // Industrials -> Transportation -> GroundTransportation
    RailTransportation,
    CargoGroundTransportation,
    PassengerGroundTransportation,
    // Industrials -> Transportation -> TransportationInfrastructure
    AirportServices,
    HighwaysAndRailtracks,
    MarinePortsAndServices,
    // Consumer Discretionary -> Automobiles and Components -> AutomobileComponents
    AutomotivePartsAndEquipment,
    TiresAndRubber,
    // Consumer Discretionary -> Automobiles and Components -> Automobiles
    AutomobileManufacturers,
    MotorcycleManufacturers,
    // Consumer Discretionary -> Consumer Durables and Apparel -> Household Durables
    ConsumerElectronics,
    HomeFurnishings,
    Homebuilding,
    HouseholdAppliances,
    HousewaresAndSpecialties,
    // Consumer Discretionary -> Consumer Durables and Apparel -> Leisure Products
    LeisureProducts,
    // Consumer Discretionary -> Consumer Durables and Apparel -> Textiles, Apprael, and Luxury Goods
    ApparelAccessoriesAndLuxuryGoods,
    Footwear,
    Textiles,
    // Consumer Discretionary -> Consumer Services -> Hotels, Restaurants, and Leisure
    CasinosAndGaming,
    HotelsResortsAndCruiseLines,
    LeisureFacilities,
    Restaurants,
    // Consumer Discretionary -> Consumer Services -> Diversified Consumer Services
    EducationServices,
    SpecializedConsumerServices,
    // Consumer Discretionary -> Consumer Discretionary Distribution and Retail -> Distributors
    Distributors,
    // Consumer Discretionary -> Consumer Discretionary Distribution and Retail -> Broadline Retail
    BroadlineRetail,
    // Consumer Discretionary -> Consumer Discretionary Distribution and Retail -> Specialty Retail
    ApparelRetail,
    ComputerAndElectronicsretail,
    HomeImprovementRetail,
    OtherSpecialtyRetail,
    AutomotiveRetail,
    HomefurnishingRetail,
    // Consumer Staples -> Consumer Staples Distribution And Retail -> Consumer Staples, Distribution, and Retail
    DrugRetail,
    FoodDistributors,
    FoodRetail,
    ConsumerStaplesMerchandiseRetail,
    // Consumer Staples -> Food, Beverage, and Tobacco -> Beverages
    Brewers,
    DistillersAndVintners,
    SoftDrinksAndNonAlcoholicBeverages,
    // Consumer Staples -> Food, Beverage, and Tobacco -> Food Products
    AgriculturalProductsAndServices,
    PackagedFoodsAndMeats,
    // Consumer Staples -> Food, Beverage, and Tobacco -> Tobacco
    Tobacco,
    // Consumer Staples -> Household and Personal Products -> Household Products
    HouseholdProducts,
    // Consumer Staples -> Household and Personal Products -> Personal Care Products
    PersonalCareProducts,
    // Health Care -> Health Care Equipment and Services -> Health Care Equipment and Supplies
    HealthCareEquipment,
    HealthCareSupplies,
    // Health Care -> Health Care Equipment and Services -> Health Care Providers and Services
    HealthCareDistributors,
    HealthCareServices,
    HealthCareFacilities,
    ManagedHealthCare,
    // Health Care -> Health Care Equipment and Services -> Health Care Technology
    HealthCareTechnology,
    // Health Care -> Pharmaceuticals, Biotechnology, and Life Sciences -> Biotechnology
    Biotechnology,
    // Health Care -> Pharmaceuticals, Biotechnology, and Life Sciences -> Pharmaceuticals
    Pharmaceuticals,
    // Health Care -> Pharmaceuticals, Biotechnology, and Life Sciences -> Life Sciences Tools and Services
    LifeSciencesToolsAndServices,
    // Financials -> Banks -> Banks
    DiversifiedBanks,
    RegionalBanks,
    // Financials -> Financial Services -> Financial Services
    DiversifiedFinancialServices,
    MultiSectorHoldings,
    SpecializedFinance,
    CommercialAndResidentialMortgageFinance,
    TransactionAndPaymentProcessingServices,
    // Financials -> Financial Services -> Consumer Finance
    ConsumerFinance,
    // Financials -> Financial Services -> Capital Markets
    AssetManagementAndCustodyBanks,
    InvestmentBankingAndBrokerage,
    DiversifiedCapitalMarkets,
    FinancialExchangesAndData,
    // Financials -> Financial Services -> Mortgage REITs,
    MortgageRealEstateInvestmentTrusts,
    // Financials -> Insurance -> Insurance
    InsuranceBrokers,
    LifeAndHealthInsurance,
    MultilineInsurance,
    PropertyAndCasualtyInsurance,
    Reinsurance,
    // Information Technology -> Software and Services -> ITServices
    ITConsultingAndOtherServices,
    InternetServicesAndInfrastructure,
    // Information Technology -> Software and Services -> Software
    ApplicationSoftware,
    SystemsSoftware,
    // Information Technology -> Technology Equipment and Hardware -> CommunicationsEquipment
    CommunicationsEquipment,
    // Information Technology -> Technology Equipment and Hardware -> TechnologyHardwareStorageAndPeripherals
    TechnologyHardwareStorageAndPeripherals,
    // Information Technology -> Technology Equipment and Hardware -> ElectronicEquipmentInstrumentsAndComponents
    ElectronicEquipmentAndInstruments,
    ElectronicComponents,
    ElectronicManufacturingServices,
    TechnologyDistributors,
    // Information Technology -> Semiconductors and Semiconductor Equipment -> SemiconductorsAndSemiconductorEquipmen
    SemiconductorMaterialsAndEquipment,
    Semiconductors,
    // Communication Services -> Telecommunication Services -> DiversifiedTelecommunicationServices
    AlternativeCarriers,
    IntegratedTelecommunicationServices,
    // Communication Services -> Telecommunication Services -> WirelessTelecommunicationServices
    WirelessTelecommunicationServices,
    // Communication Services -> Media and Entertainment -> Media
    Advertising,
    Broadcasting,
    CableAndSatellite,
    Publishing,
    // Communication Services -> Media and Entertainment -> Entertainment
    MoviesAndEntertainment,
    InteractiveHomeEntertainment,
    // Communication Services -> Media and Entertainment -> InteractiveMediaAndServices
    InteractiveMediaAndServices,
    // Utilities -> ElectricUtilities
    ElectricUtilities,
    // Utilities -> GasUtilities
    GasUtilities,
    // Utilities -> MultiUtilities
    MultiUtilities,
    // Utilities -> WaterUtilities
    WaterUtilities,
    // Utilities -> IndependentPowerAndRenewableElectricityProducers
    IndependentPowerProducersAndEnergyTraders,
    RenewableElectricity,
    // Real Estate -> Equity REITs -> DiversifiedREITs
    DiversifiedREITs,
    // Real Estate -> Equity REITs -> IndustrialREITs
    IndustrialREITs,
    // Real Estate -> Equity REITs -> HotelAndResortREITs
    HotelAndResortREITs,
    // Real Estate -> Equity REITs -> OfficeREITs
    OfficeREITs,
    // Real Estate -> Equity REITs -> HealthCareREITs
    HealthCareREITs,
    // Real Estate -> Equity REITs -> ResidentialREITs
    MultiFamilyResidentialREITs,
    SingleFamilyResidentialREITs,
    // Real Estate -> Equity REITs -> RetailREITs
    RetailREITs,
    // Real Estate -> Equity REITs -> SpecializedREITs
    OtherSpecializedREITs,
    SelfStorageREITs,
    TelecomTowerREITs,
    TimberREITs,
    DataCenterREITs,
    // Real Estate -> Real Estate Management and Development -> RealEstateManagementAndDevelopment
    DiversifiedRealEstateActivities,
    RealEstateOperatingCompanies,
    RealEstateDevelopment,
    RealEstateServices,
}

impl SubIndustry {
    pub fn industry(&self) -> Industry {
        match self {
            SubIndustry::OilAndGasDrilling => Industry::EnergyEquipmentAndServices,
            SubIndustry::OilAndGasEquipmentAndServices => Industry::EnergyEquipmentAndServices,
            SubIndustry::IntegratedOilAndGas => Industry::OilGasAndConsumeableFules,
            SubIndustry::OilAndGasExplorationAndProduction => Industry::OilGasAndConsumeableFules,
            SubIndustry::OilAndGasRefiningAndMarketing => Industry::OilGasAndConsumeableFules,
            SubIndustry::OilAndGasStorageAndTransportation => Industry::OilGasAndConsumeableFules,
            SubIndustry::CoalAndConsumeableFuels => Industry::OilGasAndConsumeableFules,
            SubIndustry::CommodityChemicals => Industry::Chemicals,
            SubIndustry::DiversifiedChemicals => Industry::Chemicals,
            SubIndustry::FertilizersAndAgriculturalChemicals => Industry::Chemicals,
            SubIndustry::IndustrialGases => Industry::Chemicals,
            SubIndustry::SpecialtyChemicals => Industry::Chemicals,
            SubIndustry::ConstructionMaterials => Industry::ConstructionMaterials,
            SubIndustry::MetalGlassAndPlasticContainers => Industry::ContainersAndPackaging,
            SubIndustry::PaperAndPlasticPackagingProductsAndMaterials => {
                Industry::ContainersAndPackaging
            }
            SubIndustry::Aluminum => Industry::MetalsAndMining,
            SubIndustry::DiversifiedMetalsAndMining => Industry::MetalsAndMining,
            SubIndustry::Copper => Industry::MetalsAndMining,
            SubIndustry::Gold => Industry::MetalsAndMining,
            SubIndustry::PreciousMetalsAndMinerals => Industry::MetalsAndMining,
            SubIndustry::Silver => Industry::MetalsAndMining,
            SubIndustry::Steel => Industry::MetalsAndMining,
            SubIndustry::ForestProducts => Industry::PaperAndForestProducts,
            SubIndustry::PaperProducts => Industry::PaperAndForestProducts,
            SubIndustry::AerospaceAndDefense => Industry::AerospaceAndDefense,
            SubIndustry::BuildingProducts => Industry::BuildingProducts,
            SubIndustry::ConstructionAndEngineering => Industry::ConstructionAndEngineering,
            SubIndustry::ElectricalComponentsAndEquipment => Industry::ElectricalEquipment,
            SubIndustry::HeavyElectricalEquipment => Industry::ElectricalEquipment,
            SubIndustry::IndustrialConglomerates => Industry::IndustrialConglomerates,
            SubIndustry::ConstructionMachineryAndHeavyTransportationEquipment => {
                Industry::Machinery
            }
            SubIndustry::AgriculturalAndFarmMachinery => Industry::Machinery,
            SubIndustry::IndustrialMachinerySuppliesAndComponents => Industry::Machinery,
            SubIndustry::TradingCompaniesAndDistributors => {
                Industry::TradingCompaniesAndDistributors
            }
            SubIndustry::CommercialPrinting => Industry::CommercialServicesAndSupplies,
            SubIndustry::EnvironmentalAndFacilitiesServices => {
                Industry::CommercialServicesAndSupplies
            }
            SubIndustry::OfficeServicesAndSupplies => Industry::CommercialServicesAndSupplies,
            SubIndustry::DiviersifiedSupportServices => Industry::CommercialServicesAndSupplies,
            SubIndustry::SecurityAndAlarmServices => Industry::CommercialServicesAndSupplies,
            SubIndustry::HumanResourcesAndEmploymentServices => Industry::ProfessionalServices,
            SubIndustry::ResearchAndConsultingServices => Industry::ProfessionalServices,
            SubIndustry::DataProcessingAndOutsourcedServices => Industry::ProfessionalServices,
            SubIndustry::AirFreightAndLogistics => Industry::AirFreightAndLogistics,
            SubIndustry::PassengerAirlines => Industry::PassengerAirlines,
            SubIndustry::MarineTransportation => Industry::MarineTransportation,
            SubIndustry::RailTransportation => Industry::GroundTransportation,
            SubIndustry::CargoGroundTransportation => Industry::GroundTransportation,
            SubIndustry::PassengerGroundTransportation => Industry::GroundTransportation,
            SubIndustry::AirportServices => Industry::TransportationInfrastructure,
            SubIndustry::HighwaysAndRailtracks => Industry::TransportationInfrastructure,
            SubIndustry::MarinePortsAndServices => Industry::TransportationInfrastructure,
            SubIndustry::AutomotivePartsAndEquipment => Industry::AutomobileComponents,
            SubIndustry::TiresAndRubber => Industry::AutomobileComponents,
            SubIndustry::AutomobileManufacturers => Industry::Automobiles,
            SubIndustry::MotorcycleManufacturers => Industry::Automobiles,
            SubIndustry::ConsumerElectronics => Industry::HouseholdDurables,
            SubIndustry::HomeFurnishings => Industry::HouseholdDurables,
            SubIndustry::Homebuilding => Industry::HouseholdDurables,
            SubIndustry::HouseholdAppliances => Industry::HouseholdDurables,
            SubIndustry::HousewaresAndSpecialties => Industry::HouseholdDurables,
            SubIndustry::LeisureProducts => Industry::LeisureProducts,
            SubIndustry::ApparelAccessoriesAndLuxuryGoods => {
                Industry::TextilesApparelAndLuxuryGoods
            }
            SubIndustry::Footwear => Industry::TextilesApparelAndLuxuryGoods,
            SubIndustry::Textiles => Industry::TextilesApparelAndLuxuryGoods,
            SubIndustry::CasinosAndGaming => Industry::HotelsRestaurantsAndLeisure,
            SubIndustry::HotelsResortsAndCruiseLines => Industry::HotelsRestaurantsAndLeisure,
            SubIndustry::LeisureFacilities => Industry::HotelsRestaurantsAndLeisure,
            SubIndustry::Restaurants => Industry::HotelsRestaurantsAndLeisure,
            SubIndustry::EducationServices => Industry::DiversifiedConsumerServices,
            SubIndustry::SpecializedConsumerServices => Industry::DiversifiedConsumerServices,
            SubIndustry::Distributors => Industry::Distributors,
            SubIndustry::BroadlineRetail => Industry::BroadlineRetail,
            SubIndustry::ApparelRetail => Industry::SpecialtyRetail,
            SubIndustry::ComputerAndElectronicsretail => Industry::SpecialtyRetail,
            SubIndustry::HomeImprovementRetail => Industry::SpecialtyRetail,
            SubIndustry::OtherSpecialtyRetail => Industry::SpecialtyRetail,
            SubIndustry::AutomotiveRetail => Industry::SpecialtyRetail,
            SubIndustry::HomefurnishingRetail => Industry::SpecialtyRetail,
            SubIndustry::DrugRetail => Industry::ConsumerStaplesDistributionAndRetail,
            SubIndustry::FoodDistributors => Industry::ConsumerStaplesDistributionAndRetail,
            SubIndustry::FoodRetail => Industry::ConsumerStaplesDistributionAndRetail,
            SubIndustry::ConsumerStaplesMerchandiseRetail => {
                Industry::ConsumerStaplesDistributionAndRetail
            }
            SubIndustry::Brewers => Industry::Beverages,
            SubIndustry::DistillersAndVintners => Industry::Beverages,
            SubIndustry::SoftDrinksAndNonAlcoholicBeverages => Industry::Beverages,
            SubIndustry::AgriculturalProductsAndServices => Industry::FoodProducts,
            SubIndustry::PackagedFoodsAndMeats => Industry::FoodProducts,
            SubIndustry::Tobacco => Industry::Tobacco,
            SubIndustry::HouseholdProducts => Industry::HouseholdProducts,
            SubIndustry::PersonalCareProducts => Industry::PersonalCareProducts,
            SubIndustry::HealthCareEquipment => Industry::HealthCareEquipmentAndSupplies,
            SubIndustry::HealthCareSupplies => Industry::HealthCareEquipmentAndSupplies,
            SubIndustry::HealthCareDistributors => Industry::HealthCareProvidersAndServices,
            SubIndustry::HealthCareServices => Industry::HealthCareProvidersAndServices,
            SubIndustry::HealthCareFacilities => Industry::HealthCareProvidersAndServices,
            SubIndustry::ManagedHealthCare => Industry::HealthCareProvidersAndServices,
            SubIndustry::HealthCareTechnology => Industry::HealthCareTechnology,
            SubIndustry::Biotechnology => Industry::Biotechnology,
            SubIndustry::Pharmaceuticals => Industry::Pharmaceuticals,
            SubIndustry::LifeSciencesToolsAndServices => Industry::LifeSciencesToolsAndServices,
            SubIndustry::DiversifiedBanks => Industry::Banks,
            SubIndustry::RegionalBanks => Industry::Banks,
            SubIndustry::DiversifiedFinancialServices => Industry::FinancialServices,
            SubIndustry::MultiSectorHoldings => Industry::FinancialServices,
            SubIndustry::SpecializedFinance => Industry::FinancialServices,
            SubIndustry::CommercialAndResidentialMortgageFinance => Industry::FinancialServices,
            SubIndustry::TransactionAndPaymentProcessingServices => Industry::FinancialServices,
            SubIndustry::ConsumerFinance => Industry::ConsumerFinance,
            SubIndustry::AssetManagementAndCustodyBanks => Industry::CapitalMarkets,
            SubIndustry::InvestmentBankingAndBrokerage => Industry::CapitalMarkets,
            SubIndustry::DiversifiedCapitalMarkets => Industry::CapitalMarkets,
            SubIndustry::FinancialExchangesAndData => Industry::CapitalMarkets,
            SubIndustry::MortgageRealEstateInvestmentTrusts => {
                Industry::MortgageRealEstateInvestmentTrusts
            }
            SubIndustry::InsuranceBrokers => Industry::Insurance,
            SubIndustry::LifeAndHealthInsurance => Industry::Insurance,
            SubIndustry::MultilineInsurance => Industry::Insurance,
            SubIndustry::PropertyAndCasualtyInsurance => Industry::Insurance,
            SubIndustry::Reinsurance => Industry::Insurance,
            SubIndustry::ITConsultingAndOtherServices => Industry::ITServices,
            SubIndustry::InternetServicesAndInfrastructure => Industry::ITServices,
            SubIndustry::ApplicationSoftware => Industry::Software,
            SubIndustry::SystemsSoftware => Industry::Software,
            SubIndustry::CommunicationsEquipment => Industry::CommunicationsEquipment,
            SubIndustry::TechnologyHardwareStorageAndPeripherals => {
                Industry::TechnologyHardwareStorageAndPeripherals
            }
            SubIndustry::ElectronicEquipmentAndInstruments => {
                Industry::ElectronicEquipmentInstrumentsAndComponents
            }
            SubIndustry::ElectronicComponents => {
                Industry::ElectronicEquipmentInstrumentsAndComponents
            }
            SubIndustry::ElectronicManufacturingServices => {
                Industry::ElectronicEquipmentInstrumentsAndComponents
            }
            SubIndustry::TechnologyDistributors => {
                Industry::ElectronicEquipmentInstrumentsAndComponents
            }
            SubIndustry::SemiconductorMaterialsAndEquipment => {
                Industry::SemiconductorsAndSemiconductorEquipment
            }
            SubIndustry::Semiconductors => Industry::SemiconductorsAndSemiconductorEquipment,
            SubIndustry::AlternativeCarriers => Industry::DiversifiedTelecommunicationServices,
            SubIndustry::IntegratedTelecommunicationServices => {
                Industry::DiversifiedTelecommunicationServices
            }
            SubIndustry::WirelessTelecommunicationServices => {
                Industry::WirelessTelecommunicationServices
            }
            SubIndustry::Advertising => Industry::Media,
            SubIndustry::Broadcasting => Industry::Media,
            SubIndustry::CableAndSatellite => Industry::Media,
            SubIndustry::Publishing => Industry::Media,
            SubIndustry::MoviesAndEntertainment => Industry::Entertainment,
            SubIndustry::InteractiveHomeEntertainment => Industry::Entertainment,
            SubIndustry::InteractiveMediaAndServices => Industry::InteractiveMediaAndServices,
            SubIndustry::ElectricUtilities => Industry::ElectricUtilities,
            SubIndustry::GasUtilities => Industry::GasUtilities,
            SubIndustry::MultiUtilities => Industry::MultiUtilities,
            SubIndustry::WaterUtilities => Industry::WaterUtilities,
            SubIndustry::IndependentPowerProducersAndEnergyTraders => {
                Industry::IndependentPowerAndRenewableElectricityProducers
            }
            SubIndustry::RenewableElectricity => {
                Industry::IndependentPowerAndRenewableElectricityProducers
            }
            SubIndustry::DiversifiedREITs => Industry::DiversifiedREITs,
            SubIndustry::IndustrialREITs => Industry::IndustrialREITs,
            SubIndustry::HotelAndResortREITs => Industry::HotelAndResortREITs,
            SubIndustry::OfficeREITs => Industry::OfficeREITs,
            SubIndustry::HealthCareREITs => Industry::HealthCareREITs,
            SubIndustry::MultiFamilyResidentialREITs => Industry::ResidentialREITs,
            SubIndustry::SingleFamilyResidentialREITs => Industry::ResidentialREITs,
            SubIndustry::RetailREITs => Industry::RetailREITs,
            SubIndustry::OtherSpecializedREITs => Industry::SpecializedREITs,
            SubIndustry::SelfStorageREITs => Industry::SpecializedREITs,
            SubIndustry::TelecomTowerREITs => Industry::SpecializedREITs,
            SubIndustry::TimberREITs => Industry::SpecializedREITs,
            SubIndustry::DataCenterREITs => Industry::SpecializedREITs,
            SubIndustry::DiversifiedRealEstateActivities => {
                Industry::RealEstateManagementAndDevelopment
            }
            SubIndustry::RealEstateOperatingCompanies => {
                Industry::RealEstateManagementAndDevelopment
            }
            SubIndustry::RealEstateDevelopment => Industry::RealEstateManagementAndDevelopment,
            SubIndustry::RealEstateServices => Industry::RealEstateManagementAndDevelopment,
        }
    }
}
