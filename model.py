"""Models and database functions for editor's dashboard."""

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import datetime


db = SQLAlchemy()

##############################################################################
# Model definitions

class DisneyDates(db.Model):
    """important events in disney history by date"""

    __tablename__ = 'disneydates'

    event_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    event_date = db.Column(db.String, nullable=False)
    event_description = db.Column(db.String(2000), nullable=False, unique=True)
    news_type = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return "%s %s" % (
          self.event_date, self.event_description)

    def get_event_by_date(self, date):
        """access event description by date"""

        d = datetime.date.today()
        day = d.day
        month = d.month

##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to the Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///disneydates'
    db.app = app
    db.init_app(app)

if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.
    from server import app
    connect_to_db(app)
    print "Connected to DB."
    db.create_all()
