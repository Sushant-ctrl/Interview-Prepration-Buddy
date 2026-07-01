# Interview Preparation Buddy

Simulates a job interview using two AI agents — one playing the interviewer, one playing the candidate. Conversations are saved as markdown files after each run.

## Setup

1. Clone the repo and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Create a `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your-key-here
   ```

## Running

**CLI:**
```bash
python main.py --role "AI Engineer" --question "What is HNSW?"
```

Both flags are optional and fall back to defaults in `config/config.py`.

**Streamlit UI:**
```bash
streamlit run streamlit_app.py
```

Enter your OpenAI API key, role, and opening question in the sidebar, then click **Start Interview**. The conversation streams live in the browser and a transcript can be downloaded when complete.

## Output

Each run saves a conversation to `conversations/{role}{n}.md`, where `n` increments automatically per role.
