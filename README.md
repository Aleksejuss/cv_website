# CV Website

Bilingual (EN/LT) static CV website for Aleksejus Sosidko.

## Stack
- Static `HTML/CSS/JS`
- JSON content files (`content/cv.en.json`, `content/cv.lt.json`)
- PDF extraction script (`scripts/extract_cv.py` with `pypdf`)

## Project Structure
- `index.html` - single-page layout with semantic sections
- `styles/main.css` - visual system, layout, responsive rules, motion
- `scripts/app.js` - data loading, rendering, language toggle, nav interactions
- `content/cv.en.json` - English structured content
- `content/cv.lt.json` - Lithuanian structured content
- `content/cv_extracted_raw.txt` - normalized extracted raw PDF text
- `scripts/extract_cv.py` - extraction and normalization pipeline
- `assets/cv/CV_A_Sosidko.pdf` - downloadable CV
- `assets/profile-placeholder.svg` - fallback portrait

## Local Setup
1. Activate env:
```powershell
conda activate cv_website
```
2. Ensure dependency:
```powershell
pip install pypdf
```
3. Regenerate content from PDF (optional):
```powershell
python scripts/extract_cv.py
```
4. Run local server:
```powershell
python -m http.server 8000
```
5. Open `http://localhost:8000`.

## Editing Content
- Update structured content directly in:
  - `content/cv.en.json`
  - `content/cv.lt.json`
- Keep both files aligned by section and key names.
- If source CV changes, replace `assets/cv/CV_A_Sosidko.pdf`, run `python scripts/extract_cv.py`, then review JSON output before commit.

## Deployment (GitHub Pages via Actions)
1. Push this repository to GitHub (workflow file: `.github/workflows/pages.yml`).
2. Open repository settings: `Settings -> Pages`.
3. In `Build and deployment`, set `Source` to `GitHub Actions`.
4. Push to `master` (or run the workflow manually from `Actions` tab).
5. After deploy finishes, open the Pages URL shown in `Settings -> Pages`.

Expected URL format:
- Project site: `https://<username>.github.io/<repo>/`
- User site (`<username>.github.io` repo): `https://<username>.github.io/`

## QA Checklist
- Language toggle switches EN/LT content.
- Nav anchors scroll to expected sections.
- Active nav item updates while scrolling.
- CV download button works.
- Layout is readable on mobile and desktop.
- Focus states are visible with keyboard navigation.

## Notes
- Missing data points are intentionally marked as `TODO` in content where extraction could not infer details.
- Contact policy in v1 is email + LinkedIn only.
