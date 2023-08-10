import emoji
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from nltk.tokenize import word_tokenize
nltk.download('stopwords')
nltk.download('punkt')
import calendar
def MostBusyUser(filtered_df):
    x = filtered_df['user'].value_counts().head(5)
    user_percentage = round(filtered_df['user'].value_counts() / filtered_df.shape[0] * 100, 2).reset_index()
    user_percentage = user_percentage.rename(columns={'index': "Name", 'user': "percentage"})
    return x,user_percentage

def createdwordcloud(selected_user,df):

    if selected_user != "Overall":
        df = df[df["user"] == selected_user]

    wc = WordCloud(width=500,height=500,min_font_size=10)
    df_wc = wc.generate(df['message'].str.cat(sep=" "))
    return df_wc

def most_freq_words(selecteduser,df):

    if selecteduser != "Overall":
        df = df[df["user"] == selecteduser]

    temp =df[df["user"] != "group_notification"]
    temp=temp[temp["message"] != "<Media omitted>"]
    # Read Hinglish stop words from the file
    f = open("stop_hinglish.txt", "r")
    hinglish_stopwords = set(f.read().splitlines())
    f.close()

    # Use NLTK English stop words and add Hinglish stop words
    english_stopwords = set(stopwords.words('english'))
    stopwords_set = english_stopwords.union(hinglish_stopwords)

    words = []
    for message in temp["message"]:
        words.extend(word_tokenize(message))
        # words.extend(message.split())
    # Apply stemming to remove similar words and remove combined stop words
    stemmer = SnowballStemmer("english")
    filtered_words = [stemmer.stem(word) for word in words if word.lower() not in stopwords_set]

    dfmostcommon = pd.DataFrame(Counter(filtered_words).most_common(20))

    return dfmostcommon

def most_used_emojis(selected_user, df, top_n=10):
    if selected_user != "Overall":
        df = df[df["user"] == selected_user]

    temp = df[df["user"] != "group_notification"]
    temp = temp[temp["message"] != "<Media omitted>"]

    emojis = []
    for message in temp["message"]:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    df_emojis = pd.DataFrame(Counter(emojis).most_common(top_n), columns=["Emoji", "Count"])
    return df_emojis

# def monthly_timeline(selected_user, df):
#     if selected_user != "Overall":
#         df = df[df["user"] == selected_user]
#
#     timeline = df.groupby(["year", "month"]).count()['message'].reset_index()
#     time = []
#     for i in range(timeline.shape[0]):
#         time.append(timeline["month"][i] + "-" + str(timeline['year'][i]))
#
#     # Move the assignment of 'time' column outside the loop
#     timeline["time"] = time
#
#     return timeline



def monthly_timeline(selected_user, df):
    if selected_user != "Overall":
        df = df[df["user"] == selected_user]

    timeline = df.groupby(["year", "month"]).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        month_abbr = timeline["month"][i]
        year = timeline["year"][i]
        time.append(f"{month_abbr}-{year}")

    # Move the assignment of 'time' column outside the loop
    timeline["time"] = time

    # Convert the "month" column to categorical with the correct order
    months_order = list(calendar.month_abbr[1:])
    timeline["month"] = pd.Categorical(timeline["month"], categories=months_order, ordered=True)

    return timeline

