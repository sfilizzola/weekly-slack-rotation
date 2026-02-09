import json
import os
import sys
import urllib.request

TEAMS_FILE = "teams.json"
STATE_FILE = "rotation_state.json"

WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL", "").strip()
WEBHOOK_URL_2 = os.environ.get("SLACK_WEBHOOK_URL_2", "").strip()
GUIDE_URL = os.environ.get("GUIDE_URL", "").strip()

def die(msg: str, code: int = 1):
    print(msg)
    sys.exit(code)

def load_json(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(path: str, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
        f.write("\n")

def post_to_slack(webhook_url: str, text: str):
    payload = {"text": text}
    req = urllib.request.Request(
        webhook_url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        body = resp.read().decode("utf-8", errors="replace")
        if resp.status < 200 or resp.status >= 300:
            die(f"Slack webhook failed: HTTP {resp.status} {body}")
        print(f"Slack response: {resp.status} {body}")

def main():
    if not WEBHOOK_URL:
        die("Missing SLACK_WEBHOOK_URL env var (set it as a GitHub Actions secret).")

    teams = load_json(TEAMS_FILE)
    if not isinstance(teams, list) or len(teams) == 0:
        die("teams.json must be a non-empty JSON array of team names.")

    state = load_json(STATE_FILE)
    idx = int(state.get("index", 0)) % len(teams)

    team = teams[idx]
    guide_part = f" You can find the how-to react guide here: {GUIDE_URL}" if GUIDE_URL else ""
    text = f"This week the alerts should be handled by *{team}*.{guide_part}"

    post_to_slack(WEBHOOK_URL, text)

    if WEBHOOK_URL_2:
        post_to_slack(WEBHOOK_URL_2, text)
        
    # rotate
    state["index"] = (idx + 1) % len(teams)
    save_json(STATE_FILE, state)
    print(f"Rotated index to {state['index']} (team was '{team}').")

if __name__ == "__main__":
    main()
