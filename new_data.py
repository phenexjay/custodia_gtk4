import pickle
import snippet
import category

data = ["Berichtsheft", [category.Category('Neue Kategorie', 1), [snippet.Snippet('Neue Kategorie', 'Neuer Snippet 1', 1, content="Inhalte :)"), snippet.Snippet('Neue Kategorie', 'Neuer Snippet 2', 1)]], [category.Category('Neue Kategorie 2', 1), [snippet.Snippet('Neue Kategorie 2', 'Neuer Snippet 1', 1, tags=["Gtk.ListBox"]), snippet.Snippet('Neue Kategorie 2', 'Neuer Snippet 2', 1)]], [category.Category('Neue Kategorie 3', 1), [snippet.Snippet('Neue Kategorie 3', 'Neuer Snippet 1', 1, tags=["JavaScript"]), snippet.Snippet('Neue Kategorie 3', 'Neuer Snippet 2', 1, tags=["PyGTK4", "Python"]), snippet.Snippet('Neue Kategorie 3', 'Neuer Snippet 3', 1)]]]
  

      
def save_collection(data):
    print("data saved...")
    collection = data[0].replace(" ", "_").lower()
    
    file = f'./saves/default.col'
    with open(file, "wb") as file:
        pickle.dump(data, file, pickle.HIGHEST_PROTOCOL)


def load_data(path):
    try:
        file = open(path, 'rb')
        data = pickle.load(file)
        file.close()
    except FileNotFoundError:
        pass
    except EOFError:
        snippets = []

    return data


save_collection(data)




