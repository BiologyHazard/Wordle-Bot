import json
import math
import numpy as np


def list2num(hint_list):
    ans = 0
    for i in hint_list:
        ans *= 3
        ans += i
    return ans


def num2list(hint_num):
    ans = []
    while hint_num > 0:
        ans.append(hint_num % 3)
        hint_num //= 3
    return list(reversed(ans))


def solve_hints():
    wordle = Wordle()
    hints = []
    for i, ans in enumerate(wordle.answers):
        print(i, ans)
        lst = []
        hints.append(lst)
        for guess in wordle.supported_guesses:
            lst.append(list2num(calc_hint(ans, guess)))
    with open(r"hints.json", 'w', encoding='utf-8') as f:
        json.dump(hints, f, indent=None, separators=(',', ':'))


def entropy_to_expected_score(ent):
    return 2 - 2**(-ent) + 1.5 / 11.5 * ent


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


class Wordle:
    WORDLE = 0
    ABSURDLE = 1

    with open(r"wordlist.json", 'r', encoding='utf-8') as f:
        wordlist = json.load(f)
    answers = wordlist['answer']
    answers_reversed = {k: v for v, k in enumerate(answers)}
    supported_guesses = wordlist['answer'] + wordlist['otherWord']
    supported_guesses_reversed = {
        k: v for v, k in enumerate(supported_guesses)}
    with open(r"hints.json", 'r', encoding='utf-8') as f:
        hint_list = json.load(f)

    def __init__(self):
        self.psb_answers = set(Wordle.answers)
        self.len_psb_answers = len(self.psb_answers)

    def give_guess(self, mode=WORDLE):
        if self.len_psb_answers == 1:
            return self.psb_answers.pop()
        guess_list = []
        left_entropy = math.log2(self.len_psb_answers)
        for guess_idx, guess in enumerate(Wordle.supported_guesses):
            prob = 1 / self.len_psb_answers if guess in self.psb_answers else 0
            hint_count = np.zeros(3**5, dtype=np.int8)
            for ans in self.psb_answers:
                hint_count[Wordle.hint_list[self.answers_reversed[ans]]
                           [guess_idx]] += 1
            if mode == Wordle.WORDLE:
                ent = 0
                for count in hint_count:
                    if count > 0:
                        ent += (count / self.len_psb_answers *
                                (-math.log2(count / self.len_psb_answers)))
                guess_list.append(
                    prob + (1 - prob) * (1 + entropy_to_expected_score(left_entropy - ent)))
            # elif mode == Wordle.ABSURDLE:
            #     guess_exp_list.append(-hint_count[0])
        min_exp = 1000000
        optimal_guess_idx = -1
        for guess_idx, exp in enumerate(guess_list):
            if exp < min_exp:
                min_exp = exp
                optimal_guess_idx = guess_idx
        # print(
        #     Wordle.supported_guesses[optimal_guess_idx], guess_list[optimal_guess_idx])
        return Wordle.supported_guesses[optimal_guess_idx]

    def store_result(self, guess, hint):
        # for psb_ans in self.possible_answers:
        #     if self.hint_dict[psb_ans][guess] != hint:
        #         self.possible_answers.remove(psb_ans)
        if hint == 242:
            self.psb_answers = guess
            self.len_psb_answers = 1
        self.psb_answers = {psb_ans for psb_ans in self.psb_answers
                            if Wordle.hint_list[Wordle.answers_reversed[psb_ans]][Wordle.supported_guesses_reversed[guess]] == hint}
        self.len_psb_answers = len(self.psb_answers)
        if self.len_psb_answers == 0:
            raise ValueError('No Solution.')
        # print(self.psb_answers)
        # self.give_guess()

    def clear(self):
        self.psb_answers = Wordle.answers
        self.len_psb_answers = len(self.psb_answers)


def simulate():
    print('hello')
    wordle = Wordle()
    for ans_idx, ans in list(enumerate(Wordle.answers))[:10]:
        print(ans, end=' ')
        score = 0
        while True:
            if score == 0:
                guess = 'soare'
            else:
                guess = wordle.give_guess()
            print(guess, end=' ')
            score += 1
            hint = Wordle.hint_list[ans_idx][Wordle.supported_guesses_reversed[guess]]
            if hint == 242:
                break
            wordle.store_result(guess, hint)
        print(ans, score)
        wordle.clear()


if __name__ == '__main__':
    # solve_hints()
    # wordle = Wordle()
    # while True:
    #     a = input()
    #     if a == 'g':
    #         wordle.give_guess()
    #     elif a == 'n':
    #         wordle.clear()
    #     else:
    #         b, c = a.split()
    #         c = [int(i) for i in c]
    #         wordle.store_result(b, c)
    simulate()
