import requests
from flask import Flask, Response, request

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
    db.init_app(app)

    @app.route("/")
    def index() -> str:
        app.logger.info("query %s", site_name)
        return site_name

    @app.route("/<path:path>", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
    def proxy(path) -> Response:
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
