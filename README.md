# Strong Post-Training from Permissive Pretraining — NeurIPS 2026 poster

Poster (140 × 90 cm, landscape) for the NeurIPS 2026 main conference.

- **`poster.pdf`** — print-ready PDF (1400 × 900 mm, one page).
- **`index.html`** — editable source: a single-file React poster. Open it in a browser
  (it loads React/Babel from unpkg, so it needs internet). Text is editable in the file;
  column widths, card heights and font scale can be dragged in the page.
  If the layout looks stale after pulling changes, click **Reset** (settings are cached in localStorage).
- **`poster-config.json`** — saved layout (column widths, card heights, font scale).
- **`stages.png`, `corpora_math500.png`, `pipeline.png`** — figures; `logos/` — affiliation logos.
- **`scripts/`** — matplotlib scripts that regenerate the figures
  (`python scripts/stages.py <outdir>` writes `draft_stages_multiples.png` → rename to `stages.png`;
  `python scripts/charts.py <outdir>` writes `corpora_math500.png`).

To re-export the PDF, use the browser's Print → Save as PDF with paper size 1400 × 900 mm and no margins.

Code, evals & checkpoints: https://github.com/MixtureVitae/permissive-post-train
