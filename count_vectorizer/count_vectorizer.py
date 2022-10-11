from typing import List


class CountVectorizer:
    """Класс для вычисления терм-документной матрицы"""
    def __init__(self, lowercase: bool = True):
        """lowercase: bool - нужно ли переводить строки в нижний регистр"""
        self.lowercase = lowercase
        self._vocabulary = {}

    def _preproc(self, corpus: List[str]) -> List[List[str]]:
        """Предобработка списка строк:
        перевод в нижний регистр и разбиение по словам"""
        processed = []
        for i in range(len(corpus)):
            sentence = corpus[i].lower() if self.lowercase else corpus[i]
            processed.append(sentence.split())
        return processed

    def _build_vicabulary(self, processed_corpus: List[List[str]]) -> None:
        """Построение словаря self._vocabulary
        ключ - слово, значение индекс слова в терм-документной матрице"""
        self._vocabulary = {}
        for words_arr in processed_corpus:
            for word in words_arr:
                if word not in self._vocabulary:
                    self._vocabulary[word] = len(self._vocabulary)

    def fit_transform(self, corpus: List[str]) -> List[List[int]]:
        """Вычисление терм-документной матрицы"""
        processed_corpus = self._preproc(corpus)
        self._build_vicabulary(processed_corpus)

        ans = [[0] * len(self._vocabulary) for _ in range(len(corpus))]
        for i, words_arr in enumerate(processed_corpus):
            for word in words_arr:
                ans[i][self._vocabulary[word]] += 1
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
