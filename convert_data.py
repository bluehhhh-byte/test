import pandas as pd
import json
import os

def convert():
    disaster_path = r"C:\Users\박준성\Downloads\시험문제\실전세트02·블루_ 재난안전모니터링\3과목_자료묶음\재난발생_현황.csv"
    facility_path = r"C:\Users\박준성\Downloads\시험문제\실전세트02·블루_ 재난안전모니터링\3과목_자료묶음\안전시설_현황.csv"
    output_path = r"c:\Users\박준성\.antigravity\.Test\test_deploy\data.json"

    # Read disaster data
    if os.path.exists(disaster_path):
        df_disaster = pd.read_csv(disaster_path, encoding='utf-8')
        # Replace NaN with None (null in JSON)
        df_disaster = df_disaster.where(pd.notnull(df_disaster), None)
        disasters = df_disaster.to_dict(orient='records')
    else:
        print(f"Error: {disaster_path} not found")
        disasters = []

    # Read facility data
    if os.path.exists(facility_path):
        df_facility = pd.read_csv(facility_path, encoding='utf-8')
        # Replace NaN with None
        df_facility = df_facility.where(pd.notnull(df_facility), None)
        facilities = df_facility.to_dict(orient='records')
    else:
        print(f"Error: {facility_path} not found")
        facilities = []

    data = {
        "disasters": disasters,
        "facilities": facilities
    }

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Successfully converted data. Saved {len(disasters)} disasters and {len(facilities)} facilities to {output_path}")

if __name__ == "__main__":
    convert()
