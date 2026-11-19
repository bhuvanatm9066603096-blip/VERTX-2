# VERTX Multimodal Digital Forensics

## Run the website on Windows

From the repository root, start the static site:

```powershell
python BACKEND/app.py
```

Open `http://127.0.0.1:8000/login.html` in Microsoft Edge. Stop the local server with `Ctrl+C`.

The site opens with `FRONTEND/login.html`. Use any Gmail address and a password ending in `@123`, then you will be redirected to `FRONTEND/index.html`:

- Email: `yourname@gmail.com`
- Password: `anything@123`

The sign-in is protected by a Flask server session. Direct access to `/`, `/index.html`, `/correlation.html`, and other frontend files now redirects unauthenticated users to `/login.html`. It is still demonstration authentication and does not verify real Gmail accounts or hashed stored passwords; replace it with a database-backed account system or OAuth identity provider before production use.


The frontend runs without the Python backend. `FRONTEND/index.html` launches the image, video, audio, and text modules in the browser; `FRONTEND/correlation.html` provides the cross-modal lab. The detector pages are stored beside the launcher so they can be maintained separately.

## Important limitations

- Scores are heuristic indicators for demonstration and triage, not a trained model or proof of authenticity.
- Results depend on the signals extracted by each module; human review is required.
- The standalone correlation visualization loads its Three.js library from `cdnjs.cloudflare.com`.
- ScamShield uses English keyword and pattern rules; its evidence band is not an accuracy estimate.
- The existing `BACKEND` folder is an incomplete prototype and is not required to run this website.
