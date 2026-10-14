"""Map PSA geography labels (they differ across tables) to one canonical region name.

Canonical names follow Antonio et al. (2024), Table 1. 'Philippines' is the national
aggregate; 'NIR' (Negros Island Region, new geographic code only) and 'AONCR' (areas
outside NCR) are kept but are not units of the regional panel.
"""

import re

REGIONS = ["NCR", "CAR", "Ilocos Region", "Cagayan Valley", "Central Luzon", "CALABARZON", "MIMAROPA",
           "Bicol Region", "Western Visayas", "Central Visayas", "Eastern Visayas", "Zamboanga Peninsula",
           "Northern Mindanao", "Davao Region", "SOCCSKSARGEN", "Caraga Region", "BARMM"]

# Ordered patterns; the first that matches wins. Matching is case-insensitive on the
# label with leading dots and spaces removed.
_PATTERNS = [
    (r"^philippines$", "Philippines"),
    (r"^(areas outside|aoncr)", "AONCR"),
    (r"negros island|^nir$", "NIR"),
    (r"national capital|^ncr$|^ncr ", "NCR"),
    (r"cordillera|^car$|^car ", "CAR"),
    (r"bangsamoro|autonomous region|armm|^barmm$", "BARMM"),
    (r"mimaropa|region iv-?b", "MIMAROPA"),
    (r"calabarzon|region iv-?a\b|region 4a", "CALABARZON"),
    (r"caraga|region xiii|region 13", "Caraga Region"),
    (r"soccsksargen|region xii\b|region 12|^reg12", "SOCCSKSARGEN"),
    (r"davao region|region xi\b|region 11", "Davao Region"),
    (r"northern mindanao|region x\b|region 10", "Northern Mindanao"),
    (r"zamboanga peninsula|region ix\b|region 9", "Zamboanga Peninsula"),
    (r"eastern visayas|region viii\b|region 8", "Eastern Visayas"),
    (r"central visayas|region vii\b|region 7", "Central Visayas"),
    (r"western visayas|region vi\b|region 6", "Western Visayas"),
    (r"bicol|region v\b|region 5", "Bicol Region"),
    (r"central luzon|region iii\b|region 3", "Central Luzon"),
    (r"cagayan valley|region ii\b|region 2", "Cagayan Valley"),
    (r"ilocos region|region i\b|region 1", "Ilocos Region"),
]


def canon(label: str) -> str | None:
    if str(label).startswith("...."):  # provinces and cities are indented four dots in PxWeb
        return None
    s = re.sub(r"^[.\s]+", "", str(label)).strip().lower()
    for pat, name in _PATTERNS:
        if re.search(pat, s):
            return name
    return None
