use serde::{Deserialize, Serialize};

#[derive(Clone, Debug, Deserialize, Display, EnumIter, EnumString, Eq, PartialEq, Serialize)]
#[strum(serialize_all = "PascalCase")]
pub enum SecurityType {
    Equity,
    Option,
    Bond,
    Forward,
    Future,
    PerpetualFuture,
    Spread,
    Fund,
    Commodity,
    Currency,
    Pair,
    Index,
}
