import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

DB_PATH = "/path/.db"

conn = sqlite3.connect(DB_PATH)

# get a few tracks and see the table
def get_tracks():  
    tracks = pd.read_sql_query(
        """
        SELECT TRACK_ID, TYPE, ENTRY_GATE, EXIT_GATE, TRAVELED_DIST, AVG_SPEED
        FROM TRACKS
        ORDER BY RANDOM()
        LIMIT 5
        """, 
        conn)
    print(tracks)
    return tracks

# query a trajectory in a track
def get_trajectory(tracks):
    track_ids = tuple(tracks['TRACK_ID'].tolist())
    traj = pd.read_sql_query(
        f"""
        SELECT TRACK_ID, TIME, X, Y, SPEED
        FROM TRAJECTORIES_0
        WHERE TRACK_ID IN {track_ids}
        ORDER BY TRACK_ID, TIME
        """, 
        conn)
    print(traj)
    return traj

def main():
    tracks = get_tracks()
    traj = get_trajectory(tracks)
    plt.figure(figsize=(6,6))
    
    for tid, df in traj.groupby('TRACK_ID'):
        plt.plot(df['X'], df['Y'], label=f'Track {tid}')
        
    plt.gca().set_aspect('equal')
    plt.title('Sample agent trajectories (UTM Zone 17T)')
    plt.xlabel('X (meters)')
    plt.ylabel('Y (meters)')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()
