from openai import OpenAI
import dotenv

from Interviewer.constants import get_interviewer_prompt, get_candidate_prompt

dotenv.load_dotenv()
client = OpenAI()

role = "AI engineer"
fundamental_question = "What is HNSW?"

def run(role: str, fundamental_question: str):
    first_question = "Great to have you here! Let's start with a fundamental question: " + fundamental_question

    interviewer_context = [
        {"role": "system", "content": get_interviewer_prompt(role)},
        {"role": "user", "content": "Hi I am here for my AI engineer interview. I am excited to be here and looking forward to the interview."},
        {"role": "assistant", "content": "Lets begin with the interview."},
        {"role": "assistant", "content": first_question},
    ]
    candidate_context = [
        {"role": "system", "content": get_candidate_prompt(role)},
        {"role": "assistant", "content": "Hi I am here for my AI engineer interview. I am excited to be here and looking forward to the interview."},
        {"role": "user", "content": "Lets begin with the interview."},
        {"role": "user", "content": first_question},
    ]

    print("==" * 100)
    count = 0
    print("Question number ", count)
    print("interviewer : ", first_question)

    while True:
        count += 1
        answer = client.responses.create(model="gpt-4o", input=candidate_context, temperature=0.1, max_output_tokens=200)
        interviewer_context.append({"role": "user", "content": answer.output_text})
        candidate_context.append({"role": "assistant", "content": answer.output_text})

        print()
        # input("Press Enter whenever you are ready")
        print("Candidate : \n", answer.output_text)

        if count > 3:
            break

        question = client.responses.create(model="gpt-5.5", input=interviewer_context, max_output_tokens=200)
        interviewer_context.append({"role": "assistant", "content": question.output_text})
        candidate_context.append({"role": "user", "content": question.output_text})

        print("=" * 100)
        print("count : ", count)
        print("=" * 100)
        print("interviewer : ", question.output_text)

        # if count > 3:
        #     interviewer_context.pop()
        #     candidate_context.pop()
        #     interviewer_context.append({"role": "assistant", "content": "Thank you for joining today"})
        #     candidate_context.append({"role": "user", "content": "Thank you for joining today"})
        #     break
