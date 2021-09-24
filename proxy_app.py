from flask import Flask, request, Response 
from requests import get, post   
import pprint

pp = pprint.PrettyPrinter(indent=4)

app = Flask(__name__)  # Python web backend library
SITE_NAME = 'https://stackoverflow.com/'
# To remove traces of proxy server in the response from web server 
excluded_headers = ['content-encoding',         
                    'content-length',       # gzip
                    'transfer-encoding',    # chunked
                    'connection']           # keep-alive

@app.route('/')
def index():
    return 'Account Sharing Server!'

@app.route('/<path:path>', methods=['GET', 'POST'])
def proxy(path):
    # print(request)

    if request.method == 'GET':
        resp = get(f'{SITE_NAME}{path}')
        headers = [(name, value) for (name, value) in resp.raw.headers.items() if name.lower() not in excluded_headers]
        # removed_headers = [(name, value) for (name, value) in resp.raw.headers.items() if name.lower() in excluded_headers]
        # pp.pprint(removed_headers)
        response = Response(resp.content, resp.status_code, headers)
        return response

    elif request.method == 'POST':
        resp = post(f'{SITE_NAME}{path}', json=request.get_json()) # file consent ?
        headers = [(name, value) for (name, value) in resp.raw.headers.items() if name.lower() not in excluded_headers]
        # removed_headers = [(name, value) for (name, value) in resp.raw.headers.items() if name.lower() in excluded_headers]
        # pp.pprint(removed_headers)
        response = Response(resp.content, resp.status_code, headers)
        return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
