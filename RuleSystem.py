import sys
import re

NOT_OPERATOR = '!'
AND_OPERATOR = '&'
OR_OPERATOR = '|'
precedence = {NOT_OPERATOR: 3, AND_OPERATOR: 2, OR_OPERATOR: 1,  '(': 0}

class RuleSystem(object):

    def __init__(self):
        self.facts = []
        self.vars = dict()
        self.rules = []

    def to_postfix(self, expr):
        operators = []
        postfix = []
        for token in expr:
            if token == NOT_OPERATOR or token == AND_OPERATOR or token == OR_OPERATOR:
                while len(operators) > 0 and precedence[token] <= precedence[operators[-1]]:
                    postfix.append(operators[-1])
                    operators.pop()
                operators.append(token)
            elif token == '(':
                operators.append('(')
            elif token == ')':
                while operators[-1] != '(':
                    postfix.append(operators.pop())
                operators.pop()
            else:
                postfix.append(token)
        while len(operators) > 0:
            postfix.append(operators.pop())
        return postfix

    def list(self):
        print("Root Variables:")
        for k in self.vars:
            if(self.vars[k][0]):
                print("\t" + k +" = \"" + self.vars[k][1] + "\"")
        print("\nLearned Variables:")
        for k in self.vars:
            if(not self.vars[k][0]):
                print("\t" + k +" = \"" + self.vars[k][1] + "\"")
        print("\nFacts:")
        for fact in self.facts:
            print("\t" + fact)
        print("\nRules:")
        for k in self.rules:
            print("\t" + k[0] + " -> " + k[1])


    def learn(self):
        didLearn = True
        while(didLearn):
            didLearn = False
            for rule in self.rules:
                if(self.parseExpression(rule[0]) and (rule[1] not in self.facts)):
                    self.facts.append(rule[1])
                    didLearn = True


    # For creating variables
    # type - the -R or -L flag
    # var - the variable name to be created
    # phrase - the english string for the variable
    def teach1(self, type, var, phrase):
        if(var not in self.vars):
            if(type == "-R"):
                self.vars[var] = (True, phrase)
            else:
                self.vars[var] = (False, phrase)

    #For setting root variables
    def teach2(self, var, bool):
        if(var in self.vars):
            if(self.vars[var][0]):
                if(var in self.facts and bool == "false"):
                    self.facts.remove(var)
                    self.resetLearned()
                elif(var not in self.facts and bool == "true"):
                    self.facts.append(var)
                    self.resetLearned()
            else:
                print("You cannot change a learned variable directly.")

    #For teaching new rules
    def teach3(self, expression, var):
        if(var in self.vars and not self.vars[var][0]):
            self.rules.append((expression, var))

    def query(self, expression):
        res = self.parseExpression(expression)
        print("Query: " + expression + " is " + str(res))
        return res

    def why(self, expression):
        self.why2(self.to_postfix(expression))
        

    def parseExpression(self, expr, verbose=False):
        p = re.compile('.*[(|&!]+.*')
        paren = p.match(expr)
        if(not paren): #if there are no connectives (single var)
            if(expr in self.facts):
                if(verbose):
                    verboselist.append("I KNOW IT IS TRUE THAT " + expr)
                    print "I KNOW IT IS TRUE THAT " + expr

                return "True"
            else:
                if(verbose):
                    verboselist.append("I KNOW IT IS NOT TRUE THAT " + expr)
                    print "I KNOW IT IS NOT TRUE THAT " + expr
                return "False"
        stack = []
        temp = ""
        parenind = 0
        lastopind = -1
        exprarr = []
        exprlen = len(expr)
        for i in range(0,exprlen):
            char = expr[i]
            if((char == '|' or char =='&') and len(stack) == 0): # reach an 'or' or 'and' and not in parentheses
                if(expr[i-1] != ')'): #if you didn't just end parentheses
                    exprarr.append(expr[lastopind+1:i]) #add non-parenthesized top level subexpressions
                    #may need additional testing
                exprarr.append(expr[i]) #adds the current operator
                lastopind = i #catch the next non-parenthesized top expression
            elif(char == '!' and len(stack) == 0):
                exprarr.append(expr[i]) 
                lastopind = i
            elif(char == '('):
                stack.append(char)
                if(len(stack) == 1):
                    parenind = i
            elif(char == ')'):
                stack.pop()
                if(len(stack) == 0):
                    exprarr.append(expr[parenind+1 : i]) #put the full sub-expression in
        #for the last subexpression if it isn't parenthesized
        if(expr[exprlen-1] != ')'):
            exprarr.append(expr[lastopind+1:])

        if verbose:
            print(expr)
            print(exprarr)
        length = len(exprarr)
        for i in range(0,length):
            if(exprarr[i] != '!' and exprarr[i] != '|' and exprarr[i] != '&'):
                if(verbose): 
                    exprarr[i] = self.parseExpression(exprarr[i], True)
                else: 
                    exprarr[i] = self.parseExpression(exprarr[i])
            elif(exprarr[i] is '!'):
                exprarr[i] = " not "
            elif(exprarr[i] is '&'):
                exprarr[i] = " and "
            elif(exprarr[i] is '|'):
                exprarr[i] = " or "

        stringcat = ""
        for el in exprarr:
            stringcat += str(el)


        return eval(stringcat)

    def why2(self, postfix_expr):
        operands = []
        reasoning = []
        for token in postfix_expr:
            if token == '&':
                v1, e1 = operands.pop()
                v2, e2 = operands.pop()

                operands.append((v1 and v2, '(%s AND %s)' % (e2, e1)))
                if v1 and v2:
                    reasoning.append('I THUS KNOW THAT %s AND %s' % (e2, e1))
                else:
                    reasoning.append('THUS I CANNOT PROVE %s AND %s' % (e2, e1))
            elif token == '|':
                v1, e1 = operands.pop()
                v2, e2 = operands.pop()
                operands.append((v1 or v2, '(%s OR %s)' % (e2, e1)))
                if v1 or v2:
                    reasoning.append('I THUS KNOW THAT %s OR %s' % (e2, e1))
                else:
                    reasoning.append('THUS I CANNOT PROVE %s OR %s' % (e2, e1))
            elif token == '!':
                v, e = operands.pop()
                operands.append((not v, '(NOT %s)' % e))
                if not v:
                    reasoning.append('I THUS KNOW THAT NOT %s' % e)
                else:
                    reasoning.append('THUS I CANNOT PROVE NOT %s' % e)
            else:
                has_rule = False
                truth = False

                var_reasoning = []
                var_rules = []

                for lhs, postfix, rhs in rules:
                    if rhs == token:
                        has_rule = True
                        expr_truth, expr_rule, expr_reasoning = why(postfix)
                        var_reasoning = var_reasoning + expr_reasoning
                        var_rules.append(expr_rule)
                        truth = truth or expr_truth
                        if truth:
                            var_reasoning = expr_reasoning
                            var_rules = [expr_rule]
                            break

                reasoning = reasoning + var_reasoning
                if has_rule:
                    operands.append((truth, variables[token]))
                    if truth:
                        reasoning.append('BECAUSE %s I KNOW THAT %s' % (var_rules[0], variables[token]))
                    else:
                        for var_rule in var_rules:
                            reasoning.append('BECAUSE IT IS NOT TRUE THAT %s I CANNOT PROVE'
                                             ' %s' % (var_rule, variables[token]))

                else:
                    operands.append((token in facts, variables[token]))
                    if token in facts:
                        reasoning.append("I KNOW THAT %s" % variables[token])
                    else:
                        reasoning.append("I KNOW IT IS NOT TRUE THAT %s" % variables[token])

        #print(operands[-1][0], operands[-1][1], reasoning)
        return operands[-1][0], operands[-1][1], reasoning





    def resetLearned(self):
        for var in self.facts:
            if(not self.vars[var][0]):
                self.facts.remove(var)


