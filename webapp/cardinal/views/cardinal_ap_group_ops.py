#!/usr/bin/env python3

''' Cardinal - An Open Source Cisco Wireless Access Point Controller

MIT License

Copyright © 2019 Cardinal Contributors

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

import time
#from cardinal.system.common import apGroupIterator
from cardinal.system.common import printCompletionTime
#from cardinal.system.common import cipherSuite
#from cardinal.system.common import processor

from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import session
from flask import url_for
from flask_login import login_required
from scout import sys

cardinal_ap_group_ops = Blueprint('cardinal_ap_group_ops_bp', __name__)
@cardinal_ap_group_ops.before_request
@login_required
def before_request():
    pass

@cardinal_ap_group_ops.route("/get-ap-group-tftp-backup", methods=["GET", "POST"])
def configApTftpBackup():
    if request.method == 'GET':
        status = request.args.get('status')
        completionTime = request.args.get('completionTime')
        return render_template("config-ap-group-tftp-backup.html", status=status, completionTime=completionTime)

    elif request.method == 'POST':
        apGroupId = session.get("apGroupId")
        apGroupName = session.get("apGroupName")
        if apGroupId is None:
            apGroupId = request.form["ap_group_id"]
        tftpIp = request.form["tftp_ip"]
        apList = apGroupIterator(apGroupId=apGroupId, tftpIp=tftpIp)
        startTime = time.time()
        task = processor(operation=sys.scoutTftpBackup, apInfo=apList)
        endTime = time.time() - startTime
        status = "INFO: Config Backup for AP Group {} Successfully Initiated!".format(apGroupName)
        completionTime = printCompletionTime(endTime)
        return redirect(url_for('cardinal_ap_group_ops_bp.configApTftpBackup', status=status, completionTime=completionTime))

@cardinal_ap_group_ops.route("/config-ap-group-http", methods=["GET"])
@login_required
def configApHttp():
    completionTime = request.args.get('completionTime')
    status = request.args.get('status')
    return render_template("config-ap-group-http.html", status=status, completionTime=completionTime)

@cardinal_ap_group_ops.route("/enable-ap-group-http", methods=["POST"])
@login_required
def enableApHttp():
    apGroupId = session.get('apGroupId')
    apGroupName = session.get('apGroupName')
    if apGroupId is None:
        apGroupId = request.form["ap_group_id"]
    apList = apGroupIterator(apGroupId=apGroupId)
    startTime = time.time()
    task = processor(operation=sys.scoutEnableHttp, apInfo=apList)
    endTime = time.time() - startTime
    status = "INFO: HTTP Server for AP Group {} Successfully Enabled!".format(apGroupName)
    completionTime = printCompletionTime(endTime)
    return redirect(url_for('cardinal_ap_group_ops_bp.configApHttp', status=status, completionTime=completionTime))

@cardinal_ap_group_ops.route("/disable-ap-group-http", methods=["POST"])
@login_required
def disableApHttp():
    apGroupId = session.get('apGroupId')
    apGroupName = session.get('apGroupName')
    if apGroupId is None:
        apGroupId = request.form["ap_group_id"]
    apList = apGroupIterator(apGroupId=apGroupId)
    startTime = time.time()
    task = processor(operation=sys.scoutDisableHttp, apInfo=apList)
    endTime = time.time() - startTime
    status = "INFO: HTTP Server for AP Group {} Successfully Disabled!".format(apGroupName)
    completionTime = printCompletionTime(endTime)
    return redirect(url_for('cardinal_ap_group_ops_bp.configApHttp', status=status, completionTime=completionTime))

@cardinal_ap_group_ops.route("/config-ap-group-snmp", methods=["GET"])
@login_required
def configApSnmp():
    completionTime = request.args.get('completionTime')
    status = request.args.get('status')
    return render_template("config-ap-group-snmp.html", status=status, completionTime=completionTime)

@cardinal_ap_group_ops.route("/enable-ap-group-snmp", methods=["POST"])
@login_required
def enableApSnmp():
    apGroupId = session.get('apGroupId')
    apGroupName = session.get('apGroupName')
    if apGroupId is None:
        apGroupId = request.form["ap_group_id"]
    apList = apGroupIterator(apGroupId=apGroupId, snmp="True")
    startTime = time.time()
    task = processor(operation=sys.scoutEnableSnmp, apInfo=apList)
    endTime = time.time() - startTime
    status = "INFO: SNMP Server for AP Group {} Successfully Enabled!".format(apGroupName)
    completionTime = printCompletionTime(endTime)
    return redirect(url_for('cardinal_ap_group_ops_bp.configApSnmp', status=status, completionTime=completionTime))

@cardinal_ap_group_ops.route("/disable-ap-group-snmp", methods=["POST"])
@login_required
def disableApSnmp():
    apGroupId = session.get('apGroupId')
    apGroupName = session.get('apGroupName')
    if apGroupId is None:
        apGroupId = request.form["ap_group_id"]
    apList = apGroupIterator(apGroupId=apGroupId)
    startTime = time.time()
    task = processor(operation=sys.scoutDisableSnmp, apInfo=apList)
    endTime = time.time() - startTime
    status = "INFO: SNMP Server for AP Group {} Successfully Disabled!".format(apGroupName)
    completionTime = printCompletionTime(endTime)
    return redirect(url_for('cardinal_ap_group_ops_bp.configApSnmp', status=status, completionTime=completionTime))
