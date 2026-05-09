import os
import sys
import django

# Set up Django environment
sys.path.append(os.getcwd())
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "analysis.settings")
django.setup()

from functions.views import get_route_analysis_data
from functions.models import PopularSearch

def test():
    print("Testing get_route_analysis_data (View logic)...")
    data, error = get_route_analysis_data("Chennai", "Coimbatore", "")
    if error:
        print(f"Error: {error}")
    else:
        print("Success! View logic returned data.")
        print(f"Source: {data.get('data_source')}")
    
    print("\nTesting PopularSearch database interaction...")
    try:
        route_text = "Chennai → Coimbatore"
        popular, created = PopularSearch.objects.get_or_create(route_text=route_text)
        print(f"Success! PopularSearch: {popular.route_text}, Created: {created}")
    except Exception as e:
        print(f"Database Error: {str(e)}")

if __name__ == "__main__":
    test()
