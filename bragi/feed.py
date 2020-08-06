from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

from flask import (Blueprint, current_app, flash, g, jsonify, redirect,
                   render_template, request, url_for)

from bragi import db
from bragi.feedclient import AtomClient, Channel, Item
from bragi.models import Entry, Feed

bp = Blueprint('feed', __name__)


@dataclass
class Subscription:
    id: int
    channel: Channel


@bp.route('/api/refresh')
def refresh(force:bool=False):
    current_app.logger.info("feed - start refresh")
    feeds = Feed.query.order_by(Feed.name.desc())
    for feed in feeds:
        current_app.logger.info(f"feed - processing {feed.url}")
        channel = AtomClient().fetch(feed.url)

        if not feed.name:
            feed.name = channel.title
        if not feed.icon:
            feed.icon = channel.icon

        for item in channel.items:
            entry = Entry.query.filter(Entry.guid == item.id).first()
            if not entry:
                entry = Entry(url=item.url, title=item.title, guid=item.id, summary=item.summary, feed_id=feed.id)
                db.session.add(entry)
        
        db.session.commit()


@bp.route('/')
def index():
    feeds = Feed.query.order_by(Feed.name.desc())
    id = request.args.get('id')
    return render_template('feed/index.html', feeds=feeds)


@bp.route('/save', methods=['POST'])
def save():
    print(request.form['url'])
    feed = Feed(url=request.form['url'], name=request.form['name'])
    db.session.add(feed)
    db.session.commit()
    refresh()
    return redirect(url_for('feed.index'))
