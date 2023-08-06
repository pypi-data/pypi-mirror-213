use pyo3::prelude::*;
use pyo3::types::PyType;
use strum::IntoEnumIterator;
use std::str::FromStr;

use finance_enums::{Currency as BaseCurrency};

#[pyclass]
pub struct Currency {
    pub code: BaseCurrency,
}

#[pymethods]
impl Currency {
    #[new]
    fn py_new(value: String) -> PyResult<Self> {
        Ok(
            Currency {
                code: BaseCurrency::from_str(value.as_str()).unwrap()
            }
        )

    }

    fn __str__(&self) -> PyResult<String>   {
        Ok(format!("{}", self.code.to_string()))
    }

    fn __repr__(&self) -> PyResult<String>   {
        Ok(format!("Currency<{}>", self.code.to_string()))
    }

    fn __eq__(&self, other: &Self) -> bool   {
        self.code == other.code
    }

    #[getter]
    fn code(&self) -> PyResult<String> {
        Ok(self.code.to_string())
    }
    
    #[getter]
    fn name(&self) -> &'static str {
        self.code.name()
    }
    
    #[classmethod]
    fn __len__(_cls: &PyType) -> PyResult<usize> {
        Ok(BaseCurrency::iter().count())
    }

    // TODO figure out how to make a class iterator,
    // is way too complicated in pyo3 rn
    #[staticmethod]
    fn members() -> Vec<Currency> {
        BaseCurrency::iter().map(|item: BaseCurrency| Currency{code: item} ).collect()
    }

    #[classattr]
    #[allow(non_snake_case)]
    fn AED() -> Currency {
        Currency {
            code: BaseCurrency::AED
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn AFN() -> Currency {
        Currency {
            code: BaseCurrency::AFN
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn ALL() -> Currency {
        Currency {
            code: BaseCurrency::ALL
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn AMD() -> Currency {
        Currency {
            code: BaseCurrency::AMD
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn ANG() -> Currency {
        Currency {
            code: BaseCurrency::ANG
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn AOA() -> Currency {
        Currency {
            code: BaseCurrency::AOA
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn ARS() -> Currency {
        Currency {
            code: BaseCurrency::ARS
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn AUD() -> Currency {
        Currency {
            code: BaseCurrency::AUD
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn AWG() -> Currency {
        Currency {
            code: BaseCurrency::AWG
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn AZN() -> Currency {
        Currency {
            code: BaseCurrency::AZN
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn BAM() -> Currency {
        Currency {
            code: BaseCurrency::BAM
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn BBD() -> Currency {
        Currency {
            code: BaseCurrency::BBD
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn BDT() -> Currency {
        Currency {
            code: BaseCurrency::BDT
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn BGN() -> Currency {
        Currency {
            code: BaseCurrency::BGN
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn BHD() -> Currency {
        Currency {
            code: BaseCurrency::BHD
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn BIF() -> Currency {
        Currency {
            code: BaseCurrency::BIF
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn BMD() -> Currency {
        Currency {
            code: BaseCurrency::BMD
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn BND() -> Currency {
        Currency {
            code: BaseCurrency::BND
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn BOB() -> Currency {
        Currency {
            code: BaseCurrency::BOB
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn BOV() -> Currency {
        Currency {
            code: BaseCurrency::BOV
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn BRL() -> Currency {
        Currency {
            code: BaseCurrency::BRL
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn BSD() -> Currency {
        Currency {
            code: BaseCurrency::BSD
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn BTN() -> Currency {
        Currency {
            code: BaseCurrency::BTN
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn BWP() -> Currency {
        Currency {
            code: BaseCurrency::BWP
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn BYN() -> Currency {
        Currency {
            code: BaseCurrency::BYN
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn BZD() -> Currency {
        Currency {
            code: BaseCurrency::BZD
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn CAD() -> Currency {
        Currency {
            code: BaseCurrency::CAD
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn CDF() -> Currency {
        Currency {
            code: BaseCurrency::CDF
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn CHE() -> Currency {
        Currency {
            code: BaseCurrency::CHE
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn CHF() -> Currency {
        Currency {
            code: BaseCurrency::CHF
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn CHW() -> Currency {
        Currency {
            code: BaseCurrency::CHW
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn CLF() -> Currency {
        Currency {
            code: BaseCurrency::CLF
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn CLP() -> Currency {
        Currency {
            code: BaseCurrency::CLP
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn COP() -> Currency {
        Currency {
            code: BaseCurrency::COP
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn COU() -> Currency {
        Currency {
            code: BaseCurrency::COU
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn CRC() -> Currency {
        Currency {
            code: BaseCurrency::CRC
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn CUC() -> Currency {
        Currency {
            code: BaseCurrency::CUC
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn CUP() -> Currency {
        Currency {
            code: BaseCurrency::CUP
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn CVE() -> Currency {
        Currency {
            code: BaseCurrency::CVE
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn CZK() -> Currency {
        Currency {
            code: BaseCurrency::CZK
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn DJF() -> Currency {
        Currency {
            code: BaseCurrency::DJF
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn DKK() -> Currency {
        Currency {
            code: BaseCurrency::DKK
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn DOP() -> Currency {
        Currency {
            code: BaseCurrency::DOP
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn DZD() -> Currency {
        Currency {
            code: BaseCurrency::DZD
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn EGP() -> Currency {
        Currency {
            code: BaseCurrency::EGP
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn ERN() -> Currency {
        Currency {
            code: BaseCurrency::ERN
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn ETB() -> Currency {
        Currency {
            code: BaseCurrency::ETB
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn EUR() -> Currency {
        Currency {
            code: BaseCurrency::EUR
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn FJD() -> Currency {
        Currency {
            code: BaseCurrency::FJD
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn FKP() -> Currency {
        Currency {
            code: BaseCurrency::FKP
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn GBP() -> Currency {
        Currency {
            code: BaseCurrency::GBP
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn GEL() -> Currency {
        Currency {
            code: BaseCurrency::GEL
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn GHS() -> Currency {
        Currency {
            code: BaseCurrency::GHS
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn GIP() -> Currency {
        Currency {
            code: BaseCurrency::GIP
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn GMD() -> Currency {
        Currency {
            code: BaseCurrency::GMD
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn GNF() -> Currency {
        Currency {
            code: BaseCurrency::GNF
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn GTQ() -> Currency {
        Currency {
            code: BaseCurrency::GTQ
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn GYD() -> Currency {
        Currency {
            code: BaseCurrency::GYD
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn HKD() -> Currency {
        Currency {
            code: BaseCurrency::HKD
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn HNL() -> Currency {
        Currency {
            code: BaseCurrency::HNL
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn HTG() -> Currency {
        Currency {
            code: BaseCurrency::HTG
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn HUF() -> Currency {
        Currency {
            code: BaseCurrency::HUF
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn IDR() -> Currency {
        Currency {
            code: BaseCurrency::IDR
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn ILS() -> Currency {
        Currency {
            code: BaseCurrency::ILS
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn INR() -> Currency {
        Currency {
            code: BaseCurrency::INR
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn IQD() -> Currency {
        Currency {
            code: BaseCurrency::IQD
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn IRR() -> Currency {
        Currency {
            code: BaseCurrency::IRR
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn ISK() -> Currency {
        Currency {
            code: BaseCurrency::ISK
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn JMD() -> Currency {
        Currency {
            code: BaseCurrency::JMD
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn JOD() -> Currency {
        Currency {
            code: BaseCurrency::JOD
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn JPY() -> Currency {
        Currency {
            code: BaseCurrency::JPY
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn KES() -> Currency {
        Currency {
            code: BaseCurrency::KES
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn KGS() -> Currency {
        Currency {
            code: BaseCurrency::KGS
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn KHR() -> Currency {
        Currency {
            code: BaseCurrency::KHR
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn KMF() -> Currency {
        Currency {
            code: BaseCurrency::KMF
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn KPW() -> Currency {
        Currency {
            code: BaseCurrency::KPW
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn KRW() -> Currency {
        Currency {
            code: BaseCurrency::KRW
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn KWD() -> Currency {
        Currency {
            code: BaseCurrency::KWD
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn KYD() -> Currency {
        Currency {
            code: BaseCurrency::KYD
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn KZT() -> Currency {
        Currency {
            code: BaseCurrency::KZT
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn LAK() -> Currency {
        Currency {
            code: BaseCurrency::LAK
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn LBP() -> Currency {
        Currency {
            code: BaseCurrency::LBP
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn LKR() -> Currency {
        Currency {
            code: BaseCurrency::LKR
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn LRD() -> Currency {
        Currency {
            code: BaseCurrency::LRD
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn LSL() -> Currency {
        Currency {
            code: BaseCurrency::LSL
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn LYD() -> Currency {
        Currency {
            code: BaseCurrency::LYD
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn MAD() -> Currency {
        Currency {
            code: BaseCurrency::MAD
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn MDL() -> Currency {
        Currency {
            code: BaseCurrency::MDL
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn MGA() -> Currency {
        Currency {
            code: BaseCurrency::MGA
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn MKD() -> Currency {
        Currency {
            code: BaseCurrency::MKD
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn MMK() -> Currency {
        Currency {
            code: BaseCurrency::MMK
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn MNT() -> Currency {
        Currency {
            code: BaseCurrency::MNT
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn MOP() -> Currency {
        Currency {
            code: BaseCurrency::MOP
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn MRU() -> Currency {
        Currency {
            code: BaseCurrency::MRU
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn MUR() -> Currency {
        Currency {
            code: BaseCurrency::MUR
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn MVR() -> Currency {
        Currency {
            code: BaseCurrency::MVR
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn MWK() -> Currency {
        Currency {
            code: BaseCurrency::MWK
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn MXN() -> Currency {
        Currency {
            code: BaseCurrency::MXN
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn MXV() -> Currency {
        Currency {
            code: BaseCurrency::MXV
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn MYR() -> Currency {
        Currency {
            code: BaseCurrency::MYR
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn MZN() -> Currency {
        Currency {
            code: BaseCurrency::MZN
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn NAD() -> Currency {
        Currency {
            code: BaseCurrency::NAD
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn NGN() -> Currency {
        Currency {
            code: BaseCurrency::NGN
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn NIO() -> Currency {
        Currency {
            code: BaseCurrency::NIO
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn NOK() -> Currency {
        Currency {
            code: BaseCurrency::NOK
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn NPR() -> Currency {
        Currency {
            code: BaseCurrency::NPR
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn NZD() -> Currency {
        Currency {
            code: BaseCurrency::NZD
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn OMR() -> Currency {
        Currency {
            code: BaseCurrency::OMR
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn PAB() -> Currency {
        Currency {
            code: BaseCurrency::PAB
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn PEN() -> Currency {
        Currency {
            code: BaseCurrency::PEN
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn PGK() -> Currency {
        Currency {
            code: BaseCurrency::PGK
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn PHP() -> Currency {
        Currency {
            code: BaseCurrency::PHP
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn PKR() -> Currency {
        Currency {
            code: BaseCurrency::PKR
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn PLN() -> Currency {
        Currency {
            code: BaseCurrency::PLN
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn PYG() -> Currency {
        Currency {
            code: BaseCurrency::PYG
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn QAR() -> Currency {
        Currency {
            code: BaseCurrency::QAR
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn RON() -> Currency {
        Currency {
            code: BaseCurrency::RON
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn RSD() -> Currency {
        Currency {
            code: BaseCurrency::RSD
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn CNY() -> Currency {
        Currency {
            code: BaseCurrency::CNY
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn RUB() -> Currency {
        Currency {
            code: BaseCurrency::RUB
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn RWF() -> Currency {
        Currency {
            code: BaseCurrency::RWF
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn SAR() -> Currency {
        Currency {
            code: BaseCurrency::SAR
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn SBD() -> Currency {
        Currency {
            code: BaseCurrency::SBD
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn SCR() -> Currency {
        Currency {
            code: BaseCurrency::SCR
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn SDG() -> Currency {
        Currency {
            code: BaseCurrency::SDG
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn SEK() -> Currency {
        Currency {
            code: BaseCurrency::SEK
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn SGD() -> Currency {
        Currency {
            code: BaseCurrency::SGD
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn SHP() -> Currency {
        Currency {
            code: BaseCurrency::SHP
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn SLE() -> Currency {
        Currency {
            code: BaseCurrency::SLE
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn SLL() -> Currency {
        Currency {
            code: BaseCurrency::SLL
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn SOS() -> Currency {
        Currency {
            code: BaseCurrency::SOS
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn SRD() -> Currency {
        Currency {
            code: BaseCurrency::SRD
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn SSP() -> Currency {
        Currency {
            code: BaseCurrency::SSP
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn STN() -> Currency {
        Currency {
            code: BaseCurrency::STN
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn SVC() -> Currency {
        Currency {
            code: BaseCurrency::SVC
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn SYP() -> Currency {
        Currency {
            code: BaseCurrency::SYP
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn SZL() -> Currency {
        Currency {
            code: BaseCurrency::SZL
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn THB() -> Currency {
        Currency {
            code: BaseCurrency::THB
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn TJS() -> Currency {
        Currency {
            code: BaseCurrency::TJS
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn TMT() -> Currency {
        Currency {
            code: BaseCurrency::TMT
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn TND() -> Currency {
        Currency {
            code: BaseCurrency::TND
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn TOP() -> Currency {
        Currency {
            code: BaseCurrency::TOP
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn TRY() -> Currency {
        Currency {
            code: BaseCurrency::TRY
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn TTD() -> Currency {
        Currency {
            code: BaseCurrency::TTD
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn TWD() -> Currency {
        Currency {
            code: BaseCurrency::TWD
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn TZS() -> Currency {
        Currency {
            code: BaseCurrency::TZS
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn UAH() -> Currency {
        Currency {
            code: BaseCurrency::UAH
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn UGX() -> Currency {
        Currency {
            code: BaseCurrency::UGX
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn USD() -> Currency {
        Currency {
            code: BaseCurrency::USD
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn USN() -> Currency {
        Currency {
            code: BaseCurrency::USN
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn UYI() -> Currency {
        Currency {
            code: BaseCurrency::UYI
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn UYU() -> Currency {
        Currency {
            code: BaseCurrency::UYU
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn UYW() -> Currency {
        Currency {
            code: BaseCurrency::UYW
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn UZS() -> Currency {
        Currency {
            code: BaseCurrency::UZS
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn VED() -> Currency {
        Currency {
            code: BaseCurrency::VED
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn VES() -> Currency {
        Currency {
            code: BaseCurrency::VES
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn VND() -> Currency {
        Currency {
            code: BaseCurrency::VND
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn VUV() -> Currency {
        Currency {
            code: BaseCurrency::VUV
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn WST() -> Currency {
        Currency {
            code: BaseCurrency::WST
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn XAF() -> Currency {
        Currency {
            code: BaseCurrency::XAF
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn XAG() -> Currency {
        Currency {
            code: BaseCurrency::XAG
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn XAU() -> Currency {
        Currency {
            code: BaseCurrency::XAU
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn XBA() -> Currency {
        Currency {
            code: BaseCurrency::XBA
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn XBB() -> Currency {
        Currency {
            code: BaseCurrency::XBB
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn XBC() -> Currency {
        Currency {
            code: BaseCurrency::XBC
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn XBD() -> Currency {
        Currency {
            code: BaseCurrency::XBD
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn XCD() -> Currency {
        Currency {
            code: BaseCurrency::XCD
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn XDR() -> Currency {
        Currency {
            code: BaseCurrency::XDR
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn XOF() -> Currency {
        Currency {
            code: BaseCurrency::XOF
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn XPD() -> Currency {
        Currency {
            code: BaseCurrency::XPD
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn XPF() -> Currency {
        Currency {
            code: BaseCurrency::XPF
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn XPT() -> Currency {
        Currency {
            code: BaseCurrency::XPT
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn XSU() -> Currency {
        Currency {
            code: BaseCurrency::XSU
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn XTS() -> Currency {
        Currency {
            code: BaseCurrency::XTS
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn XUA() -> Currency {
        Currency {
            code: BaseCurrency::XUA
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn XXX() -> Currency {
        Currency {
            code: BaseCurrency::XXX
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn YER() -> Currency {
        Currency {
            code: BaseCurrency::YER
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn ZAR() -> Currency {
        Currency {
            code: BaseCurrency::ZAR
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn ZMW() -> Currency {
        Currency {
            code: BaseCurrency::ZMW
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn ZWL() -> Currency {
        Currency {
            code: BaseCurrency::ZWL
        }
    }
}
