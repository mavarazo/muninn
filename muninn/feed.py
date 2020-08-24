from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

from flask import (Blueprint, current_app, flash, g, jsonify, redirect,
                   render_template, request, url_for)

from muninn import db
from muninn.feedclient import AtomClient, Channel, Item
from muninn.models import Entry, Feed

from sqlalchemy import or_


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
                entry = Entry(created_on=item.published, updated_on = item.updated, url=item.url, title=item.title, guid=item.id, summary=item.summary, feed_id=feed.id)
                db.session.add(entry)
        
        db.session.commit()
    
    return jsonify(success=True)


@bp.route('/api/entry/read/all', methods=['POST'])
def entry_read_all():
    entries = Entry.query.filter(Entry.read == False).all()
    for entry in entries:
        entry.read = True
 
    db.session.commit()
    return jsonify(success=True)


@bp.route('/api/entry/read', methods=['POST'])
def entry_read():
    id = request.form['entry_id']
    entry = Entry.query.filter(Entry.id == id).one_or_none()
    if not entry:
        return jsonify(success=False)

    entry.read = not entry.read
    db.session.commit()
    return jsonify(success=True)


@bp.route('/api/entry/star', methods=['POST'])
def entry_star():
    id = request.form['entry_id']
    entry = Entry.query.filter(Entry.id == id).one_or_none()
    if not entry:
        return jsonify(success=False)

    entry.starred = not entry.starred
    db.session.commit()
    return jsonify(success=True)


@bp.route('/', methods=['GET', 'POST'])
def index():
    return render_template('feed/index.html', feeds=Feed.query.order_by(Feed.name.desc()), unread=Entry.query.filter(Entry.read == False).count(), starred=Entry.query.filter(Entry.starred == True).count(), entries=get_entries(request))


def get_entries(request:request) -> list:
    if request.method == 'POST':
        search = request.form['search']
        return Entry.query.filter(or_(Entry.title.like(f'%{ search }%'), Entry.summary.like(f'%{ search }%'))).order_by(Entry.created_on.desc())
    else:
        conditions = {}
        id = request.args.get('id')
        if id:
            conditions['feed_id'] = id

        filter = request.args.get('filter')
        if filter and filter == 'unread':
            conditions['read'] = False

        if filter and filter == 'starred':
            conditions['starred'] = True
        
        return Entry.query.filter_by(**conditions).order_by(Entry.created_on.desc())


@bp.route('/save', methods=['POST'])
def save():
    feed = Feed(url=request.form['url'], name=request.form['name'])
    db.session.add(feed)
    db.session.commit()
    refresh()
    return redirect(url_for('feed.index'))
