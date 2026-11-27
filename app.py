import streamlit as st
from chat_bot import ChatBot

st.set_page_config(
    page_title="Alexa AI",
    page_icon="🤖",
    layout="centered"
)
st.subheader("What's on your mind?",  text_alignment="center")




if "bot" not in st.session_state:
    st.session_state.bot = ChatBot()


if "chat_history" not in st.session_state:
   st.session_state.chat_history = []

bot = st.session_state.bot

cost = (
    bot.input_tokens * 0.05 +
    bot.output_tokens * 0.08
) / 1_000_000



with st.sidebar:
    st.title("L- AI")

    st.subheader("Usage Statistics")

    st.metric("Total Tokens: ", bot.total_tokens)

    st.metric("Input Tokens: ", bot.input_tokens)

    st.metric("Output Tokens: ", bot.output_tokens)

    st.metric("Estimated Cost: ", f"${cost:.6f}")


for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
         st.markdown(message["content"])


user_query = st.chat_input("Ask something......")


if user_query:
    with st.chat_message("user"):
        st.markdown(user_query)


    st.session_state.chat_history.append({
        "role": "user",
        "content": user_query
    })


    with st.chat_message("assistant"):
        with st.spinner("Thinking...."):
            response = bot.bot(user_query)

        st.markdown(response)

    st.session_state.chat_history.append({
        "role": "assistant",
        "content": response
    })