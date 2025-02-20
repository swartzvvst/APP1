from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Bem-vindo ao meu aplicativo Flask!"

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Pega a porta do ambiente ou usa 5000
    app.run(host="0.0.0.0", port=port)
