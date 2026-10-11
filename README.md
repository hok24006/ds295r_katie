## LangChain Starter Agent with Susan 👩‍💻✨

Welcome! This is a starter agent project, powered by **Susan**—your supportive, warm, and hyper-accessible data science assistant! 

### What Susan is All About
Susan's core philosophy is **ELI5 (Explain Like I'm 5)**. Whether you're wrestling with complex machine learning algorithms, statistical tests, data cleaning pipelines, or math proofs, Susan translates them into super simple, intuitive analogies using everyday objects (like sorting candy, organizing toys, or baking a cake). No intimidating academic jargon without a friendly explanation first!

### What Susan Can Do
- **Data Science Tutoring & Concept Breakdown:** Demystifying intimidating topics with patience and enthusiasm.
- **Python & Pandas Coding:** Writing clean, heavily commented code so you always understand *why* each line is there.
- **Project Structuring & Debugging:** Helping you organize your data projects and troubleshoot errors step-by-step.
- **Memory & Personalization:** Susan remembers your background, learning style, and goals over time to tailor every explanation just for you.

---

## To allow easy access through terminal
**Setup (one time)**

1. Install [uv](https://docs.astral.sh/uv/getting-started/installation/).
2. Create a `.env` file in this folder with your API key:

   ```
   GOOGLE_API_KEY=your-key-here
   ```

3. From this folder, install the `agent` command:

   ```
   uv tool install --editable .
   uv tool update-shell
   ```

4. Close and reopen your terminal.

**Run it**

Open any terminal and type:

```
agent
```

Type `exit` to quit.

Because the install is *editable*, changes you make to the code show up the
next time you run `agent`. There's no need to reinstall.

If you add a new dependency to `pyproject.toml`, run this again from this folder:

```
uv tool install --editable . --reinstall
```

## Credit

Terminal command setup: https://github.com/jamesbeeson01/langchain-starter-agent
