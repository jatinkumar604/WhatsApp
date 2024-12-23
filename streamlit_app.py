import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt  # Updated import

st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")

    df = preprocessor.preprocess(data)
    st.dataframe(df)

    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")
    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)

    if st.sidebar.button("Show Analysis"):
        num_messages, words, media_msg, link_ms = helper.fetch_stats(selected_user, df)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Total Media Messages")
            st.title(media_msg)
        with col4:
            st.header("Total Links Shared")
            st.title(link_ms)

    # Finding the busiest users in the group (Group level)
    if selected_user == 'Overall':
        st.title('Most Busy Users')
        x = helper.most_busy_users(df)
        fig, ax = plt.subplots()  # Updated code
        col1, col2 = st.columns(2)

        with col1:
            ax.bar(x.index, x.values)
            st.pyplot(fig)
