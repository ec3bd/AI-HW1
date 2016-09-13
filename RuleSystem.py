import sys

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
        print("this is the learn function")

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
                elif(var not in self.facts and bool == "true"):
                    self.facts.append(var)
            else:
                print("You cannot change a learned variable directly")

    #For teaching new rules
    def teach3(self, expression, var):
        if(var in self.vars and not self.vars[var][0]):
            self.rules.append((expression, var))

    def query(self, expression):
        print(expression)

    def why(self, expression):
        print(expression)
