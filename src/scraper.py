"""
Romania Parliament Members Scraper
Scrapes deputy and senator information from cdep.ro and senat.ro
"""

import requests
from bs4 import BeautifulSoup
import json
import re
import time
from pathlib import Path
import sys
sys.path.insert(0, 'src')
import config

class ParliamentScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(config.HEADERS)
        self.members = []
        
    def scrape_deputies(self):
        '''Scrape deputies from Camera Deputaților'''
        print('=' * 60)
        print('Scraping deputies from Camera Deputaților...')
        print('=' * 60)
        
        try:
            url = 'https://www.cdep.ro/pls/parlam/structura2015.de?leg=2024'
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            response.encoding = 'utf-8'
            
            soup = BeautifulSoup(response.text, 'html5lib')
            
            # Find all deputy links - they have mp? in the URL
            deputy_links = soup.find_all('a', href=re.compile(r'structura2015\.mp\?'))
            
            print(f'Found {len(deputy_links)} deputy links')
            
            for link in deputy_links:
                name = link.text.strip()
                if name:  # Skip empty links
                    profile_url = 'https://www.cdep.ro/pls/parlam/' + link.get('href', '')
                    
                    # Try to get more info from the row
                    row = link.find_parent('tr')
                    county = ''
                    party = ''
                    
                    if row:
                        cells = row.find_all('td')
                        if len(cells) >= 2:
                            county = cells[1].text.strip()
                        if len(cells) >= 3:
                            party = cells[2].text.strip()
                    
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
                    
                    self.members.append(member)
                    print(f'  Added: {name}')
            
            print(f'\nTotal deputies: {len([m for m in self.members if m["chamber"] == "Camera Deputaților"])}')
            return True
            
        except Exception as e:
            print(f'Error scraping deputies: {e}')
            import traceback
            traceback.print_exc()
            return False
    
    def scrape_senators(self):
        '''Scrape senators from Senat'''
        print('\n' + '=' * 60)
        print('Scraping senators from Senat...')
        print('=' * 60)
        
        try:
            url = 'https://www.senat.ro/FisaSenatori.aspx'
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            response.encoding = 'utf-8'
            
            soup = BeautifulSoup(response.text, 'html5lib')
            
            # Find all senator links - they have FisaSenator.aspx in the URL
            senator_links = soup.find_all('a', href=re.compile(r'FisaSenator\.aspx\?ParlamentarID='))
            
            print(f'Found {len(senator_links)} senator links')
            
            for link in senator_links:
                name = link.text.strip()
                if name:  # Skip empty links
                    profile_url = 'https://www.senat.ro/' + link.get('href', '')
                    
                    # Try to extract info from the surrounding text
                    parent = link.find_parent()
                    text = parent.get_text() if parent else ''
                    
                    # Extract county and party from text
                    county = ''
                    party = ''
                    
                    # Look for "Circumscripția electorală" pattern
                    county_match = re.search(r'Circumscripţia electorală nr\.(\d+)\s+([^\n]+)', text)
                    if county_match:
                        county_num = county_match.group(1)
                        county_name = county_match.group(2).strip()
                        county = f'{county_name}'
                    
                    # Look for "Grupul parlamentar" pattern
                    party_match = re.search(r'Grupul parlamentar\s+([^\n]+)', text)
                    if party_match:
                        party = party_match.group(1).strip()
                    
                    member = {
                        'name': name,
                        'county': county,
                        'party': party,
                        'chamber': 'Senat',
                        'profile_url': profile_url,
                        'email': None,
                        'phone': None,
                        'cv_url': None
                    }
                    
                    self.members.append(member)
                    print(f'  Added: {name}')
            
            print(f'\nTotal senators: {len([m for m in self.members if m["chamber"] == "Senat"])}')
            return True
            
        except Exception as e:
            print(f'Error scraping senators: {e}')
            import traceback
            traceback.print_exc()
            return False
    
    def scrape_member_details(self, member):
        '''Scrape individual member profile for email and CV'''
        if not member.get('profile_url'):
            return member
        
        try:
            print(f'  Scraping details for {member["name"]}...', end=' ')
            response = self.session.get(member['profile_url'], timeout=10)
            response.raise_for_status()
            response.encoding = 'utf-8'
            
            soup = BeautifulSoup(response.text, 'html5lib')
            page_text = soup.get_text()
            
            # Look for email in page text
            emails = re.findall(config.EMAIL_PATTERN, page_text)
            if emails:
                # Filter out common false positives
                valid_emails = [e for e in emails if '@cdep.ro' in e or '@senat.ro' in e or '@parlament.ro' in e]
                if valid_emails:
                    member['email'] = valid_emails[0]
                    print(f'Email: {member["email"]}', end=' ')
            
            # Look for phone numbers
            for pattern in config.PHONE_PATTERNS:
                phones = re.findall(pattern, page_text)
                if phones:
                    member['phone'] = phones[0] if isinstance(phones[0], str) else phones[0][0]
                    print(f'Phone: {member["phone"]}', end=' ')
                    break
            
            # Look for CV link
            cv_links = soup.find_all('a', href=re.compile(r'\.(pdf|doc|docx)$', re.I))
            if not cv_links:
                # Try finding CV in text
                cv_links = soup.find_all('a', string=re.compile(r'CV|curriculum', re.I))
            
            if cv_links:
                cv_href = cv_links[0].get('href', '')
                if cv_href:
                    if not cv_href.startswith('http'):
                        base_url = 'https://www.cdep.ro/pls/parlam/' if 'cdep.ro' in member['profile_url'] else 'https://www.senat.ro/'
                        cv_href = base_url + cv_href
                    member['cv_url'] = cv_href
                    print(f'CV found', end=' ')
            
            print('✓')
            time.sleep(0.5)  # Be polite to the server
            
        except Exception as e:
            print(f'Error: {e}')
        
        return member
    
    def save_to_json(self, filename=None):
        '''Save scraped data to JSON file'''
        if filename is None:
            filename = config.OUTPUT_FILE
        
        # Ensure data directory exists
        Path('data').mkdir(exist_ok=True)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.members, f, ensure_ascii=False, indent=2)
        
        print(f'\n' + '=' * 60)
        print(f'Data saved to {filename}')
        print(f'Total members: {len(self.members)}')
        deputies = len([m for m in self.members if m["chamber"] == "Camera Deputaților"])
        senators = len([m for m in self.members if m["chamber"] == "Senat"])
        print(f'  - Deputies: {deputies}')
        print(f'  - Senators: {senators}')
        with_email = len([m for m in self.members if m.get("email")])
        print(f'  - With email: {with_email}')
        print('=' * 60)
    
    def run(self, scrape_details=False, chamber='both'):
        '''Main scraper execution'''
        print('\n' + '=' * 60)
        print('ROMANIA PARLIAMENT SCRAPER')
        print('=' * 60 + '\n')
        
        # Scrape deputies
        if chamber in ['both', 'deputies']:
            self.scrape_deputies()
        
        # Scrape senators
        if chamber in ['both', 'senators']:
            self.scrape_senators()
        
        # Optionally scrape individual profiles
        if scrape_details and self.members:
            print('\n' + '=' * 60)
            print('Scraping individual member details...')
            print('=' * 60)
            for i, member in enumerate(self.members):
                print(f'[{i+1}/{len(self.members)}]', end=' ')
                self.scrape_member_details(member)
        
        # Save results
        self.save_to_json()
        print('\n✓ Scraping Complete!\n')

def main():
    scraper = ParliamentScraper()
    
    # Run scraper
    # Set scrape_details=True to get emails/phones from individual pages
    # Set chamber to 'deputies', 'senators', or 'both'
    scraper.run(scrape_details=False, chamber='both')

if __name__ == '____main__':
    main()
