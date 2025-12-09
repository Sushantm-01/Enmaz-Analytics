import json
import requests

# Input machine file
MACHINE_FILE = "machine_filtered_2025-12-09.json"
OUTPUT_FILE = "machine_with_bearings.json"
BEARING_API = "https://srcapiv2.aams.io/AAMS/AI/BearingLocation"

HEADERS = {"Content-Type": "application/json"}

def fetch_bearings(machine_id):
    """Call BearingLocation API and return list of bearings"""
    payload = {"machineId": machine_id}
    response = requests.post(BEARING_API, json=payload, headers=HEADERS)
    if response.status_code != 200:
        print(f"Error fetching bearings for {machine_id}: {response.status_code}")
        return []
    return response.json()  # list of bearings

def main():
    # 1. Load machine filtered JSON
    with open(MACHINE_FILE, "r") as f:
        machines = json.load(f)

    result = []

    # 2. Loop through machines
    for machine in machines:
        machine_id = machine["id"]
        machine_type = machine["machineType"]
        m_no = machine["m.no"]

        # 3. Fetch bearings for this machine
        bearings_data = fetch_bearings(machine_id)

        # 4. Extract only required fields from bearings
        bearings_list = []
        for b in bearings_data:
            bearings_list.append({
                "bearingId": b.get("_id"),
                "bearingLocationType": b.get("bearingLocationType"),
                "statusName": b.get("statusName")
            })

        # 5. Add to result
        result.append({
            "m.no": m_no,
            "machineId": machine_id,
            "machineType": machine_type,
            "bearings": bearings_list
        })

    # 6. Save to output JSON
    with open(OUTPUT_FILE, "w") as f:
        json.dump(result, f, indent=4)

    print(f"Done! Output saved in {OUTPUT_FILE}")
    print(f"Total machines processed: {len(result)}")

if __name__ == "__main__":
    main()
