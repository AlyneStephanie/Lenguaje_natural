from gensim.models.doc2vec import Doc2Vec, TaggedDocument
#https://radimrehurek.com/gensim/models/doc2vec.html

sentences = [['i', 'like', 'apple', 'pie', 'for', 'dessert'],
           ['i', 'dont', 'drive', 'fast', 'cars'],
           ['data', 'science', 'is', 'fun'],
           ['chocolate', 'is', 'my', 'favorite'],
           ['my', 'favorite', 'movie', 'is', 'predator'],
           ['vanilla', 'is', 'my', 'favorite'],
           ['chocolate', 'is', 'delicious'],
           ['vanilla', 'is', 'delicious']]

tagged_data = [TaggedDocument(d, [i]) for i, d in enumerate(sentences)]
print(tagged_data)

## Train doc2vec model
model = Doc2Vec(tagged_data, vector_size=30)
#his object contains the paragraph vectors learned from the training data. There will be one such vector for each unique document tag supplied during training. They may be individually accessed using the tag as an indexed-access key
print(model.dv[0])
# Save trained doc2vec model
model.save("test_doc2vec.model")
## Load saved doc2vec model
model= Doc2Vec.load("test_doc2vec.model")
print(model.dv.most_similar(model.dv[3]))




