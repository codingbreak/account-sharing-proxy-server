import requests
from flask import Flask, Response, request, jsonify
from urllib.parse import urlparse
import http.client
from flask_jwt_extended import create_access_token
import os

from app.models import User, db
from app.extensions import jwt

from app.decorators import json_only

SITE_NAME = "https://stackoverflow.com/"

# hop-by-hop headers
excluded_headers = [
    "content-encoding",
    "content-length",
    "transfer-encoding",
    "connection",
]


def create_app(site_name: str = SITE_NAME) -> Flask:
    app = Flask(__name__, static_url_path="/nothing")  # Python web backend library
    app.config["CACHE_TYPE"] = "null"
    http.client._MAXHEADERS = 1000

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "2384asdhf@K#@J")
    db.init_app(app)
    jwt.init_app(app)

    @app.route("/")
    def index() -> str:
        app.logger.info("query %s", site_name)
        return site_name

    @app.route("/login", methods=["POST"])
    @json_only
    def login():
        email = request.json.get("email", None)
        password = request.json.get("password", None)
        if not email or not password:
            return jsonify({"msg": "Bad username or password"}), 401
        user: User = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            return jsonify({"msg": "Bad username or password"}), 401
        access_token = create_access_token(identity=email)
        return jsonify(access_token=access_token)

    @app.route("/register", methods=["POST"])
    @json_only
    def register():
        email = request.json.get("email", None)
        password = request.json.get("password", None)
        username = request.json.get("username", None)
        fullname = request.json.get("fullname", None)
        if not email or not password:
            return jsonify({"msg": "Please provide both email and password"}, 400)
        user = User.query.filter_by(email=email).first()
        if user:
            return jsonify({"msg": "Email exists"})
        new_user = User(
            email=email,
            fullname=fullname,
            password=User.create_password(password),
            username=username,
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"msg": "User is registered"}, 201)

    @app.route("/<path:path>", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
    def proxy(path) -> Response:
        # simple web-based test for exemple http://localhost:5000/stackoverflow.com/tour
        if ".com" in path:
            request_url = urlparse("https://" + path)
            if "http" in path:
                request_url = urlparse(path)

            nonlocal site_name
            site_name = "https://" + request_url.netloc + "/"

            request.url = site_name + request_url.path[1:]
            path = request_url.path[1:]

        # main app
        app.logger.info("query %s%s with method %s", site_name, path, request.method)

        resp = requests.request(
            method=request.method,
            url=request.url.replace(request.host_url, site_name),
            headers={key: value for (key, value) in request.headers if key != "Host"},
            data=request.get_data(),
            cookies=request.cookies,
            allow_redirects=False,
        )

        # Remove hop-by-hop headers
        headers = [
            (name, value)
            for (name, value) in resp.raw.headers.items()
            if name.lower() not in excluded_headers
        ]
        response = Response(resp.content, resp.status_code, headers)
        return response

    return app
