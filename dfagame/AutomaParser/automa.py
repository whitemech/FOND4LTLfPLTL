import re

class Automa:
    """
        DFA Automa:
        - alphabet         => set() ;
        - states           => set() ;
        - initial_state    => str() ;
        - accepting_states => set() ;
        - transitions      => dict(), where
        **key**: *source* ∈ states
        **value**: {*action*: *destination*)
    """
    MAX_ALPHABET = 26
    en_alphabet = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                   'u', 'v', 'w', 'x', 'y', 'z')
    used_alpha = None

    def __init__(self, alphabet, states, initial_state, accepting_states, transitions):
        self.alphabet = alphabet
        self.states = states
        self.initial_state = initial_state
        self.accepting_states = accepting_states
        self.transitions = transitions
        self.transitions_by_destination = self.group_conditions_by_consequence()
        self.validate()

    def valide_transition_start_states(self):
        for state in self.states:
            if state not in self.transitions:
                raise ValueError(
                    'transition start state {} is missing'.format(
                        state))

    def validate_initial_state(self):
        if self.initial_state not in self.states:
            raise ValueError('initial state is not defined as state')

    def validate_accepting_states(self):
        if any(not s in self.states for s in self.accepting_states):
            raise ValueError('accepting states not defined as state')

    def validate_input_symbols(self):
        alphabet_pattern = self.get_alphabet_pattern()
        for state in self.states:
            for action in self.transitions[state]:
                if not re.match(alphabet_pattern, action):
                    raise ValueError('invalid transition found')

    def get_alphabet_pattern(self):
        return re.compile("(^["+''.join(self.alphabet)+"]+$)")

    def validate(self):
        self.validate_initial_state()
        self.validate_accepting_states()
        self.valide_transition_start_states()
        self.validate_input_symbols()
        return True

    def __str__(self):
        automa = 'alphabet: {}\n'.format(str(self.alphabet))
        automa += 'states: {}\n'.format(str(self.states))
        automa += 'init_state: {}\n'.format(str(self.initial_state))
        automa += 'accepting_states: {}\n'.format(str(self.accepting_states))
        automa += 'transitions: {}'.format(str(self.transitions))
        return automa

    def create_operator_trans(self):
        '''create operator trans as a string'''
        operator  = 'trans\n'
        operator += '\t:parameters ()\n'
        operator += '\t:precondition (not (turnDomain))\n'
        operator += '\t:effect (and {0}\t)\n'.format(' '.join(self.get_whens()))
        return operator

    def get_whens(self):
        whens = []
        for destination, source_action in self.transitions_by_destination.items():
            if source_action == []:
                pass
            else:
                whens.append(self.get_formula_when(destination, source_action))
        return whens

    def get_formula_when(self, destination, source_action_list):
        formula_when  = '(when {0} {1})\n'.format(self.get_formula_condition(source_action_list),self.get_formula_statement(destination))
        return formula_when

    def get_formula_condition(self, source_action_list):
        if len(source_action_list) == 1:
            if self.get_condition_action(source_action_list[0][1]) == []:
                formula_condition = '(q{0})'.format(source_action_list[0][0])
            else:
                formula_condition = '(and (q{0}) {1})'.format(source_action_list[0][0], ' '.join(self.get_condition_action(source_action_list[0][1])))
        else:
            formula_condition = '(or {0})'.format(' '.join(self.get_or_conditions(source_action_list)))
        return formula_condition

    def get_or_conditions(self, source_action_list):
        items = []
        for source, action in source_action_list:
            formula_conditions = self.get_condition_action(action)
            if formula_conditions == []:
                items.append('(q{0})'.format(source))
            else:
                items.append( '(and (q{0}) {1})'.format(source, ' '.join(self.get_condition_action(action))))
        return items

    def get_formula_statement(self, destination):
        negated_states = []
        for state in self.states:
            if state != destination:
                negated_states.append('(not q{0})'.format(state))
            else:
                pass
        formula_statement = '(and (q{0}) {1} (turnDomain))'.format(destination, ' '.join(negated_states))
        return formula_statement

    # def get_whens(self):
    #     whens = []
    #     for state in self.states:
    #         for action in self.transitions[state]:
    #             whens.append(self.get_formula_when(state,action))
    #     return whens
    #
    # def get_formula_when(self, state, action):
    #     formula_when  = '(when {0} {1})\n'.format(self.get_formula_condition(state, action),self.get_formula_statement(state, action))
    #     return formula_when
    #
    # def get_formula_condition(self, state, action):
    #     if self.get_condition_action(action) == []:
    #         formula_condition = '(= q {0})'.format(state)
    #     else:
    #         formula_condition = '(and (= q {0}) {1})'.format(state, ' '.join(self.get_condition_action(action)))
    #     return formula_condition
    #
    # def get_formula_statement(self, state, action):
    #     formula_statement = '(and (= q {0}) (turnDomain))'.format(self.transitions[state][action])
    #     return formula_statement

    def get_condition_action(self, action):
        temp = []
        length = len(action)
        self.used_alpha = self.en_alphabet[0:length]
        i = 0
        for char in action:
            if char == '1':
                temp.append('('+self.used_alpha[i]+')')
            elif char == '0':
                temp.append('(not ('+self.used_alpha[i]+'))')
            else:
                pass
            i += 1
            if i > self.MAX_ALPHABET:
                break
        return temp

    def create_dict_by_destination(self):
        trans_by_dest = {}
        for state in self.states:
            trans_by_dest[state] = []
        return trans_by_dest

    def group_conditions_by_consequence(self):
        group_by_dest = self.create_dict_by_destination()
        for source, trans in self.transitions.items():
            i = 0
            for dest in trans.values():
                group_by_dest[dest].append((source, list(trans.keys())[i]))
                i +=1
        return group_by_dest