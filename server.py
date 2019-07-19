from jinja2 import StrictUndefined
from flask import Flask, request, render_template, session, jsonify
from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream
from sqlalchemy import select, func
import requests
import datetime
import word_freq
from model import db, connect_to_db, DisneyDates
try:
    import json
except ImportError:
    import simplejson as json

app = Flask(__name__)
app.secret_key = "dashboard"
app.jinja_env.undefined = StrictUndefined

timestamp = datetime.datetime.utcnow()
tstring = timestamp.strftime("%B %d")

@app.route("/")
def show_main_navigation_page():
    """display the main navigation page."""
    events = db.session.query(DisneyDates.event_description).filter(DisneyDates.event_date == tstring).all()

    return render_template("main-navigation.html", tstring=tstring, events=events)

def show_newswhip_trends():
    """display the list of newswhip trends."""

    newswhip = requests.get("https://api.newswhip.com/v1/region/U.S./All/1?key=3EK3EBjccXUbz")
    trend_dict = newswhip.json()

    news_trends = trend_dict['articles']
    return news_trends

def show_twitter_trends():
    """display the list of twitter trends."""
    ACCESS_TOKEN = ''
    ACCESS_SECRET = ''
    CONSUMER_KEY = ''
    CONSUMER_SECRET = ''

    oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

    twitter = Twitter(auth=oauth)
    us_trends = twitter.trends.place(_id = 23424977)
    top50 = us_trends[0]['trends']
    return top50

@app.route("/dashboard")
def show_dashboard():
    """show dash"""
    top50 = show_twitter_trends()
    get_news_trends = show_newswhip_trends()

    return render_template("dashboard.html", timestamp=timestamp, get_news_trends=get_news_trends, tstring=tstring, top50=top50)

@app.route("/blog-data.json")
def show_blog_chart():
    """show chart of blog stats."""

    data_points = {
        "labels": ["May 11", "May 12", "May 13", "May 14", "May 15", "May 16", "May 17"],
        "datasets": [
            {
                "label": "Pageviews",
                "fillColor": "rgba(27, 70, 222, 0)",
                "strokeColor": "rgba(27, 70, 222, 0.84)",
                "pointColor": "rgba(27, 70, 222, 0.84)",
                "pointStrokeColor": "#fff",
                "pointHighlightFill": "#fff",
                "pointHighlightStroke": "rgba(27, 70, 222, 0.84)",
                "data": [961577, 717138, 821046, 731375, 582673, 703544, 503072]
            },
            {
                "label": "Visits",
                "fillColor": "rgba(62, 159, 131, 0.2);",
                "strokeColor": "rgba(62, 159, 131, 0.9);",
                "pointColor": "rgba(62, 159, 131, 0.9);",
                "pointStrokeColor": "#fff",
                "pointHighlightFill": "#fff",
                "pointHighlightStroke": "rgba(62, 159, 131, 0.9);",
                "data": [406341, 317480, 376997, 292010, 244621, 355994, 235562]

            },

            {
                "label": "Unique Visitors",
                "fillColor": "rgba(238, 228, 89, 0)",
                "strokeColor": "rgba(238, 228, 89, 1)",
                "pointColor": "rgba(238, 228, 89, 1)",
                "pointStrokeColor": "#fff",
                "pointHighlightFill": "#fff",
                "pointHighlightStroke": "rgba(238, 228, 89, 1)",
                "data": [386042, 296337, 353492, 272697, 230537, 336492, 225455]

            },

            {
                "label": "M/M Average Pageviews",
                "fillColor": "rgba(3, 165, 206, 0)",
                "strokeColor": "rgba(3, 165, 206, 1)",
                "pointColor": "rgba(3, 165, 206, 1)",
                "pointStrokeColor": "#fff",
                "pointHighlightFill": "#fff",
                "pointHighlightStroke": "rgba(3, 165, 206, 1)",
                "data": [714793, 714793, 714793, 714793, 714793, 714793, 714793]
            },

            {
                "label": "M/M Average Visits",
                "fillColor": "rgba(62, 159, 131, 0.2);",
                "strokeColor": "rgba(62, 159, 131, 0.3);",
                "pointColor": "rgba(62, 159, 131, 0.3);",
                "pointStrokeColor": "#fff",
                "pointHighlightFill": "#fff",
                "pointHighlightStroke": "rgba(62, 159, 131, 0.3);",
                "data": [303997, 303997, 303997, 303997, 303997, 303997, 303997]
            },

            {
                "label": "M/M Average Unique Visitors",
                "fillColor": "rgba(238, 156, 89, 0)",
                "strokeColor": "rgba(238, 156, 89, 1)",
                "pointColor": "rgba(238, 156, 89, 1)",
                "pointStrokeColor": "#fff",
                "pointHighlightFill": "#fff",
                "pointHighlightStroke": "rgba(238, 156, 89, 1)",
                "data": [185733, 185733, 185733, 185733, 185733, 185733, 185733]
            }
        ]

    }
    return jsonify(data_points)


@app.route("/prompt-generator")
def show_prompt_generator():
    """create writing prompt."""

    all_trends = []
    news_trends = show_newswhip_trends()
    for item in news_trends:
        all_trends.append(item['headline'])
    twitter_trends = show_twitter_trends()
    for item in twitter_trends:
        all_trends.append(item['name'])

    trend_string = ' '.join(all_trends).lower()
    trends_data = trend_string.encode('utf-8')

    with open('disneyheadlines.txt', 'r') as myfile:
        data=myfile.read().lower().replace('\n', ' ')
        encoded = data.encode('utf-8')
    data = encoded + trends_data
    wordlist = word_freq.remove_punctuation(data)
    list_without_stops = word_freq.remove_stopwords(wordlist, word_freq.stopwords)
    frequency_dict = word_freq.wordlist_to_freqdict(list_without_stops)
    sorted_dict = word_freq.sort_freqdict(frequency_dict)

    tuple1 = sorted_dict[1]
    keyword_1 = tuple1[1]

    tuple2 = sorted_dict[2]
    keyword_2 = tuple2[1]

    tuple3 = sorted_dict[3]
    keyword_3 = tuple3[1]

    tuple4 = sorted_dict[4]
    keyword_4 = tuple4[1]

    tuple5 = sorted_dict[5]
    keyword_5 = tuple5[1]

    tuple6 = sorted_dict[6]
    keyword_6 = tuple6[1]

    return render_template("prompt-generator.html", keyword_1=keyword_1, keyword_2=keyword_2, 
                            keyword_3=keyword_3, keyword_4=keyword_4, keyword_5=keyword_5, 
                            keyword_6=keyword_6)

if __name__ == "__main__":
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    # DebugToolbarExtension(app)

    app.run()