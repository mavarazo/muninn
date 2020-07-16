from flask import (Blueprint, flash, g, redirect, render_template, request,
                   url_for)

from bragi import db
from bragi.models import Feed, FeedEntry

from bragi.feedclient import AtomClient

bp = Blueprint('feed', __name__)

@bp.route('/')
def index():
    feed = Feed.query.filter_by(url='https://www.computerbase.de/rss/news.xml').first()
    if not feed:
        feed = Feed(name='ComputerBase', url='https://www.computerbase.de/rss/news.xml')
        db.session.add(feed)
        db.session.commit()

    feed = AtomClient().fetch(feed.url)
    return render_template('feed.html', feed=feed)
