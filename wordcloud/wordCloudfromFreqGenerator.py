import numpy as np
import pandas as pd
import re
import csv
from collections import defaultdict
from wordcloud import WordCloud
from wordcloud import STOPWORDS
import matplotlib.pyplot as plt
from PIL import Image
from wordcloud.wordcloud import STOPWORDS

# THIS FILE IS USED TO GENERATE A WORD CLOUD FROM THE FREQUENCY CSV FILE SAVED FROM wordFrequencyGenerator.py

# Order of files:
# 1. Run printViolationComment.py 
# 2. Run wordFrequencyGenerator.py using the output from (1)
# 3. Run this file to generate word cloud from the frequency csv file made from (2)

reader = csv.reader(open('word_frequencies.csv', 'r',newline='\n'))
d = defaultdict()

# make dictionary with frequencies for each word
for k,v in reader:
    v = v.strip()
    # print(k, v)
    if v.isdigit():
        d[k] = float(v)


# Generate a word cloud image

stopwords = list(STOPWORDS)
stopwords = stopwords + ["be", "all"]

for k, v in d.items():
    if k in stopwords:
        d[k] = 0

# mask = np.array(Image.open('masks/D.jpeg')) # mask if you want the word cloud in a certain shape
# wordcloud = WordCloud(width=4800, height=2400, collocations=False, mask=mask).generate_from_frequencies(d) 
wordcloud = WordCloud(width=4800, height=2400, collocations=False).generate_from_frequencies(d) 

plt.figure()
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()
