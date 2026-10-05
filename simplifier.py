import os
from groq import Groq, NotFoundError

# Default to active production model on Groq, with fallback support
CANDIDATE_MODELS = [
    os.environ.get("GROQ_MODEL", "openai/gpt-oss-120b"),
    "openai/gpt-oss-20b",
    "llama-3.3-70b-versatile",
]
# Deduplicate while preserving order
MODELS = list(dict.fromkeys(CANDIDATE_MODELS))

PROFILES = {
    "Dyslexia-friendly": """
        Rewrite this text for someone with dyslexia.
        Use short sentences (max 12 words each).
        Use common, everyday words.
        Break up long paragraphs into smaller chunks.
        Avoid double negatives.
        Be direct and clear.
    """,
    "ADHD-friendly": """
        Rewrite this text for someone with ADHD.
        Use bullet points where possible.
        Put the most important information first.
        Keep each point brief.
        Use active voice.
        Avoid long introductions.
    """,
    "Low literacy": """
        Rewrite this text using very simple English.
        Use only basic vocabulary a 10-year-old would know.
        Use short sentences.
        Explain any technical terms in plain words.
        One idea per sentence only.
    """
}

def simplify(text, profile):
    instruction = PROFILES.get(profile, PROFILES["Dyslexia-friendly"])
    client = Groq()
    
    last_error = None
    for model_name in MODELS:
        try:
            completion = client.chat.completions.create(
                model=model_name,
                messages=[
                    {
                        "role": "user",
                        "content": f"{instruction}\n\nOriginal text:\n{text}\n\nRewritten text:"
                    }
                ],
                max_tokens=1000
            )
            return completion.choices[0].message.content
        except NotFoundError as e:
            last_error = e
            continue

    if last_error:
        raise last_error