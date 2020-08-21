from dataclasses import dataclass

from flask import (Blueprint, flash, g, redirect, render_template, request,
                   url_for)

import requests

bp = Blueprint('radio', __name__)

@bp.route('/')
def index():
    return render_template('fragments/radio_body.html', stations=stations)


@dataclass
class Station:
    name: str
    url: str

stations = [
    Station('Virgin Radio Rock Switzerland', 'http://icecast.argovia.ch/vrock'),
]
