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

from cardinal.system.accesspoints import AccessPoint
from cardinal.system.accesspoints import AccessPointGroup
from cardinal.system.common import msgAuthFailed
from cardinal.system.common import msgSpecifyValidAp
from cardinal.system.common import msgSpecifyValidApGroup
from cardinal.system.accesspoints import Ssid24Ghz
from cardinal.system.accesspoints import Ssid24GhzRadius
from cardinal.system.accesspoints import Ssid5Ghz
from cardinal.system.accesspoints import Ssid5GhzRadius
from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import session
from flask import url_for
from flask_login import login_required

cardinal_forms = Blueprint('cardinal_forms_bp', __name__)
@cardinal_forms.before_request
@login_required
def before_request():
    pass

# Add Access Point Form

@cardinal_forms.route("/forms/add-ap", methods=["GET"])
def addAccessPoint():
    apGroups = AccessPointGroup().info(struct="dict")
    return render_template("add-ap.html", apGroups=apGroups)

# Add Access Point Group Form

@cardinal_forms.route("/forms/add-ap-group", methods=["GET"])
def addAccessPointGroup():
    return render_template("add-ap-group.html")

# Delete Access Point Form

@cardinal_forms.route("/forms/delete-ap", methods=["GET"])
def deleteAccessPoint():
    accessPoints = AccessPoint().info(struct="dict")
    return render_template("delete-ap.html", aps=accessPoints)

# Delete Access Point Group Form

@cardinal_forms.route("/forms/delete-ap-group", methods=["GET"])
def deleteAccessPointGroup():
    apGroups = AccessPointGroup().info(struct="dict")
    return render_template("delete-ap-group.html", apGroups=apGroups)

# Network Toolkit Forms

@cardinal_forms.route("/forms/network-toolkit", methods=["GET"])
def networkToolkit():
    return render_template("network-toolkit.html")

# Manage AP Dashboard Form

@cardinal_forms.route("/forms/manage-ap-dashboard", methods=["GET", "POST"])
def manageApDashboard():
    if request.method == 'GET':
        status = request.args.get('status')
        accessPoints = AccessPoint().info(struct="dict")
        return render_template("choose-ap-dashboard.html", aps=accessPoints, status=status)

    elif request.method == 'POST':
        apId = request.form['ap_id']
        if len(apId) == 0:
            status = msgSpecifyValidAp()
            return redirect(url_for('cardinal_forms_bp.manageApDashboard', status=status))
        else:
            accessPoint = AccessPoint().info(id=apId, struct="dict")[0]
            session['apId'] = accessPoint["ap_id"]
            session['apName'] = accessPoint["ap_name"]
            session['apIp'] = accessPoint["ap_ip"]
            session['apTotalClients'] = accessPoint["ap_total_clients"]
            session['apBandwidth'] = accessPoint["ap_bandwidth"]
            session['apModel'] = accessPoint["ap_model"]
            return render_template("manage-ap-dashboard.html")

# Change AP IP Address Form

@cardinal_forms.route("/forms/change-ap-ip", methods=["GET"])
def configApIp():
    if request.method == 'GET':
        status = request.args.get('status')
        return render_template("change-ap-ip.html", status=status)

# Change AP Hostname Form

@cardinal_forms.route("/forms/change-ap-name", methods=["GET"])
def configApName():
    if request.method == 'GET':
        status = request.args.get('status')
        return render_template("config-ap-name.html", status=status)

# TFTP Backup Form

@cardinal_forms.route("/forms/get-ap-tftp-backup", methods=["GET"])
def configApTftpBackup():
    if request.method == 'GET':
        status = request.args.get('status')
        return render_template("config-ap-tftp-backup.html", status=status)

# Configure HTTP Form

@cardinal_forms.route("/forms/config-ap-http", methods=["GET"])
def configApHttp():
    status = request.args.get('status')
    return render_template("config-ap-http.html", status=status)

# Configure SNMP Form

@cardinal_forms.route("/forms/config-ap-snmp", methods=["GET"])
def configApSnmp():
    status = request.args.get('status')
    return render_template("config-ap-snmp.html", status=status)

