import json
import datetime
import requests

API_URL = "https://srcapiv2.aams.io/AAMS/AI/Machine"

def fetch_and_filter_machine_data():
    # 1. Today's date
    today = datetime.date.today().strftime("%Y-%m-%d")

    payload = {"date": today}
    headers = {
        "Content-Type": "application/json"
    }

    print("Calling API...")
    response = requests.post(API_URL, json=payload, headers=headers)

    # Check if API call failed
    if response.status_code != 200:
        print("API Error:", response.status_code, response.text)
        return

    raw_data = response.json()

    filtered_list = []

    # 2. Filter required fields
    for index, item in enumerate(raw_data, start=1):
        filtered_list.append({
            "m.no": index,
            "id": item.get("_id"),
            "machineType": item.get("machineType")
        })

    # 3. Output file name
    output_file = f"machine_filtered_{today}.json"

    # 4. Store result
    with open(output_file, "w") as f:
        json.dump(filtered_list, f, indent=4)

    print("✔ API data fetched successfully")
    print("✔ Filtered data saved to:", output_file)
    print("✔ Total machines:", len(filtered_list))


if __name__ == "__main__":
    fetch_and_filter_machine_data()
