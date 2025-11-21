from flask import Blueprint, request, jsonify
from app.services.ollama_service import OllamaService
from app.services.risk_service import RiskService

ai_route = Blueprint("ai_route", __name__)
ollama = OllamaService()

@ai_route.post("/ai/safety-advice")
def ai_safety_advice():
    data = request.json

    try:
        assessment = RiskService.create_assessment(data)

        prompt = f"""
                You are an AI Safety Risk Expert. Based on the following structured data,
                provide a tailored safety recommendation with actionable steps.

                Employee: {assessment['employee_id']}
                Location: {assessment['location_area']}

                Risk Score: {assessment['score']}
                Risk Level: {assessment['risk_level']}
                System Recommendation: {assessment['suggestion']}

                Risk Factors:
                - Probability: {assessment['details']['prob_weight']}
                - Severity: {assessment['details']['sev_weight']}
                - Competency Modifier: {assessment['details']['comp_multiplier']}

                Write the output in this format:

                **Risk Summary**
                - Short explanation.

                **AI Recommended Action**
                - 2–3 bullet points.

                If risk level is HIGH → include emergency instruction.
                """

        suggestion = ollama.generate(prompt)

        return jsonify({
            "risk_result": assessment,
            "ai_recommendation": suggestion
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400
