from flask import Flask

from routes.book import book_bp
from routes.user import user_bp
app = Flask(__name__)


app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(book_bp, url_prefix='/api')



if __name__ == '__main__':
    app.run(debug=True)