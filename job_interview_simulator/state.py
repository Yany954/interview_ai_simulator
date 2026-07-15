import streamlit as st

def init_state():
    defaults = {
        "screen" : "landing",
        "setup_completed" : False,
        "user_message_count" : 0,
        "feedback_shown" : False,
        "messages" : [],
        "chat_completed" : False,
        "current_question_index" : 0,
        "set_of_questions" : [],
        "culture_note" : "",
        "show_nav_confirm" : False,
        "closing_sent": False,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def reset_chat_data():
    st.session_state["messages"] = []
    st.session_state["user_message_count"] = 0
    st.session_state['current_question_index'] = 0
    st.session_state['chat_completed'] = False
    st.session_state['feedback_shown'] = False
    st.session_state['screen'] = 'interview'

def reset_all():
    st.session_state.clear()
    init_state()
    st.session_state['screen'] = 'landing'