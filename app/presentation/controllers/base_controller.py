from abc import ABC, abstractmethod
from flask import Blueprint, jsonify


class BaseController(ABC):
    """Abstract base class for all controllers providing common functionality"""

    def __init__(self, service, blueprint_name: str):
        self._service = service
        self.blueprint = Blueprint(blueprint_name, __name__)
        self._register_routes()

    @abstractmethod
    def _register_routes(self):
        """Register routes for the controller - must be implemented by subclasses"""
        pass

    def success_response(self, data=None, message="success"):
        """Standard success response format"""
        return jsonify({
            'code': 0,
            'message': message,
            'data': data
        })

