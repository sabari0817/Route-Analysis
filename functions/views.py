from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from openai import OpenAI
import json

from .models import *

import os

# ✅ NVIDIA Client (Secured)
client = OpenAI(
    api_key=os.environ.get("NVIDIA_API_KEY"),
    base_url="https://integrate.api.nvidia.com/v1"
)


# ✅ PROMPT FUNCTION (VERY IMPORTANT)
def build_prompt(route_name):
    return f"""
You are a professional transportation and market analysis data engine.

STRICT INSTRUCTIONS:
- Return ONLY valid JSON (no text, no explanation, no markdown)
- All values must be LOGICALLY CORRECT and REALISTIC
- Do NOT guess randomly
- Use approximate real-world Indian data based on known trends

CRITICAL VALIDATION RULES:
1. Population:
   - Must be realistic (small towns: 40k–100k, cities: 1L–50L)
   - Do NOT give extremely low or extremely high values

2. Visitors:
   - Yearly visitors must be >= daily visitors × 300
   - Pilgrimage cities can have higher visitors
   - Avoid unrealistic huge numbers

3. Transport Share:
   - bus + train + private MUST equal EXACTLY 100
   - No value should exceed 80 individually
   - Example: 60, 25, 15

4. Distance:
   - Must be realistic based on Indian geography
   - Range: 50 km to 1500 km

5. Transport Frequency:
   - Bus: every 15 mins to 3 hours
   - Train: every 2 to 12 hours

6. Segmentation:
   - Set flags logically (pilgrimage = true for temple cities)

TASK:
Analyze this route:
{route_name}

OUTPUT FORMAT (STRICT — DO NOT CHANGE):

{{
  "cities": [
    {{
      "name": "CityName",
      "population": 100000,
      "education": "short detail",
      "temples": "short detail",
      "tourism": "short detail",
      "industry": "short detail",
      "segmentation": {{
        "urban": true,
        "industrial": false,
        "pilgrimage": true,
        "transit": true
      }},
      "visitors": {{
        "yearly": 1000000,
        "daily": 5000,
        "festival": "festival name"
      }}
    }}
  ],

  "distances": [
    {{
      "from": "CityName",
      "to": "CityName",
      "km": 100
    }}
  ],

  "transport": {{
    "bus": 60,
    "train": 25,
    "private": 15
  }},

  "transport_detail": [
    {{
      "from": "CityName",
      "to": "CityName",
      "mode": "Bus",
      "frequency": "Every 30 mins"
    }}
  ],

  "top_visitors": [
    {{
      "state": "StateName",
      "city": "CityName",
      "count": 5000
    }}
  ],

  "parcel_service": [
    {{
      "service_name": "Service Name",
      "coverage": "Coverage Details"
    }}
  ],

  "suggestion": "Final route analysis summary"
}}
"""


# ✅ LLM CALL
def call_llm(prompt):
    response = client.chat.completions.create(
        model="meta/llama-3.1-70b-instruct",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        response_format={"type": "json_object"}
    )
    return response.choices[0].message.content


# ✅ CLEAN JSON
def clean_json(response):
    response = response.strip()

    if "```" in response:
        response = response.split("```")[1]

    return json.loads(response)


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

        prompt = build_prompt(route_name)

        # ✅ Retry (important)
        for i in range(3):
            try:
                raw = call_llm(prompt)
                data = clean_json(raw)
                break
            except Exception as e:
                if i == 2:
                    return JsonResponse({"error": f"LLM failed: {str(e)}"})

        # ✅ Safety defaults
        cities_data = data.get("cities", [])
        distances_data = data.get("distances", [])
        transport_data = data.get("transport", {})
        transport_detail_data = data.get("transport_detail", [])
        top_visitors_data = data.get("top_visitors", [])
        parcel_service_data = data.get("parcel_service", [])
        suggestion_text = data.get("suggestion", "")

        city_map = {}

        # ✅ SAVE CITY DATA
        for c in cities_data:
            city, _ = City.objects.get_or_create(
                name=c.get("name"),
                route=route
            )
            city_map[c.get("name")] = city

            Population.objects.update_or_create(
                city=city,
                defaults={"population": c.get("population", 0)}
            )

            Potential.objects.update_or_create(
                city=city,
                defaults={
                    "education": c.get("education", ""),
                    "temples": c.get("temples", ""),
                    "tourism": c.get("tourism", ""),
                    "industry": c.get("industry", ""),
                }
            )

            seg = c.get("segmentation", {})

            Segmentation.objects.update_or_create(
                city=city,
                defaults={
                    "urban": seg.get("urban", False),
                    "industrial": seg.get("industrial", False),
                    "pilgrimage": seg.get("pilgrimage", False),
                    "transit": seg.get("transit", False),
                }
            )

            vis = c.get("visitors", {})

            Visitors.objects.update_or_create(
                city=city,
                defaults={
                    "yearly": vis.get("yearly", 0),
                    "daily": vis.get("daily", 0),
                    "festival": vis.get("festival")
                }
            )

        # ✅ DISTANCES
        for d in distances_data:
            if d.get("from") in city_map and d.get("to") in city_map:
                Distance.objects.update_or_create(
                    route=route,
                    from_city=city_map[d["from"]],
                    to_city=city_map[d["to"]],
                    defaults={"km": d.get("km", 0)}
                )

        # ✅ TRANSPORT
        Transport.objects.update_or_create(
            route=route,
            defaults={
                "bus": transport_data.get("bus", 0),
                "train": transport_data.get("train", 0),
                "private": transport_data.get("private", 0)
            }
        )

        # ✅ TRANSPORT DETAIL
        for td in transport_detail_data:
            if td.get("from") in city_map and td.get("to") in city_map:
                TransportDetail.objects.update_or_create(
                    route=route,
                    from_city=city_map[td["from"]],
                    to_city=city_map[td["to"]],
                    mode=td.get("mode", "Bus"),
                    defaults={"frequency": td.get("frequency", "")}
                )

        # ✅ SUGGESTION
        SuggestedRoute.objects.update_or_create(
            route=route,
            defaults={"description": suggestion_text}
        )

        # ✅ TOP VISITORS
        for tv in top_visitors_data:
            if tv.get("city") in city_map:
                TopVisitors.objects.update_or_create(
                    route=route,
                    city=city_map[tv["city"]],
                    defaults={
                        "state": tv.get("state", ""),
                        "count": tv.get("count", 0)
                    }
                )

        # ✅ PARCEL SERVICE
        for ps in parcel_service_data:
            ParcelService.objects.update_or_create(
                route=route,
                service_name=ps.get("service_name", ""),
                defaults={"coverage": ps.get("coverage", "")}
            )

        return JsonResponse({
            "message": "Full analysis completed successfully",
            "route": route.name,
            "data": data
        })

    except Exception as e:
        return JsonResponse({"error": str(e)})