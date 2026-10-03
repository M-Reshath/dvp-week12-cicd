from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "DVP Week 12 - CI/CD with Jenkins, SonarQube & Docker"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)