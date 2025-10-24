"""
Configuration for Romania Parliament Scraper
"""

# URLs for official parliament websites
DEPUTIES_BASE_URL = 'https://www.cdep.ro/pls/parlam/'
SENATE_BASE_URL = 'https://www.senat.ro/'

# URL patterns
DEPUTIES_LIST_URL = 'https://www.cdep.ro/pls/parlam/structura.de'
DEPUTIES_BY_COUNTY_URL = 'https://www.cdep.ro/pls/parlam/structura2015.co?idl=1&leg=2020'

# Romanian counties mapping
COUNTIES = {
    '1': 'ALBA',
    '2': 'ARAD',
    '3': 'ARGEȘ',
    '4': 'BACĂU',
    '5': 'BIHOR',
    '6': 'BISTRIȚA-NĂSĂUD',
    '7': 'BOTOȘANI',
    '8': 'BRAȘOV',
    '9': 'BRĂILA',
    '10': 'BUZĂU',
    '11': 'CARAȘ-SEVERIN',
    '12': 'CĂLĂRAȘI',
    '13': 'CLUJ',
    '14': 'CONSTANȚA',
    '15': 'COVASNA',
    '16': 'DÂMBOVIȚA',
    '17': 'DOLJ',
    '18': 'GALAȚI',
    '19': 'GIURGIU',
    '20': 'GORJ',
    '21': 'HARGHITA',
    '22': 'HUNEDOARA',
    '23': 'IALOMIȚA',
    '24': 'IAȘI',
    '25': 'ILFOV',
    '26': 'MARAMUREȘ',
    '27': 'MEHEDINȚI',
    '28': 'MUREȘ',
    '29': 'NEAMȚ',
    '30': 'OLT',
    '31': 'PRAHOVA',
    '32': 'SATU MARE',
    '33': 'SĂLAJ',
    '34': 'SIBIU',
    '35': 'SUCEAVA',
    '36': 'TELEORMAN',
    '37': 'TIMIȘ',
    '38': 'TULCEA',
    '39': 'VASLUI',
    '40': 'VÂLCEA',
    '41': 'VRANCEA',
    '42': 'BUCUREȘTI',
    '43': 'DIASPORA'
}

# Email regex pattern
EMAIL_PATTERN = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

# Phone regex patterns (Romanian format)
PHONE_PATTERNS = [
    r'(\+40|0040)[\s\-]?[237]\d{2}[\s\-]?\d{3}[\s\-]?\d{3}',  # +40 format
    r'0[237]\d{2}[\s\-]?\d{3}[\s\-]?\d{3}',  # 07xx xxx xxx format
]

# Request headers
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Output file
OUTPUT_FILE = 'data/parliament_members.json'
