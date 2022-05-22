from flask import Flask
from api_v1 import api as api_v1

app = Flask(__name__)
app.register_blueprint(api_v1,url_prefix='/api/v1')

if __name__=='__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
    