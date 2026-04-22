import requests

def test_arbeitnow():
    try:
        response = requests.get("https://www.arbeitnow.com/api/job-board-api")
        if response.status_code == 200:
            print("Arbeitnow API is alive!")
            data = response.json()
            print(f"Total jobs: {len(data.get('data', []))}")
            if data.get('data'):
                print(f"Sample job: {data['data'][0]['title']} at {data['data'][0]['company_name']}")
        else:
            print(f"Arbeitnow failed: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_arbeitnow()
