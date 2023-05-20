import os
from langchain.document_loaders import TextLoader
from langchain.chat_models import ChatOpenAI
from langchain.chains.summarize import load_summarize_chain
from dotenv import load_dotenv
from fire import Fire


def summarize_transcript(input_transcript_file_path: str, output_summary_file_path: str):
    # It is used to read the OPENAI_API_KEY
    load_dotenv()

    print(f"Load transcript from '{input_transcript_file_path}'")
    text_loader = TextLoader(file_path=input_transcript_file_path)

    # By defaults, the text is split in chunks of 4000 characters (with 200 characters of overlap)
    chunks = text_loader.load_and_split()

    # If you have access to GPT-4, feel free to use it instead of GPT-3.5
    # You might be able to pass the entire transcript instead of needing to split it into chunks
    llm = ChatOpenAI(
        model_name="gpt-3.5-turbo",
        temperature=0,
        openai_api_key=os.environ["OPENAI_API_KEY"],
    )

    # The summarization is done by using the "map_reduce" chain type
    # It means that each chunk is summarized independently and then the summaries are concatenated
    # The concatenation is finally summarized to produce the final summary
    chain = load_summarize_chain(llm, chain_type="map_reduce")
    print("Start map-reduce summarization...")
    summary = chain.run(chunks)

    print(f"Write summary to '{output_summary_file_path}'")
    with open(output_summary_file_path, "w") as f:
        f.write(summary)


if __name__ == "__main__":
    Fire(summarize_transcript)
