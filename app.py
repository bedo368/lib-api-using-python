from flask import Flask

from routes.book import book_bp
from routes.order import orders_bp
from routes.user import user_bp
from flask import  request
app = Flask(__name__)


@app.before_request
def before_every_request():
    # Example: Log the request method and URL
    print(f"Received {request.method} request for {request.url}")

    # Example: Set a global variable

app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(book_bp, url_prefix='/api')

app.register_blueprint(orders_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True)