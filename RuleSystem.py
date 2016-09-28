import sys
import re

class RuleSystem(object):

    def __init__(self):
        self.facts = []
        self.vars = dict()
        self.rules = []
        self.whyStack = []

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
                    self.vars[rule[1]][2] = rule[0]
                    didLearn = True


    # For creating variables
    # type - the -R or -L flag
    # var - the variable name to be created
    # phrase - the english string for the variable
    def teach1(self, type, var, phrase):
        if(var not in self.vars):
            if(type == "-R"):
                self.vars[var] = [True, phrase]
            else:
                self.vars[var] = [False, phrase, ""]

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

        # if verbose:
        #     print(expr)
        #     print(exprarr)
        #     for el in exprarr:
        #     if(exprarr[i] != '!' and exprarr[i] != '|' and exprarr[i] != '&'):
        #         exprarr[i] = replaceExpr(exprarr[i])
        #     elif(exprarr[i] is '!'):
        #         exprarr[i] = " not "
        #     elif(exprarr[i] is '&'):
        #         exprarr[i] = " and "
        #     elif(exprarr[i] is '|'):
        #         exprarr[i] = " or "
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

        return eval(stringcat)


    def resetLearned(self):
        for var in self.facts:
            if(not self.vars[var][0]):
                self.facts.remove(var)


    def Why2(self, expr, inner = False):
        variables = sorted(re.split('&|\||!|\(|\)',expr), key=len, reverse=True)
        while '' in variables: variables.remove('')
        result = self.parseExpression(expr)
        if(not inner): print(result)
        for var in variables:
            if self.vars[var][0]:  #is it a root var
                if var in self.facts:
                    #print('I KNOW THAT %s' %(var))  #self.vars[var][1]
                    self.whyStack.append('I KNOW THAT %s' %(var))
                else:
                    #print('I KNOW IT IS NOT TRUE THAT %s' %(var))
                    self.whyStack.append('I KNOW IT IS NOT TRUE THAT %s' %(var))
            else:
                rule = self.vars[var][2] # if empty then no rule led to the truth this variable has
                if rule == "":
                    #print('I KNOW IT IS NOT TRUE THAT %s' %(var))
                    self.whyStack.append('I KNOW IT IS NOT TRUE THAT %s' %(var))
                else:
                    args = sorted(re.split('&|\||!|\(|\)', self.vars[var][2]), key=len, reverse=True)
                    while '' in args: args.remove('')
                    for arg in args:
                        statement2 = var   #self.vars[var][1]
                        if self.vars[arg][0]: #if root var
                            if self.parseExpression(self.vars[var][2]):
                                #print('BECAUSE %s I KNOW THAT %s' %(arg, statement2))
                                self.whyStack.append('BECAUSE %s I KNOW THAT %s' %(arg, statement2))
                                self.Why2(arg, True)
                            else:
                               # print('BECAUSE It IS NOT TRUE THAT %s I CANNOT PROVE %s' %(arg, statement2))  #self.vars[arg][1]
                                self.whyStack.append('BECAUSE It IS NOT TRUE THAT %s I CANNOT PROVE %s' %(arg, statement2))
                        else:
                            if self.parseExpression(self.vars[var][2]): #eval(learned[var][2]) == True:
                                #print('BECAUSE %s I KNOW THAT %s' %(arg, statement2))
                                self.whyStack.append('BECAUSE %s I KNOW THAT %s' %(arg, statement2))
                            else:
                                #print('BECAUSE IT IS NOT TRUE THAT %s I CANNOT PROVE %s' %(arg, statement2))
                                self.whyStack.append('BECAUSE IT IS NOT TRUE THAT %s I CANNOT PROVE %s' %(arg, statement2))
        expression = expr
        if(expr in self.vars.keys() and self.vars[expr][0]): return
        expr_lookup = [] # avoids replace() issues
        for v in variables:
            if self.vars[v][0]: #if it is a root var
                expression = expression.replace(v,str(len(expr_lookup)))
                expr_lookup.append(self.vars[v][1])
            else:
                expression = expression.replace(v,str(len(expr_lookup)))
                expr_lookup.append(self.vars[v][1])
        for e in reversed(range(len(expr_lookup))):
            expression = expression.replace(str(e),expr_lookup[int(e)])
        expression = expression.replace('!',' NOT ')
        expression = expression.replace('&', ' AND ')
        expression = expression.replace('|', ' OR ')
        if not inner:
            while len(self.whyStack) != 0:
                print(self.whyStack.pop())
        if result:
            print('THUS I KNOW THAT %s' %(expression))
        else:
            print('THUS I CANNOT PROVE THAT %s' %(expression))

        if not inner:
            print()
            print()
            print()



