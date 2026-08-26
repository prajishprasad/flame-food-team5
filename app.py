from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Dummy data: cafes and menus
cafes = {
    "Cafe One": ["Coffee", "Sandwich", "Muffin"],
    "Cafe Two": ["Tea", "Burger", "Fries"],
    "Cafe Three": ["Pizza", "Pasta", "Salad"]
}

# Prices for each item (in ₹) — campus-canteen style pricing
prices = {
    "Coffee": 30,
    "Sandwich": 60,
    "Muffin": 40,
    "Tea": 20,
    "Burger": 80,
    "Fries": 50,
    "Pizza": 120,
    "Pasta": 100,
    "Salad": 70
}

@app.route("/")
def home():
    """Show list of cafes"""
    return render_template("index.html", cafes=cafes)

@app.route("/cafe/<name>")
def show_cafe(name):
    """Show menu of a cafe, with prices"""
    raw_menu = cafes.get(name, [])
    # Build display strings like "Coffee - ₹30" so the template needs no changes
    menu = [f"{item} - ₹{prices.get(item, 'N/A')}" for item in raw_menu]
    return render_template("cafe.html", cafe=name, menu=menu)

@app.route("/add_to_cart/<cafe>/<item>")
def add_to_cart(cafe, item):
    """Add an item to the cart (stored in session)"""
    cart = session.get("cart", [])
    cart.append({"cafe": cafe, "item": item})
    session["cart"] = cart
    return redirect(url_for("view_cart"))

@app.route("/cart")
def view_cart():
    """View items in cart"""
    cart = session.get("cart", [])
    return render_template("cart.html", cart=cart)

@app.route("/checkout")
def checkout():
    """Clear the cart (no real payment)"""
    session["cart"] = []
    return "Thanks for ordering! Your cart is now empty."

if __name__ == "__main__":
    app.run(debug=True)