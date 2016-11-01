# Belief thresholds for the heuristic logic which determines whether a line is 
# pure or not. For example, we will consider a line is pure when it's purity 
# is larger then 0.7 within '문장' target context. However, we will consider 
# any line that has lower than perfect purity(1) as an impure line within 
# '단어' target context.
PURITY_HEURISTIC_PROBS= {
    '단어': 1,
    '문장': 0.7,
}
PURITY_HEURISTIC_DEFAULT_PROB = 0.9
