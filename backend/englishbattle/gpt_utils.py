from openai import OpenAI
import json
from django.conf import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)
def check_answer_with_gpt(japanese_sentence: str, user_translation: str) -> dict:
    system_prompt = (
        "You are a strict English teacher. Evaluate with high grammatical and semantic accuracy whether the given English sentence is a faithful and correct translation of the given Japanese sentence.\n\n"
        "Pay close attention to:\n"
        "- Grammar (e.g., tense, subject-verb agreement, articles, prepositions)\n"
        "- Word choice and nuance\n"
        "- Sentence structure and syntax\n"
        "- Overall semantic fidelity\n\n"
        "Return your answer as a JSON object with two fields:\n"
        "- \"is_correct\": true if and only if the English sentence is grammatically correct and faithfully conveys the full meaning of the Japanese sentence.\n"
        "- \"explanation\": a concise explanation in English justifying your judgment.\n\n"
        "Respond with only the JSON. Do not include any extra text."
    )

    user_prompt = f"Japanese:\n{japanese_sentence}\n\nEnglish Translation:\n{user_translation}"

    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0,
    )

    content = response.choices[0].message.content.strip()
    try:
        result = json.loads(content)
        return {
            "is_correct": bool(result.get("is_correct", False)),
            "explanation": result.get("explanation", "")
        }
    except json.JSONDecodeError:
        print("Failed to parse GPT response:", content)
        return {
            "is_correct": False,
            "explanation": "Failed to parse GPT response."
        }