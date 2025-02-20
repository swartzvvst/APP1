from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Bem-vindo ao meu aplicativo Flask!"

if __name__ == "__main__":
    app.run(debug=True)