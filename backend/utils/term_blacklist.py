# Term filtering for pharmaceutical CV analysis
# Organized blacklists to exclude obvious non-pharmaceutical terms

import re

# Compiled regex patterns for performance
MOSTLY_SPECIAL_CHARS = re.compile(r'^[^a-zA-Z0-9]*$|^[^a-zA-Z0-9]+[a-zA-Z0-9]*[^a-zA-Z0-9]+$')
FORMATTING_ARTIFACTS = re.compile(r'[\u200b\u00a0\u2000-\u200f\u2028-\u202f●•▪▫○◦■□▲△▼▽]+')  # Zero-width spaces, bullets, etc.

# Medical/Academic credentials and degrees
CREDENTIALS = {
    "MD", "MBA", "MSc", "PhD", "FACP", "FACOG", "FACS", "FACC", "FAHA",
    "FAAN", "FCCP", "FRCPC", "FRCP", "MRCP", "BSc", "BA", "BS", "MS",
    "MA", "MPH", "PharmD", "DDS", "DMD", "DO", "DPM", "OD", "PharmD"
}

# Generic business and organizational terms
BUSINESS_TERMS = {
    "development", "implementation", "processes", "strategy", "management",
    "collaboration", "operations", "execution", "organization", "restructured",
    "corporate", "commercial", "strategy", "decision", "making", "decisions",
    "leadership", "team", "teams", "project", "projects", "program", "programs",
    "portfolio", "budget", "budgets", "revenue", "profit", "cost", "costs",
    "business", "market", "marketing", "sales", "customer", "customers",
    "client", "clients", "vendor", "vendors", "supplier", "suppliers",
    "contract", "contracts", "agreement", "agreements", "partnership",
    "partnerships", "acquisition", "acquisitions", "merger", "mergers"
}

# Document structure and organizational terms
STRUCTURAL_TERMS = {
    "Board", "Directors", "Director", "company", "Company", "organization",
    "Organization", "department", "Department", "division", "Division",
    "institute", "Institute", "center", "Center", "university", "University",
    "college", "College", "hospital", "Hospital", "clinic", "Clinic",
    "foundation", "Foundation", "society", "Society", "association", "Association",
    "committee", "Committee", "board", "asset", "assets", "entity", "entities",
    "group", "Group", "unit", "Unit", "section", "Section"
}

# Symbols, formatting artifacts, and non-meaningful terms
SYMBOLS_AND_FORMATTING = {
    "●", "•", "▪", "▫", "○", "◦", "■", "□", "▲", "△", "▼", "▽",
    "\u200b", "\u00a0", "\t", "\n", "\r",
    "VC/PE", "VC", "PE", "LLC", "Inc", "Corp", "Ltd", "Co",
    "multiple", "various", "several", "many", "some", "all", "each",
    "including", "such", "like", "as", "than", "more", "less", "most"
}

# Job titles and roles
JOB_TITLES = {
    "CEO", "CTO", "CFO", "COO", "CMO", "VP", "SVP", "EVP", "President",
    "Manager", "Senior", "Junior", "Lead", "Principal", "Associate",
    "Assistant", "Coordinator", "Specialist", "Analyst", "Consultant",
    "Advisor", "Expert", "Scientist", "Researcher", "Investigator",
    "Fellow", "Intern", "Trainee", "Student", "Professor", "Doctor"
}

def clean_text(text: str) -> str:
    """
    Remove formatting artifacts from text.

    Args:
        text: The text to clean

    Returns:
        Cleaned text with formatting artifacts removed
    """
    if not text:
        return ""

    # Remove formatting artifacts
    cleaned = FORMATTING_ARTIFACTS.sub('', text)

    # Remove extra whitespace
    cleaned = ' '.join(cleaned.split())

    return cleaned.strip()

def should_exclude_term(term: str):
    if not term or not term.strip():
        return True

    term_clean = clean_text(term)

    # Check against all blacklists
    if (term_clean in CREDENTIALS or
        term_clean in BUSINESS_TERMS or
        term_clean in STRUCTURAL_TERMS or
        term_clean in SYMBOLS_AND_FORMATTING or
        term_clean in JOB_TITLES):
        return True

    # Filter out very short terms (1-2 characters) unless they could be chemical symbols
    if len(term_clean) <= 2:
        # Keep potential chemical elements/compounds (uppercase)
        if term_clean.isupper() and term_clean.isalpha():
            return False
        else:
            return True

    # Filter out terms that are mostly special characters
    if MOSTLY_SPECIAL_CHARS.match(term_clean):
        return True

    return False
