from typing import List
from collections import defaultdict


class CountVectorizer:
    """Класс для вычисления терм-документной матрицы"""
    def __init__(self, lowercase: bool = True):
        """lowercase: bool - нужно ли переводить строки в нижний регистр"""
        self.lowercase = lowercase
        self._vocabulary = None

    def _preproc(self, corpus: List[str]) -> List[List[str]]:
        """Предобработка списка строк:
        перевод в нижний регистр и разбиение по словам"""
        processed = []
        for i in range(len(corpus)):
            sentence = corpus[i].lower() if self.lowercase else corpus[i]
            processed.append(sentence.split())
        return processed

    def fit_transform(self, corpus: List[str]) -> List[List[int]]:
        """Вычисление терм-документной матрицы"""

        processed_corpus = self._preproc(corpus)

        n_sentences = len(corpus)
        self._vocabulary = defaultdict(lambda: [0] * n_sentences)
        for i, words_arr in enumerate(processed_corpus):
            for word in words_arr:
                self._vocabulary[word][i] += 1

        n_words = len(self._vocabulary)
        ans = [[0] * n_words for _ in range(n_sentences)]
        for i, freques in enumerate(self._vocabulary.values()):
            for j in range(n_sentences):
                ans[j][i] = freques[j]
        return ans

    def get_feature_names(self) -> List[str]:
        """Возвращает список слов - ключи словаря self._vocabulary"""
        return list(self._vocabulary.keys())


if __name__ == '__main__':
    vectorizer = CountVectorizer()

    corpus = ['one']
    count_matrix = vectorizer.fit_transform(corpus)
    assert vectorizer.get_feature_names() == ['one']
    assert count_matrix == [[1]]

    corpus = ['one one one one one']
    count_matrix = vectorizer.fit_transform(corpus)
    assert vectorizer.get_feature_names() == ['one']
    assert count_matrix == [[5]]

    corpus = ['one one one one one', 'one one one']
    count_matrix = vectorizer.fit_transform(corpus)
    assert vectorizer.get_feature_names() == ['one']
    assert count_matrix == [[5], [3]]

    corpus = ['one TWO TWO', 'THREE THREE THREE']
    count_matrix = vectorizer.fit_transform(corpus)
    assert vectorizer.get_feature_names() == ['one', 'two', 'three']
    assert count_matrix == [[1, 2, 0], [0, 0, 3]]

    corpus = [
              'Crock Pot Pasta Never boil pasta again',
              'Pasta Pomodoro Fresh ingredients Parmesan to taste'
             ]
    count_matrix = vectorizer.fit_transform(corpus)
    assert vectorizer.get_feature_names() == [
        'crock', 'pot', 'pasta', 'never', 'boil', 'again', 'pomodoro',
        'fresh', 'ingredients', 'parmesan', 'to', 'taste'
        ]
    assert count_matrix == [
        [1, 1, 2, 1, 1, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1]
        ]
