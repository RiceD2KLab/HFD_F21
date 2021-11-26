import csv
from wordcloud import WordCloud


# ======================================== WORD CLOUD ============================================

# Building Codes:
# violation_HighRise.csv 
# violation_APT_HTL.csv
# violation_blankTeamCode.csv
# violation_GO.csv
# violation_HazMatHiPile.csv 
# violation_PlanCk.csv
# violation_SCH_INS.csv
# violation_SpecialOps.csv
# violation_Weekends.csv

# Inspectors:
# violation_JDennis.csv
# violation_AGarcia.csv
# violation_CBoyd.csv
# violation_LKimball.csv
# violation_MRogers.csv
# 
your_list = [] 
with open('data/violation_comments_by_inspector_csv/violation_MRogers.csv', 'r') as f:
    reader = csv.reader(f)
    your_list = '\t'.join([i[1] for i in reader])


# Make all strings lowercase and remove insignificant strings

def remove_substring(s, substr):
    # type: (str, str) -> str
    return re.subn(substr, '', s)[0]


new_list = your_list.lower()

new_list = remove_substring(new_list, 'nodata')
new_list = remove_substring(new_list, 'must')
new_list = remove_substring(new_list, 'need')
new_list = remove_substring(new_list, 'required')
new_list = remove_substring(new_list, 'please')
new_list = remove_substring(new_list, 'provide')
new_list = remove_substring(new_list, 'will')
new_list = remove_substring(new_list, 'make')
new_list = remove_substring(new_list, 'sure')
new_list = remove_substring(new_list, 'apply')
new_list = remove_substring(new_list, 'last date')
new_list = remove_substring(new_list, 'last')
new_list = remove_substring(new_list, 'date')



# Generate a word cloud image
# new_list = new_list.split(' ')
# print("NEW LIST: \n", new_list)
new_list = re.sub(r'==.*?==+', '', new_list)
new_list = new_list.replace('\n', '')
print(new_list)

# wordcloud = WordCloud(collocations=False).generate(new_list)
# # print(wordcloud.words_)
# # Display the generated image:
# # the matplotlib way:
# import matplotlib.pyplot as plt

# # plt.imshow(wordcloud, interpolation='bilinear')
# # plt.axis("off")

# wordcloud = WordCloud(width=2400, height=1200).generate(new_list)
# plt.figure()
# plt.imshow(wordcloud, interpolation="bilinear")
# plt.axis("off")
# plt.show()
