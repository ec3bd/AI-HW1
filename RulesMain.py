import RuleSystem
import fileinput

def main():
    ruleSystem = RuleSystem.RuleSystem()

    for line in fileinput.input():
        parseCommand(ruleSystem, line)

def parseCommand(rs, line):
    line = line.rstrip();
    commandParts = line.split(' ')
    if(commandParts[0] == "Teach"):
        if(line.find("->") != -1):
            rs.teach3(commandParts[1], commandParts[3])
        elif (len(commandParts) == 4):
            rs.teach2(commandParts[1], commandParts[3])
        elif(len(commandParts) >= 5):
            rs.teach1(commandParts[1], commandParts[2], line.split("\"")[1])
    elif(commandParts[0] == "List"):
        rs.list()
    elif(commandParts[0] == "Learn"):
        rs.learn()
    elif(commandParts[0] == "Query"):
        rs.query(commandParts[1])
    elif(commandParts[0] == "Why"):
        rs.why(commandParts[1])
    elif(commandParts[0] == "Parse"):
        rs.parseExpression(commandParts[1])

if __name__ == "__main__":
    main()
