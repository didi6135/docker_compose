from flask import Flask
from psycopg2.extras import RealDictCursor
from config.postgres_config import create_table_if_not_exist
from controller.connection_controller import connection_blueprint



app = Flask(__name__)

app.register_blueprint(blueprint=connection_blueprint, url_prefix='/api')

if __name__ == '__main__':
    create_table_if_not_exist()
    app.run(debug=True, port=5000, host="0.0.0.0")
