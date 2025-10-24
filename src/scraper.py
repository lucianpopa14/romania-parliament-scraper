"""
Romania Parliament Members Scraper
Scrapes deputy information from cdep.ro
"""

import requests
from bs4 import BeautifulSoup
import json
import re
import time
from pathlib import Path
import config

class ParliamentScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(config.HEADERS)
        self.members = []
        
    def scrape_deputies_list(self):
        '''Scrape main list of deputies'''
        print('Scraping deputies list...')
        
        try:
            response = self.session.get(config.DEPUTIES_LIST_URL, timeout=10)
            response.raise_for_status()
            response.encoding = 'utf-8'
            
            soup = BeautifulSoup(response.text, 'html5lib')
            
            # Find the table with deputies (adjust selector based on actual structure)
            # This is a placeholder - we'll need to adjust after seeing the actual HTML
            table = soup.find('table')
            
            if not table:
                print('Could not find deputies table')
                return []
            
            rows = table.find_all('tr')[1:]  # Skip header row
            
            for row in rows:
                cols = row.find_all('td')
                if len(cols) >= 3:
                    member = self.parse_deputy_row(cols, row)
                    if member:
                        self.members.append(member)
                        print(f'Added: {member[\"name\"]} from {member[\"county\"]}')
            
            print(f'Total deputies scraped: {len(self.members)}')
            return self.members
            
        except requests.RequestException as e:
            print(f'Error scraping deputies list: {e}')
            return []
    
    def parse_deputy_row(self, cols, row):
        '''Parse individual deputy row'''
        try:
            # Extract name - usually first column with a link
            name_cell = cols[0]
            name_link = name_cell.find('a')
            
            if name_link:
                name = name_link.text.strip()
                profile_url = config.DEPUTIES_BASE_URL + name_link.get('href', '')
            else:
                name = name_cell.text.strip()
                profile_url = None
            
            # Extract county - usually second column
            county = cols[1].text.strip() if len(cols) > 1 else ''
            
            # Extract party - usually third column
            party = cols[2].text.strip() if len(cols) > 2 else ''
            
            member = {
                'name': name,
                'county': county,
                'party': party,
                'chamber': 'Camera Deputaților',
                'profile_url': profile_url,
                'email': None,
                'phone': None,
                'cv_url': None
            }
            
            return member
            
        except Exception as e:
            print(f'Error parsing row: {e}')
            return None
    
    def scrape_member_details(self, member):
        '''Scrape individual member profile for CV and contact info'''
        if not member.get('profile_url'):
            return member
        
        try:
            print(f'Scraping details for {member[\"name\"]}...')
            response = self.session.get(member['profile_url'], timeout=10)
            response.raise_for_status()
            response.encoding = 'utf-8'
            
            soup = BeautifulSoup(response.text, 'html5lib')
            
            # Look for CV link
            cv_links = soup.find_all('a', href=re.compile(r'\.pdf|\.doc|\.docx', re.I))
            if cv_links:
                cv_url = cv_links[0].get('href')
                if not cv_url.startswith('http'):
                    cv_url = config.DEPUTIES_BASE_URL + cv_url
                member['cv_url'] = cv_url
            
            # Look for email in page text
            page_text = soup.get_text()
            emails = re.findall(config.EMAIL_PATTERN, page_text)
            if emails:
                member['email'] = emails[0]
            
            # Look for phone numbers
            for pattern in config.PHONE_PATTERNS:
                phones = re.findall(pattern, page_text)
                if phones:
                    member['phone'] = phones[0]
                    break
            
            time.sleep(1)  # Be polite, don't hammer the server
            
        except Exception as e:
            print(f'Error scraping details for {member[\"name\"]}: {e}')
        
        return member
    
    def extract_email_from_cv(self, cv_url):
        '''Download and extract email from CV PDF/DOC'''
        # TODO: Implement CV downloading and parsing
        # This would use PyPDF2 or pdfplumber for PDFs
        # and python-docx for Word documents
        pass
    
    def save_to_json(self, filename=None):
        '''Save scraped data to JSON file'''
        if filename is None:
            filename = config.OUTPUT_FILE
        
        # Ensure data directory exists
        Path('data').mkdir(exist_ok=True)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.members, f, ensure_ascii=False, indent=2)
        
        print(f'Data saved to {filename}')
        print(f'Total members: {len(self.members)}')
    
    def run(self, scrape_details=False):
        '''Main scraper execution'''
        print('=== Romania Parliament Scraper ===')
        print()
        
        # Scrape main list
        self.scrape_deputies_list()
        
        # Optionally scrape individual profiles
        if scrape_details and self.members:
            print()
            print('Scraping individual member details...')
            for i, member in enumerate(self.members):
                print(f'[{i+1}/{len(self.members)}]', end=' ')
                self.scrape_member_details(member)
        
        # Save results
        self.save_to_json()
        print()
        print('=== Scraping Complete ===')

def main():
    scraper = ParliamentScraper()
    
    # Run scraper (set scrape_details=True to get emails/phones)
    # Start with False to test basic scraping first
    scraper.run(scrape_details=False)

if __name__ == '__main__':
    main()
