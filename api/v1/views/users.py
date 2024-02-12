#!/usr/bin/python3
"""Create users view for API"""
from flask import jsonify, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route("/users", strict_slashes=False)
def users():
    """returns all User objects"""
    users = storage.all(User)
    user_list = []
    for user in users.values():
        user_list.append(user.to_dict())
    return jsonify(user_list)


@app_views.route("/users/<user_id>", methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """returns a User object"""
    user = storage.get(User, user_id)
    if user is None:
        return jsonify({"error": "Not found"}), 404
    return jsonify(user.to_dict())


@app_views.route("/users/<user_id>", methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Deletes a user object and returns an empty dictionary"""
    user = storage.get(User, user_id)
    if user is None:
        return jsonify({"error": "Not found"}), 404
    storage.delete(user)
    storage.save()
    return jsonify({})


@app_views.route("/users", methods=['POST'], strict_slashes=False)
def post_user():
    """Creates a user object"""
    user = request.get_json()
    if user is None:
        return jsonify({"error": "Not a JSON"}), 400
    if "email" not in user:
        return jsonify({"error": "Missing email"}), 400
    if "password" not in user:
        return jsonify({"error": "Missing password"}), 400
    new_user = User(**user)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route("/users/<user_id>", methods=['PUT'], strict_slashes=False)
def put_user(user_id):
    """Updates a user object"""
    user = storage.get(User, user_id)
    if user is None:
        return jsonify({"error": "Not found"}), 404
    update = request.get_json()
    if update is None:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in update.items():
        if key not in ["id", "email", "created_at", "updated_at"]:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict())
