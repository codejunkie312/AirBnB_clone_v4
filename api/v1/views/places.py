#!/usr/bin/python3
"""place view for API"""
from flask import jsonify, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from models.amenity import Amenity


@app_views.route("/cities/<city_id>/places", strict_slashes=False)
def places(city_id):
    """returns all Place objects"""
    city = storage.get(City, city_id)
    if city is None:
        return jsonify({"error": "Not found"}), 404
    place_list = []
    for place in city.places:
        place_list.append(place.to_dict())
    return jsonify(place_list)


@app_views.route("/places/<place_id>", methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """returns a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        return jsonify({"error": "Not found"}), 404
    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Deletes a place object and returns an empty dictionary"""
    place = storage.get(Place, place_id)
    if place is None:
        return jsonify({"error": "Not found"}), 404
    storage.delete(place)
    storage.save()
    return jsonify({})


@app_views.route("/cities/<city_id>/places", methods=['POST'],
                 strict_slashes=False)
def post_place(city_id):
    """Creates a place object"""
    city = storage.get(City, city_id)
    if city is None:
        return jsonify({"error": "Not found"}), 404
    place = request.get_json()
    if place is None:
        return jsonify({"error": "Not a JSON"}), 400
    if "user_id" not in place:
        return jsonify({"error": "Missing user_id"}), 400
    user = storage.get(User, place["user_id"])
    if user is None:
        return jsonify({"error": "Not found"}), 404
    if "name" not in place:
        return jsonify({"error": "Missing name"}), 400
    new_place = Place(**place)
    new_place.city_id = city_id
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=['PUT'], strict_slashes=False)
def put_place(place_id):
    """Updates a place object"""
    place = storage.get(Place, place_id)
    if place is None:
        return jsonify({"error": "Not found"}), 404
    update = request.get_json()
    if update is None:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in update.items():
        if key not in ["id", "user_id", "city_id", "created_at", "updated_at"]:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict())
