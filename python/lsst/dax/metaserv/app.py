#!/usr/bin/env python

# LSST Data Management System
# Copyright 2015 AURA/LSST.
#
# This product includes software developed by the
# LSST Project (http://www.lsst.org/).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the LSST License Statement and
# the GNU General Public License along with this program.  If not,
# see <http://www.lsstcorp.org/LegalNotices/>.

from flask import Flask, request
import json
from lsst.dax.metaserv import api_v0, api_v1
from lsst.db.engineFactory import getEngineFromFile

app = Flask(__name__)

# Configure Engine
defaults_file = "~/.lsst/metaserv.ini"
engine = getEngineFromFile(defaults_file)
app.config["default_engine"] = engine


@app.route('/')
def route_root():
    fmt = request.accept_mimetypes.best_match(['application/json', 'text/html'])
    s = "Test server for testing metadata. Try adding /meta to URI.\n"
    if fmt == "text/html":
        return s
    return json.dumps(s)


@app.route('/meta')
def route_meta():
    """Lists supported versions for /meta."""
    fmt = request.accept_mimetypes.best_match(['application/json', 'text/html'])
    s = "v0\nv1\n"
    if fmt == "text/html":
        return s
    return json.dumps(s)

app.register_blueprint(api_v0.metaREST, url_prefix='/meta/v0')
app.register_blueprint(api_v1.metaserv_api_v1, url_prefix='/meta/v1')