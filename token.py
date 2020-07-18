class Token:
    def __init__(self, type_t, val , l, pos_start, post_end, gv):
        self.type = type_t
        self.value = val
        self.line = l
        self.start = pos_start
        self.end = post_end
        self.grammar_val = gv

    def __repr__(self):
        if self.value :
            return '{type:'+self.type+', value:'+str(self.value)+ ', line:'+str(self.line)+ ', pos:'+str(self.start)+ ', posf:'+str(self.end)+ ', grammar value:'+str(self.grammar_val)+ '}'
        return '{type:' + self.type + '}'