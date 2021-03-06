# index.py
# ========

"""
.. module:: index
    :synopsis: Defines what should be returned when / is requested.

.. moduleauthor:: John Brynte Turesson <johntu@kth.se>
.. moduleauthor:: Anton Erholt <aerholt@kth.se>

"""

from flask import render_template, url_for, session

from veracitor.web import app, utils
from veracitor.database import *



#app.add_url_rule('/favicon.ico', redirect_to=url_for('static', filename='images/favicon.ico'))

@app.route('/')
def index():
    """
    Initializes the web page.
    """
    uname = session.get('user_name')

    if uname:
        session.pop('error', None)

        try:
            session['user'] = extractor.get_user(uname)
            veracitor = {
                'user_name': uname,
                'title' : 'Veracitor',
                'tabs' : [
                    {
                        'name' : 'Search & Add',
                        'key' : 'search',
                        'viewid' : 'search_view',
                        'menuid' : 'search_menu',
                        'url' : 'tabs/search_tab.html'
                        },
                    {
                        'name' : 'Network',
                        'key' : 'network',
                        'viewid' : 'network_view',
                        'menuid' : 'network_menu',
                        'url' : 'tabs/network_tab.html'
                        },
                    {
                        'name' : 'Ratings',
                        'key' : 'ratings',
                        'viewid' : 'ratings_view',
                        'menuid' : 'ratings_menu',
                        'url' : 'tabs/ratings_tab.html'
                        },
                    {
                        'name' : 'Account',
                        'key' : 'account',
                        'viewid' : 'account_view',
                        'menuid' : 'account_menu',
                        'url' : 'tabs/account_tab.html'
                        }]
                }

            if session['user'].name == 'admin':
                veracitor['users'] = [usr.name for usr in user.User.objects if usr.name != 'admin']
            
        except Exception, e:
            session['error'] = 'User %s not found' % uname
            session.pop('user_name', None)
            uname = None

    if not uname:
        veracitor = {
            'title' : 'Veracitor',
            'tabs' : [{
                    'name' : 'Login',
                    'key' : 'login',
                    'viewid' : 'login_view',
                    'menuid' : 'login_menu',
                    'url' : 'tabs/login_tab.html'
                    },
                      {
                    'name' : 'Account',
                    'key' : 'account',
                    'viewid' : 'account_view',
                    'menuid' : 'account_menu',
                    'url' : 'tabs/account_tab.html'
                    }]
            }

    return render_template('index.html', vera=veracitor)
