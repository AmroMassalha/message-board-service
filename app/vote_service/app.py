import logging, os
from flask import Flask, request, jsonify, g
from flask.views import MethodView
from flasgger import Swagger

from vote_service.logic.concrete_vote_service import ConcreteVoteService
from foundations.admin.token.get_user_id_from_token import jwt_token_required

ROOTDIR = os.path.dirname(__file__)
