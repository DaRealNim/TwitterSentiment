import pickle

ironicdata = [
        # ironique, score negatif
        {'id': '1516406735858282505', 'text': "Ma vie est vraiment super !!! /s", 'author_id': '1245675276127870976', 'lang': 'fr'},
        # ironique, score negatif
        {'id': '1516406735858282505', 'text': "Jacques est \"sympathique\"", 'author_id': '1245675276127870976', 'lang': 'fr'},
        # citation, score positif
        {'id': '1516406735858282505', 'text': "\"Macroblank\" c'est sympathique", 'author_id': '1245675276127870976', 'lang': 'fr'},
        ]

negationdata = [
        # score negatif
        {'id': '1516406735858282505', 'text': "Ce film n'est pas génial.", 'author_id': '1245675276127870976', 'lang': 'fr'},
        # score neutre
        {'id': '1516406735858282505', 'text': "Je ne suis pas sur?", 'author_id': '1245675276127870976', 'lang': 'fr'},
        # score négatif
        {'id': '1516406735858282505', 'text': "Il n'est jamais bon de se précipiter.", 'author_id': '1245675276127870976', 'lang': 'fr'},
        # score positif
        {'id': '1516406735858282505', 'text': "C'est pas grave!", 'author_id': '1245675276127870976', 'lang': 'fr'},
        # score négatif, double négative
        {'id': '1516406735858282505', 'text': "Ca n'est PAS pas grave!", 'author_id': '1245675276127870976', 'lang': 'fr'},
]

with open("exemple_datasets/ironique.lst", 'wb') as handle:
    pickle.dump(ironicdata, handle,protocol=pickle.HIGHEST_PROTOCOL)

with open("exemple_datasets/negations.lst", 'wb') as handle:
    pickle.dump(negationdata, handle,protocol=pickle.HIGHEST_PROTOCOL)

