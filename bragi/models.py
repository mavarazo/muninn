from bragi import db

class JenkinsJob(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False) 
    url = db.Column(db.String, unique=True, nullable=False)

    def __repr__(self):
        return f'<JenkinsJob {self.displayname} ({self.url})>'


class RadioStation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False) 
    url = db.Column(db.String, unique=True, nullable=False)

    def __repr__(self):
        return f'<RadioStation {self.displayname} ({self.url})>'


class Feed(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    url = db.Column(db.String, unique=True, nullable=False)
    name = db.Column(db.String)
    icon = db.Column(db.String)
    entries = db.relationship("Entry")

    def unread(self):
        return Entry.query.filter(Entry.feed_id == self.id, Entry.read == False).count()

    def __repr__(self):
        return f'<Feed {self.url}>'


class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    url = db.Column(db.String)
    title = db.Column(db.String)
    guid = db.Column(db.String, unique=True)
    summary = db.Column(db.Text)
    read = db.Column(db.Boolean, default=False)
    starred = db.Column(db.Boolean, default=False)

    feed_id = db.Column(db.Integer, db.ForeignKey('feed.id'), nullable=False)

    def __repr__(self):
        return f'<FeedEntry {self.feedid}>'