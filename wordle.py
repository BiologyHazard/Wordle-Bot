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

# def check(ans, guess, output):
#     for i in range(5):
#         if output[i] == '0':
#             if guess[i] in ans:
#                 return False
#         elif output[i] == '1':
#             if (not guess[i] in ans) or (guess[i] == ans[i]):
#                 return False
#         elif output[i] == '2':
#             if not guess[i] == ans[i]:
#                 return False
#     return True


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
        json.dump(hints, f, indent=None)


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
    def __init__(self):
        with open(r"wordlist.json", 'r', encoding='utf-8') as f:
            wordlist = json.load(f)
        self.answers = wordlist['answer']
        self.supported_guesses = wordlist['answer'] + wordlist['otherWord']
        self.psb_answers = wordlist['answer']
        with open(r"hints.json", 'r', encoding='utf-8') as f:
            self.hint_list = json.load(f)

    def give_guess(self):
        guess_list = {}
        for guess_idx, guess in enumerate(self.supported_guesses):
            hint_count = {}
            for psb_ans_idx, psb_ans in enumerate(self.psb_answers):
                try:
                    hint_count[tuple(
                        self.hint_list[psb_ans_idx][guess_idx])] += 1
                except:
                    hint_count[tuple(
                        self.hint_list[psb_ans_idx][guess_idx])] = 1
            ent = 0
            for hint, count in hint_count.items():
                ent += count / len(self.psb_answers) * \
                    (-math.log2(count / len(self.psb_answers)))
            guess_list[guess_idx] = ent
        max_ent = -1
        max_guess = None
        for guess_idx, ent in enumerate(guess_list):
            if ent > max_ent:
                max_ent = ent
                max_guess = guess
        print(max_guess, max_ent)

    def store_result(self, guess, hint):
        # for psb_ans in self.possible_answers:
        #     if self.hint_dict[psb_ans][guess] != hint:
        #         self.possible_answers.remove(psb_ans)
        self.psb_answers = [psb_ans for psb_ans in self.psb_answers
                            if self.hint_list[psb_ans][guess] == hint]

    def clear(self):
        self.psb_answers = self.answers


if __name__ == '__main__':
    solve_hints()
