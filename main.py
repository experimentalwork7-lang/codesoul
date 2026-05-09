from dotenv import load_dotenv
import os
import memory
import editor
import rag
import brain

load_dotenv()
memory.init_memory()
rag.init_rag()
total_tokens = 0

GROQ_KEY = os.environ.get("GROQ_API_KEY") or open(".env").read().split("=")[1].strip()
CLAUDE_KEY = memory.load("claude_key") or None
GPT_KEY = memory.load("gpt_key") or None
GEMINI_KEY = memory.load("gemini_key") or None
GROK_KEY = memory.load("grok_key") or None
PROVIDER = memory.load("provider") or "groq"

def show_menu():
    print(f"""
╔══════════════════════════════════════════╗
║         CODESOUL ENGINE v4.0             ║
╠══════════════════════════════════════════╣
║  Just type your idea                     ║
║  set language: JavaScript                ║
║  set style: minimal                      ║
║  set provider: groq/claude/gpt/gemini    ║
║  set claude key: YOUR_KEY                ║
║  set gpt key: YOUR_KEY                   ║
║  set gemini key: YOUR_KEY                ║
║  set grok key: YOUR_KEY                  ║
║  save project: name: desc                ║
║  list projects                           ║
║  show file: filename.py                  ║
║  edit line: file: linenum: newtext       ║
║  replace: file: oldtext: newtext         ║
║  index file: filename.py                 ║
║  search: your query                      ║
║  exit                                    ║
╚══════════════════════════════════════════╝
  Active Brain: {PROVIDER.upper()}
""")

def is_thinking_task(idea):
    thinking_keywords = ["how", "why", "what", "explain", "plan", "structure", "design", "should"]
    for word in thinking_keywords:
        if word in idea.lower():
            return True
    return False

def think_and_code(your_idea):
    global total_tokens, PROVIDER, GROQ_KEY, CLAUDE_KEY, GPT_KEY, GEMINI_KEY, GROK_KEY
    language = memory.load("language") or "Python"
    style = memory.load("style") or "clean and simple"
    projects = memory.get_projects()
    project_context = ""
    if projects:
        project_context = "My existing projects:\n"
        for p in projects:
            project_context += f"- {p[0]} ({p[2]}): {p[1]}\n"
    rag_results = rag.search_codebase(your_idea)
    rag_context = ""
    if rag_results:
        rag_context = "\nRelevant code from your project:\n"
        for score, filepath, content in rag_results:
            rag_context += f"\n# {filepath}\n{content[:500]}\n"
    system_prompt = f"""You are a personal code assistant.
Always write code in {language}.
Style: {style}.
{project_context}
{rag_context}
Return working code only. No explanation."""
    result, tokens = brain.think(
        prompt=your_idea,
        system=system_prompt,
        provider=PROVIDER,
        groq_key=GROQ_KEY,
        claude_key=CLAUDE_KEY,
        gpt_key=GPT_KEY,
        gemini_key=GEMINI_KEY,
        grok_key=GROK_KEY
    )
    total_tokens += tokens
    if tokens > 0:
        print(f"[Tokens used: {tokens} | Total: {total_tokens}]")
    return result

show_menu()

while True:
    idea = input("\nWhat do you want to build?\n> ").strip()

    if idea.lower() == "exit":
        print("\n👋 CodeSoul shutting down. Your memory is saved.\n")
        break

    elif idea.lower() == "list projects":
        projects = memory.get_projects()
        if projects:
            print("\n--- YOUR PROJECTS ---")
            for p in projects:
                print(f"• {p[0]} | {p[2]} | {p[1]}")
            print("---------------------")
        else:
            print("No projects saved yet.")

    elif idea.lower().startswith("set language:"):
        memory.save("language", idea.split(":")[1].strip())
        print("Language saved!")

    elif idea.lower().startswith("set style:"):
        memory.save("style", idea.split(":")[1].strip())
        print("Style saved!")

    elif idea.lower().startswith("set provider:"):
        PROVIDER = idea.split(":")[1].strip().lower()
        memory.save("provider", PROVIDER)
        print(f"Brain switched to {PROVIDER.upper()}!")

    elif idea.lower().startswith("set claude key:"):
        CLAUDE_KEY = idea.split(":", 1)[1].strip()
        memory.save("claude_key", CLAUDE_KEY)
        print("Claude key saved!")

    elif idea.lower().startswith("set gpt key:"):
        GPT_KEY = idea.split(":", 1)[1].strip()
        memory.save("gpt_key", GPT_KEY)
        print("GPT key saved!")

    elif idea.lower().startswith("set gemini key:"):
        GEMINI_KEY = idea.split(":", 1)[1].strip()
        memory.save("gemini_key", GEMINI_KEY)
        print("Gemini key saved!")

    elif idea.lower().startswith("set grok key:"):
        GROK_KEY = idea.split(":", 1)[1].strip()
        memory.save("grok_key", GROK_KEY)
        print("Grok key saved!")

    elif idea.lower().startswith("save project:"):
        parts = idea.split(":")
        name = parts[1].strip()
        desc = parts[2].strip() if len(parts) > 2 else "no description"
        lang = memory.load("language") or "Python"
        memory.save_project(name, desc, lang)
        print(f"Project '{name}' saved!")

    elif idea.lower().startswith("show file:"):
        filepath = idea.split(":", 1)[1].strip()
        print(editor.show_file(filepath))

    elif idea.lower().startswith("edit line:"):
        parts = idea.split(":")
        filepath = parts[1].strip()
        line_num = int(parts[2].strip())
        new_content = parts[3].strip()
        print(editor.edit_line(filepath, line_num, new_content))

    elif idea.lower().startswith("replace:"):
        parts = idea.split(":")
        filepath = parts[1].strip()
        find_text = parts[2].strip()
        replace_text = parts[3].strip()
        print(editor.find_and_replace(filepath, find_text, replace_text))

    elif idea.lower().startswith("index file:"):
        filepath = idea.split(":", 1)[1].strip()
        print(rag.index_file(filepath))

    elif idea.lower().startswith("search:"):
        query = idea.split(":", 1)[1].strip()
        results = rag.search_codebase(query)
        if results:
            print("\n--- RELEVANT CODE FOUND ---")
            for score, filepath, content in results:
                print(f"\n📄 {filepath} (relevance: {score:.2f})")
                print(content[:300] + "...")
            print("---------------------------")
        else:
            print("No indexed files yet. Use 'index file: filename.py' first.")

    else:
        if is_thinking_task(idea):
            print("[ROUTER → Cloud Brain: thinking task]")
        else:
            print("[ROUTER → Local Writer: writing task]")
        print("\n--- YOUR CODE ---")
        print(think_and_code(idea))
        print("-----------------")