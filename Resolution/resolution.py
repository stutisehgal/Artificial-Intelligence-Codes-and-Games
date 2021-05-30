# -*- coding: utf-8 -*-

class Substitution:
    def __init__(self, variable, replacement):
        self.variable = variable
        self.replacement = replacement

    def __str__(self):
        return str(self.variable) + " = " + str(self.replacement)
        
        
class Variable:
    def __init__(self, variable_name):
        if variable_name[0].islower(): raise (Exception("Variable name starting with lower-case!"))
        self.variable_name = variable_name

    def __eq__(self, other):
        return isinstance(other, Variable) and self.variable_name == other.variable_name

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return self.variable_name

    def __repr__(self):
        return str(self)

    def __hash__(self):

        return str(self).__hash__()

    def occurs_in(self, other):
        if isinstance(other, Variable) and self.__eq__(other):
            return True
        if isinstance(other, Expression) and self.__str__() in other.__str__():
            return True
        return False
        
        
class Constant:
    def __init__(self, constant_name):
        if constant_name[0].isupper(): raise (Exception("Constant name starting with upper-case!"))
        self.constant_name = constant_name

    def __eq__(self, other):
        return isinstance(other, Constant) and self.constant_name == other.constant_name

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return self.constant_name

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return str(self).__hash__()
        

class Expression:

    def __init__(self, operator, arguments):
        self.operator = operator
        self.arguments = arguments

    def __str__(self):
        return "%s(%s)" % (
            self.operator,
            ", ".join(map(str, self.arguments)))

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return str(self).__hash__()

    def __eq__(self, other):
        if not isinstance(other, Expression): return False
        if self.operator != other.operator: return False
        if len(self.arguments) != len(other.arguments): return False
        return all([a1 == a2 for a1, a2 in zip(self.arguments, other.arguments)])

    def __ne__(self, other):
        return not self.__eq__(other)

def parse_expression(s):
    l, d, i = [], 0, 0
    op, args = None, []
    for j, c in enumerate(s):
        if c == "(":
            if op is None:
                op = s[:j]
                i = j + 1
            d += 1
        if c == ")":
            if d == 1:
                if j > i: args.append(s[i:j])
                i = j + 1
            d -= 1
        if c == "," and d == 1:
            args.append(s[i:j])
            i = j + 1
        if c == " " and i == j: i += 1

    if op is None:
        if s[0].isupper():
            return Variable(s)
        else:
            return Constant(s)

    return Expression(op, list(map(parse_expression, args)))


def unify_with_occurrence_check(formular1, formular2, mgu=[], trace=False):
    # pp(trace, "Unifying expression:", formular1, "with expression:", formular2)
    if mgu is None:
        return None
    elif formular1 == formular2:
        return mgu
    elif isinstance(formular1, Variable):
        return unify_variable(formular1, formular2, mgu, trace)
    elif isinstance(formular2, Variable):
        return unify_variable(formular2, formular1, mgu, trace)
    elif isinstance(formular1, Expression) and isinstance(formular2, Expression):
        if type(formular1) != type(formular2) or formular1.operator != formular2.operator or len(
                formular1.arguments) != len(formular2.arguments):
            return None
        else:
            for a, b in zip(formular1.arguments, formular2.arguments):
                mgu = unify_with_occurrence_check(a, b, mgu, trace)
            return mgu
    else:
        return None


def substitute(sub, expr):
    for s in (x for x in sub if occurs_in(x.variable, expr)):
        if isinstance(expr, Variable):
            expr = s.replacement
        else:
            expr.arguments = [substitute(sub, e) for e in expr.arguments]
    return expr


def occurs_in(var, expr):
    if var == expr:
        return True
    if not isinstance(expr, Expression):
        return False
    return any([occurs_in(var, e) for e in expr.arguments])


def unify_variable(var, exp, mgu, trace):
    for s in (x for x in mgu if x.variable == var):
        return unify_with_occurrence_check(s.replacement, exp, mgu, trace)
    t = substitute(mgu, exp)
    if occurs_in(var, t) and isinstance(t, Expression):
        print("\nCannot unify - infinte loop exception!!!")
        return None
    else:
        s = Substitution(var, t)
        mgu = mgu + [s]
        for q in (x for x in mgu if x.replacement == s.variable):
            mgu.remove(q)
            new = Substitution(q.variable, s.replacement)
            mgu = mgu + [new]
        for r in (x for x in mgu if isinstance(x.replacement, Expression)):
            mgu.remove(r)
            a = substitute(mgu, r.replacement)
            b = Substitution(r.variable, a)
            mgu = mgu + [b]
        for s in (x for x in mgu if (x.variable == x.replacement)):
            mgu.remove(s)
        return mgu


def main():
    keep_running = True

    while keep_running:

        print("\nPlease enter the first expression:")
        t1 = input("-->")
        print("\nPlease enter the second expression:")
        t2 = input("-->")

        # mgu: Most General Unifier
        mgu = unify_with_occurrence_check(parse_expression(t1), parse_expression(t2), trace=False)
        if mgu is None:
            print("\nno")
        else:
            print("\n")
            print("\n".join(map(str, mgu)))
            print("\nyes")

        print("\n\n>>> Do you want to run unifier again? (Y/N)")
        re_run = input("--> ")

        if re_run != "y" and re_run != "Y":
            keep_running = False


# Run main
if __name__ == "__main__":
    main()


