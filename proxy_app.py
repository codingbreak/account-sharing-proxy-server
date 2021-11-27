import requests
from flask import Flask, request, Response
from urllib.parse import urlparse
import http.client  # or  if you're on Python 3


app = Flask(__name__, static_url_path="/nothing")  # Python web backend library
app.config["CACHE_TYPE"] = "null"
http.client._MAXHEADERS = 1000

# hop-by-hop headers
excluded_headers = [
    "content-encoding",
    "content-length",
    "transfer-encoding",
    "connection",
]

# SITE_NAME = "https://www.youtube.com/" # "https://www.wsj.com/" # "https://reqbin.com/"
SITE_NAME = "https://stackoverflow.com/"


@app.route("/")
def index():
    app.logger.info("query %s", SITE_NAME)
    return SITE_NAME


@app.route("/<path:path>", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
def proxy(path):
    """e.g. http://localhost:5000/stackoverflow.com/tour"""

    if ".com" in path: 
        """web-based interface, e.g. http://localhost:5000/stackoverflow.com/tour"""
        request_url = urlparse("https://" + path)
        if "http" in path:
            request_url = urlparse(path)

        global SITE_NAME
        SITE_NAME = "https://" + request_url.netloc + "/"
        
        request.url = SITE_NAME + request_url.path[1:]
        path = request_url.path[1:]

    app.logger.info("query %s%s with method %s", SITE_NAME, path, request.method)

    resp = requests.request(
        method=request.method,
        url=request.url.replace(request.host_url, SITE_NAME),
        headers={key: value for (key, value) in request.headers if key != "Host"}, # if key != "Host"
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)