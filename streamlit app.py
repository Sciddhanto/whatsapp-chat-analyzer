import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("Whatsapp Chat Analyzer")

# File upload
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    # Fetch unique users and sort
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)

    if st.sidebar.button("Show Analysis"):

        # Stats Area
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)
        st.title("Top Statistics")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Media Shared")
            st.title(num_media_messages)
        with col4:
            st.header("Links Shared")
            st.title(num_links)

        # Monthly Timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Daily Timeline
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Activity Map
        st.title('Activity Map')
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most busy day")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='purple')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most busy month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        # Weekly Activity Map
        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)

        # Finding the busiest users in the group (Group level)
        if selected_user == 'Overall':
            st.title('Most Busy Users')
            x, new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values, color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        # WordCloud
        st.title("Wordcloud")
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # Most common words
        most_common_df = helper.most_common_words(selected_user, df)
        fig, ax = plt.subplots()
        ax.barh(most_common_df[0], most_common_df[1])
        plt.xticks(rotation='vertical')

        st.title('Most common words')
        st.pyplot(fig)

        # Emoji Analysis
        emoji_df = helper.emoji_helper(selected_user, df)
        st.title("Emoji Analysis")

        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f")
            st.pyplot(fig)

    # 1. Sentiment Analysis
    if st.sidebar.button("Show Sentiment Analysis"):
        sentiments = helper.sentiment_analysis(selected_user, df)
        st.title("Sentiment Analysis")

        fig, ax = plt.subplots()
        ax.pie(sentiments.values(), labels=sentiments.keys(), autopct="%0.1f%%", startangle=90, colors=['green', 'red', 'blue'])
        st.pyplot(fig)

    # 2. Active Hours
    if st.sidebar.button("Show Active Hours"):
        st.title("User's Active Hours")
        active_hours = helper.active_hours(selected_user, df)

        fig, ax = plt.subplots()
        ax.plot(active_hours.index, active_hours.values, color='orange')
        plt.xlabel("Hour of the Day")
        plt.ylabel("Message Count")
        plt.grid()
        st.pyplot(fig)

    # 3. Response Time Analysis
    if selected_user == 'Overall' and st.sidebar.button("Show Response Time Analysis"):
        avg_response_time = helper.response_time_analysis(df)
        st.title("Response Time Analysis")
        st.write(f"Average response time in the group: {avg_response_time:.2f} minutes")

    # 4. Keyword Analysis
    keyword = st.sidebar.text_input("Enter a keyword to analyze")
    if keyword and st.sidebar.button("Show Keyword Analysis"):
        keyword_count = helper.keyword_analysis(keyword, df)
        st.title("Keyword Analysis")
        st.write(f"The keyword '{keyword}' appears {keyword_count} times in the chat.")

    # 5. Message Type Analysis
    if st.sidebar.button("Show Message Type Analysis"):
        message_types = helper.message_type_analysis(selected_user, df)
        st.title("Message Type Analysis")

        fig, ax = plt.subplots()
        ax.bar(message_types.keys(), message_types.values(), color=['blue', 'yellow', 'red'])
        plt.xlabel("Message Type")
        plt.ylabel("Count")
        st.pyplot(fig)

