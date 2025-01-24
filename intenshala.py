import requests
import pymysql
from bs4 import BeautifulSoup

# Function to scrape internship details
def scrape_internship_details(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        internship_listings = []

        # Find all internship listings
        listings = soup.find_all('div', class_='internship_meta')
        
        # Loop through each listing and extract details
        for listing in listings:
            internship_details = {}

            # Extracting internship title
            title_element = listing.find('div', class_='company')
            if title_element:
                internship_details['title'] = title_element.text.strip()

            # Extracting company name
            company_element = listing.find('a', class_='link_display_like_text')
            if company_element:
                internship_details['company'] = company_element.text.strip()

            # Extracting location
            location_element = listing.find('a', class_='location_link')
            if location_element:
                internship_details['location'] = location_element.text.strip()

            # Extracting start date and duration
            details_items = listing.find_all('div', class_='item_body')
            for item in details_items:
                label = item.find_previous('div', class_='item_heading').text.strip()
                if label == 'Start Date':
                    internship_details['start_date'] = item.text.strip()
                elif label == 'Duration':
                    internship_details['duration'] = item.text.strip()

            # Extracting stipend
            stipend_element = listing.find('i', class_='fa-money')
            if stipend_element:
                internship_details['stipend'] = stipend_element.find_next_sibling('span').text.strip()

            # Extracting skills required
            skills_section = listing.find('div', {'id': 'skillNames'})
            if skills_section:
                skills = [skill.text.strip() for skill in skills_section.find_all('a')]
                internship_details['skills_required'] = ', '.join(skills)

            # Adding website and last_date_to_apply fields
            internship_details['website'] = 'Internshala'
            last_date_to_apply_element = listing.find('div', class_='apply_by')
            if last_date_to_apply_element:
                internship_details['last_date_to_apply'] = last_date_to_apply_element.text.strip()

            # Adding field and job_type fields
            internship_details['field'] = ''  # Add field if available
            internship_details['job_type'] = ''  # Add job_type if available

            internship_listings.append(internship_details)

        return internship_listings

# Function to create a new table and insert internship details into MySQL database
def create_and_insert_internship_details(internship_listings):
    connection = None
    cursor = None
    try:
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='password',
            db='db',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )

        if connection.open:
            print("Connection successful")

        cursor = connection.cursor()

        # Create a new table 'internships' if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS aainternships (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255),
                company VARCHAR(255),
                location VARCHAR(255),
                start_date VARCHAR(50),
                duration VARCHAR(50),
                stipend VARCHAR(50),
                skills_required TEXT,
                website VARCHAR(50),
                last_date_to_apply VARCHAR(50),
                field VARCHAR(50),
                job_type VARCHAR(50)
            )
        """)

        # Insert each internship detail into the 'internships' table
        for internship in internship_listings:
            sql_statement = """
            INSERT INTO aainternships (title, company, location, start_date, duration, stipend, skills_required, website, last_date_to_apply, field, job_type)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql_statement, (
                internship.get('title', ''),
                internship.get('company', ''),
                internship.get('location', ''),
                internship.get('start_date', ''),
                internship.get('duration', ''),
                internship.get('stipend', ''),
                internship.get('skills_required', ''),
                internship.get('website', ''),
                internship.get('last_date_to_apply', ''),
                internship.get('field', ''),
                internship.get('job_type', '')
            ))

        connection.commit()
        print("Data inserted successfully.")

    except pymysql.Error as e:
        print(f"Error during database operation: {e}")

    finally:
        # Safely close the cursor and connection
        if cursor:
            cursor.close()
        if connection:
            connection.close()
        print("Connection closed.")

# URL of the internship listing page
url = "https://internshala.com/internships/work-from-home-internships/"

# Scrape internship details
internship_listings = scrape_internship_details(url)

# Create a new table and insert internship details into MySQL database
create_and_insert_internship_details(internship_listings)
