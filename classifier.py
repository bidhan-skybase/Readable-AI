import textstat
from transformers import pipeline

# Load a zero-shot classification model
# This runs locally, no API key needed
classifier = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli"
)

LABELS = ["simple language", "intermediate language", "complex language"]

def get_textstat_score(text):
    """Statistical readability — Flesch-Kincaid grade level"""
    score = textstat.flesch_kincaid_grade(text)
    if score <= 6:
        return "simple", score
    elif score <= 10:
        return "intermediate", score
    else:
        return "complex", score

def get_model_score(text):
    """AI classification using zero-shot BART model"""
    result = classifier(text, LABELS)
    top_label = result["labels"][0]
    top_score = result["scores"][0]
    
    # Normalize label
    if "simple" in top_label:
        level = "simple"
    elif "intermediate" in top_label:
        level = "intermediate"
    else:
        level = "complex"
    
    return level, round(top_score * 100, 1)

def get_hard_words(text):
    """Returns words likely difficult for neurodivergent readers"""
    words = text.split()
    hard = []
    for word in words:
        clean = word.strip(".,!?;:\"'").lower()
        if len(clean) > 8 and clean.isalpha():
            hard.append(clean)
    return list(set(hard))[:10]  # top 10 unique long words

def analyze(text):
    stat_level, fk_grade = get_textstat_score(text)
    model_level, confidence = get_model_score(text)
    hard_words = get_hard_words(text)
    
    # Final decision: if both agree, high confidence
    # If they disagree, flag it
    if stat_level == model_level:
        agreement = "Both methods agree"
        final = stat_level
    else:
        agreement = f"Methods disagree — statistical says '{stat_level}', AI model says '{model_level}'"
        final = model_level  # trust model when disagreeing
    
    return {
        "final_level": final,
        "fk_grade": fk_grade,
        "model_confidence": confidence,
        "agreement": agreement,
        "hard_words": hard_words,
        "sentence_count": textstat.sentence_count(text),
        "avg_sentence_length": round(textstat.avg_sentence_length(text), 1)
    }




