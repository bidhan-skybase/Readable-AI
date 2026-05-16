import streamlit as st
from classifier import analyze
from simplifier import simplify
import os

# Page config
st.set_page_config(
    page_title="ReadableAI",
    page_icon="🧠",
    layout="wide"
)

# Header
st.title("🧠 ReadableAI")
st.markdown(
    "**An accessibility tool that analyzes text complexity "
    "and rewrites it for neurodivergent readers.**"
)
st.caption(
    "Built to explore: what cognitive assumptions does AI encode "
    "when it decides text is 'too complex'?"
)

st.divider()


# Input
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Input Text")
    sample = (
        "The implementation of neural architectures necessitates "
        "a comprehensive understanding of stochastic gradient descent "
        "and backpropagation mechanisms inherent to deep learning frameworks."
    )
    text_input = st.text_area(
        "Paste any text here",
        value=sample,
        height=200
    )
    
    analyze_btn = st.button("Analyze", type="primary", use_container_width=True)

with col2:
    st.subheader("Cognitive Profile")
    st.markdown("Choose who you're rewriting for:")
    profile = st.radio(
        "Profile",
        ["Dyslexia-friendly", "ADHD-friendly", "Low literacy"],
        label_visibility="collapsed"
    )
    
    simplify_btn = st.button(
        "Rewrite for this profile →",
        use_container_width=True
    )

st.divider()

# Analysis Results
if analyze_btn and text_input:
    with st.spinner("Analyzing..."):
        results = analyze(text_input)
    
    st.subheader("Analysis Results")
    
    # Level badge
    level_colors = {
        "simple": "🟢",
        "intermediate": "🟡", 
        "complex": "🔴"
    }
    emoji = level_colors.get(results["final_level"], "⚪")
    st.markdown(f"### {emoji} Complexity Level: **{results['final_level'].upper()}**")
    
    # Metrics
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Flesch-Kincaid Grade", f"Grade {results['fk_grade']}")
    m2.metric("AI Model Confidence", f"{results['model_confidence']}%")
    m3.metric("Sentences", results["sentence_count"])
    m4.metric("Avg. Words/Sentence", results["avg_sentence_length"])
    
    # Agreement / disagreement — this is the key insight
    if "disagree" in results["agreement"].lower():
        st.warning(f"⚠️ {results['agreement']}")
        st.caption(
            "This disagreement reveals something important: statistical readability "
            "models (built from 1940s research) and modern AI models encode different "
            "assumptions about what makes text 'difficult'. Neither is neutral."
        )
    else:
        st.success(f"✅ {results['agreement']}")
    
    # Hard words
    if results["hard_words"]:
        st.subheader("Words that may be difficult")
        st.markdown(
            "These long words may create friction for readers with dyslexia or "
            "processing differences:"
        )
        cols = st.columns(5)
        for i, word in enumerate(results["hard_words"]):
            cols[i % 5].code(word)

# Simplification Results
if simplify_btn and text_input:
    # Check API key
    if not os.environ.get("GROQ_API_KEY"):
        st.error("Add your ANTHROPIC_API_KEY to your environment variables.")
    else:
        with st.spinner(f"Rewriting for {profile} readers..."):
            rewritten = simplify(text_input, profile)
        
        st.subheader(f"Rewritten — {profile}")
        st.info(rewritten)
        
        # Run analysis on rewritten version too
        with st.spinner("Analyzing rewritten version..."):
            new_results = analyze(rewritten)
        
        st.caption(
            f"Complexity after rewriting: **{new_results['final_level'].upper()}** "
            f"(was: {analyze(text_input)['final_level']})"
        )
        
        # Ethical note — this is your HAI differentiator
        st.warning(
            "⚠️ **Ethical note:** AI simplification reflects the training data's "
            "assumptions about 'simple' language. It may still disadvantage "
            "non-native speakers or people whose cognitive style differs from "
            "what the model was trained on. Human review is always recommended."
        )

# Footer
st.divider()
st.caption(
    "ReadableAI | Built by Bidhan Marasine | "
    "Exploring how AI encodes cognitive assumptions in language"
)