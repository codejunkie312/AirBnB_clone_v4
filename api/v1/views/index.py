#!/usr/bin/python3
"""index view for API"""
from flask import jsonify
from api.v1.views import app_views


@app_views.route("/status", strict_slashes=False)
def status():
    """returns status"""
    return jsonify({"status": "OK"})


@app_views.route("/stats", strict_slashes=False)
def stats():
    """returns stats"""
    from models import storage
    from models.state import State
    from models.city import City
    from models.amenity import Amenity
    from models.place import Place
    from models.review import Review
    from models.user import User

    return jsonify({
        State.__tablename__: storage.count(State),
        City.__tablename__: storage.count(City),
        Amenity.__tablename__: storage.count(Amenity),
        Place.__tablename__: storage.count(Place),
        Review.__tablename__: storage.count(Review),
        User.__tablename__: storage.count(User)
    })
