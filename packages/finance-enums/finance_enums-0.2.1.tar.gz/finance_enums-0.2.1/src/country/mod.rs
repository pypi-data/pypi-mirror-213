use pyo3::prelude::*;
use pyo3::types::PyType;
use strum::IntoEnumIterator;
use std::str::FromStr;

use finance_enums::{CountryCode, CountryCode3};

#[pyclass]
pub struct Country {
    pub code: CountryCode,
    pub code3: CountryCode3,
    pub name: &'static str,
}

#[pymethods]
impl Country {
    #[new]
    fn py_new(value: String) -> PyResult<Self> {
        let code: CountryCode = CountryCode::from_str(value.as_str()).unwrap();

        Ok(
            Country {
                code,
                code3: code.codethree(),
                name: code.str(),
            }
        )

    }

    fn __str__(&self) -> PyResult<String>   {
        Ok(format!("{}", self.name))
    }

    fn __repr__(&self) -> PyResult<String>   {
        Ok(format!("Country<{}>", self.code.to_string()))
    }

    fn __eq__(&self, other: &Self) -> bool   {
        self.code == other.code
    }

    #[getter]
    fn code(&self) -> PyResult<String> {
        Ok(self.code.to_string())
    }
    
    #[getter]
    fn code3(&self) -> PyResult<String> {
        Ok(self.code3.to_string())
    }
    
