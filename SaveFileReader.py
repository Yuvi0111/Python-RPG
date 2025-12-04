import pickle
with open('savefile_Yuvi.dat', 'rb') as file:
    try:
        while True:
            chars = pickle.load(file)
            print(chars)
    except EOFError:
        print('End of file reached.')