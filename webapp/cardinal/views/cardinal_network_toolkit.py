#!/usr/bin/env python3

''' Cardinal - An Open Source Cisco Wireless Access Point Controller

MIT License

Copyright © 2023 Cardinal Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

'''

from cardinal.system.common import jsonResponse

from cardinal.system.common import ToolkitJob
from cardinal.system.common import AsyncOpsManager
from cardinal.system.toolkit import ping
from cardinal.system.toolkit import dig
from cardinal.system.toolkit import traceroute
from cardinal.system.toolkit import curl
from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import session
from flask import url_for
from flask_login import login_required

cardinal_network_toolkit = Blueprint('cardinal_network_toolkit_bp', __name__)
@cardinal_network_toolkit.before_request
@login_required
def before_request():
    pass

# Establish connection to AsyncOpsManager()
job = AsyncOpsManager()

@cardinal_network_toolkit.route("/api/v1/network_toolkit/jobs", methods=["GET"])
def toolkitJobs():
    '''
    Fetch results from network toolkit job.
    '''
    # Initialize a ToolkitJob() object
    job = ToolkitJob()
    jobRecord = job.info()
    return jobRecord

@cardinal_network_toolkit.route("/api/v1/network_toolkit/jobs/<int:id>", methods=["GET"])
def toolkitJobById(id):
    '''
    Fetch results from network toolkit job.
    '''
    # Initialize a ToolkitJob() object
    job = ToolkitJob()
    jobRecord = job.info(id=id)
    if len(jobRecord) == 0:
        return jsonResponse(level="ERROR", message="Network toolkit job with specified id does not exist."), 404
    else:
        return jobRecord

@cardinal_network_toolkit.route("/api/v1/network_toolkit/ping", methods=["POST"])
def doPing():
    hostname = request.form["hostname"]

    # Send ping job to Redis queue
    result = job.run(func=ping, args=dict(hostname=hostname))

    if result._status == 'queued':
        return jsonResponse(level="INFO", message="Toolkit job for ping command has been successfully dispatched", reference=result._id), 201
    else:
        return jsonResponse(level="ERROR", message="Toolkit job for ping command failed", reference=result._status), 409

@cardinal_network_toolkit.route("/api/v1/network_toolkit/traceroute", methods=["POST"])
def doTracert():
    hostname = request.form["hostname"]

    # Send ping job to Redis queue
    result = job.run(func=traceroute, args=dict(hostname=hostname))

    if result._status == 'queued':
        return jsonResponse(level="INFO", message="Toolkit job for traceroute command has been successfully dispatched", reference=result._id), 201
    else:
        return jsonResponse(level="ERROR", message="Toolkit job for traceroute command failed", reference=result._status), 409

@cardinal_network_toolkit.route("/api/v1/network_toolkit/dig", methods=["POST"])
def doDig():
    hostname = request.form["hostname"]

    # Send ping job to Redis queue
    result = job.run(func=dig, args=dict(hostname=hostname))

    if result._status == 'queued':
        return jsonResponse(level="INFO", message="Toolkit job for dig command has been successfully dispatched", reference=result._id), 201
    else:
        return jsonResponse(level="ERROR", message="Toolkit job for dig command failed", reference=result._status), 409

@cardinal_network_toolkit.route("/api/v1/network_toolkit/curl", methods=["POST"])
def doCurl():
    hostname = request.form["hostname"]

    # Send ping job to Redis queue
    result = job.run(func=curl, args=dict(hostname=hostname))

    if result._status == 'queued':
        return jsonResponse(level="INFO", message="Toolkit job for curl command has been successfully dispatched", reference=result._id), 201
    else:
        return jsonResponse(level="ERROR", message="Toolkit job for curl command failed", reference=result._status), 409
