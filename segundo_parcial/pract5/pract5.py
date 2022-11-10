import spacy
from spacy.lang.es.stop_words import STOP_WORDS
import re
from collections import Counter
from pprint import pprint
import json


def rake(news):

    nlp = spacy.load("es_core_news_sm")

    # Las stopwords seran las que pertenecen a los siguientes POS seleccionados
    stopwords = ["ADP", "CONJ", "CCONJ", "PUNCT", "SYM", "X", "DET", "SCONJ", "PRON", "SPACE", "PRT", "PART", "ADV"]
    
    tokens_obj = nlp(news)
    candidates_aux = []
    candidates = []

    tokens = []

    # Seleccion de candidatos
    for token in tokens_obj:
        if token.pos_ not in stopwords:
            candidates_aux.append(token.text)
        elif token.pos_ in stopwords and len(candidates_aux) > 0:
            candidates.append(candidates_aux)
            candidates_aux = []

    if len(candidates_aux) > 0:
        candidates.append(candidates_aux)
        candidates_aux = []


    # Arreglo con todos los tokens
    for token in tokens_obj:
        if token.pos_ not in stopwords:
            tokens.append(token.text)
    
    
    # Obtenemos la frecuencia de la palabra
    word_freq = {}
    word_freq_aux = Counter(tokens)
    for key, value in word_freq_aux.items():
        word_freq[key] = value
    

    # Obtenemos el grado de la palabra
    word_grade = {}
    for token in tokens:
        aux = 0
        for candidate in candidates:
            if token in candidate:
                aux += len(candidate)
            else:
                aux = aux
        
        word_grade[token] = aux
    

    # Obtenemos la puntuacion del grado de la palabra
    grade_score = {}
    for key in word_freq.keys():
        grade_score[key] = word_grade[key] / word_freq[key]


    # Obtenemos la puntuacion acumulada por candidato
    cumulative_score = []
    for candidate in candidates:
        cumulative_score_aux = 0
        for element in candidate:
            cumulative_score_aux += grade_score[element]
        cumulative_score.append([candidate, cumulative_score_aux])

    # Remover duplicados
    full_keywords = []
    [full_keywords.append(x) for x in cumulative_score if x not in full_keywords]

    # Ordenar kewwords de mayor a menor importancia
    full_keywords =sorted(full_keywords, key=lambda score: score[1], reverse=True)

    # Obtener las keywords con un puntaje mayor a 1
    keywords = []
    for keyword in full_keywords:
        if keyword[1] > 1:
            keywords.append(keyword)

    return(keywords)

    

def main():

    file_name = 'corpus_noticias.txt'

    corpus_news = []

    with open(file_name, 'r',encoding='utf8') as input_file:
        for line in input_file.readlines():
            corpus_news.append(line)

        for i in range(len(corpus_news)):
            new = corpus_news[i]
            new =re.sub("\d+&+","",new.replace("\n", ""))
            # new =re.sub("[a-zA-ZÀ-ÿ]+&+","",new)
            new =re.sub("&+","",new)
            # new =re.sub("[\d.]+","",new)
            new =re.sub("[\d]+","",new)
            new =re.sub("(,\s,\s)+","",new)
            corpus_news[i] = new
        
        processed = {}
        for i, news in enumerate(corpus_news):
            processed[i]= rake(news)
    
        result = {}

        for i, doc in processed.items():
            result[i] = []
            for item in doc:
                keywords = " ".join(item[0])
                score = item[1]
                result[i].append(f"{keywords} : {score}")
        
        pprint(result)
                
        with open("resultado.txt", 'w+', encoding="utf8") as f:
            f.write(json.dumps(result, indent=2))        


if __name__ == "__main__":
    main()