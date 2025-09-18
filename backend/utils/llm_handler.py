import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from typing import Dict

load_dotenv()

class PharmaceuticalValidation(BaseModel):
    results: Dict[str, bool] = Field(description="Dictionary mapping each word to boolean indicating if it's pharmaceutical")

def llm_validate_pharmaceutical_terms(word_to_sentence):
    if not word_to_sentence:
        return {}

    # Get LLM provider from environment (default to openai)
    llm_provider = os.getenv("LLM_PROVIDER", "openai").lower()

    if llm_provider == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("Warning: OPENAI_API_KEY not found, skipping LLM validation")
            return {word: False for word in word_to_sentence.keys()}

        # Setup OpenAI LLM
        llm = ChatOpenAI(
            model="gpt-4o-mini",
            api_key=api_key,
            temperature=0
        )
    else:  # gemini
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("Warning: GEMINI_API_KEY not found, skipping LLM validation")
            return {word: False for word in word_to_sentence.keys()}

        # Setup Gemini LLM
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash-exp",
            google_api_key=api_key,
            temperature=0
        )

    parser = JsonOutputParser(pydantic_object=PharmaceuticalValidation)

    # Create word-sentence pairs for the prompt
    word_contexts = []
    for word, sentence in word_to_sentence.items():
        word_contexts.append(f"Word: '{word}' in sentence: '{sentence}'")
    contexts_text = "\n".join(word_contexts)

    prompt = PromptTemplate(
        template="""You are a pharmaceutical expert analyzing CV/resume content to identify pharmaceutical, chemical, and drug-related terms.

        Your task: For each word below, determine if it refers to pharmaceutical, chemical, or drug-related terms in its specific sentence context.

        Word-Sentence pairs:
        {contexts_text}

        Classification criteria:
        - Use TRUE for: drug names, chemical compounds, active ingredients, formulations, pharmaceutical processes, biological targets, therapeutic areas
        - Use FALSE for: job titles, action verbs, company names, general business terms, non-pharmaceutical meanings

        {format_instructions}

        Return the results as a flat dictionary where each key is a word and each value is true/false.""",
        input_variables=["contexts_text"],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )

    chain = prompt | llm | parser
    try:
        result = chain.invoke({"contexts_text": contexts_text})

        print(f"LLM RESPONSE: {result}")

        if "results" in result:
            return result["results"]
        return result

    except Exception as e:
        print(f"LLM validation error: {e}")
        return {word: False for word in word_to_sentence.keys()}