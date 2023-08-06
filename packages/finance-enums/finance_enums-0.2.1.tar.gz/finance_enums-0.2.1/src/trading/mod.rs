use pyo3::prelude::*;
use pyo3::types::PyType;
use strum::IntoEnumIterator;
use std::str::FromStr;

use finance_enums::{OrderType as BaseOrderType, Side as BaseSide, TimeInForce as BaseTimeInForce, OrderFlag as BaseOrderFlag};

// pub enum TimeInForce {
//     Day,
//     GTC,
// }

// pub enum OrderFlag {
//     None,
//     FillOrKill,
//     ImmediateOrCancel,
//     AllOrNone,
// }



#[pyclass]
pub struct OrderType {
    pub typ: BaseOrderType
}

#[pymethods]
impl OrderType {
    #[new]
    fn py_new(value: String) -> PyResult<Self> {
        Ok(
            OrderType {
                typ: BaseOrderType::from_str(value.as_str()).unwrap()
            }
        )
    }
    
    fn __str__(&self) -> PyResult<String>   {
        Ok(format!("{}", self.typ.to_string()))
    }
    
    fn __repr__(&self) -> PyResult<String>   {
        Ok(format!("OrderType<{}>", self.typ.to_string()))
    }
    
    fn __eq__(&self, other: &Self) -> bool   {
        self.typ == other.typ
    }
    
    #[classmethod]
    fn __len__(_cls: &PyType) -> PyResult<usize> {
        Ok(BaseOrderType::iter().count())
    }
    
    // TODO figure out how to make a class iterator,
    // is way too complicated in pyo3 rn
    #[staticmethod]
    fn members() -> Vec<OrderType> {
        BaseOrderType::iter().map(|item: BaseOrderType| OrderType{typ: item} ).collect()
    }

    #[classattr]
    #[allow(non_snake_case)]
    fn Market() -> OrderType {
        OrderType {
            typ: BaseOrderType::Market
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn Limit() -> OrderType {
        OrderType {
            typ: BaseOrderType::Limit
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn Stop() -> OrderType {
        OrderType {
            typ: BaseOrderType::Stop
        }
    }
}


#[pyclass]
pub struct Side {
    pub typ: BaseSide
}

#[pymethods]
impl Side {
    #[new]
    fn py_new(value: String) -> PyResult<Self> {
        Ok(
            Side {
                typ: BaseSide::from_str(value.as_str()).unwrap()
            }
        )
    }
    
    fn __str__(&self) -> PyResult<String>   {
        Ok(format!("{}", self.typ.to_string()))
    }
    
    fn __repr__(&self) -> PyResult<String>   {
        Ok(format!("Side<{}>", self.typ.to_string()))
    }
    
    fn __eq__(&self, other: &Self) -> bool   {
        self.typ == other.typ
    }
    
    #[classmethod]
    fn __len__(_cls: &PyType) -> PyResult<usize> {
        Ok(BaseSide::iter().count())
    }
    
    // TODO figure out how to make a class iterator,
    // is way too complicated in pyo3 rn
    #[staticmethod]
    fn members() -> Vec<Side> {
        BaseSide::iter().map(|item: BaseSide| Side{typ: item} ).collect()
    }

    #[classattr]
    #[allow(non_snake_case)]
    fn Buy() -> Side {
        Side {
            typ: BaseSide::Buy
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn Sell() -> Side {
        Side {
            typ: BaseSide::Sell
        }
    }
}


#[pyclass]
pub struct TimeInForce {
    pub typ: BaseTimeInForce
}

#[pymethods]
impl TimeInForce {
    #[new]
    fn py_new(value: String) -> PyResult<Self> {
        Ok(
            TimeInForce {
                typ: BaseTimeInForce::from_str(value.as_str()).unwrap()
            }
        )
    }
    
    fn __str__(&self) -> PyResult<String>   {
        Ok(format!("{}", self.typ.to_string()))
    }
    
    fn __repr__(&self) -> PyResult<String>   {
        Ok(format!("TimeInForce<{}>", self.typ.to_string()))
    }
    
    fn __eq__(&self, other: &Self) -> bool   {
        self.typ == other.typ
    }
    
    #[classmethod]
    fn __len__(_cls: &PyType) -> PyResult<usize> {
        Ok(BaseTimeInForce::iter().count())
    }
    
    // TODO figure out how to make a class iterator,
    // is way too complicated in pyo3 rn
    #[staticmethod]
    fn members() -> Vec<TimeInForce> {
        BaseTimeInForce::iter().map(|item: BaseTimeInForce| TimeInForce{typ: item} ).collect()
    }

    #[classattr]
    #[allow(non_snake_case)]
    fn Day() -> TimeInForce {
        TimeInForce {
            typ: BaseTimeInForce::Day
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn GTC() -> TimeInForce {
        TimeInForce {
            typ: BaseTimeInForce::GTC
        }
    }
}



#[pyclass]
pub struct OrderFlag {
    pub typ: BaseOrderFlag
}

#[pymethods]
impl OrderFlag {
    #[new]
    fn py_new(value: String) -> PyResult<Self> {
        Ok(
            OrderFlag {
                typ: BaseOrderFlag::from_str(value.as_str()).unwrap()
            }
        )
    }
    
    fn __str__(&self) -> PyResult<String>   {
        Ok(format!("{}", self.typ.to_string()))
    }
    
    fn __repr__(&self) -> PyResult<String>   {
        Ok(format!("OrderFlag<{}>", self.typ.to_string()))
    }
    
    fn __eq__(&self, other: &Self) -> bool   {
        self.typ == other.typ
    }
    
    #[classmethod]
    fn __len__(_cls: &PyType) -> PyResult<usize> {
        Ok(BaseOrderFlag::iter().count())
    }
    
    // TODO figure out how to make a class iterator,
    // is way too complicated in pyo3 rn
    #[staticmethod]
    fn members() -> Vec<OrderFlag> {
        BaseOrderFlag::iter().map(|item: BaseOrderFlag| OrderFlag{typ: item} ).collect()
    }


    #[classattr]
    #[allow(non_snake_case)]
    fn None() -> OrderFlag {
        OrderFlag {
            typ: BaseOrderFlag::None
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn FillOrKill() -> OrderFlag {
        OrderFlag {
            typ: BaseOrderFlag::FillOrKill
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn ImmediateOrCancel() -> OrderFlag {
        OrderFlag {
            typ: BaseOrderFlag::ImmediateOrCancel
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn AllOrNone() -> OrderFlag {
        OrderFlag {
            typ: BaseOrderFlag::AllOrNone
        }
    }
}
