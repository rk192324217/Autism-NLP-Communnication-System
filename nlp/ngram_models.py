import math
from collections import defaultdict, Counter

class NGramModel:
    def __init__(self, n=2, smoothing=None):
        self.n = n
        self.smoothing = smoothing
        self.counts = defaultdict(Counter)
        self.vocab = set()

    def train(self, corpus):
        for sentence in corpus:
            tokens = ["<s>"]*(self.n-1) + sentence + ["</s>"]
            self.vocab.update(tokens)
            for i in range(len(tokens)-self.n+1):
                history = tuple(tokens[i:i+self.n-1])
                word = tokens[i+self.n-1]
                self.counts[history][word] += 1

    def prob(self, history, word):
        history_counts = self.counts[history]
        total = sum(history_counts.values())
        V = len(self.vocab)

        if self.smoothing == "laplace":
            return (history_counts[word] + 1) / (total + V)
        else:
            return history_counts[word] / total if total > 0 else 0.0

    def sentence_log_probability(self, tokens):
        tokens = ["<s>"]*(self.n-1) + tokens + ["</s>"]
        log_prob = 0.0
        for i in range(len(tokens)-self.n+1):
            history = tuple(tokens[i:i+self.n-1])
            word = tokens[i+self.n-1]
            prob = self.prob(history, word)
            if prob == 0:
                return float("-inf")
            log_prob += math.log(prob)
        return log_prob