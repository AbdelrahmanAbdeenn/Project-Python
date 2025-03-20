from flask import Response, jsonify, request
from flask.views import MethodView

from src.application.member_services import MemberServices


class MemberApi(MethodView):
    def __init__(self) -> None:
        self.memberServices = MemberServices()

    def get(self, id: int | None = None) -> Response:
        entity = self.memberServices.get(id)
        if isinstance(entity, list):
            return jsonify([(member) for member in entity])
        return jsonify(entity)

    def post(self) -> Response:
        data = request.get_json()
        if not data.get('name') or not data.get('email'):
            raise ValueError('Name and email are required')
        entity = self.memberServices.create(data)
        return jsonify(vars(entity))

    def patch(self, id: int) -> Response:
        data = request.get_json()
        if "id" in data and data['id'] != id:
            raise ValueError('Updating id is not allowed')
        entity = self.memberServices.update(id, data)
        return jsonify(entity)

    def delete(self, id: int) -> Response:
        return jsonify(self.memberServices.delete(id))
