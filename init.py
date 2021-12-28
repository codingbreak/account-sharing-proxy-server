import requests
from flask import Flask, Response, request
from urllib.parse import urlparse
import http.client

from database import db

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
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    db.init_app(app)

    @app.route("/")
    def index() -> str:
        app.logger.info("query %s", site_name)
        return site_name

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
