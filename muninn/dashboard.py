from flask import (Blueprint, Response, flash, g, redirect, render_template,
                   request, url_for)
from werkzeug.exceptions import abort

from muninn.jenkins import JenkinsClient
from muninn.models import Feed

bp = Blueprint('dashboard', __name__)


@bp.route('/')
def index():
    return render_template('dashboard.html')