# Fetch AP Info Form

@cardinal_forms.route("/forms/get-ap-info", methods=["GET"])
def fetchApInfo():
    status = request.args.get('status')
    return render_template("fetch-ap-info.html", status=status)

# Add SSIDs Menu

@cardinal_forms.route("/forms/add-ssids", methods=["GET"])
def addSsids():
    if request.method == 'GET':
        return render_template("add-ssids.html")

# Add 2.4GHz SSID Form

@cardinal_forms.route("/forms/add-ssid-24ghz", methods=["GET"])
def addSsid24Ghz():
    if request.method == 'GET':
        status = request.args.get('status')
        return render_template("add-ssid-24ghz.html", status=status)

# Add 2.4GHz RADIUS SSID Form

@cardinal_forms.route("/forms/add-ssid-24ghz-radius", methods=["GET"])
def addSsid24GhzRadius():
    if request.method == 'GET':
        status = request.args.get('status')
        return render_template("add-ssid-24ghz-radius.html", status=status)

# Add 5GHz SSID Form

@cardinal_forms.route("/forms/add-ssid-5ghz", methods=["GET"])
def addSsid5Ghz():
    if request.method == 'GET':
        status = request.args.get('status')
        return render_template("add-ssid-5ghz.html", status=status)

# Add 5GHz RADIUS SSID Form

@cardinal_forms.route("/forms/add-ssid-5ghz-radius", methods=["GET"])
def addSsid5GhzRadius():
    if request.method == 'GET':
        status = request.args.get('status')
        return render_template("add-ssid-5ghz-radius.html", status=status)

# Delete SSIDs Menu

@cardinal_forms.route("/forms/delete-ssids", methods=["GET"])
def deleteSsids():
    if request.method == 'GET':
        return render_template("delete-ssids.html")

# Delete 2.4GHz SSID Form

@cardinal_forms.route("/forms/delete-ssid-24ghz", methods=["GET"])
def deleteSsid24Ghz():
    if request.method == 'GET':
        ssids24Ghz = Ssid24Ghz().info(struct="dict")
        status = request.args.get('status')
        return render_template("delete-ssid-24ghz.html", status=status, ssids=ssids24Ghz)

# Delete 2.4GHz RADIUS SSID Form

@cardinal_forms.route("/forms/delete-ssid-24ghz-radius", methods=["GET"])
def deleteSsid24GhzRadius():
    if request.method == 'GET':
        ssids24GhzRadius = Ssid24GhzRadius().info(struct="dict")
        status = request.args.get('status')
        return render_template("delete-ssid-24ghz-radius.html", status=status, ssids=ssids24GhzRadius)

# Delete 5GHz SSID Form

@cardinal_forms.route("/forms/delete-ssid-5ghz", methods=["GET"])
def deleteSsid5Ghz():
    if request.method == 'GET':
        ssids5Ghz = Ssid5Ghz().info(struct="dict")
        status = request.args.get('status')
        return render_template("delete-ssid-5ghz.html", status=status, ssids=ssids5Ghz)

# Delete 5GHz RADIUS SSID Form

@cardinal_forms.route("/forms/delete-ssid-5ghz-radius", methods=["GET"])
def deleteSsid5GhzRadius():
    if request.method == 'GET':
        ssids5GhzRadius = Ssid5GhzRadius().info(struct="dict")
        status = request.args.get('status')
        return render_template("delete-ssid-5ghz-radius.html", status=status, ssids=ssids5GhzRadius)

# Deploy SSIDs Form (Access Point)

@cardinal_forms.route("/forms/deploy-ssids", methods=["GET"])
def deploySsids():
    return render_template("deploy-ssids.html")

# Deploy 2.4GHz SSID Form (Access Point)

@cardinal_forms.route("/forms/deploy-ssid-24ghz", methods=["GET"])
def deploySsid24Ghz():
    if request.method == 'GET':
        status = request.args.get('status')
        ssids24Ghz = Ssid24Ghz().info(struct="dict")
        return render_template("deploy-ssid-24ghz.html", status=status, ssids=ssids24Ghz)

