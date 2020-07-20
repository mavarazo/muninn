from flask import (Blueprint, flash, g, redirect, render_template, request,
                   url_for, jsonify)

from bragi import db
from bragi.models import Feed, FeedEntry

from bragi.feedclient import AtomClient

bp = Blueprint('feed', __name__)


@bp.route('/api/')
def api_all():
    return jsonify(render_template('fragments/feed_nav.html', feeds=Feed.query.all()))

@bp.route('/')
def index():
    feed = Feed.query.filter_by(id=request.args.get('id')).first()
    if not feed:
        feed = Feed(name='ComputerBase', url='https://www.computerbase.de/rss/news.xml')
        db.session.add(feed)
        db.session.commit()

    feed = AtomClient().fetch(feed.url)
    return render_template('feed.html', feed=feed)
