from typing import List
from math import log


class TfidfTransformer:
    def __init__(self):
        pass

    def tf_transform(self, count_matrix: List[List[int]]) -> List[List[float]]:
        """Вычисление term frequency"""
        tf_matrix = []
        for row in count_matrix:
            denominator = sum(row)
            tf_matrix.append([round(x / denominator, 3) for x in row])
        return tf_matrix

    def idf_transform(self, count_matrix: List[List[int]]) -> List[float]:
        """вычисление idf"""
        n_docs = len(count_matrix)
        n_words = len(count_matrix[0])

        idf = []
        for i in range(n_words):
            docs_counter = 0
            for j in range(n_docs):
                docs_counter += int(count_matrix[j][i] > 0)
            idf.append(round(log((n_docs + 1) / (docs_counter + 1)) + 1, 3))
        return idf

    def fit_transform(self, c_matrix: List[List[int]]) -> List[List[float]]:
        """Вычисление tfidf"""
        tf_matrix = self.tf_transform(c_matrix)
        idf_vector = self.idf_transform(c_matrix)
        tfidf = []
        for tf_row in tf_matrix:
            tfidf.append([round(tf * idf, 3) for (tf, idf)
                          in zip(tf_row, idf_vector)])
        return tfidf


if __name__ == '__main__':
    count_matrix = [
         [1, 1, 2, 1, 1, 1, 0, 0, 0, 0, 0, 0],
         [0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1]
      ]
    transformer = TfidfTransformer()

    tf_matrix = transformer.tf_transform(count_matrix)
    print('tf_matrix: ')
    print(*tf_matrix, sep='\n')
    print('true answer: ')
    print('[[0.143, 0.143, 0.286, 0.143, 0.143, 0.143, 0, 0, 0, 0, 0, 0]',
          '[0, 0, 0.143, 0, 0, 0, 0.143, 0.143, 0.143, 0.143, 0.143, 0.143]]',
          sep='\n')

    idf_matrix = transformer.idf_transform(count_matrix)
    print('idf_matrix: ')
    print(idf_matrix)
    print('true answer: ')
    print('[1.4, 1.4, 1.0, 1.4, 1.4, 1.4, 1.4, 1.4, 1.4, 1.4, 1.4, 1.4]')

    tfidf_matrix = transformer.fit_transform(count_matrix)
    print('tfidf_matrix: ')
    print(*tfidf_matrix, sep='\n')
    print('true answer: ')
    print('[[0.2, 0.2, 0.286, 0.2, 0.2, 0.2, 0, 0, 0, 0, 0, 0]',
          '[0, 0, 0.143, 0, 0, 0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2]]',
          sep='\n')
