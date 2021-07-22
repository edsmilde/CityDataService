
import connexion
from flask import render_template


app = connexion.App(__name__, specification_dir="./", port=8080)

app.add_api("swagger.yml")

@app.route("/")
def home():
    return render_template("home.html")


if __name__ == "__main__":
    app.run(debug=True)



