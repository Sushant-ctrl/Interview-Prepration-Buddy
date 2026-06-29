import argparse
from config import config
from Interviewer import interviewer

def parse_args():
    parser = argparse.ArgumentParser(description="Interview Preparation Buddy")
    parser.add_argument("--role", type=str, default=config.role, help="Job role to interview for")
    parser.add_argument("--question", type=str, default=config.fundamental_question, help="Opening fundamental question")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    interviewer.run(role=args.role, fundamental_question=args.question)
