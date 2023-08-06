use super::IndustryGroup;
use serde::{Deserialize, Serialize};

// macro_rules! define_fruits {
//     {$($fruit:ident -> $name:literal),* $(,)?} => {
//         #[allow(
//             missing_copy_implementations,
//             missing_debug_implementations,
//         )]
//         #[derive(Display, EnumIter, EnumString, Clone, Copy, Debug)]
//         pub enum Fruits {
//             $(
//                 // #[strum(to_string = $name)]
//                 $fruit,
//             )*
//         }
//     };
// }

// define_fruits! {
//     Apple -> "green",
//     Orange -> "orange",
// }

// macro_rules! custom_enum {
//     (
//      $(#[$meta:meta])*
//      $vis:vis enum $enum_name:ident {
//         $(
//             $field_name:ident
//         ),*$(,)+
//     }
//     ) => {
//             $(#[$meta, Debug, Display, EnumString, Eq, PartialEq])*
//             pub enum $enum_name{
//                 $(
//                     #[strum(serialize=stringify!($field_name), serialize=stringify!(lower!($field_name)), serialize=stringify!(snake!($field_name)), serialize=stringify!(shouty!($field_name)))]
//                     $field_name,
//                 )*
//             }
//     }
// }

#[derive(Clone, Debug, Deserialize, Display, EnumIter, EnumString, Eq, PartialEq, Serialize)]
#[strum(serialize_all = "PascalCase")]
pub enum Sector {
    Energy,
    Materials,
    Industrials,
    ConsumerDiscretionary,
    ConsumerStaples,
    HealthCare,
    Financials,
    InformationTechnology,
    CommunicationServices,
    Utilities,
    RealEstate,
}

impl Sector {
    pub fn industry_groups(&self) -> Vec<IndustryGroup> {
        match self {
            Sector::Energy => vec![IndustryGroup::Energy],
            Sector::Materials => vec![IndustryGroup::Materials],
            Sector::Industrials => vec![
                IndustryGroup::CapitalGoods,
                IndustryGroup::CommercialAndProfessionalServices,
                IndustryGroup::Transportation,
            ],
            Sector::ConsumerDiscretionary => vec![
                IndustryGroup::AutomobilesAndComponents,
                IndustryGroup::ConsumerDurablesAndApparel,
                IndustryGroup::ConsumerServices,
                IndustryGroup::ConsumerDiscretionaryDistributionAndRetail,
            ],
            Sector::ConsumerStaples => vec![
                IndustryGroup::ConsumerStaplesDistributionAndRetail,
                IndustryGroup::FoodBeverageAndTobacco,
                IndustryGroup::HouseholdAndPersonalProducts,
            ],
            Sector::HealthCare => vec![
                IndustryGroup::HealthCareEquipmentAndServices,
                IndustryGroup::PharmaceuticalsBiotechnologyAndLifeSciences,
            ],
            Sector::Financials => vec![
                IndustryGroup::Banks,
                IndustryGroup::FinancialServices,
                IndustryGroup::Insurance,
            ],
            Sector::InformationTechnology => vec![
                IndustryGroup::SoftwareAndServices,
                IndustryGroup::TechnologyHardwareAndEquipment,
                IndustryGroup::SemiconductorsAndSemiconductorEquipment,
            ],
            Sector::CommunicationServices => vec![
                IndustryGroup::TelecommunicationServices,
                IndustryGroup::MediaAndEntertainment,
            ],
            Sector::Utilities => vec![IndustryGroup::Utilities],
            Sector::RealEstate => vec![
                IndustryGroup::EquityRealEstateInvestmentTrusts,
                IndustryGroup::RealEstateManagementAndDevelopment,
            ],
        }
    }
}

/**********************************/
#[cfg(test)]
mod sector_tests {
    use super::*;
    use std::str::FromStr;
    use strum::IntoEnumIterator;

    #[test]
    fn test_from_str() {
        let sec = Sector::from_str("RealEstate").unwrap();
        assert_eq!(Sector::RealEstate, sec);
    }
    #[test]
    fn test_to_str() {
        let sec = Sector::RealEstate.to_string();
        assert_eq!("RealEstate", sec);
    }
    #[test]
    fn test_iter() {
        let sec: Vec<Sector> = Sector::iter().collect();
        assert_eq!(
            vec![
                Sector::Energy,
                Sector::Materials,
                Sector::Industrials,
                Sector::ConsumerDiscretionary,
                Sector::ConsumerStaples,
                Sector::HealthCare,
                Sector::Financials,
                Sector::InformationTechnology,
                Sector::CommunicationServices,
                Sector::Utilities,
                Sector::RealEstate,
            ],
            sec
        );
    }
    // #[test]
    // fn test_from_str_space() {
    //     let sec = Sector::from_str("Real Estate").unwrap();
    //     assert_eq!(Sector::RealEstate, sec);
    // }
    // #[test]
    // fn test_from_str_lower() {
    //     let sec = Sector::from_str("realestate").unwrap();
    //     assert_eq!(Sector::RealEstate, sec);
    // }
    // #[test]
    // fn test_from_str_snake() {
    //     let sec = Sector::from_str("real_estate").unwrap();
    //     assert_eq!(Sector::RealEstate, sec);
    // }
}
