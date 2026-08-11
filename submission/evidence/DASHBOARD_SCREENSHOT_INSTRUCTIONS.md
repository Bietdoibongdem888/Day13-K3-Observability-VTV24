# Dashboard screenshot — manual evidence step

This file is an instruction checklist, not a substitute for screenshot evidence.

1. From the repository root, run:

   ```powershell
   uvicorn app.main:app --host 127.0.0.1 --port 8000
   ```

2. In another terminal, generate real data:

   ```powershell
   python scripts/load_test.py --concurrency 5
   python scripts/validate_dashboard.py
   ```

3. Open `http://127.0.0.1:8000/dashboard` in a browser.
4. Verify visually before capturing:

   - title `Day 13 AI Observability`;
   - time range `last 60 minutes` and refresh `30 seconds`;
   - exactly six panels: Latency, Traffic, Errors, Cost, Tokens, Quality;
   - values are non-empty and sourced from the just-generated requests;
   - unit and threshold are visible on every panel.

5. Capture a real browser screenshot without `.env`, terminal secrets or browser credential UI.
6. Save it as `submission/evidence/12_dashboard_6_panels.png`.
7. If six panels do not fit legibly, save a second image as `12b_dashboard_6_panels.png` and reference both in `submission/REPORT.md`.

Do not rename this instruction file to `.png` and do not count it as completed evidence.
