import argparse
import interviewer

default_role = "Gen-AI Engineer"
default_question = "Briefly introduce yourself"

def parse_args():
    parser = argparse.ArgumentParser(description="Interview Preparation Buddy")
    parser.add_argument("--role", type=str, default=default_role, help="Job role to interview for")
    parser.add_argument("--question", type=str, default=default_question, help="Opening fundamental question")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    interviewer.run(opening=args.role, fundamental_question=args.question)
