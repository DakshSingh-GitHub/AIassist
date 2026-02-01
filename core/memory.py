import sqlite3
import os
import time

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, 'data', 'user_memory.db')

def init_db():
	conn = sqlite3.connect(DB_PATH)
	cur = conn.cursor()

	cur.execute("""
	        CREATE TABLE IF NOT EXISTS intent_usage (
	            intent TEXT PRIMARY KEY,
	            count INTEGER,
	            last_used REAL
	        )
	""")

	cur.execute("""
		CREATE TABLE IF NOT EXISTS auto_confirm(
			intent TEXT PRIMARY KEY
		)
	""")

	conn.commit()
	conn.close()

def record_intent(intent):
	conn = sqlite3.connect(DB_PATH)
	cur = conn.cursor()

	cur.execute("SELECT count FROM intent_usage WHERE intent=?", (intent,))
	row = cur.fetchone()

	if row:
		cur.execute("UPDATE intent_usage SET count=count+1, last_used=? WHERE intent=?", (time.time(), intent))
	else:
		cur.execute("INSERT INTO intent_usage VALUES (?, ?, ?)", (intent, 1, time.time()))

	conn.commit()
	conn.close()

def get_intent_count(intent: str):
	conn = sqlite3.connect(DB_PATH)
	cur = conn.cursor()

	cur.execute("SELECT count FROM intent_usage WHERE intent=?", (intent,))
	row = cur.fetchone()
	conn.close()

	return row[0] if row else 0

def get_most_used_intent(intents: list):
	conn = sqlite3.connect(DB_PATH)
	cur = conn.cursor()

	placeholders = ",".join("?" for _ in intents)
	query = f"SELECT intent FROM intent_usage WHERE intent IN ({placeholders}) ORDER BY count DESC LIMIT 1"
	cur.execute(query, intents)
	row = cur.fetchone()
	conn.close()

	return row[0] if row else None

def allow_auto_confirmation(intent: str):
	conn = sqlite3.connect(DB_PATH)
	cur = conn.cursor()

	cur.execute("INSERT OR IGNORE INTO auto_confirm VALUES (?)", (intent,))
	conn.commit()
	conn.close()

def is_auto_confirmed(intent: str):
	conn = sqlite3.connect(DB_PATH)
	cur = conn.cursor()
	cur.execute("""
	        SELECT intent FROM auto_confirm WHERE intent = ?
	    """, (intent,))
	row = cur.fetchone()
	conn.close()
	return row is not None

def remove_auto_confirm(intent: str):
	conn = sqlite3.connect(DB_PATH)
	cur = conn.cursor()
	cur.execute("""
	        DELETE FROM auto_confirm WHERE intent = ?
	    """, (intent,))
	conn.commit()
	conn.close()

def clear_all_autoconfirm():
	conn = sqlite3.connect(DB_PATH)
	cur = conn.cursor()
	cur.execute("""
	        DELETE FROM auto_confirm
	    """)
	conn.commit()
	conn.close()

def get_all_autoconfirms():
	conn = sqlite3.connect(DB_PATH)
	cur = conn.cursor()
	cur.execute("""
	        SELECT intent FROM auto_confirm
	    """)
	rows = cur.fetchall()
	conn.close()
	return [row[0] for row in rows]
