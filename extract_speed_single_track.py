track_id = 1
output_excel = f'data/speed_track{track_id}.xlsx'

import sqlite3
import pandas as pd

DB_PATH = "db_files\intsc_data_769.db"

conn = sqlite3.connect(DB_PATH)


traj = pd.read_sql_query(
    f"""
    SELECT TRACK_ID, TIME, SPEED_1
    FROM TRAJECTORIES_0769
    WHERE TRACK_ID = {track_id}
    ORDER BY TRACK_ID, TIME
    """, 
    conn)

traj["SPEED_2"] = traj["SPEED_1"]

conn.close()
traj.to_excel(output_excel, index=False)