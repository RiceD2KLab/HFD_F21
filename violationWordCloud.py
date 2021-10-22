import csv
from wordcloud import WordCloud


#read first column of csv file to string of words seperated
#by tab

your_list = []
with open('ViolationComment2020and2021.csv', 'r') as f:
    reader = csv.reader(f)
    your_list = '\t'.join([i[1] for i in reader])


# Generate a word cloud image
wordcloud = WordCloud().generate(your_list)

# Display the generated image:
# the matplotlib way:
import matplotlib.pyplot as plt

plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")

wordcloud = WordCloud(width=2400, height=1200).generate(your_list)
plt.figure()
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()
