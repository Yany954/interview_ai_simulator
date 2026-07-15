import streamlit as st
from job_interview_simulator.header.components import render_header
from job_interview_simulator.database.questions_data import Master_Questions_Database

def render():
    render_header(show_back=True)
    st.subheader("Personal information", divider='rainbow')
    if "name" not in st.session_state:
        st.session_state["name"] = ""
    if "experience" not in st.session_state:
        st.session_state["experience"] = ""
    if "skills" not in st.session_state:
        st.session_state["skills"] = ""

    st.session_state["name"] = st.text_input(label='Name', max_chars=40, value=st.session_state["name"],placeholder='Enter your name')

    st.session_state["experience"] = st.text_area(label='Experience', value=st.session_state["experience"], height = None, max_chars=200, placeholder='Describe your experience')

    st.session_state["skills"] = st.text_area(label='Skills', value=st.session_state["skills"], height = None, max_chars=200, placeholder='List your skills')

    # st.write(f"**Your Name:** {st.session_state['name']}")
    # st.write(f"**Your Experience:** {st.session_state['experience']}")
    # st.write(f"**Your Skills:** {st.session_state['skills']}")

    st.subheader('Company and Position', divider='rainbow')

    if "level" not in st.session_state:
        st.session_state["level"] = ""
    if "position" not in st.session_state:
        st.session_state["position"] = ""
    if "company" not in st.session_state:
        st.session_state["company"] = ""

    col1, col2 = st.columns(2)
    with col1:
        st.session_state["level"] = st.radio(
            "Choose level",
            key= "visibility",
            options=["Junior", "Mid-level", "Senior"]
        )
    with col2:
        st.session_state["position"] = st.selectbox(
            "Choose position",
            ("Data Scientist", "Software Engineer", "Product Manager", "UX Designer")
        )

    st.session_state["company"] = st.selectbox(
        "Choose company",
        ("Google", "Microsoft", "Amazon", "Facebook", "Apple")
    )

    if st.button("Start Interview"):
        if not st.session_state["name"].strip():
            st.error("Please enter your name.")
        elif not st.session_state["experience"].strip():
            st.error("Please enter your experience")
        elif not st.session_state["skills"].strip():
            st.error("Please enter your skills.")
        else:
            st.session_state["set_of_questions"] = Master_Questions_Database[st.session_state["company"]][st.session_state["position"]]
            st.session_state["culture_note"] = Master_Questions_Database[st.session_state["company"]]["culture_note"]
            st.session_state['screen'] = "interview"
            st.rerun()
        

