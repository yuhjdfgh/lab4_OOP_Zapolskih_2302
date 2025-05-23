import psycopg2

def get_connection():
    return psycopg2.connect(dbname="ooptry3", user="postgres", password="124512451245", host="localhost", port="5432")

def create(table, params):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO art_object (title, author) VALUES (%s, %s) RETURNING id", (params[0], params[1]))
        art_id = cur.fetchone()[0]
        
        if table == 'painting':
            cur.execute("INSERT INTO painting (art_object_id, size, type_color) VALUES (%s, %s, %s)", (art_id, int(params[2]), params[3]))
        else:
            cur.execute("INSERT INTO sculpture (art_object_id, weight, material) VALUES (%s, %s, %s)", (art_id, float(params[2]), params[3]))
        conn.commit()
        return art_id
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
        conn.close()

def read(table, id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        if table == 'painting':
            cur.execute("""
                SELECT a.id, a.title, a.author, p.size, p.type_color 
                FROM art_object a
                JOIN painting p ON a.id = p.art_object_id
                WHERE a.id = %s
            """, (id,))
        else:
            cur.execute("""
                SELECT a.id, a.title, a.author, s.weight, s.material 
                FROM art_object a
                JOIN sculpture s ON a.id = s.art_object_id
                WHERE a.id = %s
            """, (id,))  
        return cur.fetchone()
    finally:
        cur.close()
        conn.close()

def update(table, params):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("UPDATE art_object SET title = %s, author = %s WHERE id = %s", (params[1], params[2], params[0]))
        if table == 'painting':
            cur.execute("UPDATE painting SET size = %s, type_color = %s WHERE art_object_id = %s", (int(params[3]), params[4], params[0]))
        else:
            cur.execute("UPDATE sculpture SET weight = %s, material = %s WHERE art_object_id = %s", (float(params[3]), params[4], params[0]))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
        conn.close()

def delete(table, id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        if table == 'painting':
            cur.execute("DELETE FROM painting WHERE art_object_id = %s", (id,))
        else:
            cur.execute("DELETE FROM sculpture WHERE art_object_id = %s", (id,))
        cur.execute("DELETE FROM art_object WHERE id = %s", (id,))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
        conn.close()

def get_all_paintings():
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT a.id, a.title, a.author, p.size, p.type_color 
                FROM art_object a
                JOIN painting p ON a.id = p.art_object_id
                ORDER BY a.id
            """)
            return cur.fetchall()
    finally:
        conn.close()

def get_all_sculptures():
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT a.id, a.title, a.author, s.weight, s.material 
                FROM art_object a
                JOIN sculpture s ON a.id = s.art_object_id
                ORDER BY a.id
            """)
            return cur.fetchall()
    finally:
        conn.close()
