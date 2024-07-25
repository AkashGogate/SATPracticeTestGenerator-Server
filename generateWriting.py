from bs4 import BeautifulSoup
import os
import anthropic

def generate_content():
    sections = ['writing']
    for section in sections:
        for i in range(1, 6):
            generate_section(section, f"./Split/{section.capitalize()}/{section}_{i}.html")
    print("Content generated successfully!")

def generate_section(section, output_path):
    text = getTextForPrompting(f"./Split/{section.capitalize()}/sample.html")
    passage = generateQuestion(
        "Respond only in valid HTML format.",
        f"Generate a passage for the {section} section of an SAT test. Here are some examples of {section} sections of prior tests in HTML format: {text}. Now, generate a passage for a practice test. Return the passage in valid HTML5 format."
    )

    mcqs = generateQuestion(
        "Respond only in valid HTML format.",
        f"Here is a passage for the {section} section of an SAT test: {passage}. Generate 5 multiple choice questions for this passage. For each question, include numbers such as (A), (B), etc. Do not include answers. Add a Submit button after each question. On Submit button, add JavaScript code to do the following: 1) Indicate whether the selected answer is correct. 2) If an incorrect answer is selected, show the correct answer and a brief explanation of why that is the answer using red font. 3) For correct answers, use green font. 4) Show the time taken to select the answer once the page was fully rendered in a separate line with bold font for the 'Time Taken:' label. 5) On every submit click, clear any previous information displayed before displaying information about the clicked answer."
    )

    full_content = f"{passage}\n{mcqs}"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w') as file:
        file.write(full_content)

def getTextForPrompting(sample_html_path):
    with open(sample_html_path, 'r') as file:
        contents = file.read()
    soup = BeautifulSoup(contents, "html.parser")
    text = str(soup)
    return text[:150000] if len(text) > 150000 else text

def extract_content(message_content):
    start_index = message_content.find("<")
    end_index = message_content.rfind(">") + 1
    if start_index == -1 or end_index == -1:
        return "<p>Failed to extract content.</p>"
    return message_content[start_index:end_index]

def generateQuestion(system_prompt, user_prompt):
    client = anthropic.Anthropic(
        api_key="your_api_key_here"
    )

    response = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=2048,  # Adjust as needed
        system=system_prompt,
        messages=[
            {"role": "user", "content": user_prompt}
        ]
    )

    return extract_content(response.content)

if __name__ == "__main__":
    generate_content()
