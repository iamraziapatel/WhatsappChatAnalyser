import streamlit as st
import preprocessor as pt
import matplotlib.pyplot as plt
import helper

st.sidebar.title("Whatsapp Chat Analyser")
uploaded_file = st.sidebar.file_uploader("Upload chat txt file", type=["txt"])
if uploaded_file is not None:
    byte_data = uploaded_file.read()
    data=byte_data.decode("utf-8")
    df= pt.preprocessor(data)
    # st.dataframe(df)
    # Debugging statement: Check the columns in the DataFrame
    # st.write(df.columns)
    unique_users = list(df['user'].unique())
    # Add "Overall" option to the list of unique users at the top
    unique_users.insert(0, "Overall")
    selected_user=st.sidebar.selectbox('select user',unique_users)
    # Filter the DataFrame based on the selected user
    if selected_user == "Overall":
        filtered_df = df
    else:
        filtered_df = df[df['user'] == selected_user]

    st.header(f"CHAT ANALYSIS OF :   {selected_user}")
    st.subheader(f"Top Statistics:")

    # Calculate total messages
    total_messages = filtered_df.shape[0]

    # Calculate total words
    total_words = filtered_df['message'].str.split().apply(len).sum()
    # Calculate total media shared
    total_media = filtered_df[filtered_df['message'] == '<Media omitted>'].shape[0]
    # Calculate total links shared
    total_links = filtered_df[filtered_df['message'].str.contains(r'http|https', na=False)].shape[0]

    # Create 2 columns for headings and values
    col1, col2 ,col3,col4= st.columns(4)

    # Display headings in the first row
    col1.write("Total Messages")
    col2.write("Total Words")
    col3.write("Total Media Shared")
    col4.write("Total Links Shared")

    # Display corresponding values in the second row
    col1.write(total_messages)
    col2.write(total_words)
    col3.write(total_media)
    col4.write(total_links)

    if selected_user == "Overall":
        st.title("Most active user in the group")
        x,user_percentage = helper.MostBusyUser(filtered_df)

        col1, col2 = st.columns(2)
        with col1:
            fig, ax = plt.subplots()
            ax.bar(x.index, x.values)
            plt.xticks(rotation="vertical")
            st.pyplot(fig)
        with col2:
            st.dataframe(user_percentage.head(5))
    #         WORDCLOUD
    st.title("WordCloud")
    df_wc = helper.createdwordcloud(selected_user,filtered_df)
    fig,ax=plt.subplots()
    ax.imshow(df_wc)
    st.pyplot(fig)
    # /most commom words
    dfmostcommon= helper.most_freq_words(selected_user,filtered_df)

    # st.dataframe(dfmostcommon)
    st.title("Most used words")
    fig,ax =plt.subplots()
    ax.barh(dfmostcommon[0],dfmostcommon[1])

    plt.xticks(rotation="vertical")
    st.pyplot(fig)

    # Emoji Analysis
    emojidf=helper.most_used_emojis(selected_user,filtered_df)
    st.title("Emoji Analysis")
    col1,col2 =st.columns(2)
    with col1:
        st.dataframe(emojidf)
            # Now create the pie chart
    # Now create the pie chart with a larger size
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(emojidf["Count"], labels=emojidf["Emoji"], autopct="%1.1f%%")
    ax.axis('equal')  # Ensure the pie chart appears as a circle

    col2.pyplot(fig)

    # timelines
    st.title(" monthly Timeline")
    timeline = helper.monthly_timeline(selected_user, filtered_df)
    fig, ax = plt.subplots()
    ax.plot(timeline["time"], timeline['message'])
    plt.xticks(rotation='vertical')
    st.pyplot(fig)
    