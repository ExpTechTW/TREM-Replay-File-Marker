import requests
import os
import json
import time

replay_time_start = "2023-7-10 6:11:28"
replay_time_end = "2023-7-10 6:21:33"

lock = False

rts_replay_time = int(time.mktime(time.strptime(
    replay_time_start, "%Y-%m-%d %H:%M:%S"))) * 1000
end_time = int(time.mktime(time.strptime(
    replay_time_end, "%Y-%m-%d %H:%M:%S"))) * 1000

if not os.path.exists("./replay"):
    os.makedirs("./replay")


def fetch_data(url):
    global lock
    if lock:
        return
    lock = True
    try:
        response = requests.get(url, timeout=2.5)
        if response.status_code == 200:
            data = response.json()
            lock = False
            return data
        else:
            print(f"Request failed with status code: {response.status_code}")
    except requests.Timeout:
        print("Request timed out")
    except requests.RequestException as e:
        print(f"Request failed: {e}")
    lock = False
    return None


while rts_replay_time <= end_time:
    if lock:
        continue

    replay_time_seconds = rts_replay_time // 1000
    rts_replay_time += 1000

    rts_url = f"https://exptech.com.tw/api/v2/trem/rts?time={replay_time_seconds * 1000}"
    eew_url = f"https://exptech.com.tw/api/v1/earthquake/info?time={replay_time_seconds}&type=all"

    rts_data = fetch_data(rts_url)
    eew_data = fetch_data(eew_url)

    if rts_data and eew_data:
        with open(f"./replay/{replay_time_seconds}.trem", "w") as file:
            combined_data = {"rts": rts_data, "eew": eew_data}
            json.dump(combined_data, file)

    time.sleep(0.2)
