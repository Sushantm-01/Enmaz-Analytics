import json
import requests

INPUT_FILE = "machine_with_bearings.json"
OUTPUT_FILE = "machine_bearing_data.json"

BEARING_DATA_API = "https://srcapiv2.aams.io/AAMS/AI/Data"
HEADERS = {"Content-Type": "application/json"}


def fetch_bearing_data(machine_id, bearing_id, bearing_type):
    """Call AI/Data API for one bearing using dynamic type."""
    payload = {
        "machineId": machine_id,
        "bearingLocationId": bearing_id,
        "Axis_Id": "V-Axis",
        "type": bearing_type,         # <-- DYNAMIC TYPE
        "Analytics_Types": "MF"
    }

    response = requests.post(BEARING_DATA_API, json=payload, headers=HEADERS)

    if response.status_code != 200:
        print(f"Error fetching data: {machine_id} - {bearing_id}")
        return {}

    return response.json()


def main():
    with open(INPUT_FILE, "r") as f:
        machines = json.load(f)

    final_output = []

    for machine in machines:
        print(f"\nProcessing Machine: {machine['machineId']}")

        machine_type = machine.get("machineType", "OFFLINE")   # fallback

        machine_result = {
            "m.no": machine["m.no"],
            "machineId": machine["machineId"],
            "machineType": machine_type,
            "bearings": []
        }

        for b in machine["bearings"]:
            bearing_id = b["bearingId"]
            bearing_type = b.get("bearingLocationType", machine_type)

            print(f"  → Fetching data for Bearing: {bearing_id} (type={bearing_type})")

            bearing_data = fetch_bearing_data(
                machine["machineId"],
                bearing_id,
                bearing_type     # <-- pass dynamic type
            )

            machine_result["bearings"].append({
                "bearingId": bearing_id,
                "bearingLocationType": bearing_type,
                "statusName": b["statusName"],
                "data": bearing_data
            })

        final_output.append(machine_result)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(final_output, f, indent=4)

    print("\n--------------------------------")
    print("✔ Completed! Output saved to:", OUTPUT_FILE)
    print("--------------------------------")


if __name__ == "__main__":
    main()
