import streamlit as st
from job_interview_simulator.header.components import render_header

def render():
    render_header(show_back=False)
    st.title("Mock Interview Simulator")
    st.write("Practice real interview questions tailored to the company, role, and seniority level you're targeting — with an AI interviewer that behaves like the real thing, not a cheerleader.")
    if st.button("Start", type="primary"):
        st.session_state["screen"] = "onboarding"
        st.rerun()