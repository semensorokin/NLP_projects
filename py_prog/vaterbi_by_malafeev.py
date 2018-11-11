#! python3


START_STATE = '[START]'
START_TOKEN = '*'
END_STATE = '[END]'
END_TOKEN = '$'
EPSILON = 0.0001


def viterbi(s, states, trans_probs, emis_probs, trace=False, smoothing=False):
    err_text = "invalid start and/or end state (must be '%s' and '%s')" % (START_STATE, END_STATE)
    assert states[0] == START_STATE and states[-1] == END_STATE, err_text #проверка на то что должно бвть в списке сосотояний
    emis_probs[(START_STATE, START_TOKEN)] = 1.0
    emis_probs[(END_STATE, END_TOKEN)] = 1.0
    if trace:
        print(s)
    vit = []  # token x state x prev_vit, e.g. [... [[0], [.005, .256], [.004, .0128], [0]], ...] 
    bp = {} #backpointer
    tokens = s.split()
    tokens = [START_TOKEN] + tokens + [END_TOKEN]
    end = len(tokens)
    prev_probs = [1.0] + [0.0 for _ in states[1:]]
    smoothing_used = False
    if trace:
        print(', '.join(states))
        print(prev_probs)
    for i, token in enumerate(tokens[1:]):
        col = []  # new 'column' of states for current token
        vit.append(col)# добали пустой список в вит, и теперь имеем возможномть обращаться к ячейке табалице через col
        for cand_state in states:
            probs = []  # new variable-size list of probabilities for current state
            col.append(probs )
            prev_s_for_bp = ''
            max_for_bp = 0.0
            for j, prev_prob in enumerate(prev_probs):
                prev_state = states[j]
                trans_prob = trans_probs.get((prev_state, cand_state), 0.0)
                emis_prob = emis_probs.get((cand_state, token), 0.0)
                # some simple smoothing (for new words)
                if smoothing and not emis_prob and cand_state not in [START_STATE, END_STATE] and i != end - 2:
                    emis_prob = EPSILON
                    smoothing_used = True
                v = prev_prob * trans_prob * emis_prob
                probs.append(v)
                # backpointing
                if v > max_for_bp:
                    prev_s_for_bp = prev_state
                    max_for_bp = v
            if max_for_bp:
                bp[cand_state, i + 1] = prev_s_for_bp, i
            max_v = max(probs)
            col[-1] = max_v
        prev_probs = col
        if trace:
            print(col)
    if trace and smoothing_used:
        print('-with smoothing-')
    # 'unravel' the backpointers
    if trace:
        from pprint import pprint as pp
        print('backpointers:')
        pp(bp)
    s = END_STATE
    res_states = []
    for i in range(end - 1, 0, -1):
        res_states.append(s)
        s = bp[s, i][0]
    res_states.reverse()
    res_states.pop()
    return res_states


def main():
    states = [START_STATE, 'noun', 'verb', END_STATE]

    # transition probabilities
    hmm = {(START_STATE, 'verb'): 0.2,
           (START_STATE, 'noun'): 0.8,
           ('noun', 'verb'): 0.8,
           ('noun', END_STATE): 0.1,
           ('noun', 'noun'): 0.1,
           ('verb', 'noun'): 0.2,
           ('verb', 'verb'): 0.1,
           ('verb', END_STATE): 0.7
           }

    emis_probs = {('noun', 'fish'): 0.8,
                  ('noun', 'sleep'): 0.2,
                  ('verb', 'fish'): 0.5,
                  ('verb', 'sleep'): 0.5
                  }

    s = 'fish sleep'
    print(viterbi(s, states, hmm, emis_probs, trace=True, smoothing=True))
    while True:
        # might want to try 'zebras sleep' and 'fish walk' to illustrate smoothing,
        # but there are not enough POS in the toy model for longer and cooler examples
        s = input('Input any sequence of words "fish" and "sleep": ')
        print(viterbi(s, states, hmm, emis_probs, trace=True, smoothing=True))


if __name__ == '__main__':
    try:
        main()
    except:
        import traceback

        traceback.print_exc()
    input('Press Enter to exit.')
 