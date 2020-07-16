from bragi import db

class JenkinsJob(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    displayname = db.Column(db.String(100), nullable=False) 
    url = db.Column(db.String(255), unique=True, nullable=False)

    def __repr__(self):
        return f'<JenkinsJob {self.displayname} ({self.url})>'


class RadioStation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    displayname = db.Column(db.String(100), nullable=False) 
    url = db.Column(db.String(255), unique=True, nullable=False)

    def __repr__(self):
        return f'<RadioStation {self.displayname} ({self.url})>'


class Feed(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    url = db.Column(db.String(255), unique=True, nullable=False)

    def __repr__(self):
        return f'<FeedEntry {self.url}>'


class FeedEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    guid = db.Column(db.String(255), nullable=False)
    feed_id = db.Column(db.Integer, db.ForeignKey('feed.id'), nullable=False)

    def __repr__(self):
        return f'<FeedEntry {self.feedid}>'