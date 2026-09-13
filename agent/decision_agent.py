import os
import json
import streamlit as st

from dotenv import load_dotenv
from google import genai


# Load .env file for local development
load_dotenv()


# Get Gemini API key
api_key = os.getenv("GEMINI_API_KEY")


# Get API key from Streamlit Cloud Secrets if .env is not available
if not api_key:
    api_key = st.secrets.get("GEMINI_API_KEY")


# Check API key
if not api_key:
    raise ValueError("GEMINI_API_KEY not configured.")


# Create Gemini client
client = genai.Client(
    api_key=api_key
)


def get_agent_decision(disruption, options):

    prompt = f"""
You are an autonomous retail supply chain recovery agent.

Your job is to select the BEST recovery option.

You must follow these rules:

1. Use ONLY the options provided.
2. Never invent a vendor, route, or ID.
3. Never select an unavailable option.
4. Consider cost, delivery time, and carbon emissions.
5. Prefer the option that maintains customer service.
6. Compare all available options before making a decision.
7. Return ONLY valid JSON.
8. Do not return markdown.
9. Do not return explanations outside the JSON.
10. Confidence must be a number between 0 and 1.

DISRUPTION:
{json.dumps(disruption, indent=2)}

AVAILABLE OPTIONS:
{json.dumps(options, indent=2)}

Return exactly this JSON format:

{{
    "action": "PURCHASE or REROUTE",
    "vendor_id": "vendor id if purchase, otherwise null",
    "route_id": "route id if reroute, otherwise null",
    "reason": "short explanation",
    "confidence": 0.0
}}
"""

    try:

        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt
        )

        text = response.text.strip()

        # Remove markdown if Gemini adds it
        text = text.replace("```json", "")
        text = text.replace("```", "")
        text = text.strip()

        # Convert Gemini response to Python dictionary
        decision = json.loads(text)

        # Basic validation
        if "action" not in decision:
            return {
                "action": "INVALID",
                "reason": "Gemini response does not contain an action.",
                "confidence": 0
            }

        if decision["action"] not in ["PURCHASE", "REROUTE"]:
            return {
                "action": "INVALID",
                "reason": "Gemini returned an invalid action.",
                "confidence": 0
            }

        if "confidence" not in decision:
            decision["confidence"] = 0

        return decision

    except json.JSONDecodeError:

        return {
            "action": "INVALID",
            "reason": "Gemini returned invalid JSON.",
            "confidence": 0
        }

    except Exception as e:

        return {
            "action": "INVALID",
            "reason": f"Gemini API error: {str(e)}",
            "confidence": 0
        }