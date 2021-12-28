from init import create_app
import logging

app = create_app()

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
