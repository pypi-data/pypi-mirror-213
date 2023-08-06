import pandas as pd
import chardet

URL = "https://www.iso20022.org/sites/default/files/ISO10383_MIC/ISO10383_MIC.csv"
URL = "helpers/ISO10383_MIC.csv"

df = pd.read_csv(URL, encoding="Windows-1252")

df = df[
    ["MIC", "OPERATING MIC", "OPRT/SGMT", "MARKET NAME-INSTITUTION DESCRIPTION", "LEGAL ENTITY NAME", "LEI", "ISO COUNTRY CODE (ISO 3166)", "STATUS"]
]
df = df[df["STATUS"] != "EXPIRED"]
# df["MARKET NAME-INSTITUTION DESCRIPTION"] = df["MARKET NAME-INSTITUTION DESCRIPTION"].str.title()
# df["LEGAL ENTITY NAME"] = df["LEGAL ENTITY NAME"].str.title()
df_oprt = df[df["OPRT/SGMT"] == "OPRT"]
df_oprt.to_csv("helpers/mics_oprt.csv", index=False)

assert len(df_oprt[df_oprt["MIC"] != df_oprt["OPERATING MIC"]]) == 0

mic_to_operating = {}
mic_to_name = {}
mic_to_country = {}
mic_to_lei = {}

for record in df_oprt.to_dict(orient="records"):
    mic_to_operating[record["MIC"]] = record["OPERATING MIC"]
    mic_to_name[record["MIC"]] = record["MARKET NAME-INSTITUTION DESCRIPTION"]
    mic_to_country[record["MIC"]] = record["ISO COUNTRY CODE (ISO 3166)"]
    mic_to_lei[record["MIC"]] = record["LEI"]

to_writeout = """
use super::CountryCode;
use serde::{Deserialize, Serialize};

#[derive(Clone, Debug, Deserialize, Display, EnumIter, EnumString, Eq, PartialEq, Serialize)]
#[strum(serialize_all = "PascalCase")]
pub enum MIC {
"""

for key in mic_to_operating:
    to_writeout += f"\t{key},\n"

to_writeout += """
}

impl MIC {
    pub fn operating_mic(&self) -> &'static str {
        match self {
"""

for key, item in mic_to_operating.items():
    to_writeout += f'\t\t\t{key} => "{item}",\n'

to_writeout += """
        }
    }

    pub fn name(&self) -> &'static str {
        match self {
"""

for key, item in mic_to_name.items():
    to_writeout += f'\t\t\t{key} => "{item}",\n'

to_writeout += """
        }
    }

    pub fn country(&self) -> CountryCode {
        match self {
"""

for key, item in mic_to_country.items():
    to_writeout += f'\t\t\t{key} => CountryCode::{item},\n'

to_writeout += """
        }
    }

    pub fn lei(&self) -> &'static str {
        match self {
"""

for key, item in mic_to_lei.items():
    to_writeout += f'\t\t\t{key} => "{str(item).replace("nan", "")}",\n'

to_writeout += """
        }
    }
}
"""

with open("helpers/iso10383_generated.rs", "w") as fp:
    fp.write(to_writeout)

# replace = [
#     ("Llc", "LLC"),
#     ("L.L.C", "LLC"),
#     (" Uk", " UK"),
#     ("Cnsx Markets", "CNSX Markets"),
#     (" Ad,", " AD,"),
#     ("Spb Exchange", "SPB Exchange"),
#     ("Otc ", "OTC "),
#     ("Idx Markets", "IDX Markets"),
#     (" Bcp,", " BCP,"),
#     (" Ats", " ATS"),
#     ("Osl ", "OSL "),
#     ("Bnp Paribas", "BNP Paribas"),
#     ("Bgl ", "BGL "),
#     ("Gfi ", "GFI "),
#     ("Icap ", "ICAP "),
#     (" Otf", " Otf"),
#     ("Hsbc", "HSBC"),
#     ("Mitsubishi Ufj", "Mitsubishi UFJ"),
#     (" Apa", " APA"),
#     ("Ebx ", "EBX "),
#     ("Abn Amro", "ABN AMRO"),
#     ("Bnpp", "BNPP"),
#     ("Rmb Morgan", "RMB Morgan"),
#     ("Rbc ", "RBC "),
#     ("Xtx ", "XTX "),
#     ("Cartax", "CartaX"),
#     ("Cboe", "CBOE"),
#     ("Pngx", "PNGX"),
#     ("Immh", "IMMH"),
#     (" Fx", " FX"),
#     ("Fx ", "FX "),
#     ("Ledgeredge", "LedgerEdge"),
#     (" Mtf", " MTF"),
#     (" Na ", " NA "),
#     ("Skb Banka", "SKB Banka"),
#     ("Dsk Bank", "DSK Bank"),
#     (" Ead", " EAD"),
#     ("Otp Bank", "OTP Bank"),
#     ("  ", " "),
#     ("Memx", "MEMX"),
#     (" And ", " and "),
#     ("Ndfs", "NDFS"),
#     ("Lch ", "LCH "),
#     ("Fex ", "FEX "),
#     ("Clsa Americas", "CLSA Americas"),
#     ("Omip -", "OMIP -"),
#     (" Us ", " US "),
#     (" Sef ", " SEF "),
#     ("Xp Investments", "XP Investments"),
#     (" Of ", " of "),
#     ("Posit ", "POSIT "),
#     ("Seb ", "Seb"),
#     ("Bb Securities", "BB Securities"),
#     ("Gsx ", "GSX "),
#     ("Bmo ", "BMO "),
#     ("Trcx", "TRCX"),
#     ("Jpms", "J.P. Morgan Securities"),
#     (" The ", " the "),
#     ("Td Securities", "TD Securities"),
#     ("Ubs ", "UBS "),
#     ("Marketaxess", "MarketAxess"),
#     ("Bny Mellon", "BNY Mellon"),
#     ("Tp Icap", "TP ICAP")
#     ("Smbc", "SMBC"),
#     ("Sg Americas", "SG Americas"),
#     (" Fi ", " FI "),
#     (" Sas", " SAS"),
#     ("Cme ", "CME "),
#     ("Hrteu", "HRTEU"),
#     ("Cib Bank", "CIB Bank"),
#     ("Ebs ", "EBS "),
#     ("Tradecho", "TRADEcho"),
#     ("Xtrd", "XTRD"),
#     ("Bofa", "Bank of America"),
#     ("Brokercreditservice", "BrokerCreditService"),
#     ("Gpb-Financial", "GPB-Financial"),
#     ("Ohv", "OHV"),
#     ("Mufg", "MUFG"),
#     ("Nibc", "NIBC"),
#     ("Pjsc", "PJSC"),
#     ("Brd ", "BRD "),
#     ("Cibc", "CIBC"),
#     ("Plc", "PLC"),
#     ("Icbc", "ICBC"),
#     ("Ikb", "IKB"),
#     ("Hrt", "HRT"),
#     ("Lbbw", "LBBW"),
#     ("Ifsc", "IFSC"),
#     ("Gmg ", "GMG "),
#     ("Gtx ", "GTX "),
#     ("Jpmorgan", "J.P. Morgan"),
#     ("Trueex", "TrueEX"),
#     (".Com", ".com"),
# ]
