#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, abort, redirect, render_template, request, session
import requests

import json

app = Flask(__name__)
app.secret_key = '\x87\xb6\x1f\x0e|6l\xfbhn\xd9\x9f\xc1\xca\x08-'

AUDIENCE = 'localhost' # Change me to your complete server:port pair

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/auth/login', methods=['POST'])
def login():
    if 'assertion' not in request.form:
        abort(400)

    data = {'assertion': request.form['assertion'], 'audience': AUDIENCE}
    res = requests.post('https://verifier.login.persona.org/verify', data=data)
    if res.ok:
        verification = json.loads(res.content)

        if verification['status'] == 'okay':
            session.update({'email': verification['email']})
            return res.content

    abort(500)


@app.route('/auth/logout', methods=['POST'])
def logout():
    session.pop('email', None)
    return redirect('/')

if __name__ == '__main__':
    print "Please only connect to '%s', literally." % AUDIENCE
    print "Other IPs or hostnames will not work."
    app.run(debug=True)
