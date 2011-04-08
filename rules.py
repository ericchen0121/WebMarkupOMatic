
"""
Basic pseudocode of how each rule works: 
class HeadlineRule: 
    def condition(self, block):
        if the block fits the definition of the code, return true, else return false
    def action(self, block, handler): 
        call methods such as handler.start('headline'), handler.feed(block) and handler.end('headline'). 
        return true when this is done so no processing is done on other rules. 
"""

class Rule: 
    """
    Base class for all rules.
    """
    def action(self, block, handler):
        # appropriate type string argument
        handler.start(self.type)
        handler.feed(block)
        handler.end(self.type)
        return True


class HeadingRule(Rule): 
    """
    A heading is a single line that is at most 70 characters and 
    that doesn't end with a colon.
    """
    type = 'heading'
    def condition(self, block): 
        return not '\n' in block and len(block) <= 70 and not block[-1] == ':'

class TitleRule(Rule): 
    """
    The title is the first block in the document, provided that it is a heading.
    """
    type = 'title'

    #works only for the first block...
    first = True

    def condition(self, block): 
        if not self.first: return False
        self.first = False    
        return HeadingRule.condition(HeadingRule(), block)

class ListItemRule(Rule):
    """
    A list item is a block that begins with a hyphen (-).
    """
    type = 'listitem'
    def condition(self, block): 
        return block[0] == '-'
        
    # reimplementing the Rule.action() with a slight modification
    def action(self, block, handler):
        # appropriate type string argument
        handler.start(self.type)
        # strip the hyphen, and strip any remaining whitespace
        handler.feed(block[1:].strip())
        handler.end(self.type)
        return True
        
# necessary since there is a separate tag for the list from each list item
# this rule will first "flag" whether to start the list rule, then the list items will run
class ListRule(Rule): 
    """
    A list begins between a block that is not a list item and a subsequent
    list item. It ends after the last consecutive list item.
    """
    type = 'list'
    inside = False

    # this will test every single block 
    def condition(self, block):
        return True

    def action(self, block, handler): 
        if not self.inside and ListItemRule.condition(ListItemRule(), block): 
            handler.start(self.type)
            self.inside = True
            # not sure why I don't process the ListItem action: ListItemRule.action(self, block, handler)
        elif self.inside and not ListItemRule.condition(ListItemRule(), block):
            handler.end(self.type)
            self.inside = False
        # False allows the rule processing to continue on other blocks, else it would continue actions here
        return False

class ParagraphRule(Rule): 
    """
    A paragraph is simply a block that isn't covered by any of the other rules.
    """
    type = 'paragraph'

    # this is the default condition, and will always return true. 
    # this rule will be implemented last and catch everything else
    def condition(self, block): 
        return True


