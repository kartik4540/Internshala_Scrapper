This project scrapes internship details from the Internshala website and stores the extracted data into a MySQL database. It includes functions to scrape internship listings and insert them into a database table for further analysis or use.

Features

Scrapes internship details, including title, company, location, stipend, duration, start date, required skills, and more.

Stores the scraped data in a MySQL database table.

Automatically creates the required database table if it doesn't already exist.

Prerequisites

Python: Ensure Python 3.7 or higher is installed on your system.

MySQL: Set up a MySQL server on your local machine or remote server.

Libraries: Install the required Python libraries.

Installation

Clone the Repository

git clone <https://github.com/kartik4540/Internshala_Scrapper.git)>
cd internship-scraper

Install Required Python Libraries

Install the dependencies listed below using pip:

pip install requests pymysql beautifulsoup4

Configuration

Before running the script, update the following configurations in the script:

Database Configuration

Locate the create_and_insert_internship_details function and update the MySQL connection details:

connection = pymysql.connect(
    host='localhost',          # Update with your MySQL host (e.g., localhost or IP address)
    user='root',               # Update with your MySQL username
    password='password',       # Update with your MySQL password
    db='db',                   # Update with your database name
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

Target URL

Update the url variable with the URL of the Internshala internship listing page you want to scrape:

url = "https://internshala.com/internships/work-from-home-internships/"

Running the Script

To run the script, use the following command:

python internship_scraper.py

Output

Database Table: The script will create a table named aainternships in the specified database.

Data: The scraped internship details will be inserted into the table.

Table Schema

The table aainternships will have the following structure:

id: Auto-incrementing primary key.

title: Title of the internship.

company: Company offering the internship.

location: Internship location.

start_date: Start date of the internship.

duration: Duration of the internship.

stipend: Stipend details.

skills_required: Required skills for the internship.

website: Source website (e.g., Internshala).

last_date_to_apply: Last date to apply.

field: Field of the internship (can be updated if needed).

job_type: Job type of the internship (can be updated if needed).

Notes

Ensure you have an active internet connection while running the script to fetch data from the Internshala website.

Verify that your MySQL database server is running and accessible.

If the target website's structure changes, the scraping logic may need updates.

Contributing

Feel free to fork the repository and submit pull requests to improve the script or add features.
