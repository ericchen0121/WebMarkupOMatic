import sys, re
from handlers import *
from rules import *
from util import *

class Parser: 
    """
    A Parser reads a text file, applying rules and controlling a handler.
    """
    # constructor, creates two empty lists
    def __init__(self, handler): 
        self.handler = handler
        self.rules = []
        self.filters = []
    # adds the rule to the rule list       
    def addRule(self, rule): 
        self.rules.append(rule)
    # creates the filter, then adds the filter to the filter list 
    def addFilter(self, pattern, name): 
        # what happens here? what about the block and handler arguments? 
        def filter(block, handler): 
            return re.sub(pattern, handler.sub(name), block)
        self.filters.append(filter)
    def parse(self, file): 
        self.handler.start('websitetext1.txt')
        for block in blocks(file):
            for filter in self.filters:
                block = filter(block, self.handler)
            for rule in self.rules:
                if rule.condition(block):
                    last = rule.action(block, self.handler)
                    if last: break
        self.handler.end('websitetext1.txt')

class BasicTextParser(Parser):
    """
    A specific Parser that adds rules and filters in its constructor
    """
    def __init__(self, handler): 
        Parser.__init__(self, handler)
        self.addRule(ListRule())
        self.addRule(ListItemRule())
        self.addRule(TitleRule())
        self.addRule(HeadingRule())
        self.addRule(ParagraphRule())

        self.addFilter(r'\*(.+?)\*', 'emphasis')
        self.addFilter(r'(http://[\.a-zA-Z0-9/]+)', 'url')
        self.addFilter(r'([\.a-zA-Z0-9/]+@[\.a-zA-Z/]+[a-zA-Z]+)', 'mail')

handler = HTMLRenderer()
parser = BasicTextParser(handler)

savein = sys.stdin
saveout = sys.stdout
infile = open('websitetext1.txt', 'r')
sys.stdin = infile
outfile = open('websitetext1.html', 'w')
sys.stdout = outfile

# run the program
parser.parse(infile)

outfile.close()
infile.close()
sys.stdout = saveout
#sys.stdin = savein


