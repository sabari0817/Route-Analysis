from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from openai import OpenAI
# from .models import 
import os
import json

from .models import *

# ✅ NVIDIA Client (Secured)
client = OpenAI(
    api_key=os.environ.get("NVIDIA_API_KEY"),
    base_url="https://integrate.api.nvidia.com/v1"
)

# ✅ PROMPT FUNCTION 1: Generate Raw Text
def build_prompt(route_name):
    return f"""Act as a transportation, tourism, and route analysis expert.

Your task is to generate a COMPLETE and DETAILED route analysis.

STRICT RULES:
- You MUST follow EXACT numbering from 1 to 10
- Do NOT skip any section
- Do NOT summarize
- Do NOT give short answers
- Output must be detailed, structured, and professional
- Use bullet points and tables where needed
- Output must be READY FOR COPY-PASTE (no explanation before or after)
- If data is unknown, give realistic Indian estimates

FORMAT TO FOLLOW EXACTLY:

ROUTE NAME: {route_name}

1. Population in that area?
(Give approximate population with range for each major city and total corridor population)

2. Potential of the Area like Education, Temples, Tourist attraction, Companies?
(Clearly explain strengths like tourism, pilgrimage, industry, education)

3. Area Segmentation with Place Details
(List zones like origin, industrial, tourist, entry, destination)

4. Total Visitor Count with Place Name (Yearly & Daily)
(Give yearly + daily normal + peak)

5. Top Visitor Count (State-wise with Top 5 Cities and Count)
(Give percentage + top 5 cities per state)

6. Distance Between Two Cities (in KM)
(Create a clean table of distances)

7. Mode of Transport Used
(Give percentage split)

8. Luggage and Parcel Services
(List practical logistics movement)

9. Specific Bus and Train Details
(Show city-wise buses/day and trains/day clearly)

10. Suggested Routes
(Give 2–3 optimized routes with travel time)

IMPORTANT:
- DO NOT return summary cards
- DO NOT return UI format
- DO NOT shorten content
- DO NOT miss any section
- Each section must be clearly separated

Now generate for:
{route_name}"""


# ✅ PROMPT FUNCTION 2: Transform to JSON
def build_json_prompt(raw_text):
    return f"""You are a data transformation engine.

Convert the following unstructured route analysis data into STRICT VALID JSON.

Rules:
- Return ONLY JSON (no explanation, no text before/after)
- Use proper JSON format (double quotes, no trailing commas)
- Normalize ranges by taking mid-values (example: "10-15 million" → 12500000)
- Convert percentages to integers (example: "60% - 70%" → 65)
- Ensure all numeric fields are numbers (not strings)
- Keep city names consistent
- If multiple values exist, choose the most realistic average

Output JSON structure:

{{
  "population": [
    {{"city": "", "population": 0}}
  ],
  "potential": [
    {{
      "city": "",
      "education": "",
      "temples": "",
      "tourism": "",
      "industry": ""
    }}
  ],
  "segmentation": [
    {{
      "city": "",
      "urban": true,
      "industrial": true,
      "pilgrimage": false,
      "transit": true
    }}
  ],
  "visitors": [
    {{
      "city": "",
      "yearly": 0,
      "daily": 0,
      "festival": ""
    }}
  ],
  "distance": [
    {{"from": "", "to": "", "km": 0}}
  ],
  "transport_pattern": {{
    "bus": 0,
    "train": 0,
    "private": 0,
    "peak_days": "",
    "rush_pattern": ""
  }},
  "transport_details": [
    {{
      "from": "",
      "to": "",
      "mode": "",
      "frequency": ""
    }}
  ],
  "top_visitors": [
    {{
      "state": "",
      "city": "",
      "count": 0
    }}
  ],
  "suggested_routes": [
    {{"description": ""}}
  ]
}}

Now convert this data:

{raw_text}
"""


# ✅ LLM CALL
def call_llm(prompt, is_json=False):
    params = {
        "model": "meta/llama-3.1-70b-instruct",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3
    }
    if is_json:
        params["response_format"] = {"type": "json_object"}
        
    response = client.chat.completions.create(**params)
    return response.choices[0].message.content


# ✅ CLEAN JSON
def clean_json(response):
    response = response.strip()
    if "```json" in response:
        response = response.split("```json")[1]
    if "```" in response:
        response = response.split("```")[0]
    return json.loads(response.strip())


