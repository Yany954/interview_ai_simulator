import streamlit as st
from job_interview_simulator.state import init_state
import job_interview_simulator.screens.landing as landing
import job_interview_simulator.screens.onboarding as onboarding 
import job_interview_simulator.screens.interview as interview 
import job_interview_simulator.screens.feedback as feedback

st.set_page_config(page_title="Mock Interview Simulator", page_icon=":speech_balloon:")
init_state()

screens = {
    "landing" : landing.render,
    "onboarding" : onboarding.render,
    "interview": interview.render,
    "feedback": feedback.render
}
screens[st.session_state["screen"]]()