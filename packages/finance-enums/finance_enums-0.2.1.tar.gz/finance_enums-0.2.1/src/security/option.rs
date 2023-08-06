use pyo3::prelude::*;
use pyo3::types::PyType;
use strum::IntoEnumIterator;
use std::str::FromStr;

use finance_enums::{OptionType as BaseOptionType, OptionExerciseType as BaseOptionExerciseType};


#[pyclass]
pub struct OptionType {
    pub typ: BaseOptionType
}

#[pymethods]
impl OptionType {
    #[new]
    fn py_new(value: String) -> PyResult<Self> {
        Ok(
            OptionType {
                typ: BaseOptionType::from_str(value.as_str()).unwrap()
            }
        )
    }
    
    fn __str__(&self) -> PyResult<String>   {
        Ok(format!("{}", self.typ.to_string()))
    }
    
    fn __repr__(&self) -> PyResult<String>   {
        Ok(format!("OptionType<{}>", self.typ.to_string()))
    }
    
    fn __eq__(&self, other: &Self) -> bool   {
        self.typ == other.typ
    }
    
    #[classmethod]
    fn __len__(_cls: &PyType) -> PyResult<usize> {
        Ok(BaseOptionType::iter().count())
    }
    
    // TODO figure out how to make a class iterator,
    // is way too complicated in pyo3 rn
    #[staticmethod]
    fn members() -> Vec<OptionType> {
        BaseOptionType::iter().map(|item: BaseOptionType| OptionType{typ: item} ).collect()
    }

    #[classattr]
    #[allow(non_snake_case)]
    fn Call() -> OptionType {
        OptionType {
            typ: BaseOptionType::Call
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn Put() -> OptionType {
        OptionType {
            typ: BaseOptionType::Put
        }
    }
}

#[pyclass]
pub struct OptionExerciseType {
    pub typ: BaseOptionExerciseType
}

#[pymethods]
impl OptionExerciseType {
    #[new]
    fn py_new(value: String) -> PyResult<Self> {
        Ok(
            OptionExerciseType {
                typ: BaseOptionExerciseType::from_str(value.as_str()).unwrap()
            }
        )
    }
    
    fn __str__(&self) -> PyResult<String>   {
        Ok(format!("{}", self.typ.to_string()))
    }
    
    fn __repr__(&self) -> PyResult<String>   {
        Ok(format!("OptionExerciseType<{}>", self.typ.to_string()))
    }
    
    fn __eq__(&self, other: &Self) -> bool   {
        self.typ == other.typ
    }
    
    #[classmethod]
    fn __len__(_cls: &PyType) -> PyResult<usize> {
        Ok(BaseOptionExerciseType::iter().count())
    }
    
    // TODO figure out how to make a class iterator,
    // is way too complicated in pyo3 rn
    #[staticmethod]
    fn members() -> Vec<OptionExerciseType> {
        BaseOptionExerciseType::iter().map(|item: BaseOptionExerciseType| OptionExerciseType{typ: item} ).collect()
    }

    #[classattr]
    #[allow(non_snake_case)]
    fn American() -> OptionExerciseType {
        OptionExerciseType {
            typ: BaseOptionExerciseType::American
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn European() -> OptionExerciseType {
        OptionExerciseType {
            typ: BaseOptionExerciseType::European
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn Bermudan() -> OptionExerciseType {
        OptionExerciseType {
            typ: BaseOptionExerciseType::Bermudan
        }
    }
}
