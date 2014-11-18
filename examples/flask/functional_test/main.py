# encoding: utf-8
import logging

from flask import Flask, request
from flask.helpers import make_response
from flask.templating import render_template

import authomatic
from authomatic.adapters import WerkzeugAdapter
from tests.functional_tests import fixtures


DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
app.config.from_object(__name__)

authomatic = authomatic.Authomatic(fixtures.ASSEMBLED_CONFIG, '123',
                                   report_errors=False,
                                   logger=app.logger)

@app.route('/')
def home():
    return fixtures.render_home()


@app.route('/login/<provider_name>', methods=['GET', 'POST'])
def login(provider_name):
    response = make_response()
    result = authomatic.login(WerkzeugAdapter(request, response),
                              provider_name)

    if result:
        response.data += fixtures.render_login_result(result)

    return response


if __name__ == '__main__':
    # This does nothing unles you run this module with --testliveserver flag.

    import os
    import tempfile
    from werkzeug.serving import make_ssl_devcert
    ssl_context = make_ssl_devcert(os.path.join(tempfile.gettempdir(), 'authomatic-functional-tests'))

    import liveandletdie
    liveandletdie.Flask.wrap(app)

    # Mac
    # ln -sf /System/Library/Frameworks/Python.framework/Versions/2.6/Extras/lib/python/OpenSSL venv/lib/python2.7/
    # http://www.oesmith.co.uk/2011/05/23/pyopenssl-in-a-virtualenv-on-osx.html

    # Unix
    #
    # apt-get
    # dpkg -L python-openssl
    #
    # yum
    # rpm -ql pyOpenSSL
    #
    # Universal
    # python -c 'import os, OpenSSL; print os.path.dirname(OpenSSL.__file__)'
    #
    # ln -sf /usr/lib/python2.7/dist-packages/OpenSSL venv/lib/python2.7/

    # import pdb
    # pdb.set_trace()

    app.run(debug=True, port=8080, ssl_context=ssl_context)

    # app.run(debug=True, port=8080, ssl_context='adhoc')