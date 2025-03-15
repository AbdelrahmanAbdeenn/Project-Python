from typing import Optional

from flask import Response, jsonify, request
from flask.views import MethodView

from src.application.member_services import MemberServices


class MemberApi(MethodView):
    def __init__(self) -> None:
        self.memberServices = MemberServices()

    def get(self, id: Optional[int] = None) -> Response:
        entity = self.memberServices.get(id)
        if isinstance(entity, list):
            return jsonify([vars(member) for member in entity])
        return jsonify(vars(entity))

    def post(self) -> Response:
        data = request.get_json()
        if not data.get("name") or not data.get("email"):
            raise ValueError("Name and email are required")
        entity = self.memberServices.create(data)
        return jsonify(vars(entity))

    def put(self, id: int) -> Response:
        data = request.get_json()
        if "member_id" in data and data["member_id"] != id:
            raise ValueError("Updating member_id is not allowed")
        entity = self.memberServices.update(id, data)
        return jsonify(vars(entity))

    def delete(self, id: int) -> Response:
        return jsonify(self.memberServices.delete(id))
