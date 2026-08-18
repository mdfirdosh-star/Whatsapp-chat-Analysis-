import streamlit as st
from preprocessing import preprocess
from helper import fatch_stats,most_busy_users,create_wordcolud,most_common_word,fatch_emojis,most_busy_month
import matplotlib.pyplot as plt 
st.title("Whatsapp Chat Analyzer")
st.sidebar.title("whatsapp chat analyzer")
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data=bytes_data.decode("utf-8")
    df=preprocess(data)
    st.dataframe(df)
    user_list=df["user"].unique().tolist()
    user_list.remove("group_notification")
    user_list.sort()
    user_list.insert(0,"overall")
    select_user=st.sidebar.selectbox("show analysis wrt",user_list)
    if st.sidebar.button("show analysis"):
        num_message,words,media_files,links=fatch_stats(select_user,df)
        col1,col2,col3,col4=st.columns(4)
        with col1:
            st.header("Total Message")
            st.title(num_message)
        with col2:
            st.header("Total words")
            st.title(words)
        with col3:
            st.header("Total Media Messages")
            st.title(media_files)
        with col4:
                st.header("Total links")
                st.title(links)
    
        
# finding the busiest users in ths group 
        if select_user =="overall":
            st.title("Most Busy User")
            x,new_df=most_busy_users(df)
            col1,col2=st.columns(2)
            name=x.index
            counts=x.values
            with col1:
                 fig,ax=plt.subplots()
                 ax.bar(name,counts,color="r")
                 plt.xticks(rotation=90)
                 st.pyplot(fig)
            with col2:
                 st.dataframe(new_df)
st.space()
# wordcolud 
st.title("wordcolud")
df_wc=create_wordcolud(select_user,df)
fig,ax=plt.subplots()
ax.imshow(df_wc)
st.pyplot(fig)
st.space()
# most common words
st.title("Most Common Word In Bar Graph")
df_m=most_common_word(select_user,df)
fig,ax=plt.subplots()
ax.bar(df_m["Most_Common_Word"],df_m["No Of Words"])
plt.xticks(rotation=90)
st.pyplot(fig)
st.title("Most Common Word Dataframe")
st.dataframe(df_m)
st.space()

# Show emojis in dataframe
st.title("Show the Emojis")

emoji_df = fatch_emojis(select_user, df)

col1, col2 = st.columns(2)

with col1:
    st.dataframe(emoji_df, use_container_width=True)

with col2:
    st.header("Emoji Pie Chart")

    if emoji_df.empty:
        st.info("No emojis found for this user.")
    else:
        top_emoji = emoji_df.head(10)

        fig, ax = plt.subplots(figsize=(6, 5))

        ax.pie(
            top_emoji["count"].astype(float),
            labels=top_emoji["emoji"].astype(str),
            autopct="%1.1f%%"
        )

        ax.set_title("Top 10 Used Emojis")
        st.pyplot(fig)
        plt.close(fig)
st.space()
st.title("Most Busy Month")
st.space()
timelines=most_busy_month(select_user,df)
col1,col2=st.columns(2)
with col1:
     st.title("Most Busy Month Graph")
     fig,ax=plt.subplots()
     ax.plot(timelines["time"],timelines["message"])
     plt.xticks(rotation=90)
     plt.show()
     st.pyplot(fig)
with col2:
          st.title("Most Busy Month Bar Plot")
          fig,ax=plt.subplots()
          ax.bar(timelines["time"],timelines["message"],color="r")
          plt.xticks(rotation=90)
          plt.show()
          st.pyplot(fig)



st.title("Most Busy Year")
st.space()
timelines=most_busy_month(select_user,df)
col1,col2=st.columns(2)
with col1:
     st.title("Most Busy Year Graph")
     fig,ax=plt.subplots()
     ax.plot(timelines["year"],timelines["message"])
     plt.xticks(rotation=90)
     plt.show()
     st.pyplot(fig)
with col2:
          st.title("Most Busy Year Bar Plot")
          fig,ax=plt.subplots()
          ax.bar(timelines["year"],timelines["message"],color="r")
          plt.xticks(rotation=90)
          plt.show()
          st.pyplot(fig)


