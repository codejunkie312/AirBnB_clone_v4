#!/usr/bin/python3
"""places_reviews view for API"""
from flask import jsonify, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route("/places/<place_id>/reviews", strict_slashes=False)
def reviews(place_id):
    """returns all Review objects"""
    place = storage.get(Place, place_id)
    if place is None:
        return jsonify({"error": "Not found"}), 404
    review_list = []
    for review in place.reviews:
        review_list.append(review.to_dict())
    return jsonify(review_list)


@app_views.route("/reviews/<review_id>", methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """returns a Review object"""
    review = storage.get(Review, review_id)
    if review is None:
        return jsonify({"error": "Not found"}), 404
    return jsonify(review.to_dict())


@app_views.route("/reviews/<review_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """Deletes a review object and returns an empty dictionary"""
    review = storage.get(Review, review_id)
    if review is None:
        return jsonify({"error": "Not found"}), 404
    storage.delete(review)
    storage.save()
    return jsonify({})


@app_views.route("/places/<place_id>/reviews", methods=['POST'],
                 strict_slashes=False)
def post_review(place_id):
    """Creates a review object"""
    place = storage.get(Place, place_id)
    if place is None:
        return jsonify({"error": "Not found"}), 404
    review = request.get_json()
    if review is None:
        return jsonify({"error": "Not a JSON"}), 400
    if "user_id" not in review:
        return jsonify({"error": "Missing user_id"}), 400
    user = storage.get(User, review["user_id"])
    if user is None:
        return jsonify({"error": "Not found"}), 404
    if "text" not in review:
        return jsonify({"error": "Missing text"}), 400
    review["place_id"] = place_id
    new_review = Review(**review)
    new_review.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=['PUT'], strict_slashes=False)
def put_review(review_id):
    """Updates a review object"""
    review = storage.get(Review, review_id)
    if review is None:
        return jsonify({"error": "Not found"}), 404
    update = request.get_json()
    if update is None:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in update.items():
        if key not in ['id', 'user_id', 'place_id', 'created_at',
                       'updated_at']:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict())
