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


reader = csv.reader(open('word_frequencies.csv', 'r',newline='\n'))
d = defaultdict()

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

# mask = np.array(Image.open('masks/D.jpeg'))
# wordcloud = WordCloud(width=4800, height=2400, collocations=False, mask=mask).generate_from_frequencies(d) 
wordcloud = WordCloud(width=4800, height=2400, collocations=False).generate_from_frequencies(d) 

plt.figure()
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()
