import glob
import errno
import re


def freq_calc(words, freq_dict):
    for word in words:
        word = word.upper()
        if word in freq_dict:
            freq_dict[word] = freq_dict[word] + 1
        else:
            freq_dict[word] = 1 
    return freq_dict

def bayes_formula(word, Ps, Ph, spam, ham):
    if word in spam:
        ws = spam[word]
    else:
        ws = 0
    if word in ham:
        wh = ham[word]
    else:
        wh = 0
    if ws == 0 and wh == 0:
        return 0
    #print("P(W|S): ", ws, " P(H|W): ", wh, " P(S): ", Ps, " P(H): ", Ph)
    spamchance = ws * Ps / (ws * Ps + wh * Ph)
    return spamchance

def findSpamProbs(probs):
    result = 0
    p = 1
    pM = 1
    for pr in probs:
        if pr > 0:
            p = p * pr
            pM = pM * (1 - pr)
    result = p / (p + pM)
    return result
        
numWords = 0
ham_freqs = {}
spam_freqs = {}
ham_path = "enron_data/ham/*.txt"
spam_path = "enron_data/spam/*.txt"
test_path = "enron_data/test/*.txt"
files = glob.glob(ham_path)
pattern = re.compile(r'([A-Za-z]+[\']?[a-zA-z]*)') #finds all words in a file, including conjunctions
save_file = "savedata.txt"
save_file_2 = "savedata2.txt"
num_ham = len(files)

for fname in files:
    with open(fname) as file:
        data = file.read()
        matches = pattern.findall(data)
        freq_calc(matches, ham_freqs)
        numWords = numWords + len(matches)
print("Calculating Ham freq")
for x in ham_freqs:
    ham_freqs[x] = ham_freqs[x] / numWords

print("FINDING SPAM AND HAM PROB")
files = glob.glob(spam_path)
num_spam = len(files)
total_email = num_ham + num_spam
print(total_email)
Ps = num_spam / total_email
Ph = num_ham / total_email
print(Ps)
print(Ph)
numWords = 0
for fname in files:
    with open(fname, encoding="Latin-1") as file:
        data = file.read()
        matches = pattern.findall(data)
        freq_calc(matches, spam_freqs)
        numWords = numWords + len(matches)
print("Calculating Spam freq")
for x in spam_freqs:
    spam_freqs[x] = spam_freqs[x] / numWords

print("TESTING FOR SPAM...")
#TEST FILES
files = glob.glob(test_path)
testResults = []
for fname in files:
    probs = []
    with open (fname, encoding="Latin-1") as file:
        data = file.read()
        matches = pattern.findall(data)
        for word in matches:
            probs.append(bayes_formula(word.upper(), Ps, Ph, spam_freqs, ham_freqs))    
        testResults.append(findSpamProbs(probs))
print(testResults)

'''with open (save_file_2, "w") as file:
    file.write(str(spam_freqs))
with open (save_file, "w") as file:
    file.write(str(ham_freqs))'''






