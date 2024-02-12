#!/usr/bin/python3
"""create amenities view for API"""
from flask import jsonify, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", strict_slashes=False)
def amenities():
    """returns all Amenity objects"""
    amenities = storage.all(Amenity)
    amenity_list = []
    for amenity in amenities.values():
        amenity_list.append(amenity.to_dict())
    return jsonify(amenity_list)


@app_views.route("/amenities/<amenity_id>", methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """returns a Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        return jsonify({"error": "Not found"}), 404
    return jsonify(amenity.to_dict())


@app_views.route("/amenities/<amenity_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """Deletes a amenity object and returns an empty dictionary"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        return jsonify({"error": "Not found"}), 404
    storage.delete(amenity)
    storage.save()
    return jsonify({})


@app_views.route("/amenities", methods=['POST'], strict_slashes=False)
def post_amenity():
    """Creates a amenity object"""
    amenity = request.get_json()
    if amenity is None:
        return jsonify({"error": "Not a JSON"}), 400
    if "name" not in amenity:
        return jsonify({"error": "Missing name"}), 400
    new_amenity = Amenity(**amenity)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", methods=['PUT'],
                 strict_slashes=False)
def put_amenity(amenity_id):
    """Updates a amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        return jsonify({"error": "Not found"}), 404
    update = request.get_json()
    if update is None:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in update.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)
    amenity.save()
    return jsonify(amenity.to_dict()), 200
