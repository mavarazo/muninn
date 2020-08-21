from flask import (Blueprint, current_app, flash, g, redirect, render_template,
                   request, url_for)

from muninn.sonarqubeclient import Application, Portfolio, SonarQubeClient

portfolios = [
    Portfolio('Fachteam Bestand KVA', 'https://build.internal.adcubum.com/job/syrius3-pipeline/job/master', [Application('SYRIUS-bestand-firmenkunden-modul')])
]

bp = Blueprint('sonarqube', __name__)

@bp.route('/')
def index():
    client = SonarQubeClient(current_app.logger, current_app.config['SONARQUBE_TOKEN'], current_app.config['SONARQUBE_URL_COMPONENT'])
    for portfolio in portfolios:
        client.fetch(portfolio)
    return render_template('fragments/sonarqube_body.html', portfolios=portfolios)


@bp.context_processor
def utility_processor():
    def format_minutes_to_workingdays(value):
        return u'{0:.0f} d'.format(value / 60 / 8)
    def format_to_percentage(value):
        return u'{0:.2f} %'.format(value)

    return dict(
        format_minutes_to_workingdays=format_minutes_to_workingdays,
        format_to_percentage=format_to_percentage)
