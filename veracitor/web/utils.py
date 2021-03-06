

from json import JSONEncoder
from bson.json_util import default

from veracitor.web import app
from veracitor.database import *

from flask import Flask, render_template, request, redirect, url_for, jsonify, session, abort

log = app.logger.debug

class JSONEnc(JSONEncoder):

    def default(self, o):
        try:
            d = o.__dict__
        except:
            pass
        else:
            return d
        # Let the base class default method raise the TypeError
        return JSONEncoder.default(self, o)


def store_job_result(result):
    """Stores the job result in the app context."""
    if not hasattr(app, 'results'):
        app.results = {}
    if not hasattr(app, 'current_number_of_jobs'):
        app.current_number_of_jobs = 0
    app.results[result.id] = result

    # Here you could add the job id to the session object if the user
    # is logged in.

    app.current_number_of_jobs += 1

def get_user_as_dict(username):
    user_obj = extractor.get_user(username)

    try:
        source_ratings = []
        for source, ratings in user_obj.source_ratings.iteritems():
            for tag,rating in ratings.iteritems():
                source_ratings.append(
                    {
                        'name' : source,
                        'tag' : tag.replace(" ", "-"),
                        'rating': rating,
                        'description': extractor.get_producer(source).description
                        }
                    )  
            
        info_ratings = []
        for iurl in user_obj.info_ratings.keys():
            information = extractor.get_information(iurl)
            info_ratings.append({
                    'title': information.title,
                    'rating': user_obj.info_ratings[iurl],
                    'url': iurl,
                    'tags': [tag.name.replace(" ", "-") for tag in information.tags]
                    })
         
        groups = [{'name' : g.name,
                   'description' : g.description,
                   'producers' : [pname for pname in g.producers.keys()],
                   'tag' : g.tag.name
                   }
                  for g in user_obj.groups]
        
        user_dict = {'name' : user_obj.name,
                     'description' : user_obj.description,
                     'type_of' : user_obj.type_of,
                     'source_ratings' : source_ratings,
                     'groups' : groups,
                     'group_ratings' : user_obj.group_ratings,
                     'info_ratings' : info_ratings}
        return user_dict
    except Exception, e:
        log(e)
        return ""

@app.route('/utils/get_user', methods=['GET', 'POST'])
def get_user():
    """
    Extracts a user from the database and returns it. Only use when you KNOW
    the name of the user, and that it exists.

    """
    return jsonify(extractor.entity_to_dict(extractor.get_user(request.form["user_name"])));

@app.route('/utils/get_all_tags', methods=['GET', 'POST'])    
def get_all_tags():
    """
    Extracs all tags in the database and returns them as a dict::

       {
       "tag_names": [str]
       }
    """
    try:
        tag_names = [tag.name for tag in extractor.get_all_tags()]
        return jsonify(tag_names=tag_names)
    except:
        abort(400)

def __safe_string(url):
    """
    Help method to change url representation.
    TODO: Remove any need for this beyond private methods in the database module
    
    """
    return url.replace("|", ".")




    
