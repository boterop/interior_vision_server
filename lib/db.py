import psycopg2
import os
import json


class DB:
    def __init__(self):
        try:
            connection = psycopg2.connect(database=os.getenv("DATABASE"),
                                          user=os.getenv("POSTGRES_USER"),
                                          host=os.getenv("POSTGRES_HOST"),
                                          password=os.getenv(
                                              "POSTGRES_PASSWORD"),
                                          port=5432)

            self.connection = connection
            self.cursor = connection.cursor()
        except Exception as e:
            print("ERROR creating connection: {}".format(e))

    def get_assistant_memory(self, assistant_id, assistant_key):
        self.cursor.execute(
            "SELECT memory FROM assistants WHERE id=%s AND key=%s;", (assistant_id, assistant_key))
        result = self.cursor.fetchone()[0]
        return json.loads(result)

    def get_free_assistant(self):
        self.cursor.execute(
            "SELECT id FROM assistants WHERE key='';")
        result = self.cursor.fetchone()
        return result

    def save_memory(self, assistant_id, assistant_key, memory):
        self.cursor.execute(
            "UPDATE assistants SET memory = %s WHERE id=%s AND key=%s;", (json.dumps(memory), assistant_id, assistant_key))
        self.connection.commit()

    def update_key(self, assistant_id, assistant_key):
        self.cursor.execute(
            "UPDATE assistants SET key = %s WHERE id=%s;", (assistant_key, assistant_id))
        self.connection.commit()

    def create_memory(self, assistant_key, memory):
        self.cursor.execute(
            "INSERT INTO assistants (memory, key) VALUES (%s, %s) RETURNING id;", (json.dumps(memory), assistant_key))
        result = self.cursor.fetchone()[0]
        self.connection.commit()
        return result

    def close(self):
        self.connection.close()
