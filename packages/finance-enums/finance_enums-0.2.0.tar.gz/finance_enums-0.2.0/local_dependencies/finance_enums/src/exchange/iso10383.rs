use crate::CountryCode;
use serde::{Deserialize, Serialize};

#[derive(Clone, Debug, Deserialize, Display, EnumIter, EnumString, Eq, PartialEq, Serialize)]
#[strum(serialize_all = "PascalCase")]
pub enum MIC {
    // NYSE
    XNYS,
    ARCX,
    XASE,
    XCIS,
    XCHI,
    // NASDAQ
    XNAS,
    XNGS,
    XBOS,
    XPHL,
    // CBOE
    XCBO,
    BATS,
    BATY,
    EDGX,
    EDGA,
    // MIAX
    MPRL,
    MIHI,
    // MEMX
    MEMX,
    // IEX
    IEXG,
    // LTSE
    LTSE,
    // FINRA
    XADF,
    FINR,
}

impl MIC {
    pub fn operating_mic(&self) -> MIC {
        match self {
            // NYSE
            MIC::XNYS => MIC::XNYS,
            MIC::ARCX => MIC::XNYS,
            MIC::XASE => MIC::XNYS,
            MIC::XCIS => MIC::XNYS,
            MIC::XCHI => MIC::XNYS,
            // NASDAQ
            MIC::XNAS => MIC::XNAS,
            MIC::XNGS => MIC::XNAS,
            MIC::XBOS => MIC::XNAS,
            MIC::XPHL => MIC::XNAS,
            // CBOE
            MIC::XCBO => MIC::XCBO,
            MIC::BATS => MIC::XCBO,
            MIC::BATY => MIC::XCBO,
            MIC::EDGX => MIC::XCBO,
            MIC::EDGA => MIC::XCBO,
            // MIAX
            MIC::MPRL => MIC::MIHI,
            MIC::MIHI => MIC::MIHI,
            // MEMX
            MIC::MEMX => MIC::MEMX,
            // IEX
            MIC::IEXG => MIC::IEXG,
            // LTSE
            MIC::LTSE => MIC::LTSE,
            // FINRA
            MIC::XADF => MIC::FINR,
            MIC::FINR => MIC::FINR,
        }
    }

    pub fn name(&self) -> &'static str {
        match self {
            // NYSE
            MIC::XNYS => "New York Stock Exchange",
            MIC::ARCX => "NYSE ARCA",
            MIC::XASE => "NYSE AMEX",
            MIC::XCIS => "NYSE National",
            MIC::XCHI => "NYSE Chicago",
            // NASDAQ
            MIC::XNAS => "Nasdaq",
            MIC::XNGS => "Nasdaq Global Select",
            MIC::XBOS => "Nasdaq BX",
            MIC::XPHL => "Nasdaq PHLX",
            // CBOE
            MIC::XCBO => "CBOE Global Markets",
            MIC::BATS => "CBOE BZX",
            MIC::BATY => "CBOE BYX",
            MIC::EDGX => "CBOE EDGX",
            MIC::EDGA => "CBOE EDGA",
            // MIAX
            MIC::MPRL => "MIAX Pearl",
            MIC::MIHI => "MIAX",
            // MEMX
            MIC::MEMX => "MEMX",
            // IEX
            MIC::IEXG => "Investors Exchange",
            // LTSE
            MIC::LTSE => "Long-term Stock Exchange",
            // FINRA
            MIC::XADF => "FINRA Alternative Display Facility",
            MIC::FINR => "FINRA",
        }
    }

    pub fn country(&self) -> CountryCode {
        match self {
            // NYSE
            MIC::XNYS => CountryCode::US,
            MIC::ARCX => CountryCode::US,
            MIC::XASE => CountryCode::US,
            MIC::XCIS => CountryCode::US,
            MIC::XCHI => CountryCode::US,
            // NASDAQ
            MIC::XNAS => CountryCode::US,
            MIC::XNGS => CountryCode::US,
            MIC::XBOS => CountryCode::US,
            MIC::XPHL => CountryCode::US,
            // CBOE
            MIC::XCBO => CountryCode::US,
            MIC::BATS => CountryCode::US,
            MIC::BATY => CountryCode::US,
            MIC::EDGX => CountryCode::US,
            MIC::EDGA => CountryCode::US,
            // MIAX
            MIC::MPRL => CountryCode::US,
            MIC::MIHI => CountryCode::US,
            // MEMX
            MIC::MEMX => CountryCode::US,
            // IEX
            MIC::IEXG => CountryCode::US,
            // LTSE
            MIC::LTSE => CountryCode::US,
            // FINRA
            MIC::XADF => CountryCode::US,
            MIC::FINR => CountryCode::US,
        }
    }
}
