import pandas as pd


def words_pos_neg(path):
    df = pd.read_csv(path, sep="\t", header=None, names=['Palabra', 'Nula[%]', 'Baja[%]', 'Media[%]', 'Alta[%]', 'PFA', 'Categoria'])

    a = df.query('Categoria == "Alegría" | Categoria == "Sorpresa"')

    a.drop(['Nula[%]', 'Baja[%]', 'Media[%]', 'Alta[%]','Categoria'], axis=1, inplace=True)

    positives = {}

    for index, row in a.iterrows():
        positives[row['Palabra']] = row['PFA']

    
    b = df.query('Categoria == "Enojo" | Categoria == "Miedo" | Categoria == "Repulsión" | Categoria == "Tristeza"')

    b.drop(['Nula[%]', 'Baja[%]', 'Media[%]', 'Alta[%]','Categoria'], axis=1, inplace=True)

    negatives = {}

    for index, row in b.iterrows():
        negatives[row['Palabra']] = row['PFA']
    
    return positives, negatives


if __name__ == '__main__':
    from pprint import pprint
    p, n = words_pos_neg("SEL_full.txt")
    pprint(p)