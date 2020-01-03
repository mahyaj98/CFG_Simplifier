import string
from itertools import chain, combinations

alphabet = list(string.ascii_lowercase)
variables = list(string.ascii_uppercase)


def powerset(iterable):
    xs = list(iterable)
    return chain.from_iterable(combinations(xs, n) for n in range(len(xs) + 1))


class ContextFree:

    def __init__(self, r, s):
        self.v = variables
        self.sigma = alphabet
        self.r = r
        self.s = s

    def generalize(self):
        self.__remove_lambda()
        # print(self.r)
        self.__remove_unit_rules()
        # print(self.r)
        self.__remove_useless_variables()

    def __remove_lambda(self):
        v_n = []
        for leading_rule, result_rule in self.r.items():
            for right_result in result_rule:
                if right_result == 'λ':
                    v_n.append(leading_rule)
        sth_new_added = True
        while sth_new_added:
            sth_new_added = False
            for leading_rule, result_rule in self.r.items():
                if leading_rule not in v_n:
                    need_to_be_vn_exact = False
                    for right_result in result_rule:
                        need_to_be_vn = True
                        for element in right_result:
                            if element not in v_n:
                                need_to_be_vn = False
                        need_to_be_vn_exact = need_to_be_vn_exact or need_to_be_vn
                    if need_to_be_vn_exact:
                        sth_new_added = True
                        v_n.append(leading_rule)
        new_grammer = {}
        too_new_grammer = {}
        if len(v_n) != 0:
            for leading_rule, result_rule in self.r.items():
                for right_result in result_rule:
                    for combination in powerset(v_n):
                        if len(combination) > 0:
                            new_result = right_result
                            for element_of_combination in combination:
                                new_result = new_result.replace(element_of_combination, '')
                                new_result = new_result.replace('λ', '')

                            if len(new_result) > 0:
                                if leading_rule not in new_grammer:
                                    new_grammer[leading_rule] = []
                                new_grammer[leading_rule].append(new_result)
                        else:
                            new_result = right_result.replace('λ', '')
                            if len(new_result) > 0:
                                if leading_rule not in new_grammer:
                                    new_grammer[leading_rule] = []
                                new_grammer[leading_rule].append(new_result)
            for leading, result in new_grammer.items():
                new_grammer[leading] = list(set(result))
            for leading_rule, result_rule in new_grammer.items():
                for rule in result_rule:
                    gonna_add = True
                    for letter in rule:
                        if letter in self.v and letter not in new_grammer:
                            gonna_add = False
                    if gonna_add:
                        if leading_rule not in too_new_grammer:
                            too_new_grammer[leading_rule] = []
                        too_new_grammer[leading_rule].append(rule)
            self.r = too_new_grammer

    def __remove_useless_variables(self):
        using_variables_type_one = []
        using_variables_type_two = [self.s]
        using_variables_type_three = []
        continue_bool = True
        while continue_bool:
            continue_bool = False
            for leading, res in self.r.items():
                for element in res:
                    endless = False
                    for letter in element:
                        if not ((letter in alphabet) or (letter in using_variables_type_one)):
                            endless = True
                    if not endless and leading not in using_variables_type_one:
                        using_variables_type_one.append(leading)
                        continue_bool = True
        while len(using_variables_type_two) > 0:
            goal = using_variables_type_two.pop()
            using_variables_type_three.append(goal)
            for element in self.r[goal]:
                for letter in element:
                    if letter in variables and letter not in using_variables_type_two and letter not in using_variables_type_three:
                        using_variables_type_two.append(letter)
        new_rule = {}
        for leading, res in self.r.items():
            add = True
            if leading in variables and (
                    leading not in using_variables_type_one or leading not in using_variables_type_three):
                add = False
            if add:
                tmp_add = []
                for rule in res:
                    gonna_add = True
                    for letter in rule:
                        if (letter in self.v) and (
                                (letter not in using_variables_type_one) or (letter not in using_variables_type_three)):
                            gonna_add = False
                    if gonna_add:
                        tmp_add.append(rule)
                if len(tmp_add) > 0:
                    new_rule[leading] = []
                    new_rule[leading] = tmp_add
        self.r = new_rule

    def __remove_unit_rules(self):

        def is_unit(a_rule):
            return a_rule in self.v

        new_rules = {}
        new_rule_added = False
        for leading, res in self.r.items():
            new_rules[leading] = {}
            new_rules[leading]['unit'] = []
            new_rules[leading]['non_unit'] = []
            for rule in res:
                if is_unit(rule):
                    new_rules[leading]['unit'].append(rule)
                    new_rule_added = True
                else:
                    new_rules[leading]['non_unit'].append(rule)
        while new_rule_added:
            new_rule_added = False
            for leading, res in new_rules.items():
                for rule in res['unit']:
                    for unit_rule in new_rules[rule]['unit']:
                        if unit_rule not in new_rules[leading]['unit'] and unit_rule != leading:
                            new_rules[leading]['unit'].append(unit_rule)
                            new_rule_added = True
        too_new_rules = {}
        for leading, res in new_rules.items():
            too_new_rules[leading] = [i for i in res['non_unit']]
            for element in res['unit']:
                too_new_rules[leading] += [i for i in new_rules[element]['non_unit']]
        self.r = too_new_rules


c = ContextFree({'S': ['aA', 'aBB'], 'A': ['aaA', 'λ'], 'B': ['bC','bbC'], 'C': ['B']}, 'S')

c.generalize()
print(c.r)
