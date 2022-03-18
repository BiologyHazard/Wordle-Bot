import json
import math


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
    # wordle = Wordle()
    # hints = {}
    # for ans in wordle.answers:
    #     print(ans)
    #     dct = {}
    #     hints[ans] = dct
    #     for guess in wordle.supported_guesses:
    #         dct[guess] = calc_hint(ans, guess)
    # with open(r"hints.json", 'w', encoding='utf-8') as f:
    #     json.dump(hints, f)
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

    def give_guess(self):
        guess_list = []
        for guess_idx, guess in enumerate(self.supported_guesses):
            hint_count = [0 for i in range(3 ** 5)]
            for ans in self.psb_answers:
                hint_count[self.hint_list[self.answers_reversed[ans]]
                           [guess_idx]] += 1
            ent = 0
            for count in hint_count:
                if count > 0:
                    ent += (count / self.len_psb_answers *
                            (-math.log2(count / self.len_psb_answers)))
            guess_list.append(
                ent + int(guess in self.psb_answers) / self.len_psb_answers)
        max_ent = -1
        max_guess = None
        for guess_idx, ent in enumerate(guess_list):
            if ent > max_ent:
                max_ent = ent
                max_guess = self.supported_guesses[guess_idx]
        print(max_guess, max_ent)
        print(self.psb_answers)
        self.give_guess()

    def store_result(self, guess, hint):
        # for psb_ans in self.possible_answers:
        #     if self.hint_dict[psb_ans][guess] != hint:
        #         self.possible_answers.remove(psb_ans)
        self.psb_answers = {psb_ans for psb_ans in self.psb_answers
                            if Wordle.hint_list[Wordle.answers_reversed[psb_ans]][Wordle.supported_guesses_reversed[guess]] == list2num(hint)}
        self.len_psb_answers = len(self.psb_answers)

    def clear(self):
        self.psb_answers = self.answers
        self.len_psb_answers = len(self.psb_answers)


if __name__ == '__main__':
    # solve_hints()
    pass
