# AGENTS.md

## Purpose
This repository hosts a bilingual static CV website. Agents should preserve content quality, accessibility, and deployment simplicity.

## Architecture
- `index.html` contains all sections and semantic structure.
- `scripts/app.js` owns runtime behavior:
  - EN/LT content loading
  - language toggle + persistence
  - section rendering
  - reveal animations
  - active navigation state
- `styles/main.css` defines visual tokens and responsive layout.
- `content/*.json` is the source of rendered profile data.

## Agent Rules
- Keep the site static (no backend/framework unless explicitly requested).
- Preserve bilingual parity: any schema/content changes must be mirrored in both `cv.en.json` and `cv.lt.json`.
- Keep accessibility intact:
  - semantic headings/landmarks
  - keyboard-focus visibility
  - reduced-motion support
- Keep contact visibility policy to email + LinkedIn unless the user asks otherwise.
- Do not remove `assets/cv/CV_A_Sosidko.pdf` download path.

## Content Update Workflow
1. Replace PDF at `assets/cv/CV_A_Sosidko.pdf` (if needed).
2. Run `python scripts/extract_cv.py` in `cv_website` env.
3. Manually review and refine both JSON files.
4. Validate website behavior locally via `python -m http.server 8000`.
5. Commit with clear milestone-style commit messages.

## Commit Conventions
Use intent-focused commits, for example:
- `feat: ...` for UI/content capabilities
- `fix: ...` for regressions and polish
- `docs: ...` for documentation only
- `chore: ...` for scaffolding/tooling

## Validation Before Finalizing Changes
- `node --check scripts/app.js`
- Manually verify language toggle, nav tracking, and CV download link.
- Confirm responsive behavior around mobile and desktop breakpoints.
