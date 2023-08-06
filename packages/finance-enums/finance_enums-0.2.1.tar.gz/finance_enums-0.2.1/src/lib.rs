use pyo3::prelude::*;

mod country;
mod currency;
mod exchange;
mod instrument;
mod sector;
mod security;
mod trading;

use country::Country;
use currency::Currency;
use exchange::Exchange;
use sector::{Sector, IndustryGroup, Industry, SubIndustry};
use security::{SecurityType, EquityType, OptionType, BondType, CommodityType, FundType, OptionExerciseType, FundSubType, MutualFundEndedness};
use trading::{OrderType, Side, TimeInForce, OrderFlag};

#[pymodule]
fn finance_enums(_py: Python, m: &PyModule) -> PyResult<()> {
    // Country
    m.add_class::<Country>()?;

    // Currency
    m.add_class::<Currency>()?;

    // Exchange
    m.add_class::<Exchange>()?;

    // Sector
    m.add_class::<Sector>()?;
    m.add_class::<IndustryGroup>()?;
    m.add_class::<Industry>()?;
    m.add_class::<SubIndustry>()?;

    // Security
    m.add_class::<SecurityType>()?;
    m.add_class::<EquityType>()?;
    m.add_class::<OptionType>()?;
    m.add_class::<OptionExerciseType>()?;
    m.add_class::<BondType>()?;
    m.add_class::<CommodityType>()?;
    m.add_class::<FundType>()?;
    m.add_class::<FundSubType>()?;
    m.add_class::<MutualFundEndedness>()?;

    m.add_class::<OrderType>()?;
    m.add_class::<Side>()?;
    m.add_class::<TimeInForce>()?;
    m.add_class::<OrderFlag>()?;
    Ok(())
}
