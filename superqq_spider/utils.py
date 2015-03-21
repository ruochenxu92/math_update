__author__ = 'Xiaomin'

class utils:
    def __init__(self):
        pass

    def once_clean(self, sol):
        sol = self.remove(sol, '$')
        sol = self.remove_pair(sol, '{','}')
        sol = self.remove_pair(sol, '<','>')
        sol = self.filter_str(sol, '\\')
        return ' '.join(sol.split())


    def remove(self, my, tag):
        buffer = ''
        open_tag = False
        for i in range(len(my)):
            if (my[i] == tag and open_tag):
                open_tag = False
            elif (my[i] == tag and open_tag == False):
                open_tag = True
            elif (my[i] != tag and open_tag):
                pass
            else:
                buffer += my[i]
        return buffer

    def remove_pair(self, my, start_tag, end_tag):
        buffer = ''
        open_tag = False
        for i in range(len(my)):
            if (my[i] == end_tag):   #end
                open_tag = False
            elif (my[i] == start_tag): #start
                open_tag = True
            elif (open_tag): #inside tags
                pass
            else: #outside tags
                buffer += my[i]
        return buffer

    def filter_str(self, my, c):
        buffer = ''
        for i in range(len(my)):
            if (my[i] == c):
                buffer += ' '
            else:
                buffer += my[i]
        return buffer