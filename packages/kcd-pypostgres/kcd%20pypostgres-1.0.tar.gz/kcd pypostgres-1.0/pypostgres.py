import psycopg2
import fire
from prettytable import PrettyTable
import xlsxwriter
import sys

def db_connect(host, database, user, password,port=5432):
    print("Connecting to database...")
    conn = psycopg2.connect(
        host=host,
        port=port,
        database=database,
        user=user,
        password=password
    )    
    cur = conn.cursor()
    return conn, cur

def find_columns(host, database, user, password, column_name, port=5432):
    conn, cur = db_connect(host, database, user, password,port)
    
    cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_name")
    tables = cur.fetchall()

    for table in tables:
        cur.execute("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = '"+table[0]+"'")
        columns = cur.fetchall()
        
        
        for column in columns:
            
            if column[0].find(column_name)>=0:
                print("FOUND {} - {}".format(table, column[0]))

    
    conn.close()

def list_tables(host, database, user, password, pattern=None, port=5432, export_excel="", verbose=False):
    conn, cur = db_connect(host, database, user, password,port)
    cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_name")
    tables = cur.fetchall()
    print("Tables:")
  

    if export_excel != "":
        excel_file = export_excel
        workbook = xlsxwriter.Workbook(excel_file)
        worksheet = workbook.add_worksheet()

        row = 0
        col = 0

        worksheet.write(row, col, "table name")
        row = 1
        for table in tables:
            worksheet.write(row, col, table[0])
            row += 1
        
        workbook.close()
    else:
        if not verbose:
            if not pattern:
                for table in tables:
                    print("\t"+table[0])
            else:
                for table in tables:
                    if pattern in table[0]:
                        print("\t"+table[0])
        else:
            if not pattern:
                for table in tables:
                    cur.execute("SELECT tc.constraint_name, tc.table_name, kcu.column_name, ccu.table_name AS foreign_table_name, ccu.column_name AS foreign_column_name FROM information_schema.table_constraints AS tc JOIN information_schema.key_column_usage AS kcu ON tc.constraint_name = kcu.constraint_name JOIN information_schema.constraint_column_usage AS ccu ON ccu.constraint_name = tc.constraint_name WHERE constraint_type = 'FOREIGN KEY' AND tc.table_name='"+table[0]+"'")
                    foreign_keys = cur.fetchall()
                    
                    if len(foreign_keys)==0:
                        print("\t"+table[0]+" LOOKUP TABLE")
                    else:
                        print("\t"+table[0]+" COMPLEX TABLE")
                   
            else:
                for table in tables:
                    if pattern in table[0]:
                        cur.execute("SELECT tc.constraint_name, tc.table_name, kcu.column_name, ccu.table_name AS foreign_table_name, ccu.column_name AS foreign_column_name FROM information_schema.table_constraints AS tc JOIN information_schema.key_column_usage AS kcu ON tc.constraint_name = kcu.constraint_name JOIN information_schema.constraint_column_usage AS ccu ON ccu.constraint_name = tc.constraint_name WHERE constraint_type = 'FOREIGN KEY' AND tc.table_name='"+table[0]+"'")
                        foreign_keys = cur.fetchall()
                        
                        if len(foreign_keys)==0:
                            print("\t"+table[0]+" LOOKUP TABLE")
                        else:
                            print("\t"+table[0]+" COMPLEX TABLE")
    conn.close()

def get_foreign_keys(host, database, user, password, table, port=5432):
    conn, cur = db_connect(host, database, user, password,port)
    cur.execute("SELECT tc.constraint_name, tc.table_name, kcu.column_name, ccu.table_name AS foreign_table_name, ccu.column_name AS foreign_column_name FROM information_schema.table_constraints AS tc JOIN information_schema.key_column_usage AS kcu ON tc.constraint_name = kcu.constraint_name JOIN information_schema.constraint_column_usage AS ccu ON ccu.constraint_name = tc.constraint_name WHERE constraint_type = 'FOREIGN KEY' AND tc.table_name='"+table+"'")
    foreign_keys = cur.fetchall()
    print("Foreign Keys:")
    for foreign_key in foreign_keys:
        print("\t"+foreign_key[0]+" "+foreign_key[1]+" "+foreign_key[2]+" "+foreign_key[3]+" "+foreign_key[4])
    conn.close()

