# Paper figure instructions

The conventions every figure in `PLOT_CODE/` follows. They were collected while making the Video-Index figure; apply
them to every new figure so the paper's figures look like one set.

## Folders and formats

- Code lives in `PLOT_CODE/code/`, figures in `PLOT_CODE/figures/pdf/` and `PLOT_CODE/figures/jpg/`.
- Every figure is saved as both **PDF** and **JPEG**.
  - **The PDF is the one uploaded to Overleaf.** It is vector (fonts embedded as TrueType), so text and lines stay
    sharp at any zoom and in print. It is the clearer format for the paper.
  - The JPEG is for slides, previews and sharing: 600 dpi, quality 100, no chroma subsampling. JPEG's default
    subsampling and lower quality make text and thin hatch lines look blurry.
- Each figure has a self-contained `<figure>_shared.py` next to its normal script, with every number, label, color
  and style setting written into the file. Someone else can regenerate the figure from that one file
  (requirements: numpy, matplotlib, seaborn). Check that it reproduces the normal script's output exactly; for
  `fig_video_index_shared.py` the JPEG is pixel-identical.

## Look

- Seaborn white-grid style: clean and minimal ("Notion-like"), a light horizontal grid only, left and bottom axis
  lines only, no top/right frame.
- Colors: the first request was pastel colors. The current palette uses soft, muted tones with dark bar outlines.
  - **Baseline (frozen model): red with diagonal-line shading** (`#CB6567`, `//` hatch).
  - **Fine-tuned model: solid blue, no shading** (`#4774AE`).
  - The baseline and fine-tuned bars are told apart by **both color and shading**: diagonal lines vs. solid fill.
    The pair was checked for colorblind separation and contrast on white, and the shading keeps them apart in
    grayscale print, so the reader never has to rely on color alone.
- Font: DejaVu Sans. Nothing bold: tick labels such as "Overall" use the same weight as the rest.

## Layout and labels

- **No subplot titles.** Each panel is named in its x-axis label with a letter: "(a) Capability group",
  "(b) Video duration". The x-axis labels of side-by-side panels are **aligned on the same line**.
- **Axes are always clearly labeled**, x and y on every panel.
- **The y-label carries the metric's direction:** "Accuracy (%) ↑" for higher-is-better, "↓" for lower-is-better
  (e.g. error, loss). The arrow is part of the label text and rotates with it.
- **The number on top of every bar**: its value with one decimal (e.g. 25.0), small, centered just above the bar,
  never overlapping a neighbor or the legend. Leave enough y headroom for them.
- Tick labels include the item count, e.g. "Temporal (n=210)". Long names break before "&" so neighboring labels
  don't collide.
- An "Overall" bar comes first and is separated from the breakdown by a thin dashed divider.
- **One legend for the whole figure, centered below all panels, in a box, on one row.** Entries are named in
  full: "Frozen Molmo2-4B", "Fine-tuned Molmo2-4B".

## Checklist before a figure goes in the paper

1. Render it and look at it: no label collisions, no cut-off text, legend clear of the bars and labels.
2. The numbers match the source (here: Video-Index model-native, overall 21.1 → 25.0).
3. PDF and JPEG are both regenerated, and the `_shared.py` version still reproduces them.
4. Upload the **PDF** to Overleaf.
