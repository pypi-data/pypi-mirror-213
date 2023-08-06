use pyo3::prelude::*;
use pyo3::types::PyType;
use strum::IntoEnumIterator;
use std::str::FromStr;

use finance_enums::{EquityType as BaseEquityType};


#[pyclass]
pub struct EquityType {
    pub typ: BaseEquityType
}

#[pymethods]
impl EquityType {
    #[new]
    fn py_new(value: String) -> PyResult<Self> {
        Ok(
            EquityType {
                typ: BaseEquityType::from_str(value.as_str()).unwrap()
            }
        )
    }
    
    fn __str__(&self) -> PyResult<String>   {
        Ok(format!("{}", self.typ.to_string()))
    }
    
    fn __repr__(&self) -> PyResult<String>   {
        Ok(format!("EquityType<{}>", self.typ.to_string()))
    }
    
    fn __eq__(&self, other: &Self) -> bool   {
        self.typ == other.typ
    }
    
    #[classmethod]
    fn __len__(_cls: &PyType) -> PyResult<usize> {
        Ok(BaseEquityType::iter().count())
    }
    
    // TODO figure out how to make a class iterator,
    // is way too complicated in pyo3 rn
    #[staticmethod]
    fn members() -> Vec<EquityType> {
        BaseEquityType::iter().map(|item: BaseEquityType| EquityType{typ: item} ).collect()
    }

    #[classattr]
    #[allow(non_snake_case)]
    fn Shares() -> EquityType {
        EquityType {
            typ: BaseEquityType::Shares
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn PreferredShares() -> EquityType {
        EquityType {
            typ: BaseEquityType::PreferredShares
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn ConvertibleShares() -> EquityType {
        EquityType {
            typ: BaseEquityType::ConvertibleShares
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn PreferredConvertibleShares() -> EquityType {
        EquityType {
            typ: BaseEquityType::PreferredConvertibleShares
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn DepositoryReceipt() -> EquityType {
        EquityType {
            typ: BaseEquityType::DepositoryReceipt
        }
    }
}
