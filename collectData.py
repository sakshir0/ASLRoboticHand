import csv
import numpy as np
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.neural_network import MLPClassifier
from joblib import dump, load 
MEASURESIZE = 100
STEPSIZE = 100
MEASURE = 10 
STEP = 8

X = []
y = []

def train(fname, cls):
    global X, y
    with open(fname, 'r') as f:
        reader = csv.reader(f, delimiter=',', quotechar='|')
        #next(reader)
        l = []
        for row in reader:
            l.append([float(r) for r in row[2:]])
        for i in range(len(l) // STEP - 1):
            a = np.array(l[STEP*i:min(STEP*i + MEASURE, len(l))])
            agg = np.mean(a, axis=0)
            #agg = np.concatenate((np.mean(a, axis=0), np.std(a, axis=0)))
            X.append(agg)
            y.append(cls)

def test(fname):
    with open(fname, 'r') as f:
        reader = csv.reader(f, delimiter=',', quotechar='|')
        #next(reader)
        l = []
        for row in reader:
            l.append([float(r) for r in row[2:]])
        
        prevchar = None
        prevprob = 0.0
        for i in range(len(l) // STEPSIZE - 1):
            a = np.array(l[STEPSIZE*i:min(STEPSIZE*i + MEASURESIZE, len(l))], dtype=np.float128)
            agg = np.mean(a, axis=0)
            #agg = np.concatenate((np.mean(a, axis=0), np.std(a, axis=0)))
            ch = clf.predict(agg.reshape(1, -1))[0]
            prob = clf.predict_proba(agg.reshape(1, -1))[0]
            if True in np.isnan(prob):
                continue
            if ch != prevchar:
                # if prevchar == None:
                #     pass
                # elif prob[ord(prevchar) - 97] >= prevprob - 1e-3:
                #     continue
                prevchar = ch
                # prevprob = prob[ord(ch) - 97]
                print(ch)
                # print(clf.predict_proba(agg.reshape(1, -1)))
    print("")

def trainer(folder):
    for i in range(0,26):
        filename = 'data/{}/train_{}.csv'.format(folder, chr(i + 97))
        train(filename, chr(i + 97))

trainer('fuckyou2')
train('data/fuckyou2/train_next.csv', 'next')
train('data/fuckyou2/train_back.csv', 'back')

# train('data/fuckyou/train_a.csv', 'a')
# train('data/roll/train_c.csv', 'c')
# train('data/roll/train_n.csv', 'n')
# train('data/roll/train_o.csv', 'o')


clf = LinearDiscriminantAnalysis()
#clf = MLPClassifier()
clf.fit(X, y)
dump(clf, 'lettermodel.joblib')


# test('data/roll/test_a.csv')
# test('data/roll/test_c.csv')
# test('data/roll/test_n.csv')
# test('data/roll/test_o.csv')


# for i in range(26):
#     test('data/fuckyou2/test_{}.csv'.format(chr(i + 97)))

test('data/fuckyou2/mystery1.csv')
test('data/fuckyou2/mystery2.csv')

# test('data/test/test_a.csv')
# test('data/test/test_b.csv')
# test('data/test/test_c.csv')
# test('data/test/test_d.csv')
# test('data/test/test_e.csv')
# test('data/test/test_f.csv')
# test('data/test/test_g.csv')
# test('data/test/test_h.csv')
# test('data/test/test_i.csv')
# test('data/test/test_j.csv')
# test('data/test/test_k.csv')
# test('data/test/test_l.csv')
# test('data/test/test_m.csv')
# test('data/test/test_n.csv')
# test('data/test/test_o.csv')
# test('data/test/test_p.csv')
# test('data/test/test_q.csv')
# test('data/test/test_r.csv')
# test('data/test/test_s.csv')
# test('data/test/test_t.csv')
# test('data/test/test_u.csv')
# test('data/test/test_v.csv')
# test('data/test/test_w.csv')
# test('data/test/test_x.csv')
# test('data/test/test_y.csv')
# test('data/test/test_z.csv')






