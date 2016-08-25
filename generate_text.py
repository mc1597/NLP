#!/usr/bin/python

import re
import string
import unicodedata as ud
import matplotlib.pyplot as plt


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

def adj(oldlist):
	newlist = [i-1 for i in oldlist]
	return newlist

def func(main,locs_prev,s):
    
    final = []
    start_at = -1

    while start_at < len(main):
    	try:
        	loc = main.index(s,start_at+1)
		#print s,loc
                
        except ValueError:
        	break

        if locs_prev != [] and loc-1 in locs_prev and loc+1 not in final:                  
        	
                final.append(loc+1)
                start_at = loc
       	elif locs_prev == [] and loc+1 not in final:
                
                final.append(loc+1)
                start_at = loc
        else:        
        	start_at = start_at + 1

        
    return final

if __name__ == '__main__':
	
    #n = input('Choose the ngram value: ')
    
    tokenizer = TwitterTokenizer()
    f = open('Text2_Imp.txt')
    tweets = f.readlines()
    decoded_token = []	
    text_list = []  	
    for s in tweets:
	
	ngram_list = []	
        #print("======================================================================")
        #print(s)
        tokens = tokenizer.tokenization(s)
	for t in tokens:
		#print t
		t = t.decode('unicode-escape').encode('latin1').decode('utf8')
		decoded_token.append(t)
		
    decoded_token = [x.encode('UTF8') for x in decoded_token]		
    total_tokens = len(decoded_token)
    	
    ngram_list = []
    for token in decoded_token:
	if token not in [i[0] for i in ngram_list]:
		ngram_list.append([token,1])
	else:
		ind = [t[0] for t in ngram_list].index(token)
		ngram_list[ind][1]+=1

   
	
    ngram_list.sort(key=lambda x: x[1],reverse=True)
    #print ngram_list	
    unigram = ngram_list[0][0]
    #print unigram
    
    text_list.append(unigram)			
    ngram_prev = []	    
    for i in range(100):
	temp_list = []
    	ngram_loc = func(decoded_token,ngram_prev,text_list[-1])	
	ngram_prev = adj(ngram_loc)
    	#print ngram_loc    
    	for pos in ngram_loc:
		m = decoded_token[pos]
		if m not in [j[0] for j in temp_list]:
			temp_list.append([m,1])
		else:
			ind2 = [t[0] for t in temp_list].index(m)
			temp_list[ind2][1]+=1
	
    	temp_list.sort(key=lambda x: x[1],reverse=True)
	
    	unigram = temp_list[0][0]
	text_list.append(unigram)
    
    
    
    #print decoded_token
    print text_list	
	
