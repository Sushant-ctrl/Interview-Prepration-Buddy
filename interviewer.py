from openai import OpenAI
import dotenv

from Constants.constants import get_interviewer_prompt, get_candidate_prompt
from persistence import save_conversation

dotenv.load_dotenv()
client = OpenAI()


def run(opening: str, fundamental_question: str):
    first_question = "Great to have you here! Let's start with a fundamental question: " + fundamental_question

    interviewer_context = [
        {"role": "system", "content": get_interviewer_prompt(opening)},
        {"role": "user", "content": f"Hi I am here for my {opening} interview. I am excited to be here and looking forward to the interview."},
        {"role": "assistant", "content": "Lets begin with the interview."},
        {"role": "assistant", "content": first_question},
    ]
    candidate_context = [
        {"role": "system", "content": get_candidate_prompt(opening)},
        {"role": "assistant", "content": f"Hi I am here for my {opening} interview. I am excited to be here and looking forward to the interview."},
        {"role": "user", "content": "Lets begin with the interview."},
        {"role": "user", "content": first_question},
    ]

    conversation = [{"speaker": "interviewer", "message": first_question}]

    print("==" * 100)
    count = 0
    print("Question number ", count)
    print("interviewer : ", first_question)

    while True:
        count += 1
        answer = client.responses.create(model="gpt-4o", input=candidate_context, temperature=0.1, max_output_tokens=200)
        interviewer_context.append({"role": "user", "content": answer.output_text})
        candidate_context.append({"role": "assistant", "content": answer.output_text})
        conversation.append({"speaker": "candidate", "message": answer.output_text})

        print()
        print("Candidate : \n", answer.output_text)

        if count > 6:
            break

        question = client.responses.create(model="gpt-5.5", input=interviewer_context, max_output_tokens=200)
        interviewer_context.append({"role": "assistant", "content": question.output_text})
        candidate_context.append({"role": "user", "content": question.output_text})
        conversation.append({"speaker": "interviewer", "message": question.output_text})

        print("=" * 100)
        print("count : ", count)
        print("=" * 100)
        print("interviewer : ", question.output_text)

    saved_to = save_conversation(opening, conversation)
    print(f"\nConversation saved to: {saved_to}")
