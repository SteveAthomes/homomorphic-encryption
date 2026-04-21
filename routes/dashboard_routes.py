from flask import Blueprint, render_template, request, redirect, url_for, session, send_file
from flask_login import login_required, current_user

import sqlite3
import os
import pickle
import hashlib

from io import BytesIO
from config import Config

from he_engine import encrypt_number, decrypt_number, get_keys
from file_crypto import encrypt_file, decrypt_file

from phe import paillier
from docx import Document
import csv


# ==============================
# ENCRYPT FUNCTION
# ==============================
def encrypt_value(value):
    if value is None:
        value = "null"
    return hashlib.sha256(str(value).encode()).hexdigest()[:10]


dashboard_bp = Blueprint("dashboard", __name__)


# ==============================
# BREACH MODE TOGGLE
# ==============================
@dashboard_bp.route("/breach")
@login_required
def breach_simulation():
    session["breach"] = True
    return redirect(url_for("dashboard.dashboard"))


@dashboard_bp.route("/exit_breach")
@login_required
def exit_breach():
    session["breach"] = False
    return redirect(url_for("dashboard.dashboard"))


# ==============================
# DASHBOARD
# ==============================
@dashboard_bp.route("/")
@login_required
def dashboard():

    from aes_crypto import decrypt_text  # ✅ MUST BE HERE

    conn = sqlite3.connect(Config.DATABASE)
    cursor = conn.cursor()

    cursor.execute("SELECT id, bank_name FROM banks WHERE user_id=?", (current_user.id,))
    banks = cursor.fetchall()

    cursor.execute("""
    SELECT accounts.id, accounts.account_name, banks.bank_name
    FROM accounts
    JOIN banks ON accounts.bank_id = banks.id
    WHERE banks.user_id = ?
    """, (current_user.id,))
    accounts = cursor.fetchall()

    cursor.execute("SELECT id, dataset_name FROM datasets WHERE user_id=?", (current_user.id,))
    datasets = cursor.fetchall()

    cursor.execute("SELECT id, filename FROM files WHERE user_id=?", (current_user.id,))
    files = cursor.fetchall()

    conn.close()

    # 🔓 NORMAL MODE
    if not session.get("breach"):
        banks = [(b[0], decrypt_text(b[1])) for b in banks]
        accounts = [(a[0], decrypt_text(a[1]), decrypt_text(a[2])) for a in accounts]
        files = [(f[0], decrypt_text(f[1])) for f in files]

    # 🔥 BREACH MODE (already working)
    if session.get("breach"):
        banks = [(b[0], encrypt_value(b[1])) for b in banks]
        accounts = [(a[0], encrypt_value(a[1]), encrypt_value(a[2])) for a in accounts]
        files = [(f[0], encrypt_value(f[1])) for f in files]

    return render_template(
        "dashboard.html",
        banks=banks,
        accounts=accounts,
        datasets=datasets,
        files=files
    )
    


# ==============================
# STORAGE
# ==============================
@dashboard_bp.route("/storage")
@login_required
def storage():

    conn = sqlite3.connect(Config.DATABASE)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, filename, uploaded_at FROM files WHERE user_id=?",
        (current_user.id,)
    )
    files = cursor.fetchall()

    conn.close()

    # BREACH MODE
    if session.get("breach"):
        files = [
            (
                f[0],
                encrypt_value(f[1]),  # filename encrypted
                encrypt_value(f[1].split('.')[-1])  # file type encrypted
            )
            for f in files
        ]

        
    return render_template("storage.html", files=files)

# ==============================
# FILE UPLOAD
# ==============================
@dashboard_bp.route("/upload_file", methods=["POST"])
@login_required
def upload_file():
    os.makedirs("uploads/encrypted_files", exist_ok=True)

    file = request.files["file"]

    if not file:
        return redirect(url_for("dashboard.storage"))

    file_data = file.read()
    encrypted_data = encrypt_file(file_data)

    os.makedirs("uploads/encrypted_files", exist_ok=True)

    stored_name = f"{current_user.id}_{file.filename}"
    file_path = os.path.join("uploads/encrypted_files", stored_name)

    with open(file_path, "wb") as f:
        f.write(encrypted_data)

    conn = sqlite3.connect(Config.DATABASE)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO files (user_id, filename, stored_path) VALUES (?, ?, ?)",
        (current_user.id, file.filename, file_path)
    )

    conn.commit()
    conn.close()

    return redirect(url_for("dashboard.storage"))


# ==============================
# DOWNLOAD
# ==============================
@dashboard_bp.route("/download/<int:file_id>")
@login_required
def download_file(file_id):

    conn = sqlite3.connect(Config.DATABASE)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT filename, stored_path FROM files WHERE id=? AND user_id=?",
        (file_id, current_user.id)
    )
    file_record = cursor.fetchone()
    conn.close()

    if not file_record:
        return "Unauthorized", 403

    filename, file_path = file_record

    # 🚨 BLOCK IMAGE DOWNLOAD IN BREACH MODE
    if session.get("breach"):
        if filename.lower().endswith((".png", ".jpg", ".jpeg", ".gif")):
            return "<h3 style='color:red;'>⚠ Access Denied: Encrypted Image File</h3>"

    # NORMAL FLOW
    with open(file_path, "rb") as f:
        encrypted_data = f.read()

    decrypted_data = decrypt_file(encrypted_data)

    return send_file(
        BytesIO(decrypted_data),
        download_name=filename,
        as_attachment=True
    )

