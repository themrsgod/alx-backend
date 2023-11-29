#!/usr/bin/env python3

"""
This module provides a flask app instance
"""

from datetime import datetime
from flask import (
    Flask,
    g,
    render_template,
    request
)
from flask_babel import Babel, format_datetime
from pytz import (
    timezone,
    exceptions
)


class Config:
    """ A Config class for configuration """
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


@babel.localeselector
def get_locale() -> str:
    """ Gets the language to be used """
    locale = request.args.get('locale')
    if locale in app.config['LANGUAGES']:
        return locale
    user = g.user
    if user is not None:
        locale = user.get('locale')
        if locale is not None:
            if locale in app.config['LANGUAGES']:
                return locale
    return request.accept_languages.best_match(app.config['LANGUAGES'])


def get_user() -> str:
    """ Gets the user to be logged in as """
    user = request.args.get('login_as')
    try:
        user = int(user)
    except Exception:
        pass
    if user is not None:
        return users.get(user, None)
    return None


@babel.timezoneselector
def get_timezone() -> str:
    """ Get the timezone to be used """
    tz = request.args.get('timezone')

    if tz is None:
        try:
            tz = timezone(tz)
            return tz
        except exceptions.UnknownTimeZoneError:
            pass
    user = g.user
    if user is not None:
        tz = user.get('timezone')
        try:
            tz = timezone(tz)
            return tz
        except exceptions.UnknownTimeZoneError:
            pass
    return timezone('UTC')


@app.before_request
def before_request() -> None:
    """ Sets the global user as the logged in user """
    user = get_user()
    g.user = user
    g.time = format_datetime()


@app.route('/', strict_slashes=False)
def indexHtml() -> str:
    """ Creates html template """
    user = g.user
    login_status = 'not_logged_in'
    username = ''
    time = g.time
    time_str = 'current_time_is'
    if user is not None:
        login_status = 'logged_in_as'
        username = user.get('name')
    return render_template('index.html',
                           login_status=login_status,
                           username=username,
                           current_time=time,
                           time_str=time_str)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
