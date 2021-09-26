import time
from flask import Flask, request, Response, g  
import requests  


app = Flask(__name__)  # Python web backend library
app.config["CACHE_TYPE"] = "null"

excluded_headers = ['content-encoding',       
                    'content-length',       
                    'transfer-encoding',    
                    'connection']   

SITE_NAME = 'https://reqbin.com/'
# SITE_NAME = 'https://stackoverflow.com/'       

@app.route('/')
def index():
    return SITE_NAME

@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def proxy(path):
    # print("Request:", request)
    # start = time.perf_counter()

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
    
    # request_time = time.perf_counter() - start
    # print('Proxy - Target Server: {:.1f} ms'.format(resp.elapsed.total_seconds()*1000))
    # print('Others: {:.1f} ms'.format(request_time*1000-resp.elapsed.total_seconds()*1000))
    
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
