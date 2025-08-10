from flask import Blueprint, render_template, request
from .scraper import fetch_case_details
from .models import SearchLog
from . import db

main_routes = Blueprint('main', __name__)

@main_routes.route('/')
def index():
    """
    Renders the home page, which contains the search form.
    """
    return render_template('index.html', title='Home')


@main_routes.route('/search', methods=['GET', 'POST'])
def search():
    """
    Handles the search form submission, calls the scraper,
    logs the result, and displays it.
    """
    # This dictionary will hold the data to be displayed on the results page.
    scraped_data = {}

    # Only process the form if the request method is POST.
    if request.method == 'POST':
        # 1. Get user input from the form.
        case_type = request.form.get('case_type')
        case_number = request.form.get('case_number')
        case_year = request.form.get('case_year')

        # 2. Call our scraper function with the user's input.
        scraped_data = fetch_case_details(case_type, case_number, case_year)

        # 3. Log the search and its result to the database.
        log_entry = SearchLog(
            case_type=case_type,
            case_number=case_number,
            case_year=case_year,
            status=scraped_data['status'],
            party_names=scraped_data['party_names'],
            next_hearing_date=scraped_data['next_hearing_date'],
            pdf_link=scraped_data['pdf_link'],
            error_message=scraped_data['error_message']
        )
        db.session.add(log_entry)
        db.session.commit()
        print("--- Search logged to database ---")

    # 4. Render the results page, passing the scraped data to it.
    # The 'data' variable will be available inside the results.html template.
    return render_template('results.html', title='Search Results', data=scraped_data)