import streamlit as st
from job_interview_simulator.state import reset_chat_data, reset_all

def render_header(show_back=False):
    col1, col2, col3 = st.columns([1, 1, 8])

    with col1:
        if show_back:
            if st.button("<-", key="back_button"):
                st.session_state["show_nav_confirm"] = True
    with col2:
        if st.button("🏠", key=":home:"):
            st.session_state['screen'] = 'landing'
            st.rerun()
    
    if st.session_state.get("show_nav_confirm"):
        st.warning("What would you like to do?", )
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("Retake this interview"):
                reset_chat_data()
                st.session_state["show_nav_confirm"] = False
                st.rerun()
        with c2:
            if st.button("Start from scratch"):
                reset_all()
                st.session_state["show_nav_confirm"] = False
                st.rerun()
        with c3:
            if st.button("Cancel"):
                st.session_state["show_nav_confirm"] = False
                st.rerun()
    st.divider()        