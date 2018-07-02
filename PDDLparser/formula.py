class FormulaAnd:

    def __init__(self, andList):
        self.andList = andList
        # print(self.andList)

    def __str__(self):
        return '(and {0})'.format(', '.join(map(str, self.andList)))

    # def __iter__(self):
    #     return iter(self.andList)

class FormulaOr:

    def __init__(self, orList):
        self.orList = orList

    def __str__(self):
        return '(or {0})'.format(', '.join(map(str, self.orList)))

    # def __iter__(self):
    #     return iter(self.orList)

class FormulaNot:

    def __init__(self, formula):
        self.formula = formula
        # print(self.formula)

    def __str__(self):
        # return '(not {0})'.format(', '.join(map(str, self.formula)))
        return '(not {0})'.format(self.formula)

    # def __iter__(self):
    #     return iter(self.formula)

class FormulaImply:

    def __init__(self, formula1, formula2):
        self.formula1 = formula1
        self.formula2 = formula2

    def __str__(self):
        return '(imply {0} {1})'.format(self.formula1, self.formula2)

class FormulaExists:

    def __init__(self, variables, formula):
        self.variables = variables
        self.formula = formula

    def __str__(self):
        return '(exists ({0}) {1})'.format(', '.join(map(str, self.variables)), self.formula)

class FormulaForall:

    def __init__(self, variables, formula):
        self.variables = variables
        self.formula = formula

    def __str__(self):
        return '(forall ({0}) {1})'.format(', '.join(map(str, self.variables)), self.formula)
