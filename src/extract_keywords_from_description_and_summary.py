import os
import json
from dotenv import load_dotenv
from fire import Fire
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI


def extract_keywords_from_description_and_summary(
    input_title: str,
    input_description_file_path: str,
    input_summary_file_path: str,
    output_keywords_file_path: str,
):
    # It is used to read the OPENAI_API_KEY
    load_dotenv()

    print(f"Read description from '{input_description_file_path}'")
    with open(input_description_file_path) as f:
        description = f.read()

    print(f"Read summary from '{input_summary_file_path}'")
    with open(input_summary_file_path) as f:
        summary = f.read()

    extract_keywords_prompt = """
        Title: "{title}"

        Description:
        "{description}"

        Summary of the transcript:
        "{summary}"

        From all of the information above, extract up to 10 keywords (preferably in English).
        Use this format (make sure your output can be read by Python's `json.loads`):

        {{
            "title": "{title}",
            "keywords": ["keyword_1", "keyword_2", ...]
        }}
    """

    extract_keywords_prompt_template = ChatPromptTemplate.from_template(extract_keywords_prompt)

    messages = extract_keywords_prompt_template.format_prompt(
        title=input_title,
        description=description,
        summary=summary
    ).to_messages()

    llm = ChatOpenAI(
        temperature=0,
        openai_api_key=os.environ["OPENAI_API_KEY"],
    )

    print("Start extracting keywords...")
    response = llm(messages)
    keywords_json = json.loads(response.content)

    print(f"Write keywords to '{output_keywords_file_path}'")
    with open(output_keywords_file_path, "w") as f:
        json.dump(keywords_json, f)


if __name__ == "__main__":
    Fire(extract_keywords_from_description_and_summary)
