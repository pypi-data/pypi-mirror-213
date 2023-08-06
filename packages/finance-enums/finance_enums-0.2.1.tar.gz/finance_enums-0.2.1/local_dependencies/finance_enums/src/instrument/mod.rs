use serde::{Deserialize, Serialize};

#[derive(Clone, Debug, Deserialize, Display, EnumIter, EnumString, Eq, PartialEq, Serialize)]
#[strum(serialize_all = "PascalCase")]
pub enum InstrumentType {
    Spot,    // single instrument
    Option,  // underlying + date
    Forward, // underlying + date
    Future,  // underlying + date
    Right,   // underlying
    Spread,  // left / right legs
    Pair,    // left / right legs
    Basket,  // components
}
