from fastapi import FastAPI, UploadFile
import logging
import vertexai
from vertexai.generative_models import GenerativeModel, Part
from websearch import WebSearch

app = FastAPI()

PROJECT_ID = "gemma-hackathon-bas"
vertexai.init(project=PROJECT_ID, location="us-central1")


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/upload")
async def say_hello(file: UploadFile):
    logger = logging.getLogger(__name__)
    model = GenerativeModel("gemini-1.5-flash-002")
    # prompt = """
    # Give me the exact one search query for this Image to buy this.
    # Make sure you only return one search query with no additional text.
    # Just make sure no other response, I just want the search query.
    # """

    prompt = """
    give me a search query text to find this image on the web and I just want the first result without additional text, not a link
    """

    try:
        # Read the file content as bytes
        file_content = await file.read()

        # Create a Part object with the content and content type
        file_part = Part.from_data(file_content, mime_type="image/jpeg")

        response = model.generate_content(
            [file_part, prompt]
        )

        search_query = response.text

        print(search_query)

        link_list = [item for item in WebSearch(search_query).pages if "maps" not in item]

        return {"message": link_list[:4]}
    except Exception as e:
        logger.error(f"Error generating response: {e}")
        return {"error": "Failed to generate response"}

