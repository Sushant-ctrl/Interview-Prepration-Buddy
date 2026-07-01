import streamlit as st
from openai import OpenAI
import dotenv

from Constants.constants import get_interviewer_prompt, get_candidate_prompt
from persistence import save_conversation

dotenv.load_dotenv()

"""
This file "streamlit.py" is written by Sonnet 4.6 with moral support provided by Sushant!
"""

st.set_page_config(page_title="Interview Preparation Buddy", page_icon="🎤")

st.title("🎤 Interview Preparation Buddy")
st.caption(
    "Two AI agents simulate a job interview — one plays the interviewer, "
    "one plays the candidate. Watch the conversation unfold live."
)

# --- Sidebar controls ---
with st.sidebar:
    st.header("Settings")
    api_key = st.text_input(
        "OpenAI API key",
        type="password",
        help="Your key is used only for this session and is never stored.",
    )
    role = st.text_input("Job role", value="Gen-AI Engineer")
    question = st.text_input("Opening question", value="Briefly introduce yourself")
    rounds = st.slider("Number of exchanges", min_value=4, max_value=15, value=5)
    run_clicked = st.button("Start Interview", type="primary", use_container_width=True)

if "conversation" not in st.session_state:
    st.session_state.conversation = []

# --- Run the simulation ---
if run_clicked:
    if not api_key:
        st.error("Please enter your OpenAI API key in the sidebar.")
        st.stop()

    client = OpenAI(api_key=api_key)
    st.session_state.conversation = []

    first_question = f"Great to have you here! Let's start : {question}"

    interviewer_context = [
        {"role": "system", "content": get_interviewer_prompt(role)},
        {"role": "user", "content": f"Hi I am here for my {role} interview. I am excited to be here and looking forward to the interview."},
        {"role": "assistant", "content": "Lets begin with the interview."},
        {"role": "assistant", "content": first_question},
    ]
    candidate_context = [
        {"role": "system", "content": get_candidate_prompt(role)},
        {"role": "assistant", "content": f"Hi I am here for my {role} interview. I am excited to be here and looking forward to the interview."},
        {"role": "user", "content": "Lets begin with the interview."},
        {"role": "user", "content": first_question},
    ]

    conversation = [{"speaker": "interviewer", "message": first_question}]
    chat_box = st.container()

    with chat_box:
        with st.chat_message("assistant", avatar="🧑‍💼"):
            st.markdown(f"**Interviewer:** {first_question}")

    with st.spinner("Running interview..."):
        for count in range(1, rounds + 1):
            # Candidate responds
            answer = client.responses.create(
                model="gpt-4o",
                input=candidate_context,
                temperature=0.1,
                max_output_tokens=200,
            )
            interviewer_context.append({"role": "user", "content": answer.output_text})
            candidate_context.append({"role": "assistant", "content": answer.output_text})
            conversation.append({"speaker": "candidate", "message": answer.output_text})
            with chat_box:
                with st.chat_message("user", avatar="🙋"):
                    st.markdown(f"**Candidate:** {answer.output_text}")

            if count >= rounds:
                break

            # Interviewer asks next question
            next_q = client.responses.create(
                model="gpt-4o",
                input=interviewer_context,
                max_output_tokens=200,
            )
            interviewer_context.append({"role": "assistant", "content": next_q.output_text})
            candidate_context.append({"role": "user", "content": next_q.output_text})
            conversation.append({"speaker": "interviewer", "message": next_q.output_text})
            with chat_box:
                with st.chat_message("assistant", avatar="🧑‍💼"):
                    st.markdown(f"**Interviewer:** {next_q.output_text}")

    st.session_state.conversation = conversation
    saved_to = save_conversation(role, conversation)
    st.success(f"Interview complete! Transcript saved to `{saved_to}`")

    transcript_md = "\n\n".join(
        f"**{turn['speaker'].capitalize()}:** {turn['message']}" for turn in conversation
    )
    st.download_button(
        "Download transcript (.md)",
        data=transcript_md,
        file_name="interview_transcript.md",
        mime="text/markdown",
    )
else:
    st.info("Set your role and opening question in the sidebar, then click **Start Interview**.")