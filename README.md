# Weekly Slack Rotation 🥔

A small internal automation that posts a **weekly Slack message** rotating alert ownership between teams.

Every Monday, the bot selects the next team in a predefined list and posts a reminder message to a Slack channel, including a link to the internal “how-to react” guide.

The rotation state is persisted in the repository, making the behavior transparent, predictable, and easy to adjust.

---

## What this does

- Posts a weekly reminder message to Slack
- Rotates responsibility between teams in a fixed order
- Persists rotation state in GitHub
- Runs fully automatically via GitHub Actions
- Requires no Slack OAuth scopes (uses Incoming Webhooks only)

Example message:

> This week the alerts should be tackled by **Invoices**.  
> You can find the how-to react guide here: <link>

---

## Repository structure

├─ .github/
│  └─ workflows/
│     └─ weekly-alert-rotation.yml   # GitHub Actions schedule
├─ scripts/
│  └─ post_weekly_rotation.py        # Posting + rotation logic
├─ teams.json                        # Ordered list of teams
├─ rotation_state.json               # Current rotation index
└─ README.md

---

## Configuration

### 1. Slack Webhook (required)

This project uses a **Slack Incoming Webhook**.

Add it as a GitHub Actions secret:

- **Name:** `SLACK_WEBHOOK_URL`
- **Value:** Slack Incoming Webhook URL

Path:

Repository → Settings → Secrets and variables → Actions → Secrets

---

### 2. Teams list

Edit `teams.json` to define the rotation order:

```json
[
  "Team 1",
  "Team 2",
  "Team 3"
]
```

Rotation proceeds in order and wraps around automatically.

### 3. Guide link (optional)

To include a link to documentation in the Slack message, add a repository variable:

- **Name:** `GUIDE_URL`
- **Value:** Link to internal guide (e.g. Confluence)

Path:

Repository → Settings → Secrets and variables → Actions → Variables

## How it works

1. GitHub Actions triggers the workflow every Monday.
2. The script performs the following steps:
   - Reads the ordered team list from `teams.json`.
   - Reads the current rotation index from `rotation_state.json`.
   - Selects the team responsible for the current week.
   - Posts a message to Slack using an Incoming Webhook.
   - Advances the rotation index.
   - Commits the updated `rotation_state.json` back to the repository.
3. On the next scheduled run, the next team in the list is selected.

This design avoids date-based logic and keeps the rotation explicit, predictable, and version-controlled.

---

## Schedule

The workflow is scheduled using GitHub Actions cron and runs every Monday.

- **Time:** 08:00 UTC  
- **Berlin time:**  
  - 09:00 during CET (winter)  
  - 10:00 during CEST (summer)

The workflow also supports manual execution.

---

## Manual run (testing)

The workflow can be triggered manually at any time:

1. Go to **Actions** in the repository.
2. Select **Weekly Slack rotation**.
3. Click **Run workflow**.

This is useful for:
- Verifying configuration
- Testing Slack connectivity
- Validating rotation behavior after changes

---

## Changing the rotation

- **Add or remove teams**  
  Update `teams.json`. Rotation follows the array order.

- **Reset the rotation**  
  Set the `index` value in `rotation_state.json` back to `0`.

- **Skip a team once**  
  Manually increment the `index` value in `rotation_state.json`.

All changes are committed to the repository and fully auditable.

---

## Failure modes and safety

- If the Slack webhook call fails:
  - The workflow fails.
  - The rotation index is **not** advanced.
- If `teams.json` contains invalid JSON, the workflow fails before posting.
- If the repository becomes inactive for 60 days, GitHub may pause scheduled workflows.  
  This repository commits weekly, so the schedule remains active automatically.

---

## Ownership

This is an internal automation with no user interaction and no persistent state outside GitHub.

If the workflow stops working, common causes include:
- An expired or revoked Slack Incoming Webhook
- Invalid JSON in `teams.json`
- Missing GitHub Actions permission (`contents: write`)

---

## Why this exists

- Make alert ownership explicit
- Reduce confusion and alert fatigue
- Eliminate manual reminders
- Keep responsibility visible and predictable

This is intentionally boring, reliable automation.