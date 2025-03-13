from flask.views import MethodView
from typing import Optional, List
from src.application.member_services import MemberServices
from src.domain.entities import Member
from flask import request , jsonify

class MemberApi(MethodView):
    def __init__(self) -> None:
        self.memberServices = MemberServices()

    def get(self, id: Optional[int] = None) -> Member | List[Member]:
        return self.memberServices.get(id)
    
    def post(self) -> Member:
        data = request.get_json()
        if not data.get("name") or not data.get("email"):
            raise ValueError("Name and email are required")
        return self.memberServices.create(data)
    
    def put(self, id) -> Member:
        data = request.get_json()
        if "member_id" in data and data['member_id']!=id:
            raise ValueError("Updating member_id is not allowed")
        return self.memberServices.update(id, data)
    
    def delete(self, id: int) -> str:
        return self.memberServices.delete(id)

