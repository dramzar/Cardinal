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

from cardinal.system.common import CardinalEnv
from cardinal.system.common import msgAuthFailed
from cardinal.system.dbmodels import Users
from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import session
from flask import url_for
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash

cardinal_auth = Blueprint('cardinal_auth_bp', __name__)

@cardinal_auth.route("/")
def index():
    if current_user:
        return redirect(url_for('cardinal_auth_bp.dashboard'))

    return redirect(url_for('cardinal_auth_bp.login'))

@cardinal_auth.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")

@cardinal_auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        user = Users.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('cardinal_auth_bp.dashboard'))

        return render_template('login.html', error="Invalid user or password.", username=username)

    return render_template('login.html')

@cardinal_auth.route("/logout")
@login_required
def logout():
   session.pop('username', None)
   session.pop('apId', None)
   session.pop('apGroupId', None)
   session.pop('apGroupName', None)
   session.pop('apName', None)
   session.pop('apIp', None)
   session.pop('apTotalClients', None)
   session.pop('apBandwidth', None)
   session.pop('apModel', None)
   logout_user()
   return redirect(url_for('cardinal_auth_bp.index'))

@cardinal_auth.route("/changepass", methods=["GET", "POST"])
@login_required
def changePassword():
    if request.method == "GET":
        return render_template("change_password.html")
