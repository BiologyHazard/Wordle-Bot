import json
import random


def calc_hint(ans, guess):
    hint = [-1 for i in range(5)]
    ans_matched = [False for i in range(5)]
    for i in range(5):
        if guess[i] == ans[i]:
            hint[i] = 2
            ans_matched[i] = True
        elif guess[i] not in ans:
            hint[i] = 0
    for i in range(5):
        if hint[i] == -1:
            for j in range(5):
                if not ans_matched[j] and guess[i] == ans[j]:
                    hint[i] = 1
                    ans_matched[j] = True
                    break
            if hint[i] == -1:
                hint[i] = 0
    return hint


with open(r"wordlist.json", 'r', encoding='utf-8') as f:
    wordlist = json.load(f)
answers = wordlist['answer']
answers_reversed = {k: v for v, k in enumerate(answers)}
supported_guesses = wordlist['answer'] + wordlist['otherWord']

ans = answers[random.randrange(0, len(answers))]
while True:
    guess = input('make a guess: ')
    if guess in supported_guesses:
        print(calc_hint(ans, guess))
        if calc_hint(ans, guess) == [2, 2, 2, 2, 2]:
            print('Bingo!')
            ans = answers[random.randrange(0, len(answers))]
    else:
        print('not in the word list.')
        break