    #[getter]
    fn name(&self) -> &'static str {
        self.name
    }
    
    #[getter]
    fn flag(&self) -> PyResult<String> {
        Ok(self.code.flag().to_string())
    }

    #[classmethod]
    fn __len__(_cls: &PyType) -> PyResult<usize> {
        Ok(CountryCode::iter().count())
    }

    // TODO figure out how to make a class iterator,
    // is way too complicated in pyo3 rn
    #[staticmethod]
    fn members() -> Vec<Country> {
        CountryCode::iter().map(|item: CountryCode| Country{code: item, code3: item.codethree(), name: item.str()} ).collect()
    }

    #[classattr]
    #[allow(non_snake_case)]
    fn AF() -> Country {
        Country {
            code: CountryCode::AF,
            code3: CountryCode::AF.codethree(),
            name: CountryCode::AF.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn AX() -> Country {
        Country {
            code: CountryCode::AX,
            code3: CountryCode::AX.codethree(),
            name: CountryCode::AX.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn AL() -> Country {
        Country {
            code: CountryCode::AL,
            code3: CountryCode::AL.codethree(),
            name: CountryCode::AL.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn DZ() -> Country {
        Country {
            code: CountryCode::DZ,
            code3: CountryCode::DZ.codethree(),
            name: CountryCode::DZ.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn AS() -> Country {
        Country {
            code: CountryCode::AS,
            code3: CountryCode::AS.codethree(),
            name: CountryCode::AS.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn AD() -> Country {
        Country {
            code: CountryCode::AD,
            code3: CountryCode::AD.codethree(),
            name: CountryCode::AD.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn AO() -> Country {
        Country {
            code: CountryCode::AO,
            code3: CountryCode::AO.codethree(),
            name: CountryCode::AO.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn AI() -> Country {
        Country {
            code: CountryCode::AI,
            code3: CountryCode::AI.codethree(),
            name: CountryCode::AI.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn AQ() -> Country {
        Country {
            code: CountryCode::AQ,
            code3: CountryCode::AQ.codethree(),
            name: CountryCode::AQ.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn AG() -> Country {
        Country {
            code: CountryCode::AG,
            code3: CountryCode::AG.codethree(),
            name: CountryCode::AG.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn AR() -> Country {
        Country {
            code: CountryCode::AR,
            code3: CountryCode::AR.codethree(),
            name: CountryCode::AR.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn AM() -> Country {
        Country {
            code: CountryCode::AM,
            code3: CountryCode::AM.codethree(),
            name: CountryCode::AM.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn AW() -> Country {
        Country {
            code: CountryCode::AW,
            code3: CountryCode::AW.codethree(),
            name: CountryCode::AW.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn AU() -> Country {
        Country {
            code: CountryCode::AU,
            code3: CountryCode::AU.codethree(),
            name: CountryCode::AU.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn AT() -> Country {
        Country {
            code: CountryCode::AT,
            code3: CountryCode::AT.codethree(),
            name: CountryCode::AT.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn AZ() -> Country {
        Country {
            code: CountryCode::AZ,
            code3: CountryCode::AZ.codethree(),
            name: CountryCode::AZ.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn BS() -> Country {
        Country {
            code: CountryCode::BS,
            code3: CountryCode::BS.codethree(),
            name: CountryCode::BS.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn BH() -> Country {
        Country {
            code: CountryCode::BH,
            code3: CountryCode::BH.codethree(),
            name: CountryCode::BH.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn BD() -> Country {
        Country {
            code: CountryCode::BD,
            code3: CountryCode::BD.codethree(),
            name: CountryCode::BD.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn BB() -> Country {
        Country {
            code: CountryCode::BB,
            code3: CountryCode::BB.codethree(),
            name: CountryCode::BB.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn BY() -> Country {
        Country {
            code: CountryCode::BY,
            code3: CountryCode::BY.codethree(),
            name: CountryCode::BY.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn BE() -> Country {
        Country {
            code: CountryCode::BE,
            code3: CountryCode::BE.codethree(),
            name: CountryCode::BE.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn BZ() -> Country {
        Country {
            code: CountryCode::BZ,
            code3: CountryCode::BZ.codethree(),
            name: CountryCode::BZ.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn BJ() -> Country {
        Country {
            code: CountryCode::BJ,
            code3: CountryCode::BJ.codethree(),
            name: CountryCode::BJ.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn BM() -> Country {
        Country {
            code: CountryCode::BM,
            code3: CountryCode::BM.codethree(),
            name: CountryCode::BM.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn BT() -> Country {
        Country {
            code: CountryCode::BT,
            code3: CountryCode::BT.codethree(),
            name: CountryCode::BT.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn BO() -> Country {
        Country {
            code: CountryCode::BO,
            code3: CountryCode::BO.codethree(),
            name: CountryCode::BO.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn BQ() -> Country {
        Country {
            code: CountryCode::BQ,
            code3: CountryCode::BQ.codethree(),
            name: CountryCode::BQ.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn BA() -> Country {
        Country {
            code: CountryCode::BA,
            code3: CountryCode::BA.codethree(),
            name: CountryCode::BA.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn BW() -> Country {
        Country {
            code: CountryCode::BW,
            code3: CountryCode::BW.codethree(),
            name: CountryCode::BW.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn BV() -> Country {
        Country {
            code: CountryCode::BV,
            code3: CountryCode::BV.codethree(),
            name: CountryCode::BV.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn BR() -> Country {
        Country {
            code: CountryCode::BR,
            code3: CountryCode::BR.codethree(),
            name: CountryCode::BR.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn IO() -> Country {
        Country {
            code: CountryCode::IO,
            code3: CountryCode::IO.codethree(),
            name: CountryCode::IO.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn BN() -> Country {
        Country {
            code: CountryCode::BN,
            code3: CountryCode::BN.codethree(),
            name: CountryCode::BN.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn BG() -> Country {
        Country {
            code: CountryCode::BG,
            code3: CountryCode::BG.codethree(),
            name: CountryCode::BG.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn BF() -> Country {
        Country {
            code: CountryCode::BF,
            code3: CountryCode::BF.codethree(),
            name: CountryCode::BF.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn BI() -> Country {
        Country {
            code: CountryCode::BI,
            code3: CountryCode::BI.codethree(),
            name: CountryCode::BI.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn CV() -> Country {
        Country {
            code: CountryCode::CV,
            code3: CountryCode::CV.codethree(),
            name: CountryCode::CV.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn KH() -> Country {
        Country {
            code: CountryCode::KH,
            code3: CountryCode::KH.codethree(),
            name: CountryCode::KH.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn CM() -> Country {
        Country {
            code: CountryCode::CM,
            code3: CountryCode::CM.codethree(),
            name: CountryCode::CM.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn CA() -> Country {
        Country {
            code: CountryCode::CA,
            code3: CountryCode::CA.codethree(),
            name: CountryCode::CA.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn KY() -> Country {
        Country {
            code: CountryCode::KY,
            code3: CountryCode::KY.codethree(),
            name: CountryCode::KY.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn CF() -> Country {
        Country {
            code: CountryCode::CF,
            code3: CountryCode::CF.codethree(),
            name: CountryCode::CF.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn TD() -> Country {
        Country {
            code: CountryCode::TD,
            code3: CountryCode::TD.codethree(),
            name: CountryCode::TD.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn CL() -> Country {
        Country {
            code: CountryCode::CL,
            code3: CountryCode::CL.codethree(),
            name: CountryCode::CL.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn CN() -> Country {
        Country {
            code: CountryCode::CN,
            code3: CountryCode::CN.codethree(),
            name: CountryCode::CN.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn CX() -> Country {
        Country {
            code: CountryCode::CX,
            code3: CountryCode::CX.codethree(),
            name: CountryCode::CX.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn CC() -> Country {
        Country {
            code: CountryCode::CC,
            code3: CountryCode::CC.codethree(),
            name: CountryCode::CC.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn CO() -> Country {
        Country {
            code: CountryCode::CO,
            code3: CountryCode::CO.codethree(),
            name: CountryCode::CO.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn KM() -> Country {
        Country {
            code: CountryCode::KM,
            code3: CountryCode::KM.codethree(),
            name: CountryCode::KM.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn CG() -> Country {
        Country {
            code: CountryCode::CG,
            code3: CountryCode::CG.codethree(),
            name: CountryCode::CG.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn CD() -> Country {
        Country {
            code: CountryCode::CD,
            code3: CountryCode::CD.codethree(),
            name: CountryCode::CD.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn CK() -> Country {
        Country {
            code: CountryCode::CK,
            code3: CountryCode::CK.codethree(),
            name: CountryCode::CK.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn CR() -> Country {
        Country {
            code: CountryCode::CR,
            code3: CountryCode::CR.codethree(),
            name: CountryCode::CR.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn CI() -> Country {
        Country {
            code: CountryCode::CI,
            code3: CountryCode::CI.codethree(),
            name: CountryCode::CI.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn HR() -> Country {
        Country {
            code: CountryCode::HR,
            code3: CountryCode::HR.codethree(),
            name: CountryCode::HR.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn CU() -> Country {
        Country {
            code: CountryCode::CU,
            code3: CountryCode::CU.codethree(),
            name: CountryCode::CU.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn CW() -> Country {
        Country {
            code: CountryCode::CW,
            code3: CountryCode::CW.codethree(),
            name: CountryCode::CW.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn CY() -> Country {
        Country {
            code: CountryCode::CY,
            code3: CountryCode::CY.codethree(),
            name: CountryCode::CY.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn CZ() -> Country {
        Country {
            code: CountryCode::CZ,
            code3: CountryCode::CZ.codethree(),
            name: CountryCode::CZ.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn DK() -> Country {
        Country {
            code: CountryCode::DK,
            code3: CountryCode::DK.codethree(),
            name: CountryCode::DK.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn DJ() -> Country {
        Country {
            code: CountryCode::DJ,
            code3: CountryCode::DJ.codethree(),
            name: CountryCode::DJ.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn DM() -> Country {
        Country {
            code: CountryCode::DM,
            code3: CountryCode::DM.codethree(),
            name: CountryCode::DM.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn DO() -> Country {
        Country {
            code: CountryCode::DO,
            code3: CountryCode::DO.codethree(),
            name: CountryCode::DO.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn EC() -> Country {
        Country {
            code: CountryCode::EC,
            code3: CountryCode::EC.codethree(),
            name: CountryCode::EC.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn EG() -> Country {
        Country {
            code: CountryCode::EG,
            code3: CountryCode::EG.codethree(),
            name: CountryCode::EG.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn SV() -> Country {
        Country {
            code: CountryCode::SV,
            code3: CountryCode::SV.codethree(),
            name: CountryCode::SV.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn GQ() -> Country {
        Country {
            code: CountryCode::GQ,
            code3: CountryCode::GQ.codethree(),
            name: CountryCode::GQ.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn ER() -> Country {
        Country {
            code: CountryCode::ER,
            code3: CountryCode::ER.codethree(),
            name: CountryCode::ER.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn EE() -> Country {
        Country {
            code: CountryCode::EE,
            code3: CountryCode::EE.codethree(),
            name: CountryCode::EE.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn SZ() -> Country {
        Country {
            code: CountryCode::SZ,
            code3: CountryCode::SZ.codethree(),
            name: CountryCode::SZ.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn ET() -> Country {
        Country {
            code: CountryCode::ET,
            code3: CountryCode::ET.codethree(),
            name: CountryCode::ET.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn FK() -> Country {
        Country {
            code: CountryCode::FK,
            code3: CountryCode::FK.codethree(),
            name: CountryCode::FK.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn FO() -> Country {
        Country {
            code: CountryCode::FO,
            code3: CountryCode::FO.codethree(),
            name: CountryCode::FO.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn FJ() -> Country {
        Country {
            code: CountryCode::FJ,
            code3: CountryCode::FJ.codethree(),
            name: CountryCode::FJ.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn FI() -> Country {
        Country {
            code: CountryCode::FI,
            code3: CountryCode::FI.codethree(),
            name: CountryCode::FI.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn FR() -> Country {
        Country {
            code: CountryCode::FR,
            code3: CountryCode::FR.codethree(),
            name: CountryCode::FR.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn GF() -> Country {
        Country {
            code: CountryCode::GF,
            code3: CountryCode::GF.codethree(),
            name: CountryCode::GF.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn PF() -> Country {
        Country {
            code: CountryCode::PF,
            code3: CountryCode::PF.codethree(),
            name: CountryCode::PF.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn TF() -> Country {
        Country {
            code: CountryCode::TF,
            code3: CountryCode::TF.codethree(),
            name: CountryCode::TF.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn GA() -> Country {
        Country {
            code: CountryCode::GA,
            code3: CountryCode::GA.codethree(),
            name: CountryCode::GA.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn GM() -> Country {
        Country {
            code: CountryCode::GM,
            code3: CountryCode::GM.codethree(),
            name: CountryCode::GM.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn GE() -> Country {
        Country {
            code: CountryCode::GE,
            code3: CountryCode::GE.codethree(),
            name: CountryCode::GE.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn DE() -> Country {
        Country {
            code: CountryCode::DE,
            code3: CountryCode::DE.codethree(),
            name: CountryCode::DE.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn GH() -> Country {
        Country {
            code: CountryCode::GH,
            code3: CountryCode::GH.codethree(),
            name: CountryCode::GH.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn GI() -> Country {
        Country {
            code: CountryCode::GI,
            code3: CountryCode::GI.codethree(),
            name: CountryCode::GI.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn GR() -> Country {
        Country {
            code: CountryCode::GR,
            code3: CountryCode::GR.codethree(),
            name: CountryCode::GR.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn GL() -> Country {
        Country {
            code: CountryCode::GL,
            code3: CountryCode::GL.codethree(),
            name: CountryCode::GL.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn GD() -> Country {
        Country {
            code: CountryCode::GD,
            code3: CountryCode::GD.codethree(),
            name: CountryCode::GD.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn GP() -> Country {
        Country {
            code: CountryCode::GP,
            code3: CountryCode::GP.codethree(),
            name: CountryCode::GP.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn GU() -> Country {
        Country {
            code: CountryCode::GU,
            code3: CountryCode::GU.codethree(),
            name: CountryCode::GU.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn GT() -> Country {
        Country {
            code: CountryCode::GT,
            code3: CountryCode::GT.codethree(),
            name: CountryCode::GT.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn GG() -> Country {
        Country {
            code: CountryCode::GG,
            code3: CountryCode::GG.codethree(),
            name: CountryCode::GG.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn GN() -> Country {
        Country {
            code: CountryCode::GN,
            code3: CountryCode::GN.codethree(),
            name: CountryCode::GN.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn GW() -> Country {
        Country {
            code: CountryCode::GW,
            code3: CountryCode::GW.codethree(),
            name: CountryCode::GW.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn GY() -> Country {
        Country {
            code: CountryCode::GY,
            code3: CountryCode::GY.codethree(),
            name: CountryCode::GY.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn HT() -> Country {
        Country {
            code: CountryCode::HT,
            code3: CountryCode::HT.codethree(),
            name: CountryCode::HT.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn HM() -> Country {
        Country {
            code: CountryCode::HM,
            code3: CountryCode::HM.codethree(),
            name: CountryCode::HM.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn VA() -> Country {
        Country {
            code: CountryCode::VA,
            code3: CountryCode::VA.codethree(),
            name: CountryCode::VA.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn HN() -> Country {
        Country {
            code: CountryCode::HN,
            code3: CountryCode::HN.codethree(),
            name: CountryCode::HN.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn HK() -> Country {
        Country {
            code: CountryCode::HK,
            code3: CountryCode::HK.codethree(),
            name: CountryCode::HK.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn HU() -> Country {
        Country {
            code: CountryCode::HU,
            code3: CountryCode::HU.codethree(),
            name: CountryCode::HU.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn IS() -> Country {
        Country {
            code: CountryCode::IS,
            code3: CountryCode::IS.codethree(),
            name: CountryCode::IS.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn IN() -> Country {
        Country {
            code: CountryCode::IN,
            code3: CountryCode::IN.codethree(),
            name: CountryCode::IN.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn ID() -> Country {
        Country {
            code: CountryCode::ID,
            code3: CountryCode::ID.codethree(),
            name: CountryCode::ID.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn IR() -> Country {
        Country {
            code: CountryCode::IR,
            code3: CountryCode::IR.codethree(),
            name: CountryCode::IR.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn IQ() -> Country {
        Country {
            code: CountryCode::IQ,
            code3: CountryCode::IQ.codethree(),
            name: CountryCode::IQ.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn IE() -> Country {
        Country {
            code: CountryCode::IE,
            code3: CountryCode::IE.codethree(),
            name: CountryCode::IE.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn IM() -> Country {
        Country {
            code: CountryCode::IM,
            code3: CountryCode::IM.codethree(),
            name: CountryCode::IM.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn IL() -> Country {
        Country {
            code: CountryCode::IL,
            code3: CountryCode::IL.codethree(),
            name: CountryCode::IL.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn IT() -> Country {
        Country {
            code: CountryCode::IT,
            code3: CountryCode::IT.codethree(),
            name: CountryCode::IT.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn JM() -> Country {
        Country {
            code: CountryCode::JM,
            code3: CountryCode::JM.codethree(),
            name: CountryCode::JM.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn JP() -> Country {
        Country {
            code: CountryCode::JP,
            code3: CountryCode::JP.codethree(),
            name: CountryCode::JP.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn JE() -> Country {
        Country {
            code: CountryCode::JE,
            code3: CountryCode::JE.codethree(),
            name: CountryCode::JE.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn JO() -> Country {
        Country {
            code: CountryCode::JO,
            code3: CountryCode::JO.codethree(),
            name: CountryCode::JO.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn KZ() -> Country {
        Country {
            code: CountryCode::KZ,
            code3: CountryCode::KZ.codethree(),
            name: CountryCode::KZ.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn KE() -> Country {
        Country {
            code: CountryCode::KE,
            code3: CountryCode::KE.codethree(),
            name: CountryCode::KE.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn KI() -> Country {
        Country {
            code: CountryCode::KI,
            code3: CountryCode::KI.codethree(),
            name: CountryCode::KI.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn KP() -> Country {
        Country {
            code: CountryCode::KP,
            code3: CountryCode::KP.codethree(),
            name: CountryCode::KP.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn KR() -> Country {
        Country {
            code: CountryCode::KR,
            code3: CountryCode::KR.codethree(),
            name: CountryCode::KR.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn KW() -> Country {
        Country {
            code: CountryCode::KW,
            code3: CountryCode::KW.codethree(),
            name: CountryCode::KW.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn KG() -> Country {
        Country {
            code: CountryCode::KG,
            code3: CountryCode::KG.codethree(),
            name: CountryCode::KG.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn LA() -> Country {
        Country {
            code: CountryCode::LA,
            code3: CountryCode::LA.codethree(),
            name: CountryCode::LA.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn LV() -> Country {
        Country {
            code: CountryCode::LV,
            code3: CountryCode::LV.codethree(),
            name: CountryCode::LV.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn LB() -> Country {
        Country {
            code: CountryCode::LB,
            code3: CountryCode::LB.codethree(),
            name: CountryCode::LB.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn LS() -> Country {
        Country {
            code: CountryCode::LS,
            code3: CountryCode::LS.codethree(),
            name: CountryCode::LS.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn LR() -> Country {
        Country {
            code: CountryCode::LR,
            code3: CountryCode::LR.codethree(),
            name: CountryCode::LR.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn LY() -> Country {
        Country {
            code: CountryCode::LY,
            code3: CountryCode::LY.codethree(),
            name: CountryCode::LY.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn LI() -> Country {
        Country {
            code: CountryCode::LI,
            code3: CountryCode::LI.codethree(),
            name: CountryCode::LI.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn LT() -> Country {
        Country {
            code: CountryCode::LT,
            code3: CountryCode::LT.codethree(),
            name: CountryCode::LT.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn LU() -> Country {
        Country {
            code: CountryCode::LU,
            code3: CountryCode::LU.codethree(),
            name: CountryCode::LU.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn MO() -> Country {
        Country {
            code: CountryCode::MO,
            code3: CountryCode::MO.codethree(),
            name: CountryCode::MO.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn MG() -> Country {
        Country {
            code: CountryCode::MG,
            code3: CountryCode::MG.codethree(),
            name: CountryCode::MG.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn MW() -> Country {
        Country {
            code: CountryCode::MW,
            code3: CountryCode::MW.codethree(),
            name: CountryCode::MW.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn MY() -> Country {
        Country {
            code: CountryCode::MY,
            code3: CountryCode::MY.codethree(),
            name: CountryCode::MY.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn MV() -> Country {
        Country {
            code: CountryCode::MV,
            code3: CountryCode::MV.codethree(),
            name: CountryCode::MV.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn ML() -> Country {
        Country {
            code: CountryCode::ML,
            code3: CountryCode::ML.codethree(),
            name: CountryCode::ML.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn MT() -> Country {
        Country {
            code: CountryCode::MT,
            code3: CountryCode::MT.codethree(),
            name: CountryCode::MT.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn MH() -> Country {
        Country {
            code: CountryCode::MH,
            code3: CountryCode::MH.codethree(),
            name: CountryCode::MH.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn MQ() -> Country {
        Country {
            code: CountryCode::MQ,
            code3: CountryCode::MQ.codethree(),
            name: CountryCode::MQ.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn MR() -> Country {
        Country {
            code: CountryCode::MR,
            code3: CountryCode::MR.codethree(),
            name: CountryCode::MR.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn MU() -> Country {
        Country {
            code: CountryCode::MU,
            code3: CountryCode::MU.codethree(),
            name: CountryCode::MU.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn YT() -> Country {
        Country {
            code: CountryCode::YT,
            code3: CountryCode::YT.codethree(),
            name: CountryCode::YT.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn MX() -> Country {
        Country {
            code: CountryCode::MX,
            code3: CountryCode::MX.codethree(),
            name: CountryCode::MX.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn FM() -> Country {
        Country {
            code: CountryCode::FM,
            code3: CountryCode::FM.codethree(),
            name: CountryCode::FM.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn MD() -> Country {
        Country {
            code: CountryCode::MD,
            code3: CountryCode::MD.codethree(),
            name: CountryCode::MD.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn MC() -> Country {
        Country {
            code: CountryCode::MC,
            code3: CountryCode::MC.codethree(),
            name: CountryCode::MC.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn MN() -> Country {
        Country {
            code: CountryCode::MN,
            code3: CountryCode::MN.codethree(),
            name: CountryCode::MN.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn ME() -> Country {
        Country {
            code: CountryCode::ME,
            code3: CountryCode::ME.codethree(),
            name: CountryCode::ME.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn MS() -> Country {
        Country {
            code: CountryCode::MS,
            code3: CountryCode::MS.codethree(),
            name: CountryCode::MS.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn MA() -> Country {
        Country {
            code: CountryCode::MA,
            code3: CountryCode::MA.codethree(),
            name: CountryCode::MA.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn MZ() -> Country {
        Country {
            code: CountryCode::MZ,
            code3: CountryCode::MZ.codethree(),
            name: CountryCode::MZ.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn MM() -> Country {
        Country {
            code: CountryCode::MM,
            code3: CountryCode::MM.codethree(),
            name: CountryCode::MM.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn NA() -> Country {
        Country {
            code: CountryCode::NA,
            code3: CountryCode::NA.codethree(),
            name: CountryCode::NA.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn NR() -> Country {
        Country {
            code: CountryCode::NR,
            code3: CountryCode::NR.codethree(),
            name: CountryCode::NR.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn NP() -> Country {
        Country {
            code: CountryCode::NP,
            code3: CountryCode::NP.codethree(),
            name: CountryCode::NP.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn NL() -> Country {
        Country {
            code: CountryCode::NL,
            code3: CountryCode::NL.codethree(),
            name: CountryCode::NL.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn NC() -> Country {
        Country {
            code: CountryCode::NC,
            code3: CountryCode::NC.codethree(),
            name: CountryCode::NC.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn NZ() -> Country {
        Country {
            code: CountryCode::NZ,
            code3: CountryCode::NZ.codethree(),
            name: CountryCode::NZ.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn NI() -> Country {
        Country {
            code: CountryCode::NI,
            code3: CountryCode::NI.codethree(),
            name: CountryCode::NI.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn NE() -> Country {
        Country {
            code: CountryCode::NE,
            code3: CountryCode::NE.codethree(),
            name: CountryCode::NE.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn NG() -> Country {
        Country {
            code: CountryCode::NG,
            code3: CountryCode::NG.codethree(),
            name: CountryCode::NG.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn NU() -> Country {
        Country {
            code: CountryCode::NU,
            code3: CountryCode::NU.codethree(),
            name: CountryCode::NU.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn NF() -> Country {
        Country {
            code: CountryCode::NF,
            code3: CountryCode::NF.codethree(),
            name: CountryCode::NF.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn MK() -> Country {
        Country {
            code: CountryCode::MK,
            code3: CountryCode::MK.codethree(),
            name: CountryCode::MK.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn MP() -> Country {
        Country {
            code: CountryCode::MP,
            code3: CountryCode::MP.codethree(),
            name: CountryCode::MP.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn NO() -> Country {
        Country {
            code: CountryCode::NO,
            code3: CountryCode::NO.codethree(),
            name: CountryCode::NO.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn OM() -> Country {
        Country {
            code: CountryCode::OM,
            code3: CountryCode::OM.codethree(),
            name: CountryCode::OM.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn PK() -> Country {
        Country {
            code: CountryCode::PK,
            code3: CountryCode::PK.codethree(),
            name: CountryCode::PK.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn PW() -> Country {
        Country {
            code: CountryCode::PW,
            code3: CountryCode::PW.codethree(),
            name: CountryCode::PW.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn PS() -> Country {
        Country {
            code: CountryCode::PS,
            code3: CountryCode::PS.codethree(),
            name: CountryCode::PS.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn PA() -> Country {
        Country {
            code: CountryCode::PA,
            code3: CountryCode::PA.codethree(),
            name: CountryCode::PA.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn PG() -> Country {
        Country {
            code: CountryCode::PG,
            code3: CountryCode::PG.codethree(),
            name: CountryCode::PG.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn PY() -> Country {
        Country {
            code: CountryCode::PY,
            code3: CountryCode::PY.codethree(),
            name: CountryCode::PY.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn PE() -> Country {
        Country {
            code: CountryCode::PE,
            code3: CountryCode::PE.codethree(),
            name: CountryCode::PE.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn PH() -> Country {
        Country {
            code: CountryCode::PH,
            code3: CountryCode::PH.codethree(),
            name: CountryCode::PH.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn PN() -> Country {
        Country {
            code: CountryCode::PN,
            code3: CountryCode::PN.codethree(),
            name: CountryCode::PN.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn PL() -> Country {
        Country {
            code: CountryCode::PL,
            code3: CountryCode::PL.codethree(),
            name: CountryCode::PL.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn PT() -> Country {
        Country {
            code: CountryCode::PT,
            code3: CountryCode::PT.codethree(),
            name: CountryCode::PT.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn PR() -> Country {
        Country {
            code: CountryCode::PR,
            code3: CountryCode::PR.codethree(),
            name: CountryCode::PR.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn QA() -> Country {
        Country {
            code: CountryCode::QA,
            code3: CountryCode::QA.codethree(),
            name: CountryCode::QA.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn RE() -> Country {
        Country {
            code: CountryCode::RE,
            code3: CountryCode::RE.codethree(),
            name: CountryCode::RE.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn RO() -> Country {
        Country {
            code: CountryCode::RO,
            code3: CountryCode::RO.codethree(),
            name: CountryCode::RO.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn RU() -> Country {
        Country {
            code: CountryCode::RU,
            code3: CountryCode::RU.codethree(),
            name: CountryCode::RU.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn RW() -> Country {
        Country {
            code: CountryCode::RW,
            code3: CountryCode::RW.codethree(),
            name: CountryCode::RW.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn BL() -> Country {
        Country {
            code: CountryCode::BL,
            code3: CountryCode::BL.codethree(),
            name: CountryCode::BL.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn SH() -> Country {
        Country {
            code: CountryCode::SH,
            code3: CountryCode::SH.codethree(),
            name: CountryCode::SH.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn KN() -> Country {
        Country {
            code: CountryCode::KN,
            code3: CountryCode::KN.codethree(),
            name: CountryCode::KN.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn LC() -> Country {
        Country {
            code: CountryCode::LC,
            code3: CountryCode::LC.codethree(),
            name: CountryCode::LC.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn MF() -> Country {
        Country {
            code: CountryCode::MF,
            code3: CountryCode::MF.codethree(),
            name: CountryCode::MF.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn PM() -> Country {
        Country {
            code: CountryCode::PM,
            code3: CountryCode::PM.codethree(),
            name: CountryCode::PM.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn VC() -> Country {
        Country {
            code: CountryCode::VC,
            code3: CountryCode::VC.codethree(),
            name: CountryCode::VC.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn WS() -> Country {
        Country {
            code: CountryCode::WS,
            code3: CountryCode::WS.codethree(),
            name: CountryCode::WS.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn SM() -> Country {
        Country {
            code: CountryCode::SM,
            code3: CountryCode::SM.codethree(),
            name: CountryCode::SM.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn ST() -> Country {
        Country {
            code: CountryCode::ST,
            code3: CountryCode::ST.codethree(),
            name: CountryCode::ST.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn SA() -> Country {
        Country {
            code: CountryCode::SA,
            code3: CountryCode::SA.codethree(),
            name: CountryCode::SA.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn SN() -> Country {
        Country {
            code: CountryCode::SN,
            code3: CountryCode::SN.codethree(),
            name: CountryCode::SN.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn RS() -> Country {
        Country {
            code: CountryCode::RS,
            code3: CountryCode::RS.codethree(),
            name: CountryCode::RS.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn SC() -> Country {
        Country {
            code: CountryCode::SC,
            code3: CountryCode::SC.codethree(),
            name: CountryCode::SC.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn SL() -> Country {
        Country {
            code: CountryCode::SL,
            code3: CountryCode::SL.codethree(),
            name: CountryCode::SL.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn SG() -> Country {
        Country {
            code: CountryCode::SG,
            code3: CountryCode::SG.codethree(),
            name: CountryCode::SG.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn SX() -> Country {
        Country {
            code: CountryCode::SX,
            code3: CountryCode::SX.codethree(),
            name: CountryCode::SX.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn SK() -> Country {
        Country {
            code: CountryCode::SK,
            code3: CountryCode::SK.codethree(),
            name: CountryCode::SK.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn SI() -> Country {
        Country {
            code: CountryCode::SI,
            code3: CountryCode::SI.codethree(),
            name: CountryCode::SI.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn SB() -> Country {
        Country {
            code: CountryCode::SB,
            code3: CountryCode::SB.codethree(),
            name: CountryCode::SB.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn SO() -> Country {
        Country {
            code: CountryCode::SO,
            code3: CountryCode::SO.codethree(),
            name: CountryCode::SO.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn ZA() -> Country {
        Country {
            code: CountryCode::ZA,
            code3: CountryCode::ZA.codethree(),
            name: CountryCode::ZA.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn GS() -> Country {
        Country {
            code: CountryCode::GS,
            code3: CountryCode::GS.codethree(),
            name: CountryCode::GS.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn SS() -> Country {
        Country {
            code: CountryCode::SS,
            code3: CountryCode::SS.codethree(),
            name: CountryCode::SS.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn ES() -> Country {
        Country {
            code: CountryCode::ES,
            code3: CountryCode::ES.codethree(),
            name: CountryCode::ES.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn LK() -> Country {
        Country {
            code: CountryCode::LK,
            code3: CountryCode::LK.codethree(),
            name: CountryCode::LK.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn SD() -> Country {
        Country {
            code: CountryCode::SD,
            code3: CountryCode::SD.codethree(),
            name: CountryCode::SD.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn SR() -> Country {
        Country {
            code: CountryCode::SR,
            code3: CountryCode::SR.codethree(),
            name: CountryCode::SR.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn SJ() -> Country {
        Country {
            code: CountryCode::SJ,
            code3: CountryCode::SJ.codethree(),
            name: CountryCode::SJ.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn SE() -> Country {
        Country {
            code: CountryCode::SE,
            code3: CountryCode::SE.codethree(),
            name: CountryCode::SE.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn CH() -> Country {
        Country {
            code: CountryCode::CH,
            code3: CountryCode::CH.codethree(),
            name: CountryCode::CH.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn SY() -> Country {
        Country {
            code: CountryCode::SY,
            code3: CountryCode::SY.codethree(),
            name: CountryCode::SY.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn TW() -> Country {
        Country {
            code: CountryCode::TW,
            code3: CountryCode::TW.codethree(),
            name: CountryCode::TW.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn TJ() -> Country {
        Country {
            code: CountryCode::TJ,
            code3: CountryCode::TJ.codethree(),
            name: CountryCode::TJ.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn TZ() -> Country {
        Country {
            code: CountryCode::TZ,
            code3: CountryCode::TZ.codethree(),
            name: CountryCode::TZ.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn TH() -> Country {
        Country {
            code: CountryCode::TH,
            code3: CountryCode::TH.codethree(),
            name: CountryCode::TH.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn TL() -> Country {
        Country {
            code: CountryCode::TL,
            code3: CountryCode::TL.codethree(),
            name: CountryCode::TL.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn TG() -> Country {
        Country {
            code: CountryCode::TG,
            code3: CountryCode::TG.codethree(),
            name: CountryCode::TG.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn TK() -> Country {
        Country {
            code: CountryCode::TK,
            code3: CountryCode::TK.codethree(),
            name: CountryCode::TK.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn TO() -> Country {
        Country {
            code: CountryCode::TO,
            code3: CountryCode::TO.codethree(),
            name: CountryCode::TO.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn TT() -> Country {
        Country {
            code: CountryCode::TT,
            code3: CountryCode::TT.codethree(),
            name: CountryCode::TT.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn TN() -> Country {
        Country {
            code: CountryCode::TN,
            code3: CountryCode::TN.codethree(),
            name: CountryCode::TN.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn TR() -> Country {
        Country {
            code: CountryCode::TR,
            code3: CountryCode::TR.codethree(),
            name: CountryCode::TR.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn TM() -> Country {
        Country {
            code: CountryCode::TM,
            code3: CountryCode::TM.codethree(),
            name: CountryCode::TM.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn TC() -> Country {
        Country {
            code: CountryCode::TC,
            code3: CountryCode::TC.codethree(),
            name: CountryCode::TC.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn TV() -> Country {
        Country {
            code: CountryCode::TV,
            code3: CountryCode::TV.codethree(),
            name: CountryCode::TV.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn UG() -> Country {
        Country {
            code: CountryCode::UG,
            code3: CountryCode::UG.codethree(),
            name: CountryCode::UG.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn UA() -> Country {
        Country {
            code: CountryCode::UA,
            code3: CountryCode::UA.codethree(),
            name: CountryCode::UA.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn AE() -> Country {
        Country {
            code: CountryCode::AE,
            code3: CountryCode::AE.codethree(),
            name: CountryCode::AE.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn GB() -> Country {
        Country {
            code: CountryCode::GB,
            code3: CountryCode::GB.codethree(),
            name: CountryCode::GB.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn US() -> Country {
        Country {
            code: CountryCode::US,
            code3: CountryCode::US.codethree(),
            name: CountryCode::US.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn UM() -> Country {
        Country {
            code: CountryCode::UM,
            code3: CountryCode::UM.codethree(),
            name: CountryCode::UM.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn UY() -> Country {
        Country {
            code: CountryCode::UY,
            code3: CountryCode::UY.codethree(),
            name: CountryCode::UY.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn UZ() -> Country {
        Country {
            code: CountryCode::UZ,
            code3: CountryCode::UZ.codethree(),
            name: CountryCode::UZ.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn VU() -> Country {
        Country {
            code: CountryCode::VU,
            code3: CountryCode::VU.codethree(),
            name: CountryCode::VU.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn VE() -> Country {
        Country {
            code: CountryCode::VE,
            code3: CountryCode::VE.codethree(),
            name: CountryCode::VE.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn VN() -> Country {
        Country {
            code: CountryCode::VN,
            code3: CountryCode::VN.codethree(),
            name: CountryCode::VN.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn VG() -> Country {
        Country {
            code: CountryCode::VG,
            code3: CountryCode::VG.codethree(),
            name: CountryCode::VG.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn VI() -> Country {
        Country {
            code: CountryCode::VI,
            code3: CountryCode::VI.codethree(),
            name: CountryCode::VI.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn WF() -> Country {
        Country {
            code: CountryCode::WF,
            code3: CountryCode::WF.codethree(),
            name: CountryCode::WF.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn EH() -> Country {
        Country {
            code: CountryCode::EH,
            code3: CountryCode::EH.codethree(),
            name: CountryCode::EH.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn YE() -> Country {
        Country {
            code: CountryCode::YE,
            code3: CountryCode::YE.codethree(),
            name: CountryCode::YE.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn ZM() -> Country {
        Country {
            code: CountryCode::ZM,
            code3: CountryCode::ZM.codethree(),
            name: CountryCode::ZM.str(),
        }
    }
    #[classattr]
    #[allow(non_snake_case)]
    fn ZW() -> Country {
        Country {
            code: CountryCode::ZW,
            code3: CountryCode::ZW.codethree(),
            name: CountryCode::ZW.str(),
        }
    }
}
