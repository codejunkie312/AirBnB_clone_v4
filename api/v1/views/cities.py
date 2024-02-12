#!/usr/bin/python3
"""Create  city view for API"""
from flask import jsonify, request
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route("/states/<state_id>/cities", strict_slashes=False)
def cities(state_id):
    """returns all City objects"""
    state = storage.get(State, state_id)
    if state is None:
        return jsonify({"error": "Not found"}), 404
    city_list = []
    for city in state.cities:
        city_list.append(city.to_dict())
    return jsonify(city_list)


@app_views.route("/cities/<city_id>", methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """returns a City object"""
    city = storage.get(City, city_id)
    if city is None:
        return jsonify({"error": "Not found"}), 404
    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>", methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """Deletes a city object and returns an empty dictionary"""
    city = storage.get(City, city_id)
    if city is None:
        return jsonify({"error": "Not found"}), 404
    storage.delete(city)
    storage.save()
    return jsonify({})


@app_views.route("/states/<state_id>/cities", methods=['POST'],
                 strict_slashes=False)
def post_city(state_id):
    """Creates a city object"""
    state = storage.get(State, state_id)
    if state is None:
        return jsonify({"error": "Not found"}), 404
    city = request.get_json()
    if city is None:
        return jsonify({"error": "Not a JSON"}), 400
    if "name" not in city:
        return jsonify({"error": "Missing name"}), 400
    city["state_id"] = state_id
    new_city = City(**city)
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=['PUT'], strict_slashes=False)
def put_city(city_id):
    """Updates a city object"""
    city = storage.get(City, city_id)
    if city is None:
        return jsonify({"error": "Not found"}), 404
    update = request.get_json()
    if update is None:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in update.items():
        if key not in ["id", "state_id", "created_at", "updated_at"]:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict()), 200
