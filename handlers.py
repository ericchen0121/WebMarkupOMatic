class Handler: 
    """
    An object that handles method calls from the Parser. 

    The Parser will call the start() and end() methods at the 
    beginning of each block, with the proper block name as a parameter.
    The sub() method returns a method that will be used in regex substitution.
    When called with a name such as 'emphasis', it will return the proper
    substitution function.
    """

    def callback(self, prefix, name, *args): 
        # binds attribute to method
        method = getattr(self, prefix+name, None)
        # if attribute is a method, return it
        if callable(method): return method(*args)
    # helper method for callback() with prefix 'start_'
    def start(self, name): 
        self.callback('start_', name)
    # helper method for callback() with prefix 'end_'
    def end(self, name): 
        self.callback('end_', name)
    # for sub methods    
    def sub(self, name): 
        def substitution(match):
            result = self.callback('sub_', name, match)
            if result is None: match.group(0)
            return result
        return substitution

class HTMLRenderer(Handler): 
    def start_paragraph(self):
        print '<p>'
    def end_paragraph(self):
        print '</p>'     
    def feed(self, data):
        print data
    def start_heading(self): 
        print '<h2>'
    def end_heading(self): 
        print '</h2>'
    def start_title(self): 
        print '<h1>'
    def end_title(self): 
        print '</h1>'
    def start_list(self): 
        print '<ul>'
    def end_list(self): 
        print '</ul>'
    def start_listitem(self): 
        print '<li>'
    def end_listitem(self): 
        print '</li>'
    def sub_emphasis(self, match): 
        return '<em>%s</em>' % match.group(1)
    def sub_url(self, match): 
        return '<a href = "%s">%s</a>' % (match.group(1), match.group(1))
    def sub_mail(self, match): 
        return '<a href = "mailto:%s">%s</a>' % (match.group(1), match.group(1))
