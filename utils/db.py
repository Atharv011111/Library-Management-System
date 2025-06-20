import sqlite3

DB_NAME = 'library.db'

def init_db():
    try:
        with sqlite3.connect(DB_NAME) as conn:
            c = conn.cursor()
            # Create tables
            c.execute('''CREATE TABLE IF NOT EXISTS books (
                            isbn TEXT PRIMARY KEY,
                            title TEXT,
                            author TEXT,
                            available INTEGER DEFAULT 1
                        )''')
            c.execute('''CREATE TABLE IF NOT EXISTS members (
                            id TEXT PRIMARY KEY,
                            name TEXT,
                            role TEXT
                        )''')
            c.execute('''CREATE TABLE IF NOT EXISTS borrow_history (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            member_id TEXT,
                            isbn TEXT,
                            borrow_date TEXT,
                            return_date TEXT,
                            FOREIGN KEY(member_id) REFERENCES members(id),
                            FOREIGN KEY(isbn) REFERENCES books(isbn)
                        )''')

            # Add late_fee column if missing
            c.execute("PRAGMA table_info(borrow_history)")
            columns = [row[1] for row in c.fetchall()]
            if 'late_fee' not in columns:
                c.execute("ALTER TABLE borrow_history ADD COLUMN late_fee INTEGER DEFAULT 0")
                print("✅ 'late_fee' column added to borrow_history.")

            # Add default admin if not present
            admin_id = 'admin001'
            admin_name = 'Admin'
            c.execute("SELECT id FROM members WHERE id = ? AND role = 'admin'", (admin_id,))
            if not c.fetchone():
                c.execute("INSERT INTO members (id, name, role) VALUES (?, ?, 'admin')", (admin_id, admin_name))
                print(f"✅ Default admin '{admin_name}' added with ID '{admin_id}'.")

    except sqlite3.Error as e:
        print(f"Database initialization error: {e}")
