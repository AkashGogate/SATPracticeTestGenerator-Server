from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from bs4 import BeautifulSoup
import os
import random
import re
from openai import OpenAI
import anthropic

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to your frontend's domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Get ready to practice the SAT!"}

@app.get("/reading_regenerate")
async def generate_reading():
    section = "reading"
    for i in range(1, 6):
        generate_section(section, f"./Split/{section.capitalize()}/{section}_{i}.html")
    fileName = "./Split/completed.html"
    with open(fileName, 'r') as file:
        content = file.read()
    return HTMLResponse(content=content)

@app.get("/writing_regenerate")
async def generate_writing():
    section = "writing"
    for i in range(1, 6):
        generate_section(section, f"./Split/{section.capitalize()}/{section}_{i}.html")
    fileName = "./Split/completed.html"
    with open(fileName, 'r') as file:
        content = file.read()
    return HTMLResponse(content=content)

@app.get("/math_nocalc_regenerate")
async def generate_math_nocalc():
    section = "math_nocalc"
    for i in range(1, 6):
        generate_section(section, f"./Split/{section.capitalize()}/{section}_{i}.html")
    fileName = "./Split/completed.html"
    with open(fileName, 'r') as file:
        content = file.read()
    return HTMLResponse(content=content)

@app.get("/math_calc_regenerate", response_class=HTMLResponse)
async def generate_math_calc():
    section = "math_calc"
    for i in range(1, 6):
        generate_section(section, f"./Split/{section.capitalize()}/{section}_{i}.html")
        
    fileName = "./Split/completed.html"
    with open(fileName, 'r') as file:
        content = file.read()
    return HTMLResponse(content=content)

@app.get("/reading", response_class=HTMLResponse)
async def get_reading():
    fileName = "./Split/Reading/reading_" + str(random.randint(1,5)) + ".html"
    with open(fileName, 'r') as file:
        content = file.read()
    print(content)
    return HTMLResponse(content=content)

@app.get("/writing", response_class=HTMLResponse)
async def get_writing():
    fileName = "./Split/Writing/writing_" + str(random.randint(1,5)) + ".html"
    with open(fileName, 'r') as file:
        content = file.read()
    return HTMLResponse(content=content)

@app.get("/math_nocalc", response_class=HTMLResponse)
async def get_math_nocalc():
    fileName = "./Split/Math_nocalc/math_nocalc_" + str(random.randint(1,5)) + ".html"
    with open(fileName, 'r') as file:
        content = file.read()
    return HTMLResponse(content=content)

@app.get("/math_calc", response_class=HTMLResponse)
async def get_math_calc():
    fileName = "./Split/Math_calc/math_calc_" + str(random.randint(1,5)) + ".html"
    with open(fileName, 'r') as file:
        content = file.read()
    return HTMLResponse(content=content)

@app.get("/reading_tips", response_class=HTMLResponse)
async def get_reading_tip():
    fileName = "./Split/Reading/reading_tips.html"
    with open(fileName, 'r') as file:
        content = file.read()
    return HTMLResponse(content=content)

@app.get("/writing_tips", response_class=HTMLResponse)
async def get_writing_tip():
    fileName = "./Split/Writing/writing_tips.html"
    with open(fileName, 'r') as file:
        content = file.read()
    return HTMLResponse(content=content)

@app.get("/math_nocalc_tips", response_class=HTMLResponse)
async def get_math_nocalc_tip():
    fileName = "./Split/Math_nocalc/math_nocalc_tips.html"
    with open(fileName, 'r') as file:
        content = file.read()
    return HTMLResponse(content=content)

@app.get("/math_calc_tips", response_class=HTMLResponse)
async def get_math_calc_tip():
    fileName = "./Split/Math_calc/math_calc_tips.html"
    with open(fileName, 'r') as file:
        content = file.read()
    return HTMLResponse(content=content)

