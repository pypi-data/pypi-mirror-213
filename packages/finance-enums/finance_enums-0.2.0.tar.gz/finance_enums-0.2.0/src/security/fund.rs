use pyo3::prelude::*;
use pyo3::types::PyType;
use strum::IntoEnumIterator;
use std::str::FromStr;

use finance_enums::{FundType as BaseFundType, FundSubType as BaseFundSubType, MutualFundEndedness as BaseMutualFundEndedness};


#[pyclass]
pub struct FundType {
    pub typ: BaseFundType
}

#[pymethods]
impl FundType {
    #[new]
    fn py_new(value: String) -> PyResult<Self> {
        Ok(
            FundType {
                typ: BaseFundType::from_str(value.as_str()).unwrap()
            }
        )
    }
    
    fn __str__(&self) -> PyResult<String>   {
        Ok(format!("{}", self.typ.to_string()))
    }
    
    fn __repr__(&self) -> PyResult<String>   {
        Ok(format!("FundType<{}>", self.typ.to_string()))
    }
    
    fn __eq__(&self, other: &Self) -> bool   {
        self.typ == other.typ
    }
    
    #[classmethod]
    fn __len__(_cls: &PyType) -> PyResult<usize> {
        Ok(BaseFundType::iter().count())
    }
    
    // TODO figure out how to make a class iterator,
    // is way too complicated in pyo3 rn
    #[staticmethod]
    fn members() -> Vec<FundType> {
        BaseFundType::iter().map(|item: BaseFundType| FundType{typ: item} ).collect()
    }

    #[classattr]
    #[allow(non_snake_case)]
    fn ETF() -> FundType {
        FundType {
            typ: BaseFundType::ETF
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn MutualFund() -> FundType {
        FundType {
            typ: BaseFundType::MutualFund
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn REIT() -> FundType {
        FundType {
            typ: BaseFundType::REIT
        }
    }

}
#[pyclass]
pub struct FundSubType {
    pub typ: BaseFundSubType
}

#[pymethods]
impl FundSubType {
    #[new]
    fn py_new(value: String) -> PyResult<Self> {
        Ok(
            FundSubType {
                typ: BaseFundSubType::from_str(value.as_str()).unwrap()
            }
        )
    }
    
    fn __str__(&self) -> PyResult<String>   {
        Ok(format!("{}", self.typ.to_string()))
    }
    
    fn __repr__(&self) -> PyResult<String>   {
        Ok(format!("FundSubType<{}>", self.typ.to_string()))
    }
    
    fn __eq__(&self, other: &Self) -> bool   {
        self.typ == other.typ
    }
    
    #[classmethod]
    fn __len__(_cls: &PyType) -> PyResult<usize> {
        Ok(BaseFundSubType::iter().count())
    }
    
    // TODO figure out how to make a class iterator,
    // is way too complicated in pyo3 rn
    #[staticmethod]
    fn members() -> Vec<FundSubType> {
        BaseFundSubType::iter().map(|item: BaseFundSubType| FundSubType{typ: item} ).collect()
    }

    #[classattr]
    #[allow(non_snake_case)]
    fn Index() -> FundSubType {
        FundSubType {
            typ: BaseFundSubType::Index
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn Sector() -> FundSubType {
        FundSubType {
            typ: BaseFundSubType::Sector
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn Active() -> FundSubType {
        FundSubType {
            typ: BaseFundSubType::Active
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn Passive() -> FundSubType {
        FundSubType {
            typ: BaseFundSubType::Passive
        }
    }
}

#[pyclass]
pub struct MutualFundEndedness {
    pub typ: BaseMutualFundEndedness
}

#[pymethods]
impl MutualFundEndedness {
    #[new]
    fn py_new(value: String) -> PyResult<Self> {
        Ok(
            MutualFundEndedness {
                typ: BaseMutualFundEndedness::from_str(value.as_str()).unwrap()
            }
        )
    }
    
    fn __str__(&self) -> PyResult<String>   {
        Ok(format!("{}", self.typ.to_string()))
    }
    
    fn __repr__(&self) -> PyResult<String>   {
        Ok(format!("MutualFundEndedness<{}>", self.typ.to_string()))
    }
    
    fn __eq__(&self, other: &Self) -> bool   {
        self.typ == other.typ
    }
    
    #[classmethod]
    fn __len__(_cls: &PyType) -> PyResult<usize> {
        Ok(BaseMutualFundEndedness::iter().count())
    }
    
    // TODO figure out how to make a class iterator,
    // is way too complicated in pyo3 rn
    #[staticmethod]
    fn members() -> Vec<MutualFundEndedness> {
        BaseMutualFundEndedness::iter().map(|item: BaseMutualFundEndedness| MutualFundEndedness{typ: item} ).collect()
    }

    #[classattr]
    #[allow(non_snake_case)]
    fn Open() -> MutualFundEndedness {
        MutualFundEndedness {
            typ: BaseMutualFundEndedness::Open
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn Close() -> MutualFundEndedness {
        MutualFundEndedness {
            typ: BaseMutualFundEndedness::Close
        }
    }
}