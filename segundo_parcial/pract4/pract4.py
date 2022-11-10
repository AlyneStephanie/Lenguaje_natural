import spacy
import re
from gensim.models.doc2vec import Doc2Vec, TaggedDocument


def tokenizing(file_name):
    nlp = spacy.load("es_core_news_sm")
    # nlp.max_length = 1600000

    corpus_news = []
    with open(file_name, 'r',encoding='utf8') as input_file:
        for line in input_file.readlines():
            corpus_news.append(line)
        

        for i in range(len(corpus_news)):
            new = corpus_news[i]
            new =re.sub("\d+&+","",new.replace("\n", ""))
            new =re.sub("[a-zA-ZÀ-ÿ]+&+","",new)
            new =re.sub("&+","",new)
            new =re.sub("[\d.]+","",new)
            new =re.sub("(,\s,\s)+","",new)
            corpus_news[i] = new
        

        for i in range(len(corpus_news)):
            tokens = nlp(corpus_news[i])
            news = []
            for token in tokens:
                news.append(token.text)
            corpus_news[i] = news
        
        return corpus_news


def doc_similarity(tokenized_files, dm_model, vector_size_model, window_model):
    documents = []
    for corpus_news in tokenized_files:
        tagged_data = [TaggedDocument(d, [i]) for i, d in enumerate(corpus_news)]

        ## Train doc2vec model
        model = Doc2Vec(tagged_data, dm=dm_model, vector_size=vector_size_model, window=window_model)

        # Save trained doc2vec model
        model.save("test_doc2vec.model")

        ## Load saved doc2vec model
        model= Doc2Vec.load("test_doc2vec.model")
        

        most_similar_documents = []
        

        for i, e in enumerate(tagged_data):
            most_similar_vec = model.dv.most_similar(model.dv[i])
            document_similarity = [i, most_similar_vec[1][0],most_similar_vec[1][1]]
            most_similar_documents.append(document_similarity)

        sorted_documents = sorted(most_similar_documents, key=lambda similarity: similarity[2], reverse=True)[0:20]

        documents.append(sorted_documents)

    return documents


def main():
    with open("results.txt", "wt+") as f:
        files = ['corpus_noticias.txt', 'noticias_salida.txt']

        dm_model = [0, 1]
        vector_size_model = [100, 300]
        window_model = [5, 10]

        ten_most_similar_docs =[]

        tokenized_files = []
        for file_name in files:
            tokenized_files.append(tokenizing(file_name))

        for i in dm_model:
            for j in vector_size_model:
                for k in window_model:
                    ten_most_similar_docs.append(doc_similarity(tokenized_files, i, j, k))

        # for i in ten_most_similar_docs:
            # print(i)
        for i in range(len(ten_most_similar_docs)):
            for j in range(len(ten_most_similar_docs[i])):
                for k in range(len(ten_most_similar_docs[i][j])):
                    f.write(f"noticia {ten_most_similar_docs[i][j][k][0]} - noticia {ten_most_similar_docs[i][j][k][1]}   Valor similitud: {ten_most_similar_docs[i][j][k][2]}")
                    f.write("\n")
                f.write("\n")



if __name__ == "__main__":
    main()