from flask import (Blueprint, Response, flash, g, redirect, render_template,
                   request, url_for)
from werkzeug.exceptions import abort

from bragi.jenkins import JenkinsClient

bp = Blueprint('dashboard', __name__)



@bp.route('/')
def index():
    return render_template('dashboard.html')