def generate_section(section, output_path):
    print("Generating Question")
    text = getTextForPrompting(f"./Split/{section.capitalize()}/sample.html")
    if section == "math_nocalc":
        passage = "Generate Math (No Calculator) section practice problem for a SAT test. Here is an example of Math (No Calculator) sections of past test in HTML format: ```" + text + "```. Some of the HTML content may be as embedded images. " + " 1) Create the problem. " +  " 2) Generate the image for the graph/figure for the problem and embed it in the response HTML as an embedded svg tag. If any math equations are included, surround the entire equation using parentheses. Include axis scale markings for graphs." + " 3) Provide 5 multiple choice questions for it, each with 4 multiple choice options. For each of the 5 multiple choice questions, include numbers such as (A), (B) etc for the possible answers. Each possible answer should be a clickable radio button. Add a Submit button after each question. On Submit button, add javascript code to do the following: i) indicate whether the correct answer. ii) If an incorrect answer was selected, show the correct answer and provide a brief explanation of why that is the answer. Use red color font. iii) For correct answer use green font. iv) Show the time taken (in seconds) to select the answer once the page was fully rendered. Display in a separate line. Use bold font for the Time Taken: label. v) On every submit click, clear any previous information displayed before displaying information about the clicked answer. Respond in HTML5 format. Give enough spacing between questions and submit button." + " Respond in valid HTML5 format. Finish the response."
        
    elif section == "math_calc":
        passage = "Generate Math (Calculator) section practice problem for a SAT test. Here is an example of Math (Calculator) sections of past test in HTML format: ```" + text + "```. Some of the HTML content may be as embedded images. " + " 1) Create the problem. " +  " 2) Generate the image for the graph/figure for the problem and embed it in the response HTML as an embedded svg tag. If any math equations are included, surround the entire equation using parentheses. Include axis scale markings for graphs." + " 3) Provide 5 multiple choice questions for it, each with 4 multiple choice options. For each of the 5 multiple choice questions, include numbers such as (A), (B) etc for the possible answers. Each possible answer should be a clickable radio button. Add a Submit button after each question. On Submit button, add javascript code to do the following: i) indicate whether the correct answer. ii) If an incorrect answer was selected, show the correct answer and provide a brief explanation of why that is the answer. Use red color font. iii) For correct answer use green font. iv) Show the time taken (in seconds) to select the answer once the page was fully rendered. Display in a separate line. Use bold font for the Time Taken: label. v) On every submit click, clear any previous information displayed before displaying information about the clicked answer. Respond in HTML5 format. Give enough spacing between questions and submit button." + " Respond in valid HTML5 format. Finish the response."
    
    elif section == "reading":
        passage = "Generate Reading practice problem for a SAT test. Here is an example of Reading section of past test in HTML format: ```" + text + "```. Some of the HTML content may be as embedded images. " + "Generate a new Reading passage. For lines references used in the questions for it, label the corresponding lines in the passage as a superscript in the beginning of the line. For this passage, Provide 5 multiple choice questions for it, each with 4 multiple choice options. For each of the 5 multiple choice questions, include numbers such as (A), (B) etc for the possible answers. Each possible answer should be a clickable radio button. Add a Submit button after each question. On Submit button, add javascript code to do the following: i) indicate whether the correct answer. ii) If an incorrect answer was selected, show the correct answer and provide a brief explanation of why that is the answer. Use red color font. iii) For correct answer use green font. iv) Show the time taken (in seconds) to select the answer once the page was fully rendered. Display in a separate line. Use bold font for the Time Taken: label. v) On every submit click, clear any previous information displayed before displaying information about the clicked answer. Respond in HTML5 format. Give enough spacing between questions and submit button." + " Respond in valid HTML5 format. Finish the response."
    else:
        passage = "Generate Writing practice problem for a SAT test. Here is an example of Writing section of past test in HTML format: ```" + text + "```. Some of the HTML content may be as embedded images. " + "Generate a new Writing passage. For numbered references in the passage use a superscript. Underline the referenced words using the html <u> tag. For this passage, Provide 5 multiple choice questions for it, each with 4 multiple choice options. For each of the 5 multiple choice questions, include numbers such as (A), (B) etc for the possible answers. Each possible answer should be a clickable radio button. Add a Submit button after each question. On Submit button, add javascript code to do the following: i) indicate whether the correct answer. ii) If an incorrect answer was selected, show the correct answer and provide a brief explanation of why that is the answer. Use red color font. iii) For correct answer use green font. iv) Show the time taken (in seconds) to select the answer once the page was fully rendered. Display in a separate line. Use bold font for the Time Taken: label. v) On every submit click, clear any previous information displayed before displaying information about the clicked answer. Respond in HTML5 format. Give enough spacing between questions and submit button." + " Respond in valid HTML5 format. Finish the response."
    
    passageFull = generate_question_with_check(
        "You are a SAT Test Development specialist.",
        f"{passage}", 
        section
    )

    full_content = f"{passageFull}"
    with open(output_path, 'w') as file:
        file.write(full_content)

