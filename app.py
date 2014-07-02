# -*- coding: utf-8 -*-
"""
Some comments about the app
"""

import requests
import random
from flask import Flask, render_template, request, make_response, session, jsonify
from authomatic.adapters import WerkzeugAdapter
from authomatic import Authomatic

from config import CONFIG

app = Flask(__name__)

# Temp lang naman
app.config['SECRET_KEY'] = 'holyshitthisisasecret'

# Instantiate Authomatic.
authomatic = Authomatic(CONFIG, 'your secret string', report_errors=False)


@app.route('/')
def index():
    """
    Home handler
    """

    return render_template('index.html')


@app.route('/login/<provider_name>/', methods=['GET', 'POST'])
def login(provider_name):
    """
    Login handler, must accept both GET and POST to be able to use OpenID.
    """

    # We need response object for the WerkzeugAdapter.
    response = make_response()

    # Log the user in, pass it the adapter and the provider name.
    result = authomatic.login(WerkzeugAdapter(request, response), provider_name)

    # If there is no LoginResult object, the login procedure is still pending.
    if result:
        if result.user:
          '''
          Save session here
          '''
          session['credentials'] = result.user.credentials.serialize()
          # We need to update the user to get more info.
          result.user.update()

        # The rest happens inside the template.
        #return render_template('login.html', result=result)
        return render_template('yolo.html', tweet={})

    # Don't forget to return the response.
    return response


@app.route('/yolo', methods=['GET', 'POST'])
def yolo():
  hashtag  = request.args.get('hashtag')
  how_many = request.args.get('how_many') # Wala pa
  url = 'https://api.twitter.com/1.1/search/tweets.json'
  params = {
    'q': hashtag,
    'count': 20,
  }
  res = authomatic.access(session['credentials'], url, params=params)

  if res.data['statuses']:
    tweet=random.choice(res.data['statuses'])
  else:
    # None huhu
    tweet = None

  #random.sample = if more than 1
  return render_template('yolo.html', tweet=tweet, tweets=res.data)

if __name__ == '__main__':
    app.run(port=5001, debug=True)
