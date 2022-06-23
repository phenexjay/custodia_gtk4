import pickle
import category
import snippet
# import tags

def save_data(data):
    collection = data[0].replace(" ", "_").lower()
    
    file = f'./saves/{collection}.col'
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
        data = []

    return data