# Deploy 2.4GHz RADIUS SSID Form (Access Point)

@cardinal_forms.route("/forms/deploy-ssid-24ghz-radius", methods=["GET"])
def deploySsid24GhzRadius():
    if request.method == 'GET':
        status = request.args.get('status')
        ssids24GhzRadius = Ssid24GhzRadius().info(struct="dict")
        return render_template("deploy-ssid-24ghz-radius.html", status=status, ssids=ssids24GhzRadius)

# Deploy 5GHz SSID Form (Access Point)

@cardinal_forms.route("/forms/deploy-ssid-5ghz", methods=["GET"])
def deploySsid5Ghz():
    if request.method == 'GET':
        status = request.args.get('status')
        ssids5Ghz = Ssid5Ghz().info(struct="dict")
        return render_template("deploy-ssid-5ghz.html", status=status, ssids=ssids5Ghz)

# Deploy 5GHz RADIUS SSID Form (Access Point)

@cardinal_forms.route("/forms/deploy-ssid-5ghz-radius", methods=["GET"])
def deploySsid5GhzRadius():
    if request.method == 'GET':
        status = request.args.get('status')
        ssids5GhzRadius = Ssid5GhzRadius().info(struct="dict")
        return render_template("deploy-ssid-5ghz-radius.html", status=status, ssids=ssids5GhzRadius)

# Remove SSIDs Form (Access Point)

@cardinal_forms.route("/forms/remove-ssids", methods=["GET"])
def removeSsids():
    return render_template("remove-ssids.html")

# Remove 2.4GHz SSID Form (Access Point)

@cardinal_forms.route("/forms/remove-ssid-24ghz", methods=["GET"])
def removeSsid24Ghz():
    if request.method == 'GET':
        status = request.args.get('status')
        ssids24Ghz = Ssid24Ghz().info(struct="dict")
        return render_template("remove-ssid-24ghz.html", status=status, ssids=ssids24Ghz)

# Remove 2.4GHz RADIUS SSID Form (Access Point)

@cardinal_forms.route("/forms/remove-ssid-24ghz-radius", methods=["GET"])
def removeSsid24GhzRadius():
    if request.method == 'GET':
        status = request.args.get('status')
        ssids24GhzRadius = Ssid24GhzRadius().info(struct="dict")
        return render_template("remove-ssid-24ghz.html", status=status, ssids=ssids24GhzRadius)

# Remove 5GHz SSID Form (Access Point)

@cardinal_forms.route("/forms/remove-ssid-5ghz", methods=["GET"])
def removeSsid5Ghz():
    if request.method == 'GET':
        status = request.args.get('status')
        ssids5Ghz = Ssid5Ghz().info(struct="dict")
        return render_template("remove-ssid-5ghz.html", status=status, ssids=ssids5Ghz)

# Remove 5GHz SSID Form (Access Point)

@cardinal_forms.route("/forms/remove-ssid-5ghz-radius", methods=["GET"])
def removeSsid5GhzRadius():
    if request.method == 'GET':
        status = request.args.get('status')
        ssids5GhzRadius = Ssid5GhzRadius().info(struct="dict")
        return render_template("remove-ssid-5ghz-radius.html", status=status, ssids=ssids5GhzRadius)

# Manage AP Group Dashboard Form

@cardinal_forms.route("/forms/manage-ap-group-dashboard", methods=["GET", "POST"])
def chooseApGroupDashboard():
    if request.method == 'GET':
        status = request.args.get('status')
        apGroups = AccessPointGroup().info(struct="dict")
        return render_template("choose-ap-group-dashboard.html", apGroups=apGroups, status=status)

    elif request.method == 'POST':
        apGroupId = request.form["ap_group_id"]
        if len(apGroupId) == 0:
            status = msgSpecifyValidApGroup()
            return redirect(url_for('cardinal_forms_bp.chooseApGroupDashboard', status=status))
        else:
            apGroupName = AccessPointGroup().info(id=apGroupId, struct="dict")[0]["ap_group_name"]
            session['apGroupId'] = apGroupId
            session['apGroupName'] = apGroupName
            return render_template("manage-ap-group-dashboard.html")

