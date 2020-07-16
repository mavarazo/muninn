from flask import (Blueprint, flash, g, redirect, render_template, request,
                   url_for)

from bragi.jenkinsclient import JenkinsClient, Job

jobs = [
    Job('main', 'https://build.internal.adcubum.com/job/syrius3-pipeline/job/master', True, False),
    Job('rel3_10_HEAD', 'https://build.internal.adcubum.com/job/syrius3-pipeline/job/rel3_10_HEAD', True, False),
    Job('rel3_09_HEAD', 'https://build.internal.adcubum.com/job/syrius3-pipeline/job/rel3_09_HEAD', True, False),
]


bp = Blueprint('jenkins', __name__)

@bp.route('/')
def index():
    client = JenkinsClient()
    for job in jobs:
        client.fetch(job)
        job.healthy = client.get_health()
        job.status = client.get_status()

    return render_template('fragments/jenkins_body.html', jobs=jobs)
