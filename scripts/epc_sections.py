import random

PROJECT_OVERVIEW = [
    "The project consists of the construction of a Tier III data center supporting mission-critical operations.",
    "The EPC contractor shall deliver a fully operational facility including civil, mechanical, electrical and commissioning works.",
    "The facility shall comply with Uptime Institute Tier III recommendations.",
    "The project includes utility power integration, UPS systems, cooling systems, and fire protection."
]

COOLING = [
    "The cooling system shall provide N+1 redundancy.",
    "Supply air temperature shall remain between 18°C and 27°C.",
    "CRAH units shall support automatic failover.",
    "Chilled water pumps shall operate with redundant motors.",
    "Cooling equipment shall support SNMP monitoring.",
    "Each cooling unit shall include vibration monitoring sensors.",
    "Cooling redundancy shall be verified during commissioning."
]

ELECTRICAL = [
    "UPS capacity shall be 500 KVA.",
    "Generator backup shall support 72 hours of continuous operation.",
    "Power Distribution Units shall provide branch circuit monitoring.",
    "Electrical panels shall comply with IEC standards.",
    "Emergency shutdown shall disconnect non-critical loads.",
    "Dual power feeds shall be provided for critical equipment."
]

FIRE = [
    "VESDA detection shall be installed.",
    "FM200 suppression shall protect all server rooms.",
    "Fire alarm panels shall integrate with the BMS.",
    "Emergency evacuation procedures shall be displayed.",
    "Smoke detectors shall be installed in all electrical rooms."
]

NETWORK = [
    "Dual fiber entry points shall be provided.",
    "All network racks shall use Cat6A cabling.",
    "Core switches shall support redundant uplinks.",
    "Network monitoring shall integrate with the NOC.",
    "Fiber optic backbone shall use single-mode fiber."
]

COMMISSIONING = [
    "All UPS systems shall pass load testing.",
    "Generator synchronization tests shall be completed.",
    "Cooling performance shall be verified under full load.",
    "Integrated System Testing shall be completed before handover.",
    "Commissioning reports shall include all test results."
]

QUALITY = [
    "All construction activities shall follow QA/QC procedures.",
    "Inspection reports shall be approved before the next activity.",
    "All materials shall comply with project specifications.",
    "Vendor documentation shall be reviewed before installation."
]


SECTIONS = {
    "Project Overview": PROJECT_OVERVIEW,
    "Cooling System": COOLING,
    "Electrical System": ELECTRICAL,
    "Fire Protection": FIRE,
    "Network Infrastructure": NETWORK,
    "Commissioning": COMMISSIONING,
    "Quality Assurance": QUALITY,
}


def generate_section(title, paragraphs=15):
    """Generate one document section."""

    lines = [f"{title}\n"]

    source = SECTIONS[title]

    for _ in range(paragraphs):
        lines.append(random.choice(source))

    return lines