# Deploy SSIDs Form (Access Point Group Management)

@cardinal_forms.route("/forms/deploy-ssids-group", methods=["GET"])
def deploySsidsGroup():
    return render_template("deploy-ssids-group.html")

# Deploy 2.4GHz SSID Form (Access Point Group)

@cardinal_forms.route("/forms/deploy-ssid-24ghz-group", methods=["GET"])
def deploySsid24GhzGroup():
    if request.method == 'GET':
        status = request.args.get('status')
        ssids24Ghz = Ssid24Ghz().info(struct="dict")
        return render_template("deploy-ssid-24ghz-group.html", status=status, ssids=ssids24Ghz)

# Deploy 2.4GHz RADIUS SSID Form (Access Point Group)

@cardinal_forms.route("/forms/deploy-ssid-24ghz-radius-group", methods=["GET"])
def deploySsid24GhzGroupRadius():
    if request.method == 'GET':
        status = request.args.get('status')
        ssids24GhzRadius = Ssid24GhzRadius().info(struct="dict")
        return render_template("deploy-ssid-24ghz-radius-group.html", status=status, ssids=ssids24GhzRadius)

# Deploy 5GHz SSID Form (Access Point Group)

@cardinal_forms.route("/forms/deploy-ssid-5ghz-group", methods=["GET"])
def deploySsid5GhzGroup():
    if request.method == 'GET':
        status = request.args.get('status')
        ssids5Ghz = Ssid5Ghz().info(struct="dict")
        return render_template("deploy-ssid-5ghz-group.html", status=status, ssids=ssids5Ghz)

# Deploy 5GHz RADIUS SSID Form (Access Point Group)

@cardinal_forms.route("/forms/deploy-ssid-5ghz-radius-group", methods=["GET"])
def deploySsid5GhzRadiusGroup():
    if request.method == 'GET':
        status = request.args.get('status')
        ssids5GhzRadius = Ssid5GhzRadius().info(struct="dict")
        return render_template("deploy-ssid-5ghz-radius-group.html", status=status, ssids=ssids5GhzRadius)

# Remove SSIDs Form (Access Point Group)

@cardinal_forms.route("/forms/remove-ssids-group", methods=["GET"])
def removeSsidsGroup():
    return render_template("remove-ssids-group.html")

# Remove 2.4GHz SSID Form (Access Point Group)

@cardinal_forms.route("/forms/remove-ssid-24ghz-group", methods=["GET"])
def removeSsid24GhzGroup():
    if request.method == 'GET':
        status = request.args.get('status')
        ssids24Ghz = Ssid24Ghz().info(struct="dict")
        return render_template("remove-ssid-24ghz-group.html", status=status, ssids=ssids24Ghz)

# Remove 2.4GHz RADIUS SSID Form (Access Point Group)

@cardinal_forms.route("/forms/remove-ssid-24ghz-radius-group", methods=["GET"])
def removeSsid24GhzRadiusGroup():
    if request.method == 'GET':
        status = request.args.get('status')
        ssids24GhzRadius = Ssid24GhzRadius().info(struct="dict")
        return render_template("remove-ssid-24ghz-radius-group.html", status=status, ssids=ssids24GhzRadius)

# Remove 5GHz SSID Form (Access Point Group)

@cardinal_forms.route("/forms/remove-ssid-5ghz-group", methods=["GET"])
def removeSsid5GhzGroup():
    if request.method == 'GET':
        status = request.args.get('status')
        ssids5Ghz = Ssid5Ghz().info(struct="dict")
        return render_template("remove-ssid-5ghz-group.html", status=status, ssids=ssids5Ghz)

# Remove 5GHz RADIUS SSID Form (Access Point Group)

@cardinal_forms.route("/forms/remove-ssid-5ghz-radius-group", methods=["GET"])
def removeSsid5GhzRadiusGroup():
    if request.method == 'GET':
        status = request.args.get('status')
        ssids5GhzRadius = Ssid5GhzRadius().info(struct="dict")
        return render_template("remove-ssid-5ghz-radius-group.html", status=status, ssids=ssids5GhzRadius)
