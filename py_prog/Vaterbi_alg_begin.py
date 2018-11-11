#(iutkina@hse.ru)
# transition probabilities
trans_probs = {('[START]', 'verb'): 0.2, ('[START]', 'noun'): 0.8, ('noun', 'verb'): 0.8, ('noun', '[END]'): 0.1,
('noun', 'noun'): 0.1,
('verb', 'noun'): 0.2,
('verb', 'verb'): 0.1,
('verb', '[END]'): 0.7 }
# emission probabilities
emis_probs = {('noun', 'fish'): 0.8, ('noun', 'sleep'): 0.2,
('verb', 'fish'): 0.5, ('verb', 'sleep'): 0.5 }
s = 'fish sleep'
s1= ['[START]', 'fish', 'sleep', '[END]']
for i,k in enumerate(s1):
    if k=="[START]" and i==0:
        prob=1
        print (prob)
token1 = s1[1]
k=[]
print (token1)
for j in emis_probs.items():
    if j[0][1]==token1:
        prob1=j[1]
        print (prob1)
        tran=(s1[0],j[0][0])
        for o in trans_probs.items():
            if o[0]==tran:
                prob1*=o[1]
                k.append(prob1)
print(k)
print(k.index(max(k)))
token2=s1[2]
for j2 in emis_probs.items():
    if j[0][1]==token2:
        prob2=j[1]
        print (prob2)
        tran=(s1[0],j[0][0])
        for o in trans_probs.items():
            if o[0]==tran:
                prob1*=o[1]
                k.append(prob1)

#for i in trans_probs:
#    print(i)
#def viterbi(s, states, trans_probs, emis_probs):


#>>> viterbi(s, states, trans_probs, emis_probs)
#fish sleep
#[START] 1.0
#noun 0.6400000000000001
#verb 0.25600000000000006
#[END] 0.17920000000000003