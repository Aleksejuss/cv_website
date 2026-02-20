# AGENTS.md

## Purpose
This repository hosts an English-only static CV website. Agents should preserve content quality, accessibility, and deployment simplicity.

## Architecture
- `index.html` contains all sections and semantic structure.
- `scripts/app.js` owns runtime behavior:
  - English content loading
  - section rendering
  - reveal animations
  - active navigation state
- `styles/main.css` defines visual tokens and responsive layout.
- `content/cv.en.json` is the source of rendered profile data.

## Agent Rules
- Keep the site static (no backend/framework unless explicitly requested).
- Keep content changes in `content/cv.en.json` consistent with the rendered section schema.
- Keep accessibility intact:
  - semantic headings/landmarks
  - keyboard-focus visibility
  - reduced-motion support
- Keep contact visibility policy to email + LinkedIn unless the user asks otherwise.
- Do not remove `assets/cv/CV_A_Sosidko.pdf` download path.

## Content Update Workflow
1. Replace PDF at `assets/cv/CV_A_Sosidko.pdf` (if needed).
2. Run `python scripts/extract_cv.py` in `cv_website` env.
3. Manually review and refine `content/cv.en.json`.
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
- Manually verify nav tracking and CV download link.
- Confirm responsive behavior around mobile and desktop breakpoints.
