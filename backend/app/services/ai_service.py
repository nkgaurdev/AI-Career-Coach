import logging

from google import genai
from google.genai import types
from pydantic import ValidationError

from app.core.config import settings
from app.schemas.resume import ResumeData


logger = logging.getLogger(__name__)


# Initialize the Gemini client
try:
    client = genai.Client(api_key=settings.GEMINI_API_KEY)
except Exception as e:
    logger.error(f"Failed to initialize Gemini client: {e}")
    client = None


def parse_resume_with_gemini(resume_text: str) -> ResumeData:
    """
    Extract structured information from raw resume text using Gemini.
    """

    if not client:
        raise RuntimeError(
            "Gemini client is not initialized. Check your API key."
        )

    if not resume_text or not resume_text.strip():
        raise ValueError("Resume text cannot be empty.")

    prompt = (
        "You are an expert Applicant Tracking System (ATS) and resume parser.\n"
        "Extract the information from the following resume text and format it "
        "as a structured JSON object matching the provided schema.\n\n"
        "Resume Text:\n"
        f"{resume_text}"
    )

    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=ResumeData,
            ),
        )

        if not response.text:
            raise ValueError("Gemini returned an empty response.")

        parsed_data = ResumeData.model_validate_json(response.text)

        return parsed_data

    except ValidationError as e:
        logger.error(
            f"Validation error when parsing Gemini response: {e}"
        )
        raise ValueError(
            f"Failed to validate extracted resume data: {e}"
        )

    except Exception as e:
        logger.error(
            f"Error during Gemini API call: {e}"
        )
        raise RuntimeError(
            "Failed to extract resume info via Gemini. "
            "Please try again later."
        )