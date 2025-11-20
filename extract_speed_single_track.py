track_id = 1
output_excel = f'data/speed_track{track_id}.xlsx'

import sqlite3
import pandas as pd

DB_PATH = "db_files\intsc_data_769.db"

conn = sqlite3.connect(DB_PATH)


traj = pd.read_sql_query(
    f"""
    SELECT TRACK_ID, TIME, SPEED
    FROM TRAJECTORIES_0769
    WHERE TRACK_ID = {track_id}
    ORDER BY TRACK_ID, TIME
    """, 
    conn)
conn.close()

traj["SPEED_0"] = traj["SPEED"]
traj["SPEED_1"] = traj["SPEED"].shift(1)
traj.dropna()
print(traj)

traj.to_excel(output_excel, index=False)