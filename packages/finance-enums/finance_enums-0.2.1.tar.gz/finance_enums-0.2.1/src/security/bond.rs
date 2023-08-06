use pyo3::prelude::*;
use pyo3::types::PyType;
use strum::IntoEnumIterator;
use std::str::FromStr;

use finance_enums::{BondType as BaseBondType};

#[pyclass]
pub struct BondType {
    pub typ: BaseBondType
}

#[pymethods]
impl BondType {
    #[new]
    fn py_new(value: String) -> PyResult<Self> {
        Ok(
            BondType {
                typ: BaseBondType::from_str(value.as_str()).unwrap()
            }
        )
    }
    
    fn __str__(&self) -> PyResult<String>   {
        Ok(format!("{}", self.typ.to_string()))
    }
    
    fn __repr__(&self) -> PyResult<String>   {
        Ok(format!("BondType<{}>", self.typ.to_string()))
    }
    
    fn __eq__(&self, other: &Self) -> bool   {
        self.typ == other.typ
    }
    
    #[classmethod]
    fn __len__(_cls: &PyType) -> PyResult<usize> {
        Ok(BaseBondType::iter().count())
    }
    
    // TODO figure out how to make a class iterator,
    // is way too complicated in pyo3 rn
    #[staticmethod]
    fn members() -> Vec<BondType> {
        BaseBondType::iter().map(|item: BaseBondType| BondType{typ: item} ).collect()
    }

    #[classattr]
    #[allow(non_snake_case)]
    fn Corporate() -> BondType {
        BondType {
            typ: BaseBondType::Corporate
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn Government() -> BondType {
        BondType {
            typ: BaseBondType::Government
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn Municipal() -> BondType {
        BondType {
            typ: BaseBondType::Municipal
        }
    }
}
