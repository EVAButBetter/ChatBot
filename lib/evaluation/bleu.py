import math
import numpy as np

def bleu_score(candidate, references, weights):
    """
    Calculate the BLEU score of a candidate sentence given a list of reference sentences and the n-gram weights.

    :param candidate: The candidate sentence to be evaluated.
    :param references: The list of reference sentences to be used for evaluation.
    :param weights: The list of n-gram weights to be used for evaluation. Each weight corresponds to the n-gram order.
    :return: The BLEU score of the candidate sentence.
    """
    candidate = candidate.split()
    reference_counts = []
    candidate_counts = []
    for i in range(len(weights)):
        reference_counts.append({})
        candidate_counts.append({})
    for reference in references:
        reference = reference.split()
        for i in range(len(weights)):
            for j in range(len(reference) - i):
                ngram = ' '.join(reference[j:j+i+1])
                if ngram in reference_counts[i]:
                    reference_counts[i][ngram] += 1
                else:
                    reference_counts[i][ngram] = 1
    for i in range(len(weights)):
        for j in range(len(candidate) - i):
            ngram = ' '.join(candidate[j:j+i+1])
            if ngram in candidate_counts[i]:
                candidate_counts[i][ngram] += 1
            else:
                candidate_counts[i][ngram] = 1
    precisions = []
    for i in range(len(weights)):
        total = sum(candidate_counts[i].values())
        if total == 0:
            precisions.append(0)
        else:
            correct = 0
            for ngram, count in candidate_counts[i].items():
                if ngram in reference_counts[i]:
                    correct += min(count, reference_counts[i][ngram])
            precisions.append(correct / total)
    brevity_penalty = min(1, math.exp(1 - len(references[0].split()) / len(candidate)))
    product = np.prod(precisions)
    bleu = brevity_penalty * math.pow(product, 1 / len(weights))
    return bleu

candidate = "where is your movil phone you bought last weekend?"
references = ["where is your movil phone which you bought last weekend in the plaza spain?"]
weights = [1,2,3,4]
_score = bleu_score(candidate, references, weights)
print(_score)