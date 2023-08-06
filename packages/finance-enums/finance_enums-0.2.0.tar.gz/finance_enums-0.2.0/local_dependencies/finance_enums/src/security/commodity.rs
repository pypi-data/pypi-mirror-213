use serde::{Deserialize, Serialize};

#[derive(Clone, Debug, Deserialize, Display, EnumIter, EnumString, Eq, PartialEq, Serialize)]
#[strum(serialize_all = "PascalCase")]
pub enum CommodityType {
    Energy,
    Metals,
    Agriculture,
}

// TODO
// #[derive(Clone, Debug, Deserialize, Display, EnumIter, EnumString, Eq, PartialEq, Serialize)]
// #[strum(serialize_all = "PascalCase")]
// pub enum CommoditySubType {
//     EnergyType(Energy),
//     MetalType(Metals),
//     AgricultureType(Agriculture),
// }

#[derive(Clone, Debug, Deserialize, Display, EnumIter, EnumString, Eq, PartialEq, Serialize)]
#[strum(serialize_all = "PascalCase")]
pub enum Energy {
    Crude,
    WTICrude,
    BrentCrude,
    NaturalGas,
}

#[derive(Clone, Debug, Deserialize, Display, EnumIter, EnumString, Eq, PartialEq, Serialize)]
#[strum(serialize_all = "PascalCase")]
pub enum Metals {
    Gold,
    Silver,
    Copper,
    Platinum,
    Palladium,
}

#[derive(Clone, Debug, Deserialize, Display, EnumIter, EnumString, Eq, PartialEq, Serialize)]
#[strum(serialize_all = "PascalCase")]
pub enum Agriculture {
    Corn,
    Wheat,
    Oats,
    Soybean,
    Cocoa,
    Coffee,
    Sugar,
    Cotten,
    OrangeJuice,
    Cattle,
    Hogs,
}
