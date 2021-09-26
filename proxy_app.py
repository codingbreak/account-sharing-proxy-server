import time
from flask import Flask, request, Response, g  
import requests  


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
    # print(request.headers)
    start = time.perf_counter()

    if request.method == 'GET':
        resp = requests.get(f'{SITE_NAME}{path}')

    elif request.method == 'POST':
        resp = requests.post(f'{SITE_NAME}{path}', json=request.get_json()) # file consent ?

    headers = [(name, value) for (name, value) in resp.raw.headers.items() if name.lower() not in excluded_headers]
    # removed_headers = [(name, value) for (name, value) in resp.raw.headers.items() if name.lower() in excluded_headers]
    # print(removed_headers)
    response = Response(resp.content, resp.status_code, headers)
    
    request_time = time.perf_counter() - start

    print('Proxy - Target Server: {:.1f} ms'.format(resp.elapsed.total_seconds()*1000))
    print('Others: {:.1f} ms'.format(request_time*1000-resp.elapsed.total_seconds()*1000))
    
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