# ==============================
# ANALYTICS
# ==============================
@dashboard_bp.route("/analytics")
@login_required
def analytics_home():

    conn = sqlite3.connect(Config.DATABASE)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(DISTINCT bank_id) FROM bank_accounts")
    total_banks = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM bank_accounts")
    total_accounts = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM bank_transactions")
    total_transactions = cursor.fetchone()[0]

    cursor.execute("SELECT COALESCE(SUM(amount),0) FROM bank_transactions")
    total_volume = cursor.fetchone()[0]

    cursor.execute("""
    SELECT 
        (SELECT bank_name FROM banks WHERE id = ba.bank_id),
        COALESCE(SUM(CASE WHEN bt.to_account = ba.id THEN bt.amount END),0),
        COALESCE(SUM(CASE WHEN bt.from_account = ba.id THEN bt.amount END),0),
        COUNT(bt.id)
    FROM bank_accounts ba
    LEFT JOIN bank_transactions bt
        ON bt.from_account = ba.id OR bt.to_account = ba.id
    GROUP BY ba.bank_id
    """)

    bank_stats = cursor.fetchall()
    conn.close()

    if session.get("breach"):
        total_banks = encrypt_value(total_banks)
        total_accounts = encrypt_value(total_accounts)
        total_transactions = encrypt_value(total_transactions)
        total_volume = encrypt_value(total_volume)

        bank_stats = [[encrypt_value(v) for v in row] for row in bank_stats]

    return render_template("analytics.html",
        total_banks=total_banks,
        total_accounts=total_accounts,
        total_transactions=total_transactions,
        total_volume=total_volume,
        bank_stats=bank_stats
    )


# ==============================
# FINANCE
# ==============================
@dashboard_bp.route("/finance")
@login_required
def finance_home():

    from aes_crypto import decrypt_text

    conn = sqlite3.connect(Config.DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT 
        (SELECT bank_name FROM banks WHERE id = a1.bank_id),
        a1.account_name,
        a1.account_type,
        a1.account_name,
        a2.account_name,
        t.amount
    FROM bank_transactions t
    LEFT JOIN bank_accounts a1 ON t.from_account = a1.id
    LEFT JOIN bank_accounts a2 ON t.to_account = a2.id
    ORDER BY t.id DESC
    """)

    transactions = cursor.fetchall()

    cursor.execute("SELECT id, account_name FROM bank_accounts")
    accounts = cursor.fetchall()

    conn.close()

    # 🔓 DECRYPT (NORMAL MODE ONLY)
    if not session.get("breach"):
        transactions = [
            (
                decrypt_text(t[0]) if t[0] else "N/A",
                decrypt_text(t[1]),
                t[2],
                decrypt_text(t[3]),
                decrypt_text(t[4]),
                t[5]
            )
            for t in transactions
        ]

        accounts = [(a[0], decrypt_text(a[1])) for a in accounts]

    # 🔥 BREACH MODE (KEEP AS IS)
    if session.get("breach"):
        transactions = [[encrypt_value(v) for v in row] for row in transactions]
        accounts = [(a[0], encrypt_value(a[1])) for a in accounts]

    return render_template(
        "finance_home.html",
        transactions=transactions,
        accounts=accounts
    )


# ==============================
# CREATE BANK
# ==============================
@dashboard_bp.route("/create_bank", methods=["POST"])
@login_required
def create_bank():

    from aes_crypto import encrypt_text

    bank_name = encrypt_text(request.form["bank_name"])

    conn = sqlite3.connect(Config.DATABASE)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO banks (user_id, bank_name) VALUES (?, ?)",
        (current_user.id, bank_name)
    )

    conn.commit()
    conn.close()

    return redirect(url_for("dashboard.finance_home"))


# ==============================
# CREATE BANK ACCOUNT
# ==============================
@dashboard_bp.route("/create_bank_account", methods=["POST"])
@login_required
def create_bank_account():

    from aes_crypto import encrypt_text

    bank_id = request.form["bank_id"]
    name = encrypt_text(request.form["account_name"])
    acc_type = request.form["account_type"]

    conn = sqlite3.connect(Config.DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO bank_accounts (bank_id, account_name, account_type)
    VALUES (?, ?, ?)
    """,(bank_id, name, acc_type))

    conn.commit()
    conn.close()

    return redirect(url_for("dashboard.finance_home"))


# ==============================
# TRANSFER MONEY
# ==============================
@dashboard_bp.route("/transfer_money", methods=["POST"])
@login_required
def transfer_money():
    
    if session.get("breach"):
        return "<h3 style='color:red;'>⚠ Transactions Disabled in Breach Mode</h3>"

    from_account = request.form["from_account"]
    to_account = request.form["to_account"]
    amount = request.form["amount"]

    conn = sqlite3.connect(Config.DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO bank_transactions (from_account, to_account, amount)
    VALUES (?, ?, ?)
    """, (from_account, to_account, amount))

    conn.commit()
    conn.close()

    return redirect(url_for("dashboard.finance_home"))

