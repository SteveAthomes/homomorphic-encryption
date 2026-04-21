
import sqlite3
from config import Config


def init_db():
    conn = sqlite3.connect(Config.DATABASE)
    cursor = conn.cursor()

    # ==========================
    # USERS TABLE
    # ==========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # ==========================
    # STORAGE FILES
    # ==========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS files (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        filename TEXT,
        stored_path TEXT,
        uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)

    # ==========================
    # BANKS
    # ==========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS banks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        bank_name TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)

    # ==========================
    # ACCOUNTS
    # ==========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS accounts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        bank_id INTEGER,
        account_name TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(bank_id) REFERENCES banks(id)
    )
    """)

    # ==========================
    # TRANSACTIONS
    # ==========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        from_account INTEGER,
        to_account INTEGER,
        amount BLOB,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(from_account) REFERENCES accounts(id),
        FOREIGN KEY(to_account) REFERENCES accounts(id)
    )
    """)

    # ==========================
    # ANALYTICS DATASETS
    # ==========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS datasets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        dataset_name TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)

    # ==========================
    # DATASET VALUES (ENCRYPTED)
    # ==========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS dataset_values (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        dataset_id INTEGER,
        value BLOB,
        FOREIGN KEY(dataset_id) REFERENCES datasets(id)
    )
    """)
    
    # ==========================
# BANK ACCOUNTS
# ==========================

    cursor.execute("""
CREATE TABLE IF NOT EXISTS bank_accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bank_id INTEGER,
    account_name TEXT,
    account_type TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(bank_id) REFERENCES banks(id)
)
""")

# ==========================
# BANK TRANSACTIONS
# ==========================

    cursor.execute("""
CREATE TABLE IF NOT EXISTS bank_transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    from_account INTEGER,
    to_account INTEGER,
    amount INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(from_account) REFERENCES bank_accounts(id),
    FOREIGN KEY(to_account) REFERENCES bank_accounts(id)
)
""")

    conn.commit()

import sqlite3
from config import Config


def init_db():
    conn = sqlite3.connect(Config.DATABASE)
    cursor = conn.cursor()

    # ==========================
    # USERS TABLE
    # ==========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # ==========================
    # STORAGE FILES
    # ==========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS files (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        filename TEXT,
        stored_path TEXT,
        uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)

    # ==========================
    # BANKS
    # ==========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS banks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        bank_name TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)

    # ==========================
    # ACCOUNTS
    # ==========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS accounts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        bank_id INTEGER,
        account_name TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(bank_id) REFERENCES banks(id)
    )
    """)

    # ==========================
    # TRANSACTIONS
    # ==========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        from_account INTEGER,
        to_account INTEGER,
        amount BLOB,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(from_account) REFERENCES accounts(id),
        FOREIGN KEY(to_account) REFERENCES accounts(id)
    )
    """)

    # ==========================
    # ANALYTICS DATASETS
    # ==========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS datasets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        dataset_name TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)

    # ==========================
    # DATASET VALUES (ENCRYPTED)
    # ==========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS dataset_values (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        dataset_id INTEGER,
        value BLOB,
        FOREIGN KEY(dataset_id) REFERENCES datasets(id)
    )
    """)
    
    # ==========================
# BANK ACCOUNTS
# ==========================

    cursor.execute("""
CREATE TABLE IF NOT EXISTS bank_accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bank_id INTEGER,
    account_name TEXT,
    account_type TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(bank_id) REFERENCES banks(id)
)
""")

# ==========================
# BANK TRANSACTIONS
# ==========================

    cursor.execute("""
CREATE TABLE IF NOT EXISTS bank_transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    from_account INTEGER,
    to_account INTEGER,
    amount INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(from_account) REFERENCES bank_accounts(id),
    FOREIGN KEY(to_account) REFERENCES bank_accounts(id)
)
""")

    conn.commit()

    conn.close()