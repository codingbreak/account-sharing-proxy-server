from flask import Flask, request, Response, g
import requests  
import logging


app = Flask(__name__, static_url_path='/nothing')  # Python web backend library

# hop-by-hop headers
excluded_headers = ['content-encoding',       
                    'content-length',       
                    'transfer-encoding',    
                    'connection']   

SITE_NAME = 'https://reqbin.com/'
# SITE_NAME = 'https://stackoverflow.com/'       


@app.route('/')
def index():
    app.logger.info('home page')
    return SITE_NAME


@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def proxy(path):
    app.logger.info('query %s with method %s', path, request.method)

    resp = requests.request(
        method=request.method,
        url=request.url.replace(request.host_url, SITE_NAME),
        headers={key: value for (key, value) in request.headers if key != 'Host'},
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False)

    # Remove hop-by-hop headers
    headers = [(name, value) for (name, value) in resp.raw.headers.items() if name.lower() not in excluded_headers]
    
    response = Response(resp.content, resp.status_code, headers)
    
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
