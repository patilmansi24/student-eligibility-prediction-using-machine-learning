from config.database import get_connection

conn = get_connection()
print("✅ Connected to Supabase PostgreSQL successfully!")

cursor = conn.cursor()
cursor.execute("SELECT NOW();")
print("Current Timestamp:", cursor.fetchone())
conn.close()
