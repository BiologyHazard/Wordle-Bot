import json


def check(ans, guess, output):
    for i in range(5):
        if output[i] == '0':
            if guess[i] in ans:
                return False
        elif output[i] == '1':
            if (not guess[i] in ans) or (guess[i] == ans[i]):
                return False
        elif output[i] == '2':
            if not guess[i] == ans[i]:
                return False
    return True


def calc_hint(ans, guess):
    hint = []
    for i in range(5):
        if guess[i] == ans[i]:
            hint[i] = 2
        elif guess[i] not in ans:
            hint[i] = 0
        else:
            pass


with open(r"wordlist.json", 'r', encoding='utf-8') as f:
    wordlist = json.load(f)
# answers = wordlist['answer']
# all_words = wordlist['otherWord'] + answers

answers = wordlist['answer']
all_words = wordlist['answer'] + wordlist['otherWord']

possible_words = wordlist['answer']
while True:
    s = input()
    if s == 'new':
        possible_words = wordlist['answer']
        continue
    s1, s2 = s.split()
    possible_words = [x for x in possible_words if check(x, s1, s2)]
    # for i in possible_words:
    #     if check(i, s1, s2):
    #         print(i)
    #     else:
    #         possible_words.remove(i)
    print(possible_words)
