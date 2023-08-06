use pyo3::prelude::*;
use pyo3::types::PyType;
use strum::IntoEnumIterator;
use std::str::FromStr;

use finance_enums::MIC;
use super::Country;

#[pyclass]
pub struct Exchange{
    pub mic: MIC,
}

#[pymethods]
impl Exchange {
    #[new]
    fn py_new(value: String) -> PyResult<Self> {
        Ok(
            Exchange {
                mic: MIC::from_str(value.as_str()).unwrap()
            }
        )

    }

    fn __str__(&self) -> PyResult<String>   {
        Ok(format!("{}", self.mic.to_string()))
    }

    fn __repr__(&self) -> PyResult<String>   {
        Ok(format!("Exchange<{}>", self.mic.to_string()))
    }

    fn __eq__(&self, other: &Self) -> bool   {
        self.mic == other.mic
    }

    fn country(&self) -> Country {
        Country {
            code: self.mic.country(),
            code3: self.mic.country().codethree(),
            name: self.mic.country().str(),
        }
    }

    #[classmethod]
    fn __len__(_cls: &PyType) -> PyResult<usize> {
        Ok(MIC::iter().count())
    }

    // TODO figure out how to make a class iterator,
    // is way too complicated in pyo3 rn
    #[staticmethod]
    fn members() -> Vec<Exchange> {
        MIC::iter().map(|item: MIC| Exchange{mic: item} ).collect()
    }

    #[classattr]
    #[allow(non_snake_case)]
    fn XNYS() -> Exchange {
        Exchange {
            mic: MIC::XNYS
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn ARCX() -> Exchange {
        Exchange {
            mic: MIC::ARCX
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn XASE() -> Exchange {
        Exchange {
            mic: MIC::XASE
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn XCIS() -> Exchange {
        Exchange {
            mic: MIC::XCIS
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn XCHI() -> Exchange {
        Exchange {
            mic: MIC::XCHI
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn XNAS() -> Exchange {
        Exchange {
            mic: MIC::XNAS
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn XNGS() -> Exchange {
        Exchange {
            mic: MIC::XNGS
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn XBOS() -> Exchange {
        Exchange {
            mic: MIC::XBOS
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn XPHL() -> Exchange {
        Exchange {
            mic: MIC::XPHL
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn XCBO() -> Exchange {
        Exchange {
            mic: MIC::XCBO
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn BATS() -> Exchange {
        Exchange {
            mic: MIC::BATS
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn BATY() -> Exchange {
        Exchange {
            mic: MIC::BATY
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn EDGX() -> Exchange {
        Exchange {
            mic: MIC::EDGX
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn EDGA() -> Exchange {
        Exchange {
            mic: MIC::EDGA
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn MPRL() -> Exchange {
        Exchange {
            mic: MIC::MPRL
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn MIHI() -> Exchange {
        Exchange {
            mic: MIC::MIHI
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn MEMX() -> Exchange {
        Exchange {
            mic: MIC::MEMX
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn IEXG() -> Exchange {
        Exchange {
            mic: MIC::IEXG
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn LTSE() -> Exchange {
        Exchange {
            mic: MIC::LTSE
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn XADF() -> Exchange {
        Exchange {
            mic: MIC::XADF
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn FINR() -> Exchange {
        Exchange {
            mic: MIC::FINR
        }
    }
}
