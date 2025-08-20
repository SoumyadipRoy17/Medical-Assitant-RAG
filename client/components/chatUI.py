import streamlit as st
from utils.api import ask_question


def render_chat():
    st.subheader("💬 Chat with your assistant")

    if "messages" not in st.session_state:
        st.session_state.messages=[]

    # render existing chat history
    for msg in st.session_state.messages:
        role = "👤 User" if msg["role"] == "user" else "🤖 Assistant"
        st.markdown(f"**{role}:** {msg['content']}")

    # input and response
    user_input=st.text_input("Type your question....")
    if user_input:
        st.markdown(f"**User:** {user_input}")

        st.session_state.messages.append({"role":"user","content":user_input})

        response=ask_question(user_input)
        if response.status_code==200:
            data=response.json()
            answer=data["response"]
            sources=data.get("sources",[])
            st.markdown(f"**Assistant:** {answer}")

            # if sources:
            #     st.markdown("📄 **Sources: **")
            #     for src in sources:
            #         st.markdown(f"- `{src}`")
            st.session_state.messages.append({"role":"assistant","content":answer})
        else:
            st.error(f"Error: {response.text}")