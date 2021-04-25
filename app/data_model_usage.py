from pandas import Series
from data_model.find_songs import FindSongs

FEATURES = ['name', 'artists', 'popularity']

get_song_info = lambda x:  x[FEATURES].to_list()


def display_heading(x):
    print(x)
    print('-'*len(x))

def display_song_entry(x, border=True):
    info = get_song_info(x)
    print(info)

def display_song_entries(x):
    entries = [get_song_info(y) for _,y in x.iterrows()]
    for entry in entries:
        print(entry)

fs = FindSongs()

test_vecs = ["Never gonna give you up astley", "be happy  mcferrin", "Fast Chapman", "Uptown Funk  Mars ", "I'm yours Mraz", "Walk like an egyptian bangles", "Manic Monday", "Last Christmas Wham"]

for t in test_vecs:

    heading = f"Best 5 matches for '{t}'"
    display_heading(heading)
    display_song_entries(fs.find_song_entry(t, best_choice=False))
    print('\n')
    
    heading = f"Best match for '{t}'"
    display_heading(heading)
    choice = fs.find_song_entry(t)
    display_song_entry(choice)
    print('\n')
    
    heading = f'Recommendations based on choice of  {get_song_info(choice)}'
    display_heading(heading)
    display_song_entries(fs.get_recommendations(choice))
    print('='*80)
    print('\n')

