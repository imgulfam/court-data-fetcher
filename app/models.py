from . import db
from datetime import datetime

class SearchLog(db.Model):
    """
    Represents a log entry for each case search performed by a user.
    """
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # User inputs
    case_type = db.Column(db.String(100), nullable=False)
    case_number = db.Column(db.String(50), nullable=False)
    case_year = db.Column(db.String(10), nullable=False)
    
    # Scraper results
    status = db.Column(db.String(20), nullable=False) # e.g., 'Success', 'Error'
    party_names = db.Column(db.String(500))
    next_hearing_date = db.Column(db.String(50))
    pdf_link = db.Column(db.String(500))
    error_message = db.Column(db.String(500))

    def __repr__(self):
        """
        Provides a developer-friendly string representation of the object.
        """
        return f"<SearchLog {self.id} - {self.case_type} {self.case_number}/{self.case_year}>"