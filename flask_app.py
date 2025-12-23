from flask import Flask, redirect, render_template, request, url_for
from dotenv import load_dotenv
import os
import git
import hmac
import hashlib
from db import db_read, db_write
from auth import login_manager, authenticate, register_user
from flask_login import login_user, logout_user, login_required, current_user
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

# Load .env variables
load_dotenv()
W_SECRET = os.getenv("W_SECRET")

# Init flask app
app = Flask(__name__)
app.config["DEBUG"] = True
app.secret_key = "supersecret"

# Init auth
login_manager.init_app(app)
login_manager.login_view = "login"

# DON'T CHANGE
def is_valid_signature(x_hub_signature, data, private_key):
    hash_algorithm, github_signature = x_hub_signature.split('=', 1)
    algorithm = hashlib.__dict__.get(hash_algorithm)
    encoded_key = bytes(private_key, 'latin-1')
    mac = hmac.new(encoded_key, msg=data, digestmod=algorithm)
    return hmac.compare_digest(mac.hexdigest(), github_signature)

# DON'T CHANGE
@app.post('/update_server')
def webhook():
    x_hub_signature = request.headers.get('X-Hub-Signature')
    if is_valid_signature(x_hub_signature, request.data, W_SECRET):
        repo = git.Repo('./mysite')
        origin = repo.remotes.origin
        origin.pull()
        return 'Updated PythonAnywhere successfully', 200
    return 'Unathorized', 401

# Auth routes
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        user = authenticate(
            request.form["username"],
            request.form["password"]
        )

        if user:
            login_user(user)
            return redirect(url_for("index"))

        error = "Benutzername oder Passwort ist falsch."

    return render_template(
        "auth.html",
        title="In dein Konto einloggen",
        action=url_for("login"),
        button_label="Einloggen",
        error=error,
        footer_text="Noch kein Konto?",
        footer_link_url=url_for("register"),
        footer_link_label="Registrieren"
    )


@app.route("/register", methods=["GET", "POST"])
def register():
    error = None

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        ok = register_user(username, password)
        if ok:
            return redirect(url_for("login"))

        error = "Benutzername existiert bereits."

    return render_template(
        "auth.html",
        title="Neues Konto erstellen",
        action=url_for("register"),
        button_label="Registrieren",
        error=error,
        footer_text="Du hast bereits ein Konto?",
        footer_link_url=url_for("login"),
        footer_link_label="Einloggen"
    )

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))



# App routes
@app.route("/")
@login_required
def index():
    return render_template("index.html")

@app.route("/rezepte", methods=["GET", "POST"])
@login_required
def rezepte_page():
    # POST - Add new recipe
    if request.method == "POST":
        name = request.form["name"]
        db_write("INSERT INTO rezepte (user_id, name) VALUES (%s, %s)", (current_user.id, name, ))
        return redirect(url_for("rezepte_page"))

    # GET - List and search recipes
    search = request.args.get("search", "")
    if search:
        rezepte = db_read("SELECT id, name FROM rezepte WHERE user_id=%s AND name LIKE %s", (current_user.id, f"%{search}%"))
    else:
        rezepte = db_read("SELECT id, name FROM rezepte WHERE user_id=%s", (current_user.id,))
    return render_template("rezepte_page.html", rezepte=rezepte, search=search)

@app.route("/rezept/<int:rezept_id>", methods=["GET", "POST"])
@login_required
def rezept_detail(rezept_id):
    # POST - Add ingredient
    if request.method == "POST":
        name = request.form["name"]
        number = request.form.get("number")
        einheit = request.form.get("einheit")
        db_write("INSERT INTO zutaten (rezept_id, name, number, einheit) VALUES (%s, %s, %s, %s)", (rezept_id, name, number, einheit, ))
        return redirect(url_for("rezept_detail", rezept_id=rezept_id))

    # GET - Show recipe details
    rezept = db_read("SELECT id, name FROM rezepte WHERE user_id=%s AND id=%s", (current_user.id, rezept_id), single=True)
    if not rezept:
        return "Rezept nicht gefunden", 404
    
    zutaten = db_read("SELECT name, number, einheit FROM zutaten WHERE rezept_id=%s", (rezept_id,))
    return render_template("rezept_detail.html", rezept=rezept, zutaten=zutaten)

@app.route("/einkaufsliste", methods=["GET", "POST"])
@login_required
def einkaufsliste():
    shopping_list = []
    matched_rezept = None
    vorhandene_zutaten = []
    
    if request.method == "POST":
        # Parse the ingredients the user has at home
        zutaten_input = request.form.get("zutaten", "")
        vorhandene_zutaten = [z.strip().lower() for z in zutaten_input.split(",") if z.strip()]
        
        if vorhandene_zutaten:
            # Get all user's recipes with their ingredients
            user_rezepte = db_read("SELECT id, name FROM rezepte WHERE user_id=%s", (current_user.id,))
            
            best_match = None
            best_match_count = 0
            
            for rezept in user_rezepte:
                rezept_zutaten = db_read("SELECT name, number, einheit FROM zutaten WHERE rezept_id=%s", (rezept["id"],))
                
                # Count how many ingredients match
                match_count = sum(1 for z in rezept_zutaten if z["name"].lower() in vorhandene_zutaten)
                
                if match_count > best_match_count:
                    best_match_count = match_count
                    best_match = {"rezept": rezept, "zutaten": rezept_zutaten, "match_count": match_count}
            
            if best_match:
                matched_rezept = best_match["rezept"]
                # Calculate shopping list (ingredients not at home)
                for zutat in best_match["zutaten"]:
                    if zutat["name"].lower() not in vorhandene_zutaten:
                        shopping_list.append(zutat)
    
    return render_template("einkaufsliste.html", 
                         shopping_list=shopping_list, 
                         matched_rezept=matched_rezept,
                         vorhandene_zutaten=", ".join(vorhandene_zutaten))


if __name__ == "__main__":
    app.run()
