use pyo3::prelude::*;
use pyo3::types::PyType;
use strum::IntoEnumIterator;
use std::str::FromStr;

use finance_enums::{Sector as BaseSector};
use super::IndustryGroup;

#[pyclass]
pub struct Sector {
    pub typ: BaseSector,
}

#[pymethods]
impl Sector {
    #[new]
    fn py_new(value: String) -> PyResult<Self> {
        Ok(
            Sector {
                typ: BaseSector::from_str(value.as_str()).unwrap()
            }
        )

    }

    fn __str__(&self) -> PyResult<String>   {
        Ok(format!("{}", self.typ.to_string()))
    }

    fn __repr__(&self) -> PyResult<String>   {
        Ok(format!("Sector<{}>", self.typ.to_string()))
    }

    fn __eq__(&self, other: &Self) -> bool   {
        self.typ == other.typ
    }

    fn industry_groups(&self) -> Vec<IndustryGroup> {
        self.typ.industry_groups().iter().map(|item| IndustryGroup{typ: item.clone()} ).collect()
    }

    #[classmethod]
    fn __len__(_cls: &PyType) -> PyResult<usize> {
        Ok(BaseSector::iter().count())
    }

    // TODO figure out how to make a class iterator,
    // is way too complicated in pyo3 rn
    #[staticmethod]
    fn members() -> Vec<Sector> {
        BaseSector::iter().map(|item: BaseSector| Sector{typ: item} ).collect()
    }

    // Enum values
    #[classattr]
    #[allow(non_snake_case)]
    fn Energy() -> Sector {
        Sector {
            typ: BaseSector::Energy
        }
    }

    #[classattr]
    #[allow(non_snake_case)]
    fn Materials() -> Sector {
        Sector {
            typ: BaseSector::Materials
        }
    }

    #[classattr]
    #[allow(non_snake_case)]
    fn Industrials() -> Sector {
        Sector {
            typ: BaseSector::Industrials
        }
    }

    #[classattr]
    #[allow(non_snake_case)]
    fn ConsumerDiscretionary() -> Sector {
        Sector {
            typ: BaseSector::ConsumerDiscretionary
        }
    }

    #[classattr]
    #[allow(non_snake_case)]
    fn ConsumerStaples() -> Sector {
        Sector {
            typ: BaseSector::ConsumerStaples
        }
    }

    #[classattr]
    #[allow(non_snake_case)]
    fn HealthCare() -> Sector {
        Sector {
            typ: BaseSector::HealthCare
        }
    }

    #[classattr]
    #[allow(non_snake_case)]
    fn Financials() -> Sector {
        Sector {
            typ: BaseSector::Financials
        }
    }

    #[classattr]
    #[allow(non_snake_case)]
    fn InformationTechnology() -> Sector {
        Sector {
            typ: BaseSector::InformationTechnology
        }
    }

    #[classattr]
    #[allow(non_snake_case)]
    fn CommunicationServices() -> Sector {
        Sector {
            typ: BaseSector::CommunicationServices
        }
    }

    #[classattr]
    #[allow(non_snake_case)]
    fn Utilities() -> Sector {
        Sector {
            typ: BaseSector::Utilities
        }
    }

    #[classattr]
    #[allow(non_snake_case)]
    fn RealEstate() -> Sector {
        Sector {
            typ: BaseSector::RealEstate
        }
    }
}
