#!/usr/bin/python3
"""places_amenities view"""
from api.v1.views import app_views
from flask import jsonify, request
from models import storage
from models.place import Place
from models.amenity import Amenity


@app_views.route("/places/<place_id>/amenities", methods=["GET"],
                 strict_slashes=False)
def get_place_amenities(place_id):
    """get place amenities"""
    place = storage.get(Place, place_id)
    if place is None:
        return jsonify({"error": "Not found"}), 404
    amenities = [amenity.to_dict() for amenity in place.amenities]
    return jsonify(amenities)


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["DELETE"],
                 strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    """delete place amenity"""
    place = storage.get(Place, place_id)
    if place is None:
        return jsonify({"error": "Not found"}), 404
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        return jsonify({"error": "Not found"}), 404
    if amenity not in place.amenities:
        return jsonify({"error": "Not found"}), 404
    place.amenities.remove(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>/amenities/<amenity_id>", methods=["POST"],
                 strict_slashes=False)
def post_place_amenity(place_id, amenity_id):
    """post place amenity"""
    place = storage.get(Place, place_id)
    if place is None:
        return jsonify({"error": "Not found"}), 404
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        return jsonify({"error": "Not found"}), 404
    if amenity in place.amenities:
        return jsonify(amenity.to_dict()), 200
    place.amenities.append(amenity)
    storage.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route("/places_search", methods=["POST"],
                 strict_slashes=False)
def post_places_search():
    """search for places"""
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    places = storage.all(Place).values()
    if "states" in data:
        places = [place for place in places if place.state_id in
                  data["states"]]
    if "cities" in data:
        places = [place for place in places if place.city_id in
                  data["cities"]]
    if "amenities" in data:
        amenities = data["amenities"]
        places = [place for place in places if all(amenity in place.amenities
                                                   for amenity in amenities)]
    places = [place.to_dict() for place in places]
    return jsonify(places)
