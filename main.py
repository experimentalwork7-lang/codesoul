from groq import Groq
from dotenv import load_dotenv
import os
import memory

load_dotenv()
memory.init_memory()
total_tokens = 0

client = Groq(api_key=open(".env").read().split("=")[1].strip())

def show_menu():
    print("""
╔══════════════════════════════╗
║       CODESOUL ENGINE        ║
╠══════════════════════════════╣
║  Just type your idea         ║
║  set language: JavaScript    ║
║  set style: minimal          ║
║  save project: name: desc    ║
║  list projects               ║
║  exit                        ║
╚══════════════════════════════╝
""")

def is_thinking_task(idea):
    thinking_keywords = ["how", "why", "what", "explain", "plan", "structure", "design", "should"]
    for word in thinking_keywords:
        if word in idea.lower():
            return True
    return False

def think_and_code(your_idea):
    global total_tokens
    language = memory.load("language") or "Python"
    style = memory.load("style") or "clean and simple"
    projects = memory.get_projects()
    project_context = ""
    if projects:
        project_context = "My existing projects:\n"
        for p in projects:
            project_context += f"- {p[0]} ({p[2]}): {p[1]}\n"
    system_prompt = f"""You are a personal code assistant.
Always write code in {language}.
Style: {style}.
{project_context}
Return working code only. No explanation."""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": your_idea}
        ]
    )
    tokens = response.usage.total_tokens
    total_tokens += tokens
    print(f"[Tokens used: {tokens} | Total: {total_tokens}]")
    return response.choices[0].message.content

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
    elif idea.lower().startswith("save project:"):
        parts = idea.split(":")
        name = parts[1].strip()
        desc = parts[2].strip() if len(parts) > 2 else "no description"
        lang = memory.load("language") or "Python"
        memory.save_project(name, desc, lang)
        print(f"Project '{name}' saved!")
    else:
        if is_thinking_task(idea):
            print("[ROUTER → Cloud Brain: thinking task]")
        else:
            print("[ROUTER → Local Writer: writing task]")
        print("\n--- YOUR CODE ---")
        print(think_and_code(idea))
        print("-----------------")