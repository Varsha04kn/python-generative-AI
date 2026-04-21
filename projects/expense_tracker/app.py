from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = "expense_secret"
DB = "expenses.db"

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                date TEXT NOT NULL,
                note TEXT
            )
        """)

@app.route("/")
def index():
    category = request.args.get("category", "")
    month = request.args.get("month", "")
    with get_db() as conn:
        query = "SELECT * FROM expenses WHERE 1=1"
        params = []
        if category:
            query += " AND category = ?"
            params.append(category)
        if month:
            query += " AND strftime('%Y-%m', date) = ?"
            params.append(month)
        query += " ORDER BY date DESC"
        expenses = conn.execute(query, params).fetchall()
        total = sum(e["amount"] for e in expenses)
        categories = conn.execute("SELECT DISTINCT category FROM expenses").fetchall()
    return render_template("index.html", expenses=expenses, total=total,
                           categories=categories, selected_category=category, selected_month=month)

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        title    = request.form["title"].strip()
        amount   = request.form["amount"]
        category = request.form["category"].strip()
        date     = request.form["date"]
        note     = request.form.get("note", "").strip()
        if not title or not amount or not category or not date:
            flash("All fields except note are required.", "danger")
            return redirect(url_for("add"))
        with get_db() as conn:
            conn.execute("INSERT INTO expenses (title, amount, category, date, note) VALUES (?,?,?,?,?)",
                         (title, float(amount), category, date, note))
        flash("Expense added successfully!", "success")
        return redirect(url_for("index"))
    return render_template("form.html", expense=None, today=datetime.today().strftime("%Y-%m-%d"))

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    with get_db() as conn:
        expense = conn.execute("SELECT * FROM expenses WHERE id=?", (id,)).fetchone()
    if not expense:
        flash("Expense not found.", "danger")
        return redirect(url_for("index"))
    if request.method == "POST":
        title    = request.form["title"].strip()
        amount   = request.form["amount"]
        category = request.form["category"].strip()
        date     = request.form["date"]
        note     = request.form.get("note", "").strip()
        with get_db() as conn:
            conn.execute("UPDATE expenses SET title=?, amount=?, category=?, date=?, note=? WHERE id=?",
                         (title, float(amount), category, date, note, id))
        flash("Expense updated!", "success")
        return redirect(url_for("index"))
    return render_template("form.html", expense=expense, today=datetime.today().strftime("%Y-%m-%d"))

@app.route("/delete/<int:id>")
def delete(id):
    with get_db() as conn:
        conn.execute("DELETE FROM expenses WHERE id=?", (id,))
    flash("Expense deleted.", "warning")
    return redirect(url_for("index"))

@app.route("/db-viewer")
def db_viewer():
    with get_db() as conn:
        tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
        table_data = {}
        for t in tables:
            name = t["name"]
            rows = conn.execute(f"SELECT * FROM {name}").fetchall()
            cols = [d[0] for d in conn.execute(f"SELECT * FROM {name} LIMIT 1").description] if rows else []
            table_data[name] = {"cols": cols, "rows": [dict(r) for r in rows]}
    return render_template("db_viewer.html", table_data=table_data)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
