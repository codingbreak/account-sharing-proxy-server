import requests
from flask import Flask, Response, request
from urllib.parse import urlparse
import http.client 

from database import db

SITE_NAME = "https://stackoverflow.com/"
credentials = {}

# hop-by-hop headers
excluded_headers = [
    "content-encoding",
    "content-length",
    "transfer-encoding",
    "connection",
]


def create_app(site_name: str = SITE_NAME) -> Flask:
    app = Flask(__name__, static_url_path="/nothing")  
    app.config["CACHE_TYPE"] = "null"
    http.client._MAXHEADERS = 1000

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///:memory:"
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

            nonlocal site_name      # proxy function can rewrite site_name
            site_name = "https://" + request_url.netloc + "/"

            request.url = site_name + request_url.path[1:]
            path = request_url.path[1:]

        ### main app
        # app.logger.info("query %s%s with method %s", site_name, path, request.method)
        # global credentials

        # modify cookies
        cookies = {
            "_ga": "GA1.2.175757698.1640032605",
            "_gat": "1",
            "_gid": "GA1.2.1897489970.1640032605",
            "prov": "36428d0c-73f7-a53e-029b-6d7aa18db122",
            "OptanonAlertBoxClosed": "2021-12-28T13:34:48.822Z",
        }
        cookies = {"_ga": "GA1.2.175757698.1640032605",
                   "_gat": "1",
                   "_gid": "GA1.2.1897489970.1640032605",
                   "prov": "abf315bc-9ba0-ef69-5af3-c3d79eaeca92"}

        # proxy server sends request to web server
        # s = requests.session()
        resp = requests.request(
            method=request.method,
            url=request.url.replace(request.host_url, site_name),
            # headers=headers,
            data=request.get_data(),
            cookies=cookies, #request.cookies,
            allow_redirects=False,
        )

        # read cookies from website
        if resp.status_code == 200:
            # credentials[path] = resp.cookies
            print("\tWebsite:", site_name, path, request.method, request.get_data())
            print("\tRequest Cookies:", cookies) 
            print("\tResponse Cookies:", resp.cookies.get_dict())

        # change headers
        headers = [
            (name, value)
            for (name, value) in resp.raw.headers.items()
            if name.lower() not in excluded_headers
        ]
        
        # proxy server returns response to the website
        response = Response(resp.content, resp.status_code, headers)
        return response

    return app
