import psycopg2

def db_insert(data_to_insert):
    try:
        # Establish the connection
        conn = psycopg2.connect(
            dbname="defaultdb", 
            user="doadmin", 
            password="AVNS_Lke4NPamARm9-4X7IQu", 
            host="db-postgresql-nyc3-10726-do-user-15531455-0.c.db.ondigitalocean.com", 
            port="25060"
        )
    
        # Create a cursor object
        cur = conn.cursor()
    
        insert_query = """
                        INSERT INTO public.user_details (email, username, password, date_joined)
                        VALUES (%s, %s, %s, %s)
                        """
        # Execute the query
        cur.execute(insert_query, data_to_insert)
    
        # Commit the transaction
        conn.commit()
        cur.close()
        conn.close()
    

    except Exception as e:
        print(f"An error occurred: {e}")


