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


def count(main,sub):
    locs_prev = []
    locs_curr = []
    final = []
    start_at = -1
    for s in sub:
        #print s
        final = []
        while start_at < len(main):
            try:
                loc = main.index(s,start_at+1)
                #print s,loc
            except ValueError:
                break
            if locs_prev != [] and loc-1 in locs_prev:
                    #print "In here",loc,s
                    locs_curr.append(loc)
                    final.append(loc+1)
                    start_at = loc
            elif locs_prev == []:
                    locs_curr.append(loc)
                    final.append(loc+1)
                    start_at = loc
            else:        
                start_at += 1
        locs_prev = locs_curr
        locs_curr = []
        
        start_at = -1
    return len(locs_prev)
	
def Probability(text,vocab,freq,n):
	N = len(text)
	V = len(vocab)
	return float(freq+1)/float(N+(V**n))

def common(text,sample):
	count = 0
	text_init = [x[0] for x in text]
	sample_init = [x[0] for x in sample]
	for element in sample_init:
        	if element in text_init:
        	    count += 1
	return count

def func(tweets):
    
    num_sen = len(tweets) 
    ending = []
    full_text = []	
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
	full_text += decoded_token		
	length = len(decoded_token)
	
	for tok in decoded_token:
		if tok not in [t[0] for t in ending]:
			ending.append([tok,1])
		else:
			ind = [t[0] for t in ending].index(tok)
			ending[ind][1]+=1
			

    ending.sort(key=lambda x: x[-1],reverse=True)
    return ending,full_text
#for l in ending:
#	l[-1]/=float(num_sen)

if __name__ == '__main__':
   
    	
    tokenizer = TwitterTokenizer() 
    fname = raw_input('Input file name: ')
    g = open(fname)	
    word = g.readlines()	
    
    #print word_list		
    books = {'Text1_Pride.txt':'Jane Austen','Text2_Imp.txt':'Oscar Wilde','Text3_Iliad.txt':'Homer','Text4_Jeeves.txt':'P.G. Wodehouse','Text5_SecretGarden.txt':'Burnett'} 	
    	
    #books = ['Text1_Pride.txt']
    ending = []
    full = []	
    num = 0
    ranking = []	
    unique_word_list,tmp = func(word) 		
    for i in range(len(books)):	
    	f = open(books.keys()[i])	
	tweets = f.readlines()
	temp1,temp2 = func(tweets)
	num = common(temp1,unique_word_list)
    	ending.append(temp1)	 		
	full.append(temp2)	 				
	#print "The sample file has",num,"words common with the book",books.keys()[i]
	ranking.append([books.values()[i],num])
    
    ranking.sort(key=lambda x: x[1],reverse=True)			
    for r in ranking:
	print r[0],":",r[1]	
    author = ranking[0][0]	
    print "The sample file is classified as the work of",author


