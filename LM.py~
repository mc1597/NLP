#!/usr/bin/python

import re
import string
import unicodedata as ud
import matplotlib.pyplot as plt
import numpy as np

regex_strings = (
    #glyph:
    r"""
    (?:(\\x..){1,})
    """,	
    # Phone numbers:
    r"""
    (?:
      (?:            
        \+?[01]
        [\-\s.]*
      )?            
      (?:            
        [\(]?
        \d{3}
        [\-\s.\)]*
      )?    
      \d{3}          
      [\-\s.]*   
      \d{4}          
    )"""
    ,
    # Emoticons:
    r"""
    (?:
      [<>]?
      [:;=8]                     
      [\-o\*\']?                 
      [\)\]\(\[dDpP/\$\:\}\{@\|/] 
      |
      [\)\]\(\[dDpP/\$\:\}\{@\|/] 
      [\-o\*\']?                 
      [:;=8]                     
      [<>]?
    )"""
    ,
    # HTML tags:
    r"""(?:<[^>]+>)"""
    ,
    # URLs:
    r"""(?:http[s]?://t.co/[a-zA-Z0-9]+)"""
    ,
    #Incomplete Sentence:
    r"""(?:[\w_:/]+\\xe2\\x80\\xa6)"""
    ,	 
    # Twitter username:
    r"""(?:@[\w_]+)"""
    ,
    # Twitter hashtags:
    r"""(?:\#+[\w_]+[\w\'_\-]*[\w_]+)"""
    ,
  
    # Remaining word types:
    r"""
    (?:[a-z][a-z'\-_]+[a-z])       # Words with ' or -
    |
    (?:[+\-]?\d+[,/.:-]\d+[+\-]?)  # Numbers, fractions,etc also handled
    |
    (?:[\w_]+)                     # Normal words - no ' or -
    |
    (?:[?!.](?:\s*[?!.]){1,})      # Punctuation including ... or !! etc. 
    |
    (?:\S)                         # Remaining
   	
    """
)

word_re = re.compile(r"""(%s)""" % "|".join(regex_strings), re.VERBOSE | re.I | re.UNICODE)
#glyph_re = re.compile(r"(\\x.*\\x..)", re.VERBOSE | re.I | re.UNICODE)
amp = "&amp;"

###########################################################################################
class TwitterTokenizer(object):

    def tokenization(self, tweet):
	tweet = repr(tweet)
	tweet = string.replace(tweet,'\\n','')
	tweet = string.replace(tweet,'\\\'','\'')
	tweet = tweet[1:-1]	
	#print "TWEET: ",tweet
        matches = word_re.finditer(tweet)
        return [match.group() for match in matches]


def func(f):
    tokenizer = TwitterTokenizer()
    tweets = f.readlines()
    num_sen = len(tweets) 
    ending = []
    for s in tweets:
	decoded_token = []
	ngram_list = []	
	temp = []
        #print("======================================================================")
        #print(s)
        tokens = tokenizer.tokenization(s)
	for t in tokens:
		#print t
		t = t.decode('unicode-escape').encode('latin1').decode('utf8')
		decoded_token.append(t)
	
	
	decoded_token = [x.encode('UTF8') for x in decoded_token]
	#print decoded_token
			
	length = len(decoded_token)
	
	for tok in decoded_token:
		if tok not in [t[0] for t in ending]:
			ending.append([tok,1])
		else:
			ind = [t[0] for t in ending].index(tok)
			ending[ind][1]+=1
			

    ending.sort(key=lambda x: x[-1],reverse=True)
    return ending
#for l in ending:
#	l[-1]/=float(num_sen)

if __name__ == '__main__':
	
    books = ['Text1_Pride.txt','Text2_Imp.txt','Text3_Iliad.txt','Text4_Jeeves.txt','Text5_SecretGarden.txt'] 	
    ending = []
    for i in range(len(books)):	
    	f = open(books[i])	
    	ending.append(func(f))	 		
	plt.loglog([x for x in range(1,len(ending[i])+1)],[t[1] for t in ending[i]],basex=np.e,basey=np.e,label=books[i])

plt.legend()
plt.show()
					
	



