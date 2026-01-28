import math
from collections import defaultdict


class NGramModel:
    def __init__(self, n=2, smoothing=None):
        self.n = n
        self.smoothing = smoothing
        self.ngram_counts = defaultdict(int)
        self.context_counts = defaultdict(int)
        self.vocab = set()

    def train(self, tokens):
        if len(tokens) < self.n:
            return

        for i in range(len(tokens) - self.n + 1):
            context = tuple(tokens[i:i + self.n - 1])
            target = tokens[i + self.n - 1]

            self.ngram_counts[(context, target)] += 1
            self.context_counts[context] += 1
            self.vocab.add(target)

    def probability(self, context, word):
        if self.smoothing == "laplace":
            return (
                self.ngram_counts[(context, word)] + 1
            ) / (
                self.context_counts[context] + len(self.vocab)
            )

        # Unsmoothed
        if self.context_counts[context] == 0:
            return 0

        return self.ngram_counts[(context, word)] / self.context_counts[context]

    def sentence_log_probability(self, tokens):
        if len(tokens) < self.n:
            return float("-inf")

        log_prob = 0.0

        for i in range(len(tokens) - self.n + 1):
            context = tuple(tokens[i:i + self.n - 1])
            target = tokens[i + self.n - 1]

            prob = self.probability(context, target)

            if prob == 0:
                return float("-inf")

            log_prob += math.log(prob)

        return log_prob
