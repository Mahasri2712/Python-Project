import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox

# Sample Songs Data
songs_data = {
    "song_id": [1, 2, 3, 4, 5],
    "title": ["Song A", "Song B", "Song C", "Song D", "Song E"],
    "artist": ["Artist 1", "Artist 2", "Artist 1", "Artist 3", "Artist 4"],
    "genre": ["Pop", "Rock", "Pop", "Jazz", "Rock"]
}

# Sample User Interaction Data
user_data = {
    "user_id": [101, 102, 101, 103, 102, 103, 104, 105, 104],
    "song_id": [1, 2, 2, 3, 4, 1, 3, 5, 2],
    "rating": [5, 4, 3, 5, 2, 4, 5, 3, 4]
}

# Create DataFrames
songs_df = pd.DataFrame(songs_data)
user_df = pd.DataFrame(user_data)

# Popularity-Based Recommendation
def get_popular_songs():
    popularity_df = user_df.groupby('song_id')['rating'].mean().reset_index()
    popularity_df = popularity_df.merge(songs_df, on='song_id')
    popular_songs = popularity_df.sort_values('rating', ascending=False)
    return popular_songs[['title', 'artist', 'rating']]

# Collaborative Filtering Recommendation
# Collaborative Filtering Recommendation
def recommend_songs(user_id):
    try:
        # Create the user-song rating matrix
        user_song_matrix = user_df.pivot(index='user_id', columns='song_id', values='rating').fillna(0)
        
        # Check if the user exists in the dataset
        if user_id not in user_song_matrix.index:
            return pd.DataFrame([], columns=['title', 'artist', 'genre'])

        # Calculate user similarity using Pearson correlation
        user_similarity = user_song_matrix.corr(method='pearson')

        # Get similar users
        if user_id not in user_similarity.columns:
            return pd.DataFrame([], columns=['title', 'artist', 'genre'])

        similar_users = user_similarity[user_id].sort_values(ascending=False)[1:]  # Exclude self
        similar_users_ids = similar_users[similar_users > 0].index

        if similar_users_ids.empty:
            return pd.DataFrame([], columns=['title', 'artist', 'genre'])

        # Aggregate song ratings from similar users
        recommended_songs = user_song_matrix.loc[similar_users_ids].sum(axis=0).sort_values(ascending=False)
        recommended_songs = recommended_songs[recommended_songs > 0]  # Filter out zero scores

        # Exclude songs already rated by the user
        user_rated_songs = user_song_matrix.loc[user_id]
        recommended_songs = recommended_songs[~recommended_songs.index.isin(user_rated_songs[user_rated_songs > 0].index)]

        # Merge recommendations with song details
        if recommended_songs.empty:
            return pd.DataFrame([], columns=['title', 'artist', 'genre'])

        recommended_songs = recommended_songs.reset_index().rename(columns={0: 'score'})
        recommended_songs = recommended_songs.merge(songs_df, left_on='song_id', right_on='song_id')
        return recommended_songs[['title', 'artist', 'genre']]
    except Exception as e:
        print(f"Error in recommendation: {e}")
        return pd.DataFrame([], columns=['title', 'artist', 'genre'])
# Content-Based Filtering Recommendation
def recommend_by_genre(liked_song_id):
    if liked_song_id not in songs_df['song_id'].values:
        return pd.DataFrame([], columns=['title', 'artist', 'genre'])

    genre = songs_df.loc[songs_df['song_id'] == liked_song_id, 'genre'].values[0]
    similar_songs = songs_df[songs_df['genre'] == genre]
    return similar_songs[['title', 'artist', 'genre']]

# Tkinter GUI
def create_gui():
    def show_popularity():
        result = get_popular_songs()
        display_results(result)

    def show_collaborative():
        try:
            user_id = int(user_id_entry.get())
            result = recommend_songs(user_id)
            if result.empty:
                messagebox.showinfo("Info", f"No recommendations found for User ID {user_id}. Try a different ID or add more data.")
            else:
                display_results(result)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid User ID.")


    def show_content_based():
        try:
            song_id = int(song_id_entry.get())
            result = recommend_by_genre(song_id)
            if result.empty:
                messagebox.showinfo("Info", f"No recommendations found for Song ID {song_id}.")
            else:
                display_results(result)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid Song ID.")

    def display_results(result):
        for widget in result_frame.winfo_children():
            widget.destroy()

        if result.empty:
            tk.Label(result_frame, text="No Results", font=("Arial", 12)).pack()
        else:
            tree = ttk.Treeview(result_frame, columns=list(result.columns), show='headings', height=10)
            for col in result.columns:
                tree.heading(col, text=col)
                tree.column(col, anchor='center')

            for index, row in result.iterrows():
                tree.insert("", "end", values=list(row))

            tree.pack(fill='both', expand=True)

    # Main window
    root = tk.Tk()
    root.title("Music Recommendation System")

    # Frames
    input_frame = tk.Frame(root, pady=10)
    input_frame.pack()

    result_frame = tk.Frame(root, pady=10)
    result_frame.pack(fill='both', expand=True)

    # Popularity-Based Recommendation Button
    tk.Button(input_frame, text="Popular Songs", command=show_popularity, width=20).grid(row=0, column=0, padx=10)

    # Collaborative Filtering Input
    tk.Label(input_frame, text="User ID:").grid(row=0, column=1, padx=10)
    user_id_entry = tk.Entry(input_frame, width=10)
    user_id_entry.grid(row=0, column=2, padx=10)
    tk.Button(input_frame, text="Recommend for User", command=show_collaborative, width=20).grid(row=0, column=3, padx=10)

    # Content-Based Filtering Input
    tk.Label(input_frame, text="Song ID:").grid(row=1, column=1, padx=10)
    song_id_entry = tk.Entry(input_frame, width=10)
    song_id_entry.grid(row=1, column=2, padx=10)
    tk.Button(input_frame, text="Recommend by Genre", command=show_content_based, width=20).grid(row=1, column=3, padx=10)

    # Run the application
    root.mainloop()

# Run GUI
create_gui()
