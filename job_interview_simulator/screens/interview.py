import streamlit as st
from openai import OpenAI
from job_interview_simulator.header.components import render_header

def render():
    render_header(show_back=True)
    st.info(
        f"Good afternoon {st.session_state['name']}! Let's get started with the interview.",
        icon="👋"
    )

    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    if "openai_model" not in st.session_state:
        st.session_state.openai_model = "gpt-4o"

    if not st.session_state.messages:
        st.session_state.messages = [{
            "role": "system",
            "content": (
                f"You are an HR executive interviewing {st.session_state['name']}, "
                f"who has experience in {st.session_state['experience']} and skills in {st.session_state['skills']}. "
                f"Interview them for the position {st.session_state['level']} {st.session_state['position']} at {st.session_state['company']}. "
                f"Phrase follow-up questions using this company's lens: {st.session_state['culture_note']}. "
                f"Calibrate expected depth for a {st.session_state['level']} candidate — a Junior should get more benefit "
                f"of the doubt on scope, a Senior should be pushed on ownership and tradeoffs. "
                f"You are neutral, precise, and economical with words. You do not praise or criticize answers verbally. "
                f"Instead of praising, transition directly into the next question or follow-up with no evaluative commentary. "
                f"Real interviewers usually just say 'Okay, next—' or nothing at all before pivoting. "
                f"Never use words like Great, Perfect, Awesome, or Nice job, or exclamation-point affirmations."
            )
        }]

    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    total_questions = len(st.session_state["set_of_questions"])
    interview_done = st.session_state["current_question_index"] >= total_questions and st.session_state.get("closing_sent", False)

    if not interview_done:
        if prompt := st.chat_input("Escribe tu respuesta:", max_chars=1000):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            current_index = st.session_state["current_question_index"]

            if current_index < total_questions:
                question = st.session_state["set_of_questions"][current_index]
                instruction = (
                    f"Respond to what the interviewee just said, then ask this question "
                    f"(verbatim or as a natural transition): {question}"
                )
                st.session_state["current_question_index"] += 1
            else:
                instruction = (
                    "The interviewee has now answered all required questions. "
                    "Briefly acknowledge their final answer and let them know the interview is complete. "
                    "Do not ask another question."
                )
                st.session_state["closing_sent"] = True

            st.session_state.messages.append({"role": "system", "content": instruction})

            with st.chat_message("assistant"):
                stream = client.chat.completions.create(
                    model=st.session_state.openai_model,
                    messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                    stream=True
                )
                response = st.write_stream(stream)

            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()
    else:
        st.success("Interview complete.")
        if st.button("See Feedback", type="primary"):
            st.session_state["screen"] = "feedback"
            st.rerun()