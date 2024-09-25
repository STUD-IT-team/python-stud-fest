import psycopg2
import csv

CSV_FILE = 'file/members.csv'

def export_members_to_csv():
    conn = None
    try:
        conn = psycopg2.connect(
            dbname="bauman_festival_bot",
            user="admin",
            password="admin",
            host="pgrrs",
            port="5432"
        )
        cur = conn.cursor()

        cur.execute("SELECT tg, name, group_name FROM member")

        rows = cur.fetchall()

        with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            
            writer.writerow(['id', 'tg', 'name', 'group_name'])
            
            writer.writerows(rows)

        print(f"Data successfully exported to {CSV_FILE}")

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
    finally:
        if conn is not None:
            conn.close()

export_members_to_csv()
