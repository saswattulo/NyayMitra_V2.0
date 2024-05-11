import json
import os
import streamlit as st
from llama_index.core import StorageContext, load_index_from_storage
import gtts  


os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

def main():

    index_placeholder = None
    st.set_page_config(page_title = "NyayMitra", page_icon="👩‍⚖️")
    st.header('NyayMitra 👩‍⚖️')
    
    if "conversation" not in st.session_state:
        st.session_state.conversation = None

    if "activate_chat" not in st.session_state:
        st.session_state.activate_chat = False

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar = message['avatar']):
            st.markdown(message["content"])

    with st.sidebar:
        st.subheader('Start your chat here')
        if st.button('Click Here'):
            with st.spinner('Processing'):

                storage_context = StorageContext.from_defaults(persist_dir="index_v2.0")
                new_index = load_index_from_storage(storage_context)
                query_engine = new_index.as_query_engine()
                if "query_engine" not in st.session_state:
                    st.session_state.query_engine = query_engine
                st.session_state.activate_chat = True

    if st.session_state.activate_chat == True:
        if prompt := st.chat_input("Ask your question"):
            with st.chat_message("user", avatar = '👨🏻'):
                st.markdown(prompt)
            st.session_state.messages.append({"role": "user", 
                                              "avatar" :'👨🏻',
                                              "content": prompt})

            query_index_placeholder = st.session_state.query_engine
            pdf_response = query_index_placeholder.query(prompt)
            cleaned_response = pdf_response.response
            with st.chat_message("assistant", avatar='🤖'):
                st.markdown(cleaned_response)
                tts = gtts.gTTS(text=cleaned_response, lang='en')
                tts.save("speech.mp3")
                st.audio("speech.mp3")
            st.session_state.messages.append({"role": "assistant", 
                                              "avatar" :'🤖',
                                              "content": cleaned_response})
        else:
            st.markdown(
                ' '
                )


if __name__ == '__main__':
    main()
