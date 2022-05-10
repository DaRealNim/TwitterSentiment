import pickle

data = [
        # ironique, score negatif
        {'id': '1516406735858282505', 'text': "Ma vie est vraiment super !!! /s", 'author_id': '1245675276127870976', 'lang': 'fr'},
        # ironique, score negatif
        {'id': '1516406735858282505', 'text': "Jacques est \"sympathique\"", 'author_id': '1245675276127870976', 'lang': 'fr'},
        # citation, score positif
        {'id': '1516406735858282505', 'text': "\"Macroblank\" c'est sympathique", 'author_id': '1245675276127870976', 'lang': 'fr'},
        ]

with open("exemple_datasets/ironique.lst", 'wb') as handle:
    pickle.dump(data, handle,protocol=pickle.HIGHEST_PROTOCOL)
