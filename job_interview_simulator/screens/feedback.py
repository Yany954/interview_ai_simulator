import streamlit as st
from job_interview_simulator.header.components import render_header
from openai import OpenAI

def render():
    render_header(show_back=True)
    st.subheader('Feedback', divider='rainbow')
    conversation_history = "\n".join([f"{msg['role'].capitalize()}: {msg['content']}" for msg in st.session_state.messages if msg['role'] != 'system'])
    feedback_client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    feedback_completion = feedback_client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": """You are a helpful tool that provides feedback on a  interviewee performance.
             Scoring rubric (use this exact scale, do not soften it):
            - 1-2: The interviewee gave no real answer — blank, a single word/character, random text, or a response with no connection to the question asked.
            - 3-4: The interviewee attempted an answer but it was vague, generic, or missing the specifics the question asked for (no concrete example, no reasoning shown).
            - 5-6: The interviewee gave a relevant, on-topic answer but it lacked depth, structure, or a clear outcome.
            - 7-8: The interviewee gave a clear, specific, well-structured answer with a concrete example and reasoning.
            - 9-10: The interviewee gave an exceptional answer — specific, well-structured, insightful, and demonstrated clear expertise.

            Critical rules:
            - Judge ONLY the actual content of each answer against the question that was asked. Do not give credit for effort, politeness, or engagement if the content itself doesn't answer the question.
            - If most or all answers in the transcript are non-answers (blank, one character, gibberish, or off-topic), the Overall Score MUST be 1 or 2. Do not round up out of leniency.
            - Do not infer or assume competence that isn't demonstrated in the text. Absence of an answer is not neutral — it is a failure to answer.
            - Before assigning a score, briefly check each answer against the rubric bands above internally, then give the score that matches the weakest pattern across the transcript, not the most generous one.

             Output format — follow exactly, no extra commentary:
             Overall Score: //Your score
             Feedback: //Here you put your feedback
             Give only the score and feedback, do not ask any additional questions or provide any other information.
             """
            },
            {"role": "user", "content": f"This is the interview you need to evaluate. You are only a tool and shouldn't engage in conversation:{conversation_history}"}
        ]
    )
    st.write(feedback_completion.choices[0].message.content)
