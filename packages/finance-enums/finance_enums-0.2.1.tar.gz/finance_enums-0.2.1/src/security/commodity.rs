use pyo3::prelude::*;
use pyo3::types::PyType;
use strum::IntoEnumIterator;
use std::str::FromStr;

use finance_enums::{CommodityType as BaseCommodityType};

#[pyclass]
pub struct CommodityType {
    pub typ: BaseCommodityType
}

#[pymethods]
impl CommodityType {
    #[new]
    fn py_new(value: String) -> PyResult<Self> {
        Ok(
            CommodityType {
                typ: BaseCommodityType::from_str(value.as_str()).unwrap()
            }
        )
    }
    
    fn __str__(&self) -> PyResult<String>   {
        Ok(format!("{}", self.typ.to_string()))
    }
    
    fn __repr__(&self) -> PyResult<String>   {
        Ok(format!("CommodityType<{}>", self.typ.to_string()))
    }
    
    fn __eq__(&self, other: &Self) -> bool   {
        self.typ == other.typ
    }
    
    #[classmethod]
    fn __len__(_cls: &PyType) -> PyResult<usize> {
        Ok(BaseCommodityType::iter().count())
    }
    
    // TODO figure out how to make a class iterator,
    // is way too complicated in pyo3 rn
    #[staticmethod]
    fn members() -> Vec<CommodityType> {
        BaseCommodityType::iter().map(|item: BaseCommodityType| CommodityType{typ: item} ).collect()
    }

    #[classattr]
    #[allow(non_snake_case)]
    fn Energy() -> CommodityType {
        CommodityType {
            typ: BaseCommodityType::Energy
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn Metals() -> CommodityType {
        CommodityType {
            typ: BaseCommodityType::Metals
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn Agriculture() -> CommodityType {
        CommodityType {
            typ: BaseCommodityType::Agriculture
        }
    }
}
