from dotenv import load_dotenv
from groq import Groq
load_dotenv()


client = Groq()
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
    
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile", # Free, powerful frontier model
        messages=[
            {
                "role": "user",
                "content": f"{instruction}\n\nOriginal text:\n{text}\n\nRewritten text:"
            }
        ],
        max_tokens=1000
    )
    
    return completion.choices[0].message.content