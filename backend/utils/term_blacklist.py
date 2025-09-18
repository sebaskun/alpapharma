import re

# Compiled regex patterns for performance
MOSTLY_SPECIAL_CHARS = re.compile(r'^[^a-zA-Z0-9]*$|^[^a-zA-Z0-9]+[a-zA-Z0-9]*[^a-zA-Z0-9]+$')
FORMATTING_ARTIFACTS = re.compile(r'[\u200b\u00a0\u2000-\u200f\u2028-\u202f●•▪▫○◦■□▲△▼▽]+')  # Zero-width spaces, bullets, etc.

# Study codes and clinical trial patterns
STUDY_CODE_PATTERN = re.compile(r'^(NCT\d+|[A-Z]\d+[A-Z]-[A-Z]{2,3}-[A-Z]{4,6}|[A-Z]{2,3}\d+|US-\d+-[A-Z]\d+|\d{4}–\d{4})$')
DATE_PATTERN = re.compile(r'^\d{1,2}/\d{4}$|^\d{4}–\d{4}$|^\d{1,2}/\d{1,2}/\d{4}$')

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
    "Fellow", "Intern", "Trainee", "Student", "Professor", "Doctor",
    "Independent", "Member", "Inventor", "Instructor", "Clinical"
}

# CV section headers
CV_SECTIONS = {
    "POSITIONS", "HIGHLIGHTS", "EDUCATION", "CERTIFICATIONS", "LICENSURE",
    "PUBLICATIONS", "EXPERIENCE", "BACKGROUND", "SUMMARY", "OBJECTIVE",
    "SKILLS", "ACHIEVEMENTS", "AWARDS", "REFERENCES", "CONTACT"
}

# Date and time related terms
DATE_TERMS = {
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
    "Present", "Current", "Ongoing", "Active", "Expired"
}

# Common CV words and document structure
COMMON_CV_WORDS = {
    "Page", "Title", "Report", "Case", "Study", "Treatment", "Where",
    "including", "design", "concept", "implementation", "publication",
    "choice", "method", "focus", "expression", "combination", "standard",
    "care", "safety", "efficacy", "subjects", "patients", "participants",
    "advanced", "metastatic", "stage", "cohort", "versus", "placebo"
}

# US State abbreviations
US_STATES = {
    "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "ID",
    "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS",
    "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK",
    "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV",
    "WI", "WY"
}

# Common country codes and geographic terms
GEOGRAPHIC_TERMS = {
    "US", "USA", "UK", "EU", "NATO", "UN", "NYC", "LA", "DC",
    "China", "Japan", "Maryland", "Miami", "Boston", "California", "Texas",
    "Europe", "Asia", "New", "Florida", "Illinois", "Virginia", "Ohio"
}

# Pharmaceutical company names
PHARMA_COMPANIES = {
    "GSK", "AstraZeneca", "AbbVie", "Celgene", "Pfizer", "Merck", "Novartis",
    "Roche", "Sanofi", "Bayer", "Apexigen", "Arcus", "Acerta", "Innate",
    "Taiho", "Amgen", "Genentech", "Biogen", "Pharmaceuticals"
}

# Academic and publication terms
ACADEMIC_TERMS = {
    "Publication", "Award", "Patent", "Patents", "PUBLICATION", "PRESENTATIONS",
    "Abstract", "Poster", "Conference", "Journal", "Article", "Paper", "Review"
}

# Organization abbreviations
ORGANIZATION_ABBREVS = {
    "NIH", "NCI", "FDA", "EMA", "WHO", "CDC", "ASCO", "AACR", "ESMO", "AAAS"
}

def clean_text(text: str) -> str:
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
        term_clean in JOB_TITLES or
        term_clean in CV_SECTIONS or
        term_clean in DATE_TERMS or
        term_clean in COMMON_CV_WORDS or
        term_clean in US_STATES or
        term_clean in GEOGRAPHIC_TERMS or
        term_clean in PHARMA_COMPANIES or
        term_clean in ACADEMIC_TERMS or
        term_clean in ORGANIZATION_ABBREVS):
        return True

    # Filter out study codes and clinical trial patterns
    if STUDY_CODE_PATTERN.match(term_clean):
        return True

    # Filter out date patterns
    if DATE_PATTERN.match(term_clean):
        return True

    # Filter out very short terms (1-2 characters) unless they could be chemical symbols
    if len(term_clean) <= 2:
        # Now that we've filtered out states/countries above,
        # keep potential chemical elements/compounds (uppercase)
        if term_clean.isupper() and term_clean.isalpha():
            return False
        else:
            return True

    # Filter out terms that are mostly special characters
    if MOSTLY_SPECIAL_CHARS.match(term_clean):
        return True

    return False
