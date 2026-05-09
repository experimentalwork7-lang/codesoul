def think(prompt, system, provider="groq", groq_key=None, claude_key=None, gpt_key=None, gemini_key=None, grok_key=None):

    if provider == "claude":
        import anthropic
        client = anthropic.Anthropic(api_key=claude_key)
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1000,
            system=system,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text, 0

    elif provider == "gpt":
        from openai import OpenAI
        client = OpenAI(api_key=gpt_key)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content, response.usage.total_tokens

    elif provider == "gemini":
        import google.generativeai as genai
        genai.configure(api_key=gemini_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(system + "\n" + prompt)
        return response.text, 0

    elif provider == "grok":
        from openai import OpenAI
        client = OpenAI(api_key=grok_key, base_url="https://api.x.ai/v1")
        response = client.chat.completions.create(
            model="grok-beta",
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content, response.usage.total_tokens

    else:
        from groq import Groq
        client = Groq(api_key=groq_key)
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content, response.usage.total_tokens