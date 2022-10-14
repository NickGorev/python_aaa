from typing import List
from count_vectorizer import CountVectorizer
from tfidf_transformer import TfidfTransformer


class TfidfVectorizer(CountVectorizer):
    def __init__(self, lowercase: bool = True):
        super().__init__(lowercase)
        self._transformer = TfidfTransformer()

    def fit_transform(self, corpus: List[str]) -> List[List[float]]:
        matrix = super().fit_transform(corpus)
        return self._transformer.fit_transform(matrix)


if __name__ == '__main__':
    corpus = [
        'Crock Pot Pasta Never boil pasta again',
        'Pasta Pomodoro Fresh ingredients Parmesan to taste'
     ]
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(corpus)
    print('feature names:')
    print(vectorizer.get_feature_names())
    print('true answer:')
    print("['crock', 'pot', 'pasta', 'never', 'boil', 'again', 'pomodoro',"
          " 'fresh', 'ingredients', 'parmesan', 'to', 'taste']")
    print('tfidf_matrix:')
    print(*tfidf_matrix, sep='\n')
    print('true answer:')
    print('[[0.2, 0.2, 0.286, 0.2, 0.2, 0.2, 0, 0, 0, 0, 0, 0]',
          '[0, 0, 0.143, 0, 0, 0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2]]',
          sep='\n')
