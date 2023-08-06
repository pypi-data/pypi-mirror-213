import os
import os.path
from base64 import b64encode


flags = os.listdir("flags")

output = """
    pub fn flag(&self) -> &'static str {
        match self {
"""
for flag in flags:
    with open(f"flags/{flag}", "rb") as fp:
        flagdata = fp.read()
    output += f"            CountryCode::{flag.replace('.png', '')} => \"{b64encode(flagdata).decode('ascii')}\",\n"
output += "}"

print(output)
