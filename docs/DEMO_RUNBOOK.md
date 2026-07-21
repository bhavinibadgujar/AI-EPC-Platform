# Demo Runbook

## Backend

Run the single FastAPI entry point from the repo root:

```powershell
uvicorn backend.main:app --reload
```

Health check:

```powershell
Invoke-RestMethod http://localhost:8000/api/health
```

`backend/app/main.py` is archived as a compatibility shim that imports `backend.main:app`.

## Frontend

Run the active frontend from:

```powershell
cd epc-ai-copilot
npm run dev
```

The stale duplicate `Frontend/epc-ai-copilot` tree has been removed.

## Reset Demo Data

With the backend running:

```powershell
.\scripts\reset_demo_seed.ps1
```

Sample demo files are in `demo/`:

- `sample_spec.txt`
- `sample_vendor_submittal.txt`
- `sample_schedule.csv`
