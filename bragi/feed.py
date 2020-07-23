from dataclasses import dataclass, field
from typing import List, Optional

from flask import (Blueprint, flash, g, jsonify, redirect, render_template,
                   request, url_for)

from bragi import db
from bragi.feedclient import AtomClient, AtomFeed, AtomEntry
from bragi.models import Feed, FeedEntry

bp = Blueprint('feed', __name__)


@dataclass
class Subscription:
    id: int
    feed: AtomFeed


@bp.route('/')
def index():
    feeds = Feed.query.order_by(Feed.name.desc())
    id = request.args.get('id')
    subscriptions = []
    inbox = []
    for feed in feeds:
        response = AtomClient().fetch(feed.url)
        subscription = Subscription(feed.id, response)
        subscriptions.append(subscription)
        if not id or feed.id == id:
            inbox.extend(response.entries)

    inbox.sort(key=lambda r: r.published, reverse=True)
    return render_template('feed/index.html', subscriptions=subscriptions, inbox=inbox)
