# ReadableAI — Text Complexity Analysis for Neurodivergent Readers

## What problem does this solve?
AI systems that process or present text encode assumptions about 
who the "normal" reader is. These assumptions — built into training 
data, readability formulas, and language models — systematically 
disadvantage readers with dyslexia, ADHD, or low literacy. 

This tool makes those assumptions visible and gives users control 
over how text is adapted to their cognitive needs.

## What does it do?
- Classifies any text into simple / intermediate / complex using 
  both a 1940s statistical model (Flesch-Kincaid) and a modern 
  transformer-based AI model (BART)
- Surfaces disagreements between the two — revealing that different 
  AI systems encode different definitions of "difficulty"
- Rewrites text for three neurodivergent profiles (dyslexia, ADHD, 
  low literacy) using a large language model
- Highlights long words that create reading friction

## What I learned about AI's limitations
The most interesting outcome was when the two models *disagreed*. 
Statistical models trained in the 1940s weight syllable count and 
sentence length. Modern transformers weight semantic complexity and 
contextual familiarity. Neither captures what actually makes text 
hard for a specific reader — because "difficulty" is not a property 
of text alone, it is a relationship between text and reader.

The simplification feature also surfaced a deeper problem: LLMs 
simplify toward a "median" reader that reflects their training data. 
This median is typically educated, English-native, and neurotypical. 
Simplified text may still exclude the very readers it claims to serve.

This is the core question I want to pursue: 
how do we design AI systems that account for cognitive diversity 
rather than optimizing for a fictional average user?

## Tech stack
- HuggingFace Transformers (facebook/bart-large-mnli)
- Textstat (Flesch-Kincaid, sentence analysis)  
- Anthropic Claude API (text simplification)
- Streamlit (interface)
- Python 3.11
