from flask import Flask, render_template, request
import json

app = Flask(__name__)

# Load products from JSON
def load_products():
    with open("products.json", "r", encoding="utf-8") as f:
        return json.load(f)

@app.route("/")
def splash():
    return render_template("splash.html")

@app.route("/home", methods=["GET", "POST"])
def home():
    products = load_products()
    query = ""
    if request.method == "POST":
        query = request.form.get("query", "").lower()
        products = [p for p in products if query in p["title"].lower()]
    return render_template("index.html", products=products, query=query)

if __name__ == "__main__":
    app.run(debug=True)
