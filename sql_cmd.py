import getpass
import psycopg2

p = getpass.getpass('>> Password:')
conn = psycopg2.connect("host=localhost dbname=postgres user=postgres password={}".format(p))
cur = conn.cursor()
s = """UPDATE user_accounts 
        SET 
        "user_descrip" = 'Lorem ipsum dolor',
        "user_total_bank" = 777.0
         WHERE "user_name" = 'Fulano de Tal' 
         ;"""
cur.execute(s)
conn.commit()