def describe_table(host, database, user, password, table, port=5432):
    conn, cur = db_connect(host, database, user, password,port)
    cur.execute("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = '"+table+"'")
    columns = cur.fetchall()
    print("Columns:")
    
    for column in columns:
        print("\t"+column[0]+" "+column[1])

    
    cur.execute("SELECT tc.constraint_name, tc.table_name, kcu.column_name, ccu.table_name AS foreign_table_name, ccu.column_name AS foreign_column_name FROM information_schema.table_constraints AS tc JOIN information_schema.key_column_usage AS kcu ON tc.constraint_name = kcu.constraint_name JOIN information_schema.constraint_column_usage AS ccu ON ccu.constraint_name = tc.constraint_name WHERE constraint_type = 'FOREIGN KEY' AND tc.table_name='"+table+"'")
    foreign_keys = cur.fetchall()
    print("Foreign Keys:")
    if len(foreign_keys)==0:
        print("\tLookup tables")
    for foreign_key in foreign_keys:
        print("\t"+foreign_key[0]+" "+foreign_key[1]+" "+foreign_key[2]+" "+foreign_key[3]+"("+foreign_key[4]+")")
     
    conn.close()

def make_report(host, database, user, password, port=5432):
    pass

def prettify_results(headers, result):
    table = PrettyTable(headers)
    for row in result:
        table.add_row(row)
    sys.stdout.buffer.write(str(table).encode('utf-8'))


    
def execute_select(host, database, user, password, query, port=5432):
    conn, cur = db_connect(host, database, user, password,port)
    cur.execute(query)
    results = cur.fetchall()
    print("Results:")
    
    prettify_results([desc[0] for desc in cur.description],results)
    conn.close()

def stdin_select(host, database, user, password,port=5432):
    """Execute a select from stdin"""

    conn, cur = db_connect(host, database, user, password,port)
    query = sys.stdin.read()
    cur.execute(query)
    results = cur.fetchall()
    print("Results:")
    
    prettify_results([desc[0] for desc in cur.description],results)
    conn.close()

def stdin_query(host, database, user, password,port=5432):
    """Execute a query from stdin"""

    conn, cur = db_connect(host, database, user, password,port)
    query = sys.stdin.read()
    cur.execute(query)
    conn.commit()
    num_rows = cur.rowcount
    print(f"{num_rows} righe modificate.")
    
    
    conn.close()


def execute_query(host, database, user, password, query, port=5432):
    conn, cur = db_connect(host, database, user, password,port)
    cur.execute(query)


    
    conn.commit()
    num_rows = cur.rowcount
    print(f"{num_rows} righe modificate.")
    
    
    conn.close()


def search_string(host, database, user, password,search_string, port=5432, verbose=False):
    conn, cur = db_connect(host, database, user, password, port)
    
    
    cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
    tables = cur.fetchall()
    for table in tables:
        table_name = table[0]
        if verbose:
            print("Reading from {}".format(table_name))
        cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name = %s", (table_name,))
        columns = cur.fetchall()
        column_names = [column[0] for column in columns]

        search_query = "SELECT * FROM {} WHERE ".format(table_name)
        search_conditions = ["{}::text ILIKE %s".format(column_name) for column_name in column_names]
        search_query += " OR ".join(search_conditions)

        # Esecuzione della query per cercare la stringa in tutte le colonne della tabella corrente
        try:
            query = search_query.replace(r"%s","'%{}%'".format(search_string))
            cur.execute(query)
            rows = cur.fetchall()
            for row in rows:
                print("[{}] - {}".format(table_name, row))
        except Exception as e:
            print("Skipping invalid query on: {}".format(table_name))
            conn.rollback()
            conn, cur = db_connect(host, database, user, password, port)
    cur.close()
    conn.close()

def main():
    
    fire.Fire({
        'list_tables': list_tables,
        'describe_table': describe_table,
        'execute_select': execute_select,
        'search_string': search_string,
        'execute_query': execute_query,
        'stdin_select': stdin_select,
        'stdin_query': stdin_query,
        'report': make_report,
        'find_columns': find_columns
    })


