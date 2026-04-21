from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, Response
import sqlite3, os, json, csv, io, smtplib, re
from email.mime.text import MIMEText
from datetime import datetime, timedelta
from collections import defaultdict

app = Flask(__name__)
app.secret_key = 'smartstock_secret_key'
DB = 'smartstock.db'

# ── DB SETUP ──────────────────────────────────────────────────────────────────
def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as db:
        db.executescript('''
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT DEFAULT 'General',
                quantity REAL DEFAULT 0,
                unit TEXT DEFAULT 'units',
                min_stock REAL DEFAULT 5,
                barcode TEXT,
                expiry_date TEXT,
                location TEXT DEFAULT 'Home',
                image_url TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            );
            CREATE TABLE IF NOT EXISTS usage_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_id INTEGER,
                quantity_used REAL,
                logged_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(item_id) REFERENCES items(id)
            );
            CREATE TABLE IF NOT EXISTS locations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL
            );
        ''')
        # Seed default locations
        for loc in ['Home', 'Shop', 'Warehouse']:
            try:
                db.execute("INSERT OR IGNORE INTO locations (name) VALUES (?)", (loc,))
            except:
                pass
        # Seed sample data if empty
        count = db.execute("SELECT COUNT(*) FROM items").fetchone()[0]
        if count == 0:
            samples = [
                ('Rice', 'Food', 10, 'kg', 2, None, (datetime.now() + timedelta(days=180)).strftime('%Y-%m-%d'), 'Home'),
                ('Milk', 'Food', 2, 'liters', 1, None, (datetime.now() + timedelta(days=2)).strftime('%Y-%m-%d'), 'Home'),
                ('Sugar', 'Food', 0.5, 'kg', 1, None, None, 'Home'),
                ('Laptop Charger', 'Electronics', 1, 'units', 1, None, None, 'Shop'),
                ('Motor Oil', 'Automotive', 3, 'liters', 1, None, (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d'), 'Warehouse'),
            ]
            for s in samples:
                db.execute("INSERT INTO items (name,category,quantity,unit,min_stock,barcode,expiry_date,location) VALUES (?,?,?,?,?,?,?,?)", s)
            # Seed usage logs
            items = db.execute("SELECT id FROM items").fetchall()
            import random
            for item in items:
                for i in range(7):
                    day = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d %H:%M:%S')
                    db.execute("INSERT INTO usage_log (item_id, quantity_used, logged_at) VALUES (?,?,?)",
                               (item['id'], round(random.uniform(0.1, 1.5), 2), day))
        db.commit()

# ── HELPERS ───────────────────────────────────────────────────────────────────
def predict_days_left(item_id, current_qty):
    with get_db() as db:
        logs = db.execute(
            "SELECT quantity_used, logged_at FROM usage_log WHERE item_id=? ORDER BY logged_at DESC LIMIT 30",
            (item_id,)
        ).fetchall()
    if not logs:
        return None
    total_used = sum(r['quantity_used'] for r in logs)
    if len(logs) > 1:
        first = datetime.strptime(logs[-1]['logged_at'], '%Y-%m-%d %H:%M:%S')
        last  = datetime.strptime(logs[0]['logged_at'],  '%Y-%m-%d %H:%M:%S')
        days_span = max((last - first).days, 1)
    else:
        days_span = 1
    avg_per_day = total_used / days_span
    if avg_per_day <= 0:
        return None
    return round(current_qty / avg_per_day, 1)

def get_smart_alerts():
    alerts = []
    today = datetime.now().date()
    with get_db() as db:
        # Sort by quantity ascending so most critical (lowest qty) comes first
        items = db.execute("SELECT * FROM items ORDER BY quantity ASC").fetchall()
    for item in items:
        days_left = predict_days_left(item['id'], item['quantity'])
        qty = item['quantity']
        unit = item['unit']
        name = item['name']
        min_s = item['min_stock']

        # ── Quantity-based severity levels ──
        if qty == 0:
            alerts.append({
                'type': 'critical', 'icon': '🚨', 'severity': 'CRITICAL',
                'msg': f"<b>{name}</b> is <b>OUT OF STOCK</b> — 0 {unit} remaining",
                'item': dict(item), 'qty': qty
            })
        elif qty <= min_s:
            day_msg = f" — will finish in <b>{days_left} days</b>" if days_left else ""
            alerts.append({
                'type': 'low', 'icon': '⚠️', 'severity': 'LOW',
                'msg': f"<b>{name}</b> is <b>LOW</b> — only <b>{qty} {unit}</b> left{day_msg}",
                'item': dict(item), 'qty': qty
            })
        elif qty <= min_s * 2:
            alerts.append({
                'type': 'warning', 'icon': '🔔', 'severity': 'WARNING',
                'msg': f"<b>{name}</b> is running down — <b>{qty} {unit}</b> left (min: {min_s})",
                'item': dict(item), 'qty': qty
            })

        # ── Expiry alerts ──
        if item['expiry_date']:
            exp = datetime.strptime(item['expiry_date'], '%Y-%m-%d').date()
            diff = (exp - today).days
            if diff < 0:
                alerts.append({
                    'type': 'expired', 'icon': '🚫', 'severity': 'EXPIRED',
                    'msg': f"<b>{name}</b> has <b>EXPIRED</b> ({abs(diff)} days ago) — {qty} {unit} remaining",
                    'item': dict(item), 'qty': qty
                })
            elif diff <= 3:
                alerts.append({
                    'type': 'expiring', 'icon': '🕐', 'severity': 'EXPIRING',
                    'msg': f"<b>{name}</b> expires in <b>{diff} day(s)</b> — {qty} {unit} remaining",
                    'item': dict(item), 'qty': qty
                })
    return alerts

# ── ROUTES ────────────────────────────────────────────────────────────────────
@app.route('/')
def dashboard():
    with get_db() as db:
        items      = db.execute("SELECT * FROM items").fetchall()
        locations  = db.execute("SELECT name FROM locations").fetchall()
        total      = len(items)
        low_stock  = [i for i in items if i['quantity'] <= i['min_stock']]
        today      = datetime.now().date()
        expiring   = [i for i in items if i['expiry_date'] and
                      0 <= (datetime.strptime(i['expiry_date'], '%Y-%m-%d').date() - today).days <= 3]
        expired    = [i for i in items if i['expiry_date'] and
                      datetime.strptime(i['expiry_date'], '%Y-%m-%d').date() < today]

        # Weekly usage chart data
        usage_by_day = defaultdict(float)
        for i in range(6, -1, -1):
            day = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
            usage_by_day[day] = 0
        logs = db.execute(
            "SELECT DATE(logged_at) as day, SUM(quantity_used) as total FROM usage_log "
            "WHERE logged_at >= ? GROUP BY day",
            ((datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d'),)
        ).fetchall()
        for log in logs:
            usage_by_day[log['day']] = round(log['total'], 2)

        chart_labels = list(usage_by_day.keys())
        chart_data   = list(usage_by_day.values())

    alerts = get_smart_alerts()
    return render_template('dashboard.html',
        total=total, low_stock=low_stock, expiring=expiring, expired=expired,
        alerts=alerts, items=items, locations=[l['name'] for l in locations],
        chart_labels=json.dumps(chart_labels), chart_data=json.dumps(chart_data))

@app.route('/inventory')
def inventory():
    location = request.args.get('location', 'All')
    category = request.args.get('category', 'All')
    search   = request.args.get('search', '')
    with get_db() as db:
        query = "SELECT * FROM items WHERE 1=1"
        params = []
        if location != 'All':
            query += " AND location=?"; params.append(location)
        if category != 'All':
            query += " AND category=?"; params.append(category)
        if search:
            query += " AND (name LIKE ? OR barcode LIKE ?)"; params += [f'%{search}%', f'%{search}%']
        items     = db.execute(query, params).fetchall()
        locations = db.execute("SELECT name FROM locations").fetchall()
        categories = db.execute("SELECT DISTINCT category FROM items").fetchall()
    predictions = {item['id']: predict_days_left(item['id'], item['quantity']) for item in items}
    today = datetime.now().date()
    today_str = today.strftime('%Y-%m-%d')
    soon_str = (today + timedelta(days=3)).strftime('%Y-%m-%d')
    return render_template('inventory.html', items=items,
        locations=[l['name'] for l in locations],
        categories=[c['category'] for c in categories],
        selected_location=location, selected_category=category,
        search=search, predictions=predictions, today=today, today_str=today_str, soon_str=soon_str)

@app.route('/item/add', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        with get_db() as db:
            db.execute(
                "INSERT INTO items (name,category,quantity,unit,min_stock,barcode,expiry_date,location) VALUES (?,?,?,?,?,?,?,?)",
                (request.form['name'], request.form['category'], float(request.form['quantity']),
                 request.form['unit'], float(request.form['min_stock']),
                 request.form.get('barcode',''), request.form.get('expiry_date') or None,
                 request.form['location'])
            )
            db.commit()
        flash('Item added successfully!', 'success')
        return redirect(url_for('inventory'))
    with get_db() as db:
        locations = db.execute("SELECT name FROM locations").fetchall()
    return render_template('item_form.html', item=None, locations=[l['name'] for l in locations])

@app.route('/item/edit/<int:item_id>', methods=['GET', 'POST'])
def edit_item(item_id):
    with get_db() as db:
        item = db.execute("SELECT * FROM items WHERE id=?", (item_id,)).fetchone()
        locations = db.execute("SELECT name FROM locations").fetchall()
        if request.method == 'POST':
            db.execute(
                "UPDATE items SET name=?,category=?,quantity=?,unit=?,min_stock=?,barcode=?,expiry_date=?,location=? WHERE id=?",
                (request.form['name'], request.form['category'], float(request.form['quantity']),
                 request.form['unit'], float(request.form['min_stock']),
                 request.form.get('barcode',''), request.form.get('expiry_date') or None,
                 request.form['location'], item_id)
            )
            db.commit()
            flash('Item updated!', 'success')
            return redirect(url_for('inventory'))
    return render_template('item_form.html', item=item, locations=[l['name'] for l in locations])

@app.route('/item/delete/<int:item_id>', methods=['POST'])
def delete_item(item_id):
    with get_db() as db:
        db.execute("DELETE FROM items WHERE id=?", (item_id,))
        db.execute("DELETE FROM usage_log WHERE item_id=?", (item_id,))
        db.commit()
    flash('Item deleted.', 'info')
    return redirect(url_for('inventory'))

@app.route('/item/use/<int:item_id>', methods=['POST'])
def use_item(item_id):
    qty = float(request.form.get('quantity', 1))
    with get_db() as db:
        db.execute("UPDATE items SET quantity = MAX(0, quantity - ?) WHERE id=?", (qty, item_id))
        db.execute("INSERT INTO usage_log (item_id, quantity_used) VALUES (?,?)", (item_id, qty))
        db.commit()
    return redirect(url_for('inventory'))

@app.route('/analytics')
def analytics():
    with get_db() as db:
        # Top 5 most used
        most_used = db.execute(
            "SELECT i.name, SUM(u.quantity_used) as total FROM usage_log u "
            "JOIN items i ON i.id=u.item_id GROUP BY u.item_id ORDER BY total DESC LIMIT 5"
        ).fetchall()
        # Least used
        least_used = db.execute(
            "SELECT i.name, SUM(u.quantity_used) as total FROM usage_log u "
            "JOIN items i ON i.id=u.item_id GROUP BY u.item_id ORDER BY total ASC LIMIT 5"
        ).fetchall()
        # Category breakdown
        cat_data = db.execute(
            "SELECT category, COUNT(*) as cnt FROM items GROUP BY category"
        ).fetchall()
        # Weekly usage
        weekly = db.execute(
            "SELECT DATE(logged_at) as day, SUM(quantity_used) as total FROM usage_log "
            "WHERE logged_at >= ? GROUP BY day ORDER BY day",
            ((datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d'),)
        ).fetchall()

    return render_template('analytics.html',
        most_used=most_used, least_used=least_used,
        cat_labels=json.dumps([r['category'] for r in cat_data]),
        cat_data=json.dumps([r['cnt'] for r in cat_data]),
        weekly_labels=json.dumps([r['day'] for r in weekly]),
        weekly_data=json.dumps([round(r['total'], 2) for r in weekly]))

@app.route('/alerts')
def alerts():
    return render_template('alerts.html', alerts=get_smart_alerts())

@app.route('/send-email-alert', methods=['POST'])
def send_email_alert():
    recipient = request.form.get('email', '').strip()
    if not recipient:
        flash('Please enter a valid email.', 'info')
        return redirect(url_for('alerts'))
    alert_list = get_smart_alerts()
    if not alert_list:
        flash('No alerts to send!', 'info')
        return redirect(url_for('alerts'))
    body = 'SmartStock AI — Alert Summary\n\n'
    for a in alert_list:
        body += '• ' + re.sub('<[^>]+>', '', a['msg']) + '\n'
    try:
        smtp_user = os.getenv('SMTP_USER')
        smtp_pass = os.getenv('SMTP_PASS')
        if smtp_user and smtp_pass:
            msg = MIMEText(body)
            msg['Subject'] = 'SmartStock AI Alerts'
            msg['From'] = smtp_user
            msg['To'] = recipient
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as s:
                s.login(smtp_user, smtp_pass)
                s.sendmail(smtp_user, recipient, msg.as_string())
            flash(f'Alert email sent to {recipient}!', 'success')
        else:
            flash('[Demo] Set SMTP_USER & SMTP_PASS in .env to send real emails.', 'info')
    except Exception as e:
        flash(f'Email error: {e}', 'info')
    return redirect(url_for('alerts'))

@app.route('/export/csv')
def export_csv():
    with get_db() as db:
        items = db.execute('SELECT * FROM items').fetchall()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID','Name','Category','Quantity','Unit','Min Stock','Barcode','Expiry Date','Location','Created At'])
    for item in items:
        writer.writerow([item['id'], item['name'], item['category'], item['quantity'],
                         item['unit'], item['min_stock'], item['barcode'] or '',
                         item['expiry_date'] or '', item['location'], item['created_at']])
    output.seek(0)
    return Response(output, mimetype='text/csv',
                    headers={'Content-Disposition': 'attachment; filename=smartstock_inventory.csv'})

@app.route('/reorder')
def reorder():
    with get_db() as db:
        items = db.execute('SELECT * FROM items WHERE quantity <= min_stock').fetchall()
    reorder_list = []
    for item in items:
        days = predict_days_left(item['id'], item['quantity'])
        reorder_list.append({
            'id': item['id'], 'name': item['name'], 'category': item['category'],
            'quantity': item['quantity'], 'unit': item['unit'],
            'min_stock': item['min_stock'], 'location': item['location'],
            'days_left': days, 'suggested_qty': round(item['min_stock'] * 3, 1)
        })
    return render_template('reorder.html', reorder_list=reorder_list)

@app.route('/reorder/confirm', methods=['POST'])
def reorder_confirm():
    item_id = int(request.form['item_id'])
    qty = float(request.form['qty'])
    with get_db() as db:
        item = db.execute('SELECT * FROM items WHERE id=?', (item_id,)).fetchone()
        db.execute('UPDATE items SET quantity = quantity + ? WHERE id=?', (qty, item_id))
        db.commit()
    flash(f'Reordered {qty} {item["unit"]} of {item["name"]} from dummy store!', 'success')
    return redirect(url_for('reorder'))

@app.route('/suggestions')
def suggestions():
    with get_db() as db:
        items = db.execute('SELECT * FROM items').fetchall()
    result = []
    for item in items:
        with get_db() as db:
            logs = db.execute(
                'SELECT quantity_used, logged_at FROM usage_log WHERE item_id=? ORDER BY logged_at ASC',
                (item['id'],)
            ).fetchall()
        if len(logs) < 2:
            continue
        total_used = sum(r['quantity_used'] for r in logs)
        first = datetime.strptime(logs[0]['logged_at'], '%Y-%m-%d %H:%M:%S')
        last  = datetime.strptime(logs[-1]['logged_at'], '%Y-%m-%d %H:%M:%S')
        days_span = max((last - first).days, 1)
        avg_per_day = total_used / days_span
        reorder_cycle = round(item['min_stock'] / avg_per_day, 1) if avg_per_day > 0 else None
        days_left = predict_days_left(item['id'], item['quantity'])
        result.append({
            'name': item['name'], 'unit': item['unit'],
            'avg_per_day': round(avg_per_day, 2),
            'reorder_cycle': reorder_cycle,
            'days_left': days_left,
            'suggestion': f"You use {item['name']} at ~{round(avg_per_day,2)} {item['unit']}/day. "
                          + (f"Reorder every ~{reorder_cycle} days." if reorder_cycle else "")
        })
    return render_template('suggestions.html', suggestions=result)

@app.route('/locations')
def location_summary():
    with get_db() as db:
        locations = db.execute('SELECT name FROM locations').fetchall()
        summary = []
        for loc in locations:
            rows = db.execute('SELECT * FROM items WHERE location=?', (loc['name'],)).fetchall()
            items = [dict(i) for i in rows]
            low = [i for i in items if i['quantity'] <= i['min_stock']]
            summary.append({'name': loc['name'], 'total': len(items), 'low': len(low), 'items': items})
    return render_template('locations.html', summary=summary)

@app.route('/api/barcode/<barcode>')
def barcode_lookup(barcode):
    with get_db() as db:
        item = db.execute("SELECT * FROM items WHERE barcode=?", (barcode,)).fetchone()
    if item:
        return jsonify({'found': True, 'name': item['name'], 'category': item['category'],
                        'quantity': item['quantity'], 'unit': item['unit']})
    return jsonify({'found': False, 'barcode': barcode})

@app.route('/api/predict/<int:item_id>')
def api_predict(item_id):
    with get_db() as db:
        item = db.execute("SELECT * FROM items WHERE id=?", (item_id,)).fetchone()
    if not item:
        return jsonify({'error': 'Not found'}), 404
    days = predict_days_left(item_id, item['quantity'])
    reorder = datetime.now() + timedelta(days=max(0, (days or 0) - 2))
    return jsonify({
        'name': item['name'], 'current_qty': item['quantity'],
        'days_left': days,
        'reorder_by': reorder.strftime('%Y-%m-%d') if days else 'N/A',
        'suggestion': f"Reorder {item['name']} by {reorder.strftime('%b %d')}" if days else "No data yet"
    })

@app.route('/api/voice', methods=['POST'])
def voice_command():
    text = request.json.get('text', '').lower()
    with get_db() as db:
        items = db.execute("SELECT * FROM items").fetchall()
    for item in items:
        if item['name'].lower() in text:
            if 'check' in text or 'stock' in text:
                days = predict_days_left(item['id'], item['quantity'])
                return jsonify({'reply': f"{item['name']}: {item['quantity']} {item['unit']} left. "
                                         + (f"Lasts ~{days} days." if days else "")})
            if 'add' in text:
                import re
                nums = re.findall(r'\d+\.?\d*', text)
                qty = float(nums[0]) if nums else 1
                db.execute("UPDATE items SET quantity=quantity+? WHERE id=?", (qty, item['id']))
                db.commit()
                return jsonify({'reply': f"Added {qty} {item['unit']} of {item['name']}."})
    return jsonify({'reply': "Sorry, I couldn't find that item. Try: 'check stock of milk' or 'add 2 sugar'"})

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
