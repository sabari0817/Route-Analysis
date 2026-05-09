import os
import json
import requests
from django.utils import timezone

def generate_route_analysis(source, destination, via=None):
    """
    Calls the NVIDIA API to generate route analysis data in the expected JSON format.
    """
    api_key = os.getenv("NVIDIA_API_KEY")
    if not api_key:
        return None, "NVIDIA_API_KEY is not set in the environment variables."

    # Prompt definition
    prompt = f"""
You are a professional transportation analyst. Generate a highly detailed Route Analysis for: {source} to {destination}{f' via {via}' if via else ''}.
Return ONLY valid JSON. No conversational filler.

The JSON MUST follow this structure exactly:
1. route_summary: {{ "path": "string", "total_distance": int, "estimated_time": float }}
2. population_data: {{ "source": {{ "name": "string", "count": int }}, "destination": {{ "name": "string", "count": int }} }}
3. area_segmentation: {{ "job_business_areas": ["string"], "student_areas": ["string"], "tourist_areas": ["string"] }}
4. visitor_data: [ {{ "place_name": "string", "yearly": int, "daily": int }} ]
5. demand_distribution: [ {{ "state": "string", "percentage": float, "cities": [ {{ "name": "string", "percentage": float }} ] }} ]
6. distance_details: [ {{ "segment": "string", "distance_km": int }} ]
7. transport_distribution: {{ "bus": float, "train": float, "car": float, "taxi": float, "flight": float }}
8. logistics_services: {{ "parcel_movement": {{ "bus": float, "train": float, "courier": float, "taxi": float }}, "modes_used": ["string"] }}
9. transport_schedule: [ {{ "from": "{destination}", "to": "{source}", "bus_trips": int, "train_trips": int }} ]
10. suggested_routes: [ {{ "option": int, "path": "string", "distance": int, "time": float }} ]
11. dashboard_data: {{
      "traffic_trends": [ {{ "time": "string", "value": int }} ],
      "travel_time_by_hour": [ {{ "hour": "string", "minutes": int }} ],
      "live_updates": [ {{ "incident": "string", "severity": "Low"|"High", "time": "string" }} ],
      "weather": {{ "impact": "Low"|"High", "details": "string" }},
      "area_potential": [ {{ "district": "string", "population": int, "potential_score": int, "business_potential": "string", "growth_rate": float, "sectors": [ {{ "name": "string", "score": int }} ] }} ],
      "corridor_potential": {{ "business": int, "student": int, "tourist": int }}
    }}
"""

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "meta/llama-3.1-8b-instruct",
        "messages": [
            {"role": "system", "content": "You are a professional transportation data analyst. Provide consistent, deterministic JSON data."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.1,
        "max_tokens": 4096
    }
    content = ""
    try:
        # Increased timeout to 90 seconds to allow for complex generations
        response = requests.post(
            "https://integrate.api.nvidia.com/v1/chat/completions", 
            headers=headers, 
            json=payload,
            timeout=180
        )
        response.raise_for_status()
        
        response_data = response.json()
        content = response_data['choices'][0]['message']['content'].strip()
        
        # Extract JSON from potential conversational filler
        start_index = content.find('{')
        end_index = content.rfind('}')
        
        if start_index != -1 and end_index != -1:
            json_content = content[start_index:end_index+1]
            try:
                parsed_json = json.loads(json_content)
                return parsed_json, None
            except json.JSONDecodeError:
                # If extraction failed, fall back to stripping markdown
                pass

        # Original cleanup logic as fallback
        if content.startswith("```json"):
            content = content[7:]
        elif content.startswith("```"):
            content = content[3:]
            
        if content.endswith("```"):
            content = content[:-3]
            
        parsed_json = json.loads(content.strip())
        return parsed_json, None

    except requests.exceptions.Timeout:
        print("API Error: Request timed out")
        return None, "Unable to fetch route analysis at the moment (request timed out)"
    except requests.exceptions.RequestException as e:
        error_msg = "Unable to fetch route analysis at the moment"
        print(f"API Error: {str(e)}") 
        if hasattr(e, 'response') and e.response is not None:
            print(f"API Response Body: {e.response.text}")
        return None, error_msg
    except json.JSONDecodeError as e:
        import traceback
        with open('django_error.log', 'a', encoding='utf-8') as f:
            f.write(f"\n--- JSON DECODE ERROR AT {timezone.now()} ---\n")
            f.write(f"Error: {str(e)}\n")
            f.write(f"Raw Content: {content}\n")
            f.write("------------------------------\n")
        return None, "Unable to fetch route analysis at the moment (invalid response format)"
    except Exception as e:
        import traceback
        print(f"Unexpected Error: {str(e)}")
        traceback.print_exc()
        return None, "Unable to fetch route analysis at the moment"
