# Importa pacote Flask do modulo flask
from flask import Flask #as app
from controllers import routes

# Instanciando Flask no app.py
app = Flask(__name__, template_folder="views", static_url_path="/static")

routes.init_app(app)

if __name__ == "__main__":
    # Roda servidor no localhost, porta 5000; 0.0.0.0 = rede LAN
    app.run(host="localhost", port=4000, debug=True)