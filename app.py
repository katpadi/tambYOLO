# -*- coding: utf-8 -*-
"""
Some comments about the app
"""

from flask import Flask, render_template, request, make_response
from authomatic.adapters import WerkzeugAdapter
from authomatic import Authomatic

from config import CONFIG

app = Flask(__name__)

# Instantiate Authomatic.
authomatic = Authomatic(CONFIG, 'your secret string', report_errors=False)
'''
app.secret_key = 'development'
app.config.from_object('config')
'''
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login/<provider_name>/', methods=['GET', 'POST'])
def login(provider_name):
  response = make_response()
  result = authomatic.login(WerkzeugAdapter(request, response), provider_name)
  if result:
      if result.user:
          result.user.update()
      return render_template('login.html', result=result)
  return response

if __name__ == '__main__':
    app.run(port=5001, debug=True)