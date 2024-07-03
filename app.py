import json
import os
import fitz  
from openai import OpenAI
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key="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"
)
def extraction(pdf_path):
    doc = fitz.open(pdf_path)
    full_text = [page.get_text() for page in doc]
    return '\n'.join(full_text)
def json_(resume_text):
    prompt = f"""
    Parse the following resume into JSON format with key-value pairs for name, email, phone, education, experience, and skills.

    Resume:
    {resume_text}

    Output JSON:
    """
    completion = client.chat.completions.create(
        model="nvidia/nemotron-4-340b-instruct",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        top_p=0.7,
        max_tokens=1024,
        stream=True
    )
    json_output = ""
    for chunk in completion:
        if chunk.choices[0].delta.content:
            json_output += chunk.choices[0].delta.content
    return json_output.strip()
def main():
    resume_path = input("Please enter the path to your resume (.pdf) file: ").strip()
    if not os.path.exists(resume_path):
        print("Please check the path and try again.")
        return
    resume_text = extraction(resume_path)
    json_output = json_(resume_text)
    output_directory = './output'
    os.makedirs(output_directory, exist_ok=True)
    output_file = os.path.join(output_directory, 'resume_info.json')
    with open(output_file, 'w') as json_file:
        json_file.write(json_output)
    print(f"File has been saved in JSON format: {output_file}")
if __name__ == '__main__':
    main()
