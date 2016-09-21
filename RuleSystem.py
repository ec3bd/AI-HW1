import sys
import re

class RuleSystem(object):

    def __init__(self):
        self.facts = []
        self.vars = dict()
        self.rules = []

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
        print(self.parseExpression(expression))
        self.parseExpression(expression, True)


    def parseExpression(self, expr, verbose=False):
        p = re.compile('.*[(|&!]+.*')
        paren = p.match(expr)
        if(not paren):
            if(expr in self.facts):
                return "True"
            else:
                return "False"
        stack = []
        temp = ""
        parenind = 0
        lastopind = -1
        exprarr = []
        exprlen = len(expr)
        for i in range(0,exprlen):
            char = expr[i]
            if((char == '|' or char =='&') and len(stack) == 0):
                if(expr[i-1] != ')'): exprarr.append(expr[lastopind+1:i])#may need additional testing
                exprarr.append(expr[i])
                lastopind = i
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
                    exprarr.append(expr[parenind+1 : i])
        #for the last subexpression if it isn't parenthesized
        if(expr[exprlen-1] != ')'):
            exprarr.append(expr[lastopind+1:])

        if verbose:
            print(expr)
            print(exprarr)
        length = len(exprarr)
        for i in range(0,length):
            if(exprarr[i] != '!' and exprarr[i] != '|' and exprarr[i] != '&'):
                if(verbose): exprarr[i] = self.parseExpression(exprarr[i], True)
                else: exprarr[i] = self.parseExpression(exprarr[i])
            elif(exprarr[i] is '!'):
                exprarr[i] = " not "
            elif(exprarr[i] is '&'):
                exprarr[i] = " and "
            elif(exprarr[i] is '|'):
                exprarr[i] = " or "

        stringcat = ""
        for el in exprarr:
            stringcat += str(el)

        if verbose:
            print(stringcat)
        return eval(stringcat)

    def resetLearned(self):
        for var in self.facts:
            if(not self.vars[var][0]):
                self.facts.remove(var)
    

