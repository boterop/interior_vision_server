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

    def get_assistant_memory(self, assistant_id):
        self.cursor.execute(
            "SELECT memory FROM assistants WHERE id=%s;", (assistant_id, ))
        result = self.cursor.fetchone()[0]
        self.connection.close()
        return json.loads(result)

    def save_memory(self, assistant_id, memory):
        self.cursor.execute(
            "UPDATE assistants SET memory = %s WHERE id=%s;", (json.dumps(memory), assistant_id))
        self.connection.commit()
        self.connection.close()

    def create_memory(self, memory):
        self.cursor.execute(
            "INSERT INTO assistants (memory) VALUES (%s) RETURNING id;", (json.dumps(memory),))
        result = self.cursor.fetchone()[0]
        self.connection.commit()
        self.connection.close()
        return result
