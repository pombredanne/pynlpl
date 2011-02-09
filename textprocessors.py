###############################################################
#  PyNLPl - Text Processors
#       by Maarten van Gompel (proycon)
#       http://ilk.uvt.nl/~mvgompel
#       Induction for Linguistic Knowledge Research Group
#       Universiteit van Tilburg
#       
#       Licensed under GPLv3
# 
# This is a Python library containing text processors
#
###############################################################

import unicodedata
import string

class Windower:
    """Moves a sliding window over a list of tokens, returning all windows"""

    def __init__(self, tokens, n=1, beginmarker = "<begin>", endmarker = "<end>"):
        if isinstance(tokens, str) or  isinstance(unicode, str):
            self.tokens = tokens.split()
        else:
            self.tokens = tuple(tokens)
        self.n = n
        self.beginmarker = beginmarker
        self.endmarker = endmarker

    def __iter__(self):
        l = len(self.tokens)

        if self.beginmarker:
            beginmarker = (self.beginmarker),  #tuple
        if self.endmarker:
            endmarker = (self.endmarker),  #tuple

        for i in xrange(-(self.n - 1),l):
            begin = i
            end = i + self.n
            if begin >= 0 and end <= l:
                yield tuple(self.tokens[begin:end])
            elif begin < 0 and end > l:
                if not self.beginmarker or not self.endmarker:
                    continue
                else:
                   yield tuple(((begin * -1) * beginmarker  ) + self.tokens + ((end - l) * endmarker ))
            elif begin < 0:
                if not self.beginmarker: 
                   continue   
                else: 
                   yield tuple(((begin * -1) * beginmarker ) + self.tokens[0:end])
            elif end > l:
                if not self.endmarker:
                   continue
                else:
                   yield tuple(self.tokens[begin:] + ((end - l) * endmarker))


def calculate_overlap(haystack, needle, allowpartial=True):
    """Calculate the overlap between two sequences. Yields (overlap, placement) tuples (multiple because there may be multiple overlaps!). The former is the part of the sequence that overlaps, and the latter is -1 if the overlap is on the left side, 0 if it is a subset, 1, if it overlaps on the right side"""    
    needle = tuple(needle)
    haystack = tuple(haystack)
    solutions = []
    
    
    if allowpartial: 
        for l in range(1,min(len(needle) - 1, len(haystack))):        
            #Search for overlap left (including partial overlap!)
            if needle[-l:] == haystack[:l]:
                solutions.append( (needle[-l:], -1) )
            #Search for overlap right (including partial overlap!)
            if needle[:l] == haystack[-l:]:
                solutions.append( (needle[:l], 1) )

    if len(needle) <= len(haystack):
        for option in Windower(haystack,len(needle)):
            if option == needle:
                solutions.append( (needle, 0) )

    return solutions
            
    

def crude_tokenizer(line):
    """This is a very crude tokenizer"""
    tokens = []
    buffer = ''
    for c in line.strip():
        if c == ' ' or c in string.punctuation:
            if buffer:
                tokens.append(buffer)
                buffer = ''
        else:
            buffer += c          
    if buffer: tokens.append(buffer)  
    return tokens

def strip_accents(s, encoding= 'utf-8'):
      if isinstance(s,unicode):
          return unicodedata.normalize('NFKD', s).encode('ASCII', 'ignore')
      else:
          return unicodedata.normalize('NFKD', unicode(s,encoding)).encode('ASCII', 'ignore')


