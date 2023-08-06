use serde::{Deserialize, Serialize};

#[derive(Clone, Debug, Deserialize, Display, EnumIter, EnumString, Eq, PartialEq, Serialize)]
#[strum(serialize_all = "PascalCase")]
pub enum EquityType {
    Shares,
    PreferredShares,
    ConvertibleShares,
    PreferredConvertibleShares,
    DepositoryReceipt,
}
