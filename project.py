import requests
# Fetch data from given API URL and return the JSON response
def fetch_data_from_api(api_url):
    response = requests.get(api_url)
    try:
        if response.json():
            return response.json()
    except requests.RequestException as e:
        print(f"Error occurred while fetching data from the API, HTTP Status Code:{response.status_code}")
        return None

# Get countries by region and print their names
def get_countries_by_region(data,region):
    if data is None:
        print("No data available to filter by region.Please check the API URL or your internet connection.")
        return
    available_regions = set(country['region'] for country in data if 'region' in country)
    countries_in_region = [country for country in data if country['region'] == region]
    if len(countries_in_region) > 0:
        return countries_in_region,available_regions
    else:
        return [], available_regions

# Sort filtered countries by a given filter (default is population)
def sort_countries_by(countries,by="population"):
    if countries is None:
        print("No data available to sort.")
        return []
    if by not in countries[0]:
        print(f"Invalid filter '{by}' provided. Please use a valid filter.")
        return []
    sorted_countries = sorted(countries, key=lambda x: x[by], reverse=True)
    return sorted_countries
# Fetch the most populated countries from the sorted list
def fetch_the_most_populated_countries(sorted_countries=None, n:int=2):
    if sorted_countries is None:
        print("No sorted countries data available")
        return []
    return sorted_countries[:n]

# Print countries with population, area, and name
def print_countries(countries:list,sorted = True,sort_by="population"):
    if sorted:
        countries = sort_countries_by(countries, by=sort_by)
        print(f"\n{len(countries)} {'most populated countries'.upper()}\n")
    else:
        print(f"\n{len(countries)} {'countries'.upper()}\n")
    print("Code", "\tPopulation\t", "Area\t", "\tName")
    print("="*80)
    for country in countries:
        if 'cioc' not in country.keys():
            country['cioc'] = "N/A"
        if 'population' not in country.keys():
            country['population'] = "N/A"
        if 'area' not in country.keys():
            country['area'] = "N/A"
        print(f"{country['cioc']}\t{country['population']:<11}\t {country['area']:<8}\t{country['name']}")
        print("-"*80)

    

if __name__ == "__main__":
    API_URL = "https://countries.dev/countries"
    country_data = fetch_data_from_api(API_URL)
    filtered_countries = None
    while True:
        region = input("Enter the region name to filter countries (e.g Asia, Europe): ")
        filtered_countries, available_regions = get_countries_by_region(country_data, region)
        if filtered_countries is not None and len(filtered_countries) > 0:
            break
        print(f"No countries found in the region: {region}")
        print(f"Please enter a valid region name e.g.({', '.join(available_regions)})")

    print_countries(filtered_countries, sorted=True,sort_by='name')
    #all_sorted_countries = sort_countries_by(filtered_countries)
    #most_populated_countries =fetch_the_most_populated_countries(all_sorted_countries, 2)
    #print_countries(most_populated_countries,sorted=True)
    