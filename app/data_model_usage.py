from data_model.find_songs import FindSongs


fs = FindSongs()

test_vecs = ["be happy  mcferrin", "Fast Chapman", "Uptown Funk  Mars ", "I'm yours Mraz", "Walk like an egyptian bangles", "Manic Monday", "Last Christmas Wham"]

for t in test_vecs:
    print(fs.find_song_entry(t, best_choice=False))

    choice = fs.find_song_entry(t)
    print(choice)
    
    recs = fs.get_recommendations(choice)
    print(recs)
