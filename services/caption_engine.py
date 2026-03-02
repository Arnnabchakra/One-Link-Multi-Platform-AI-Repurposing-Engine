import os
from dotenv import load_dotenv

load_dotenv()

# Try to import Groq safely
try:
    from groq import Groq
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    GROQ_AVAILABLE = True
except Exception:
    GROQ_AVAILABLE = False


def generate_caption(platform, niche, transcript, cta):

    prompt = f"""
Generate a 2-3 line caption for {platform}.
Tone must match platform.
Niche: {niche}.
Transcript:
{transcript}
CTA: {cta}
"""

    # 🔹 If Groq available, try AI
    if GROQ_AVAILABLE and os.getenv("GROQ_API_KEY"):
        try:
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            print("Groq failed, using fallback:", e)

    # 🔹 Fallback caption generator (no API needed)
    return fallback_caption(platform, niche, transcript, cta)


def fallback_caption(platform, niche, transcript, cta):

    base = f"{niche} insights you don’t want to miss!\n{transcript[:120]}..."

    if platform == "instagram":
        return base + "\n🔥 #trending #viral #reels"

    if platform == "twitter":
        return (base[:250] + "...")[:280]

    if platform == "linkedin":
        return "Professional update:\n\n" + base

    if platform == "youtube":
        return f"Title: {niche} Explained\n\nDescription:\n{base}\n\nTags: {niche}, shorts, trending"

    return base