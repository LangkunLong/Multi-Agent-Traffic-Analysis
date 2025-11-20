import sqlite3
import pandas as pd

# extracting the average speed and tangential acceleartion of all the cars along a specific route
# picking entry and exit to be west_entry_gate to east_exit_gate (or the other way around I could not determine that)

db_files = [f'db_files\intsc_data_{i}.db' for i in range(769, 786)]
ENTRY_GATE = 126
EXIT_GATE = 130
output_excel = 'multi_agent_speed_accel_data.xlsx'

all_data = []

for db_file in db_files:
    
    print(f"current file: {db_file}")
    conn = sqlite3.connect(db_file)
    
    df = pd.read_sql_query(
        """
        SELECT TRACK_ID, ENTRY_GATE, EXIT_GATE, AVG_SPEED_TOTAL, AVG_TANGENTIAL_ACC_TOTAL
        FROM TRAJECTORY_MOVEMENTS
        WHERE TYPE = 'Car' AND ENTRY_GATE = {ENTRY_GATE} AND EXIT_GATE = {EXIT_GATE}
        """,
        conn
    )
    
    # add a column to track which file this came from (769-785)
    df['SOURCE_FILE'] = db_file
    
    all_data.append(df)
    conn.close()

# combine everything together
if all_data:
    final_df = pd.concat(all_data, ignore_index=True)

    # convert avg speed from km/h to m/s
    final_df['AVG_SPEED_TOTAL'] = final_df['AVG_SPEED_TOTAL'] / 3.6

    output_columns = [
        'TRACK_ID', 
        'AVG_SPEED_TOTAL', 
        'AVG_TANGENTIAL_ACC_TOTAL',
        'SOURCE_FILE'
    ]
    
    final_df[output_columns].to_excel(output_excel, index=False)
    print("Finished Extracting")
else:
    print("Something wrong with SQL query")