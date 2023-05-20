import re
import requests
from fire import Fire


def get_description_from_youtube(input_url: str, output_description_file_path: str):
    print(f"Load description from '{input_url}'")
    content_text = requests.get(input_url).text

    pattern = r'"shortDescription":"(.*)","isCrawlable":true'
    match = re.search(pattern, content_text)

    if match is None:
        raise ValueError(f"Could not find description at the given URL '{input_url}'")

    description = match.group(1)

    print(f"Write description to '{output_description_file_path}'")
    with open(output_description_file_path, "w") as f:
        f.write(description)


if __name__ == "__main__":
    Fire(get_description_from_youtube)
