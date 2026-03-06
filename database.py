import psycopg2

conn = None #if connection fails, conn is NOne.

# Connect to the photon datatbase
try : 
  conn = psycopg2.connect(
    dbname="photon",
    # user="student",
    # password="student",
    # host="localhost"
  )

  cursor = conn.cursor()

  cursor.execute("INSERT INTO players VALUES (2, 'ReaClark', 1)")
  cursor.execute("INSERT INTO players VALUES (3, 'IndJones', 2)")

  cursor.execute("SELECT * FROM players")
  records = cursor.fetchall()
  for row in records:
    print(row)


except Exception as e:
  print(f"An error occurred: {e}")
  conn = None #connection safety

def close_connection():
  if conn: 
    conn.close()
    print("Database connection closed")

#Functions for adding players: 
def playerIdExist(player_id):
    if not conn:
        return None
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT codename FROM players WHERE player_id = %s", (player_id,))
            result = cursor.fetchone()
            return result[0] if result else None
    except Exception as e:
        print(f"Error checking player ID: {e}")
        return None

def insert_player(player_id, codename, equipment_id):
    if not conn:
        return False #explicit result
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO players (player_id, codename, equipment_id) VALUES (%s, %s, %s)",
                (player_id, codename, equipment_id)
            )
            conn.commit()
            print(f"Inserted player {player_id} - {codename} - {equipment_id}")
            return True #success!
    except Exception as e:
        print(f"Error inserting player: {e}")
        return False #again, explicit result



