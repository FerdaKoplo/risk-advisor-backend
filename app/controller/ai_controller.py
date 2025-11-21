from flask import Blueprint, request, jsonify
from app.services.ollama_service import OllamaService
from app.services.risk_service import RiskService
import re
import json

ai_route = Blueprint("ai_route", __name__)
ollama = OllamaService()

# def safe_parse_ai_response(raw: str) -> dict:
#     """
#     Tries to extract a JSON object from messy AI output.
#     If it fails, returns None.
#     """
#     if not raw:
#         return None
#     cleaned = re.sub(r'```(?:json)?|```', '', raw, flags=re.IGNORECASE)
#     match = re.search(r'\{.*\}', cleaned, flags=re.DOTALL)
#     if match:
#         try:
#             return json.loads(match.group(0))
#         except json.JSONDecodeError:
#             return None
#     return None

@ai_route.post("/ai/safety-advice")
def ai_safety_advice():
    data = request.json
    required_fields = ['employee_id', 'location_area', 'prob_input', 'sev_input', 'comp_input']
    if not data or any(field not in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        assessment = RiskService.create_assessment(data)

        # Simplified prompt: only emergency action if risk HIGH
        prompt = f"""
You are an industrial safety expert.

Return ONLY the emergency action if the risk is HIGH. 
If the risk is not HIGH, respond with 'None'.
Do NOT include summaries or general actions.

Employee: {assessment['employee_id']}
Location: {assessment['location_area']}
Risk Level: {assessment['risk_level']}
Score: {assessment['score']}
"""

        raw_suggestion = ollama.generate(prompt)
        emergency_advice = raw_suggestion.strip()

        return jsonify({
            "status": "success",
            "source": "RandomForest + Ollama AI",
            "assessment": assessment,
            "emergency": emergency_advice
        }), 200

    except Exception as e:
        print(f"Error in ai_safety_advice: {str(e)}")
        return jsonify({"error": str(e)}), 400
