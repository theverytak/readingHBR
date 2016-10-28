# Belief thresholds for the heuristic logic which determines whether a line is 
# pure or not. For example, we will consider a line pure when it's purity is 
# larger then 0.7 within '문장' target context.
MAYBE_HEURISTIC_PROBS= {
    '단어': 1,
    '문장': 0.7,
}
MAYBE_HEURISTIC_DEFAULT_PROB = 0.9