# ✅ MAIN VIEWS
def index(request):
    return render(request, 'index.html')

@csrf_exempt
def full_analysis_view(request):
    route_name = request.GET.get("route")

    if not route_name:
        return JsonResponse({"error": "Route required"})

    try:
        route, _ = Route.objects.get_or_create(name=route_name)

        # STEP 1: Generate Raw Text
        prompt1 = build_prompt(route_name)
        raw_text = ""
        for i in range(3):
            try:
                raw_text = call_llm(prompt1)
                break
            except Exception as e:
                if i == 2:
                    return JsonResponse({"error": f"LLM Step 1 failed: {str(e)}"})

        # STEP 2: Transform to JSON
        prompt2 = build_json_prompt(raw_text)
        data = {}
        for i in range(3):
            try:
                raw_json = call_llm(prompt2, is_json=True)
                data = clean_json(raw_json)
                break
            except Exception as e:
                if i == 2:
                    # Fallback gracefully if JSON parsing fails, still return the raw text
                    data = {}

        # STEP 3: DB Population
        if data:
            city_map = {}

            # Populate Cities & Population
            for p in data.get("population", []):
                city_name = p.get("city", "")
                if city_name:
                    city, _ = City.objects.get_or_create(name=city_name, route=route)
                    city_map[city_name] = city
                    Population.objects.update_or_create(
                        city=city,
                        defaults={"population": p.get("population", 0)}
                    )

            # Potential
            for p in data.get("potential", []):
                if p.get("city") in city_map:
                    Potential.objects.update_or_create(
                        city=city_map[p["city"]],
                        defaults={
                            "education": p.get("education", ""),
                            "temples": p.get("temples", ""),
                            "tourism": p.get("tourism", ""),
                            "industry": p.get("industry", ""),
                        }
                    )

            # Segmentation
            for s in data.get("segmentation", []):
                if s.get("city") in city_map:
                    Segmentation.objects.update_or_create(
                        city=city_map[s["city"]],
                        defaults={
                            "urban": s.get("urban", False),
                            "industrial": s.get("industrial", False),
                            "pilgrimage": s.get("pilgrimage", False),
                            "transit": s.get("transit", False),
                        }
                    )

            # Visitors
            for v in data.get("visitors", []):
                if v.get("city") in city_map:
                    Visitors.objects.update_or_create(
                        city=city_map[v["city"]],
                        defaults={
                            "yearly": v.get("yearly", 0),
                            "daily": v.get("daily", 0),
                            "festival": v.get("festival", "")
                        }
                    )

            # Distance
            for d in data.get("distance", []):
                if d.get("from") in city_map and d.get("to") in city_map:
                    Distance.objects.update_or_create(
                        route=route,
                        from_city=city_map[d["from"]],
                        to_city=city_map[d["to"]],
                        defaults={"km": d.get("km", 0)}
                    )

            # Transport
            tp = data.get("transport_pattern", {})
            Transport.objects.update_or_create(
                route=route,
                defaults={
                    "bus": tp.get("bus", 0),
                    "train": tp.get("train", 0),
                    "private": tp.get("private", 0)
                }
            )

            # Transport Details
            for td in data.get("transport_details", []):
                if td.get("from") in city_map and td.get("to") in city_map:
                    TransportDetail.objects.update_or_create(
                        route=route,
                        from_city=city_map[td["from"]],
                        to_city=city_map[td["to"]],
                        mode=td.get("mode", "Bus"),
                        defaults={"frequency": td.get("frequency", "")}
                    )

            # Top Visitors
            for tv in data.get("top_visitors", []):
                if tv.get("city") in city_map:
                    TopVisitors.objects.update_or_create(
                        route=route,
                        city=city_map[tv["city"]],
                        defaults={
                            "state": tv.get("state", ""),
                            "count": tv.get("count", 0)
                        }
                    )

            # Suggested Routes
            sr_text = "\\n".join([sr.get("description", "") for sr in data.get("suggested_routes", [])])
            SuggestedRoute.objects.update_or_create(
                route=route,
                defaults={"description": sr_text}
            )

        # Return both the raw text (for the UI) and the structured JSON data
        return JsonResponse({
            "message": "Full analysis completed successfully",
            "route": route.name,
            "data": raw_text,
            "json_data": data
        })

    except Exception as e:
        return JsonResponse({"error": str(e)})
