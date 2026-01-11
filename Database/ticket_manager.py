import sqlite3
import os
from datetime import datetime

BASE_DIR = os.path.dirname(__file__)
DB_NAME = os.path.join(BASE_DIR, "tickets.db")


def create_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_name TEXT NOT NULL,
        issue TEXT NOT NULL,
        priority TEXT NOT NULL,
        status TEXT NOT NULL,
        os TEXT,
        processor TEXT,
        disk_free TEXT,
        ip_address TEXT,
        internet_status TEXT,
        created_at TEXT NOT NULL
    )
""")

    conn.commit()
    conn.close()


def create_ticket(user_name, issue, priority, diagnostics=None):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    os_name = diagnostics.get("OS") if diagnostics else None
    processor = diagnostics.get("Processor") if diagnostics else None
    disk_free = diagnostics.get("Disk Free (GB)") if diagnostics else None
    ip_addr = diagnostics.get("IP Address") if diagnostics else None
    internet = diagnostics.get("Internet") if diagnostics else None

    cursor.execute("""
        INSERT INTO tickets (
            user_name, issue, priority, status,
            os, processor, disk_free, ip_address, internet_status, created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        user_name,
        issue,
        priority,
        "Open",
        os_name,
        processor,
        str(disk_free),
        ip_addr,
        internet,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()


def view_tickets():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tickets")
    tickets = cursor.fetchall()

    conn.close()
    return tickets

def update_ticket_status(ticket_id, new_status):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE tickets
        SET status = ?
        WHERE id = ?
    """, (new_status, ticket_id))

    conn.commit()
    conn.close()

def search_tickets_by_user(user_name):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM tickets
        WHERE user_name LIKE ?
    """, (f"%{user_name}%",))

    results = cursor.fetchall()
    conn.close()
    return results


def filter_tickets_by_status(status):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM tickets
        WHERE status = ?
    """, (status,))

    results = cursor.fetchall()
    conn.close()
    return results