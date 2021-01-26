import csv

for i in range(26):
    if i == 25 or i == 9:
        continue 
    l = []
    with open('data/fuckyou/train_{}.csv'.format(chr(i + 97)), 'r') as f:
        reader = csv.reader(f, delimiter=',', quotechar='|')
        for row in reader:
            l.append(row)
    ln = len(l) // 2
    with open('data/fuckyou2/train_{}.csv'.format(chr(i + 97)), 'ab') as f:
        wr = csv.writer(f, dialect='excel')
        for j in range(ln):
            wr.writerow(l[j])
    with open('data/fuckyou2/test_{}.csv'.format(chr(i + 97)), 'ab') as f:
        wr = csv.writer(f, dialect='excel')
        for j in range(ln, len(l)):
            wr.writerow(l[j])