def getTextForPrompting(sample_html_path):
    with open(sample_html_path, 'r') as file:
        contents = file.read()
    soup = BeautifulSoup(contents, "html.parser")
    text = str(soup)
    return text[:100000] if len(text) > 100000 else text

def extract_content(message_content):
    pattern = r'```(.*?)```'
    match = re.search(pattern, message_content, re.DOTALL)
    if match:
        text = match.group(1)
        round2 = text
        if text.startswith("html"):
            round2 = text[4:]
        round3 = round2.replace("\(", "(")
        round4 = round3.replace("\)", ")")
        return round4.replace("\'","'")
    else:
        return None

def generate_question_with_check(system_prompt, user_prompt, section):
    client = OpenAI(api_key="your_api_key_here")
    
    #generating
    if section == "math_nocalc" or section == "math_calc":
        completion = client.chat.completions.create(
            model="gpt-4o",
            temperature=0,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
        message_content = completion.choices[0].message.content
        extracted_text = extract_content(message_content)
        
    else:
        completion = client.chat.completions.create(
            model="gpt-4o",
            #temperature=0,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
        message_content = completion.choices[0].message.content
        extracted_text = extract_content(message_content)
    
    
    #validating
    if section == "math_nocalc" or section == "math_calc":
        message = client.chat.completions.create(
        model="gpt-4o",
        temperature=0,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": "You are given a " + section +" Section of a SAT Practice Test. It contains a " + section + " problem along with multiple choice questions for it and possible answers in HTML format. Equations are enclosed in parentheses. Use the complete equation when solving for answer. Your task is to solve each of the Multiple Choice questions. Identify the correct answer and mark as such in the javascript. There should be 5 multiple choice questions and 4 possible answers for each, only one of which is correct. Make sure to correct both the HTML and the java script to make sure the right answer is correctly determined, and the radio button that represents the correct answer is present and that the answer exists. Here is the original practice test:```"+extracted_text+"```. Return the corrected version of this test in valid HTML format. All questions must have the correct answer indicated properly, and make sure the explanation for the right answer is present and not just, for example, \"The correct answer is B. Explanation: [Provide explanation here]\"."}
            ]
        )
    else:
        message = client.chat.completions.create(
        model="gpt-4o",
        temperature=0,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": "You are given a " + section +" Section of a SAT Practice Test. It contains a " + section + " passage along with multiple choice questions for it and possible answers in HTML format. Your task is to solve each of the Multiple Choice questions. Identify the correct answer and mark as such in the javascript. There should be 5 multiple choice questions and 4 possible answers for each, only one of which is correct. Make sure to correct both the HTML and the java script to make sure the right answer is correctly determined, and the radio button that represents the correct answer is present and that the answer exists. Here is the original practice test:```"+extracted_text+"```. Return the corrected version of this test in valid HTML format. All questions must have the correct answer indicated properly, and make sure the explanation for the right answer is present and not just, for example, \"The correct answer is B. Explanation: [Provide explanation here]\"."}
            ]
        )    
    
    
    message_content = message.choices[0].message.content
    validated_text = extract_content(message_content)
    
    # client = anthropic.Anthropic(
    #     api_key="your_api_key_here"
    # )

    # message = client.messages.create(
    #     model="claude-3-opus-20240229",
    #     max_tokens=1000,
    #     temperature=0.0,
    #     system=system_prompt,
    #     messages=[
    #         {"role": "user", "content": "woohoo"}
    #     ]
    # )
    
    # text_block = str(message.content)

    # start_quote_index = text_block.find("'") + 1  # Index after the first single quote
    # end_quote_index = text_block.find("'", start_quote_index)  # Index of the second single quote
    # extracted_text = text_block[start_quote_index:end_quote_index]
    
    print(validated_text)
    
    return validated_text

# Run by saying: uvicorn your_script_name:app --reload