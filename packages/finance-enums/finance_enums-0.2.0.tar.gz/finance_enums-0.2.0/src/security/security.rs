use pyo3::prelude::*;
use pyo3::types::PyType;
use strum::IntoEnumIterator;
use std::str::FromStr;

use finance_enums::{SecurityType as BaseSecurityType};

#[pyclass]
pub struct SecurityType {
    pub typ: BaseSecurityType
}

#[pymethods]
impl SecurityType {
    #[new]
    fn py_new(value: String) -> PyResult<Self> {
        Ok(
            SecurityType {
                typ: BaseSecurityType::from_str(value.as_str()).unwrap()
            }
        )
    }
    
    fn __str__(&self) -> PyResult<String>   {
        Ok(format!("{}", self.typ.to_string()))
    }
    
    fn __repr__(&self) -> PyResult<String>   {
        Ok(format!("SecurityType<{}>", self.typ.to_string()))
    }
    
    fn __eq__(&self, other: &Self) -> bool   {
        self.typ == other.typ
    }
    
    #[classmethod]
    fn __len__(_cls: &PyType) -> PyResult<usize> {
        Ok(BaseSecurityType::iter().count())
    }
    
    // TODO figure out how to make a class iterator,
    // is way too complicated in pyo3 rn
    #[staticmethod]
    fn members() -> Vec<SecurityType> {
        BaseSecurityType::iter().map(|item: BaseSecurityType| SecurityType{typ: item} ).collect()
    }


    #[classattr]
    #[allow(non_snake_case)]
    fn Equity() -> SecurityType {
        SecurityType {
            typ: BaseSecurityType::Equity
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn Option() -> SecurityType {
        SecurityType {
            typ: BaseSecurityType::Option
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn Bond() -> SecurityType {
        SecurityType {
            typ: BaseSecurityType::Bond
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn Forward() -> SecurityType {
        SecurityType {
            typ: BaseSecurityType::Forward
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn Future() -> SecurityType {
        SecurityType {
            typ: BaseSecurityType::Future
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn PerpetualFuture() -> SecurityType {
        SecurityType {
            typ: BaseSecurityType::PerpetualFuture
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn Spread() -> SecurityType {
        SecurityType {
            typ: BaseSecurityType::Spread
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn Fund() -> SecurityType {
        SecurityType {
            typ: BaseSecurityType::Fund
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn Commodity() -> SecurityType {
        SecurityType {
            typ: BaseSecurityType::Commodity
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn Currency() -> SecurityType {
        SecurityType {
            typ: BaseSecurityType::Currency
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn Pair() -> SecurityType {
        SecurityType {
            typ: BaseSecurityType::Pair
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn Index() -> SecurityType {
        SecurityType {
            typ: BaseSecurityType::Index
        }
    }
}
