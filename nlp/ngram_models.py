from collections import Counter
import math

class NGramModel:
    def __init__(self, n=2, smoothing=None, k=1):
        self.n = n
        self.smoothing = smoothing
        self.k = k
        self.ngram_counts = Counter()
        self.context_counts = Counter()
        self.vocab = set()

    def train(self, tokens):
        for i in range(len(tokens) - self.n + 1):
            ngram = tuple(tokens[i:i+self.n])
            context = tuple(tokens[i:i+self.n-1])

            self.ngram_counts[ngram] += 1
            self.context_counts[context] += 1
            self.vocab.update(ngram)

    def probability(self, ngram):
        context = ngram[:-1]

        if self.smoothing == "laplace":
            return (
                self.ngram_counts[ngram] + self.k
            ) / (
                self.context_counts[context] + self.k * len(self.vocab)
            )

        # Unsmoothened
        if self.context_counts[context] == 0:
            return 0.0

        return self.ngram_counts[ngram] / self.context_counts[context]

    def sentence_log_probability(self, tokens):
        log_prob = 0.0
        for i in range(len(tokens) - self.n + 1):
            ngram = tuple(tokens[i:i+self.n])
            prob = self.probability(ngram)

            if prob > 0:
                log_prob += math.log(prob)
            else:
                log_prob += math.log(1e-10)

        return log_prob
