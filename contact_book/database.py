import sqlite3
from datetime import datetime
import uuid

DB_NAME = "contact.db"


# def connect_db():
#     return sqlite3.connect(DB_NAME) 

def connect_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_db():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contacts(
                   id TEXT PRIMARY KEY,
                   name TEXT NOT NULL,
                   phone TEXTN NOT NULL UNIQUE,
                   email TEXT,
                   address TEXT,
                   created_at TIMESTAMP
            )
        """)
    
    conn.commit()
    conn.close()


def add_contact(name, phone, email, address):
    conn = connect_db()
    cursor = conn.cursor()


    try:
        cursor.execute("""
            INSERT INTO contacts (id, name, phone, email, address, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """,(
            str(uuid.uuid4()),
            name,
            phone,
            email,
            address,
            datetime.now()
        )

        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False #phone duplicate 
    finally:
        conn.close()

def get_contacts(order_by="created_at DESC"):
    conn = connect_db()
    cursor = conn.cursor()

    query = f"SELECT * FROM contacts ORDER BY {order_by}"
    cursor.execute(query)
    rows = cursor.fetchall()

    conn.close()
    return rows

def delete_contact(contact_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM contacts WHERE id = ?", (contact_id,))
    conn.commit()
    conn.close()

def update_contact(contact_id, name, phone, email, address):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            UPDATE contacts
            SET name=?, phone=?, email=?, address=?
            WHERE id=?
        """, (name, phone, email, address, contact_id))

        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def search_contacts(keyword):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM contacts
        WHERE name LIKE ? OR phone LIKE ?
        ORDER BY created_at DESC
    """, (f"%{keyword}%", f"%{keyword}%"))

    rows = cursor.fetchall()
    conn.close()
    return rows


if __name__ == "__main__":
    initialize_db()
    print("Database ready")