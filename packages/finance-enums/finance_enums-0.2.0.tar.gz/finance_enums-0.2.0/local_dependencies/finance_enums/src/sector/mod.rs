// https://en.wikipedia.org/wiki/Global_Industry_Classification_Standard
// https://www.msci.com/our-solutions/indexes/gics
mod industry;
mod industry_group;
#[allow(clippy::module_inception)]
mod sector;
mod subindustry;

pub use industry::*;
pub use industry_group::*;
pub use sector::*;
pub use subindustry::*;
