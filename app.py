import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, lookupID


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():

    # Get the user id for current session
    user_id = session["user_id"]

    # Get user portfolio from database
    portfolio = db.execute("SELECT coins FROM widgets WHERE user_id = ?", user_id)

    return render_template("index.html", pf=portfolio)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")



@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":

        registrant = request.form.get("username")

        # Blank username gets an "apology"
        if not registrant:
            return apology("freakin give me a username man", 400)

        # Unavailable username gets an "apology"
        row = db.execute("SELECT * FROM users WHERE username = ?", registrant)
        if len(row) != 0:
            return apology("some goat-spawned toad already got that alias", 400)

        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Require a password
        if not password or not confirmation:
            return apology("go back and fill in the password ya woolhead", 400)

        # Passwords should match
        if password != confirmation:
            return apology("passy no matchy!", 400)

        # Run the password through the scrambulator
        hash = generate_password_hash(password)

        # Insert the new finance bro into the database
        bro = db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", registrant, hash)

        # Remember user as logged in
        session["user_id"] = bro

        # Alert user on redirect
        flash("Registered!")
        return redirect("/")

    # If user sends by GET
    else:
        return render_template("register.html")


@app.route("/account", methods=["GET", "POST"])
@login_required
def account():

    if request.method == "POST":

        # Ensure fields are not left blank
        old = request.form.get("old")
        new = request.form.get("new")
        confirm = request.form.get("confirm")

        if not old or not new or not confirm:
            return apology("one or more of your fields are blank", 400)

        # Query database for logged in user
        user_id = session["user_id"]
        rows = db.execute("SELECT * FROM users WHERE id = ?", user_id)

        # Ensure old password is correct
        if not check_password_hash(rows[0]["hash"], old):
            return apology("invalid username and/or password", 403)
        else:

            # Passwords should match
            if new != confirm:
                return apology("passy no matchy!", 400)

            # Run the new password through the scrambulator
            hash = generate_password_hash(new)

            # Update database with new password
            db.execute("UPDATE users SET hash = ? WHERE id = ?", hash, user_id)

        flash("Password changed!")
        return redirect("/")

    # User access via GET
    else:
        return render_template("account.html")


@app.route("/delete", methods=["POST"])
@login_required
def delete():

    if request.method == "POST":

        # Ensure fields are not left blank
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            return apology("one or more of your fields are blank", 400)

        # Query database for logged in user
        user_id = session["user_id"]
        rows = db.execute("SELECT * FROM users WHERE id = ?", user_id)

        # Ensure username and password is correct
        if rows[0]["username"] != username:
            return apology("invalid username", 403)

        if not check_password_hash(rows[0]["hash"], password):
            return apology("invalid password", 403)

        # Delete user from database if all conditions are met
        db.execute("DELETE FROM widgets WHERE user_id = ?", user_id)
        db.execute("DELETE FROM users WHERE username = ?", username)

        return redirect("/logout")

    else:
        return redirect("/account")

@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    if request.method == "POST":
        # Get user input and determine if es no valido, hombre
        symbol = request.form.get("symbol")

        # If input field left blank
        if not symbol:
            return apology("no symbol input", 400)

        coin = lookup(symbol)

        # No es valido
        if coin != symbol.upper():
            return apology("symbol no es valido, tonto!", 400)


        coinID = lookupID(symbol)
        user_id = session["user_id"]

        # Ensure coins do not yet exist
        exist = db.execute("SELECT coins FROM widgets WHERE user_id = ?", user_id)
        for x in exist:
            if coinID == (x["coins"]):
                return apology("coin already in yer dashboard!")


        # Update the widget database with user id and their coinID(s) and symbol name
        db.execute("INSERT INTO widgets (user_id, coins, symbol) VALUES (?, ?, ?)", user_id, coinID, symbol.upper())

        return redirect("/")

    else:
        return redirect("index.html")


@app.route("/remove", methods=["GET", "POST"])
@login_required
def remove():

    if request.method == "POST":

        # Grab list of coins to be deleted from checked boxes
        undesirables = request.form.getlist('checkbox')

        for i in undesirables:
            db.execute("DELETE FROM widgets WHERE symbol = ?", i)

        return redirect("/")
        
    else:
         # Get the user id for current session
        user_id = session["user_id"]

        # Get user portfolio from database
        portfolio = db.execute("SELECT symbol FROM widgets WHERE user_id = ?", user_id)

        return render_template("remove.html", pf=portfolio)
