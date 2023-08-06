use pyo3::prelude::*;
use pyo3::types::PyType;
use strum::IntoEnumIterator;
use std::str::FromStr;

use finance_enums::{IndustryGroup as BaseIndustryGroup};
use super::{Sector, Industry};

#[pyclass]
pub struct IndustryGroup {
    pub typ: BaseIndustryGroup,
}

#[pymethods]
impl IndustryGroup {
    #[new]
    fn py_new(value: String) -> PyResult<Self> {
        Ok(
            IndustryGroup {
                typ: BaseIndustryGroup::from_str(value.as_str()).unwrap()
            }
        )

    }

    fn __str__(&self) -> PyResult<String>   {
        Ok(format!("{}", self.typ.to_string()))
    }

    fn __repr__(&self) -> PyResult<String>   {
        Ok(format!("IndustryGroup<{}>", self.typ.to_string()))
    }

    fn __eq__(&self, other: &Self) -> bool   {
        self.typ == other.typ
    }

    fn sector(&self) -> Sector {
        Sector {
            typ: self.typ.sector()
        }
    }

    fn industries(&self) -> Vec<Industry> {
        self.typ.industries().iter().map(|item| Industry{typ: item.clone()} ).collect()
    }

    #[classmethod]
    fn __len__(_cls: &PyType) -> PyResult<usize> {
        Ok(BaseIndustryGroup::iter().count())
    }

    // TODO figure out how to make a class iterator,
    // is way too complicated in pyo3 rn
    #[staticmethod]
    fn members() -> Vec<IndustryGroup> {
        BaseIndustryGroup::iter().map(|item: BaseIndustryGroup| IndustryGroup{typ: item} ).collect()
    }

    // Energy
    #[classattr]
    #[allow(non_snake_case)]
    fn Energy() -> IndustryGroup {
        IndustryGroup {
            typ: BaseIndustryGroup::Energy
        }
    }

    // Materials
    #[classattr]
    #[allow(non_snake_case)]
    fn Materials() -> IndustryGroup {
        IndustryGroup {
            typ: BaseIndustryGroup::Materials
        }
    }

    // Industrials
    #[classattr]
    #[allow(non_snake_case)]
    fn CapitalGoods() -> IndustryGroup {
        IndustryGroup {
            typ: BaseIndustryGroup::CapitalGoods
        }
    }

    #[classattr]
    #[allow(non_snake_case)]
    fn CommercialAndProfessionalServices() -> IndustryGroup {
        IndustryGroup {
            typ: BaseIndustryGroup::CommercialAndProfessionalServices
        }
    }

    #[classattr]
    #[allow(non_snake_case)]
    fn Transportation() -> IndustryGroup {
        IndustryGroup {
            typ: BaseIndustryGroup::Transportation
        }
    }
    
    // Consumer Discretionary
    #[classattr]
    #[allow(non_snake_case)]
    fn AutomobilesAndComponents() -> IndustryGroup {
        IndustryGroup {
            typ: BaseIndustryGroup::AutomobilesAndComponents
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn ConsumerDurablesAndApparel() -> IndustryGroup {
        IndustryGroup {
            typ: BaseIndustryGroup::ConsumerDurablesAndApparel
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn ConsumerServices() -> IndustryGroup {
        IndustryGroup {
            typ: BaseIndustryGroup::ConsumerServices
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn ConsumerDiscretionaryDistributionAndRetail() -> IndustryGroup {
        IndustryGroup {
            typ: BaseIndustryGroup::ConsumerDiscretionaryDistributionAndRetail
        }
    }
    // Consumer Staples
    #[classattr]
    #[allow(non_snake_case)]
    fn ConsumerStaplesDistributionAndRetail() -> IndustryGroup {
        IndustryGroup {
            typ: BaseIndustryGroup::ConsumerStaplesDistributionAndRetail
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn FoodBeverageAndTobacco() -> IndustryGroup {
        IndustryGroup {
            typ: BaseIndustryGroup::FoodBeverageAndTobacco
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn HouseholdAndPersonalProducts() -> IndustryGroup {
        IndustryGroup {
            typ: BaseIndustryGroup::HouseholdAndPersonalProducts
        }
    }
    // Health Care
    #[classattr]
    #[allow(non_snake_case)]
    fn HealthCareEquipmentAndServices() -> IndustryGroup {
        IndustryGroup {
            typ: BaseIndustryGroup::HealthCareEquipmentAndServices
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn PharmaceuticalsBiotechnologyAndLifeSciences() -> IndustryGroup {
        IndustryGroup {
            typ: BaseIndustryGroup::PharmaceuticalsBiotechnologyAndLifeSciences
        }
    }
    // Financials
    #[classattr]
    #[allow(non_snake_case)]
    fn Banks() -> IndustryGroup {
        IndustryGroup {
            typ: BaseIndustryGroup::Banks
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn FinancialServices() -> IndustryGroup {
        IndustryGroup {
            typ: BaseIndustryGroup::FinancialServices
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn Insurance() -> IndustryGroup {
        IndustryGroup {
            typ: BaseIndustryGroup::Insurance
        }
    }
    // Information Technology
    #[classattr]
    #[allow(non_snake_case)]
    fn SoftwareAndServices() -> IndustryGroup {
        IndustryGroup {
            typ: BaseIndustryGroup::SoftwareAndServices
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn TechnologyHardwareAndEquipment() -> IndustryGroup {
        IndustryGroup {
            typ: BaseIndustryGroup::TechnologyHardwareAndEquipment
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn SemiconductorsAndSemiconductorEquipment() -> IndustryGroup {
        IndustryGroup {
            typ: BaseIndustryGroup::SemiconductorsAndSemiconductorEquipment
        }
    }
    // Communication Services
    #[classattr]
    #[allow(non_snake_case)]
    fn TelecommunicationServices() -> IndustryGroup {
        IndustryGroup {
            typ: BaseIndustryGroup::TelecommunicationServices
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn MediaAndEntertainment() -> IndustryGroup {
        IndustryGroup {
            typ: BaseIndustryGroup::MediaAndEntertainment
        }
    }
    // Utilities
    #[classattr]
    #[allow(non_snake_case)]
    fn Utilities() -> IndustryGroup {
        IndustryGroup {
            typ: BaseIndustryGroup::Utilities
        }
    }
    // Real Estate
    #[classattr]
    #[allow(non_snake_case)]
    fn EquityRealEstateInvestmentTrusts() -> IndustryGroup {
        IndustryGroup {
            typ: BaseIndustryGroup::EquityRealEstateInvestmentTrusts
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn RealEstateManagementAndDevelopment() -> IndustryGroup {
        IndustryGroup {
            typ: BaseIndustryGroup::RealEstateManagementAndDevelopment
        }
    }
}
