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
            # We need to update the user to get more info.
            result.user.update()

        # The rest happens inside the template.
        return render_template('login.html', result=result)

    # Don't forget to return the response.
    return response

def yolo():
  '''
  Pass oauth here?
  Call the API
  set url = 'https://api.twitter.com/1.1/search/tweets.json?q=%23meetmatt&count=5'
  set response = result.provider.access(url)
  if response.status == 200
    if response.data.errors
      Damn that error: {{ response.data.errors }}
    endif
    if response.data
      Your 5 most recent hashtags:<br />
      for tweet in response.data
        <h1>  print tweet.screen_name</h1>
        <h3>{{ tweet.text }}</h3>
        Posted on: {{ tweet.created_at }}
      endfor
    endif
  endif

  Then process response...
  '''
  return "Yeah bitch"

if __name__ == '__main__':
    app.run(port=5001, debug=True)