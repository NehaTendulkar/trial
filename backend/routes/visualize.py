from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse
import os
import io
import json
import re
import ast
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv
import logging

load_dotenv()
logger = logging.getLogger(__name__)
router = APIRouter()

client = OpenAI(
    api_key=os.environ.get("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

def extract_json(text):
    """Extract the first JSON-like block."""
    match = re.search(r"\{[\s\S]*\}", text)
    return match.group(0) if match else text

@router.post("/visualize")
async def visualize(file: UploadFile = File(...), query: str = Form(...)):
    try:
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents))
        head = df.head(5).to_csv(index=False)

        prompt = f"""
You are a data analyst. Given this CSV preview:

{head}

The user asked:
"{query}"

Return ONLY a valid JSON dictionary for a Plotly chart in this format:
{{ "data": [...], "layout": {{...}} }}

Use only double quotes for all keys and strings.
Do NOT include markdown, explanation, or extra text.
        """

        logger.info("Sending prompt to LLM...")
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{"role": "user", "content": prompt}]
        )

        result = response.choices[0].message.content
        logger.info("Received response from LLM")
        logger.warning(f"Raw Model Output:\n{result}")

        json_text = extract_json(result)

        try:
            chart_json = json.loads(json_text)
        except json.JSONDecodeError:
            logger.warning(" JSON failed, trying ast.literal_eval")
            chart_json = ast.literal_eval(json_text)

        return JSONResponse(content=chart_json)

    except Exception as e:
        logger.error(f" Error: {str(e)}")
        return JSONResponse(content={"error": f"Unexpected error: {str(e)}"}, status_code=500)


@router.post('/visualize')
async def visualise(file:UploadFile=File(...),query:str=Form(...)):
    files=await file.read()
    df=pd.read_csv(io.BytesIO(files))
    head=df.head[5].to_csv(index=False)


    
    prompt="""You are a data analyst and have the data of the following format 
    {head}
    Your job is to on basis of the query provided {query} youve to generate the appropriate columns for PlotPy
    and generate the response only in {{"data":[...],"layout":{{...}}}"""
    response=client.chats.completion.create(prompt=prompt,)
    