from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
link=URLExtract()
def fatch_stats(select_user,df):
    if select_user != "overall":
        df=df[df["user"]==select_user]
      # fatch the number of massage
    number_message=df.shape[0]

    #fatch the number of message words 
    word=[]
    for message in df["message"]:
      word.extend(message.split())
    # fatch of media files 
    media_files=df[df["message"]=="<Media omitted>"].shape[0]
    # total shared links 
    links=[]
    for message in df["message"]:
      links.extend(link.find_urls(message)) 
    return number_message,len(word),media_files,len(links) 



# finding the busiest users in ths group 
def most_busy_users(df):
    x=df["user"].value_counts()
    
    df=round((df["user"].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={"user":"name","count":"percent"})
    return x,df
#word colud
def create_wordcolud(select_user,df):
    if select_user != "overall":
        df=df[df["user"]==select_user]

        # Group notifications remove
    temp=df[df["user"] != "group_notification"]
        # Media omitted remove
    temp=temp[temp["message"] != "<Media omitted>"]
    # remove the stopwords for hinglish 
    def remove_stop_words_hinglish(message):
        with open(r"stop_hinglish.txt", "r", encoding="utf-8") as f:
          stop_words = f.read()
        y=[]
        for i in message.lower().split():
            if i  not in  stop_words:
                y.append(i)
        return " ".join(y)
    # remove the stopwords for english
    from nltk.corpus import stopwords
    import nltk
    nltk.download('stopwords')
    def remove_stop_words_english(message):
        y=[]
        for i in message.lower().split():
            if i not in stopwords.words("english"):
                y.append(i)
        return " ".join(y)
    wc=WordCloud(width=500,height=500,min_font_size=10,background_color="white")
    temp["message"]=temp["message"].apply(remove_stop_words_hinglish)
    temp["message"]=temp["message"].apply(remove_stop_words_english)
    df_wc=wc.generate(temp["message"].str.cat(sep=" "))
    return df_wc
# find the most common word 
from collections import Counter

def most_common_word(select_user, df):

    # User filter
    if select_user != "overall":
        df = df[df["user"] == select_user]

    # Group notifications remove
    temp = df[df["user"] != "group_notification"]

    # Media omitted remove
    temp = temp[temp["message"] != "<Media omitted>"]

    # Stop words file
    with open(r"stop_hinglish.txt", "r", encoding="utf-8") as f:
        stop_words = f.read()

    words = []

    for message in temp["message"]:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
    
    return_df=pd.DataFrame(Counter(words).most_common(20))
    return_df=return_df.rename(columns={0:"Most_Common_Word",1:"No Of Words"})
    return return_df

# emoji analysis
import emoji
import pandas as pd
from collections import Counter

def fatch_emojis(select_user, df):

    # Selected user ka data
    if select_user != "overall":
        df = df[df["user"] == select_user]

    emojis = []

    # Messages se emojis extract karo
    for message in df["message"].dropna():
        for c in message:
            if c in emoji.EMOJI_DATA:
                emojis.append(c)

    # Agar koi emoji nahi mila
    if not emojis:
        return pd.DataFrame(columns=["emoji", "count"])
    # Emoji count
    emoji_df = pd.DataFrame(
        Counter(emojis).most_common(),
        columns=["emoji", "count"]
    )

    return emoji_df

def most_busy_month(select_user,df):

    timeline=df.groupby(["year","month","num_month"]).count()["message"].reset_index()
    time=[]
    for i in range(timeline.shape[0]):
        time.append(timeline["month"][i]+"_"+str(timeline["year"][i]))
    timeline["time"]=time
    return timeline
