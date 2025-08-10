# Court-Data Fetcher & Mini-Dashboard

This project is a web application that allows a user to fetch case metadata and the latest orders/judgments for a specific Indian court.

## Features

- Simple web interface to input case details (Case Type, Number, and Year).
- A robust backend scraper built with Python and Playwright.
- Automatically handles the text-based CAPTCHA on the court website.
- Performs a 2-step scrape to first find the "Orders" page and then retrieve the direct document link.
- Logs every query and its result into a local SQLite database.
- Displays the fetched party names, hearing date, and a direct link to the latest order.

## Tech Stack

- **Backend:** Python, Flask
- **Scraping:** Playwright
- **HTML Parsing:** BeautifulSoup
- **Database:** SQLite with Flask-SQLAlchemy
- **Frontend:** HTML, Jinja2 Templating , CSS 

---

## Court Chosen

This application is specifically configured to scrape the **Delhi High Court** public portal:
- URL: `https://delhihighcourt.nic.in/app/get-case-type-status`

---

## Setup and Installation

To run this project locally, please follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone [Your-GitHub-Repo-URL]
    cd court-data-fetcher
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    # For Windows
    python -m venv venv
    .\venv\Scripts\activate

    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Install Playwright's browser binaries:**
    ```bash
    playwright install
    ```

5.  **Run the application:**
    ```bash
    python run.py
    ```

6.  Open your web browser and navigate to `http://127.0.0.1:5000`.

---

## CAPTCHA Strategy

The target website uses a text-based CAPTCHA where the required code is present as plain text within an HTML element on the page.

The circumvention strategy is as follows:
1.  The Playwright scraper loads the page fully, just like a real browser.
2.  It uses a CSS selector (`#captcha-code`) to read the text directly from the CAPTCHA element.
3.  It then uses another selector (`#captchaInput`) to find the input box.
4.  Finally, it fills the input box with the text it read, perfectly replicating a user's action and bypassing the check.

This method is reliable, legal, and does not require any third-party services.


## Project Structure
```bash
court_data_fetcher/
│
├── app/                      # Core application logic
│   ├── __init__.py
│   ├── routes.py             # Flask routes / API endpoints
│   ├── scraper.py            # Playwright logic to fetch court data
│   ├── parser.py             # HTML parsing logic (BeautifulSoup or similar)
│   └── database.py           # SQLite DB models and helper functions
│
├── templates/    
|   └── base.html            # HTML templates (for rendering UI)
│   └── index.html
│   └── result.html
│
├── static/                   # Static assets (CSS)
│   └── style.css              
├── README.md                 # Setup, usage, CAPTCHA strategy
├── requirements.txt          # Python dependencies
└── run.py                    # Entry point for Flask app
```


<img width="525" height="621" alt="image" src="https://github.com/user-attachments/assets/9686c9cb-f399-46dc-8622-e501ebf98332" />
