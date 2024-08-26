
from dotenv import load_dotenv
import os
import psycopg2
from llama_index.core.tools import FunctionTool
from pydantic import Field

load_dotenv()
conn = psycopg2.connect(database = "LLM_SQL", 
                        user = os.environ['POSTGRES_USERNAME'], 
                        host= 'localhost',
                        password = os.environ['POSTGRES_PASSWORD'],
                        port = 5432)


cursor = conn.cursor()
def add_state(stateName: str) -> str:
    """Tool to ADD state in the Table"""
    try:
        cursor.execute("INSERT INTO state(state) VALUES (%s)", (stateName,))
        conn.commit()
        return "Query Successful"
    except (Exception, psycopg2.Error) as error:
        conn.rollback()
        return "Error: " + str(error)

def update_state(oldStateName: str = Field(description="State name to be changed"), 
                 newStateName: str = Field(description="New State Name")) -> str:
    """Tool to UPDATE state in the Table"""
    try:
        cursor.execute("UPDATE state SET state = %s WHERE state = %s", (newStateName, oldStateName))
        conn.commit()
        return "Query Successful"
    except (Exception, psycopg2.Error) as error:
        conn.rollback()
        return "Error: " + str(error)

def read_states() -> str:
    """Tool to READ all states from the Table"""
    try:
        cursor.execute("SELECT state FROM state")
        states = cursor.fetchall()
        return "States: " + ', '.join([state[0] for state in states])
    except (Exception, psycopg2.Error) as error:
        return "Error: " + str(error)

def delete_state(stateName: str) -> str:
    """Tool to DELETE a state from the Table"""
    try:
        cursor.execute("DELETE FROM state WHERE state = %s", (stateName,))
        conn.commit()
        return "Query Successful"
    except (Exception, psycopg2.Error) as error:
        conn.rollback()
        return "Error: " + str(error)


add_tool = FunctionTool.from_defaults(fn=add_state)
update_tool = FunctionTool.from_defaults(fn=update_state)
delete_tool = FunctionTool.from_defaults(fn=delete_state)
read_tool = FunctionTool.from_defaults(fn=read_states)

all_tools  = [add_tool, update_tool, delete_tool, read_tool]