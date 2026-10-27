#!/usr/bin/env python3
"""Self-contained script for the Video-Index figure (frozen vs fine-tuned Molmo2-4B), for sharing.

Everything needed is in this file: the numbers, labels, colors and style. No result files, no project code.
Requires: numpy, matplotlib, seaborn.

  python fig_video_index_shared.py [--out-dir DIR]
Writes DIR/pdf/video_index_native.pdf (vector) and DIR/jpg/video_index_native.jpg (600 dpi); DIR defaults to
./figures next to this script.

Data: Video-Index (840 multiple-choice items), the official lmms-eval `video_index` task (each model's own frame
sampling, "model-native"), official scorer. Every item scores 0 or 1, so each split is stored as
(label, number of items, items correct for frozen Molmo2-4B, items correct for the fine-tuned Molmo2-4B) and the
plotted accuracy is 100 * correct / n. Fine-tuned model: cka_temporal exp38 T4 LoRA (all 0-34 attn+MLP) anneal run,
checkpoint-108. Duration buckets: <= 60 s, 60-600 s, > 600 s.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

CAPABILITY_GROUPS = [  # (label, n, frozen correct, fine-tuned correct)
    ("Overall", 840, 177, 210),
    ("Perception", 210, 44, 48),
    ("Temporal", 210, 37, 54),
    ("Spatial\n& physical", 210, 50, 56),
    ("Reasoning\n& knowledge", 210, 46, 52),
]
VIDEO_DURATIONS = [
    ("≤ 1 min", 442, 128, 155),
    ("1–10 min", 246, 26, 31),
    ("> 10 min", 152, 23, 24),
]

FROZEN_LABEL, FINETUNED_LABEL = "Frozen Molmo2-4B", "Fine-tuned Molmo2-4B"
XLABEL_LEFT, XLABEL_RIGHT = "(a) Capability group", "(b) Video duration"
YLABEL = "Accuracy (%) ↑"  # the arrow marks the metric's direction: higher is better

# Frozen = hatched muted red, fine-tuned = solid slate blue. The pair passes palette checks on white (lightness,
# chroma, colorblind separation, contrast >= 3:1); the hatch keeps the two apart without color (grayscale print).
FROZEN, FROZEN_HATCH, FINETUNED = "#CB6567", "//", "#4774AE"
EDGE, INK, INK_MUTED, SPINE, GRID = "#2f2f2f", "#2b2b2b", "#555555", "#555555", "#e9e9e9"


def apply_style() -> None:
    sns.set_theme(style="whitegrid", context="paper", font="DejaVu Sans")
    plt.rcParams.update({
        "axes.edgecolor": SPINE, "axes.linewidth": 0.8, "axes.labelcolor": INK, "axes.labelsize": 10,
        "axes.titlesize": 10, "xtick.color": INK, "ytick.color": INK_MUTED, "xtick.labelsize": 9,
        "ytick.labelsize": 9, "grid.color": GRID, "grid.linewidth": 0.7, "hatch.color": EDGE, "hatch.linewidth": 0.6,
        "legend.fontsize": 9, "legend.frameon": True, "legend.edgecolor": "#bdbdbd", "legend.fancybox": True,
        "legend.framealpha": 1.0, "pdf.fonttype": 42, "ps.fonttype": 42, "savefig.bbox": "tight",
        "savefig.pad_inches": 0.03,
    })


def accuracies(rows: list) -> list:
    return [(label, n, 100 * frozen / n, 100 * finetuned / n) for label, n, frozen, finetuned in rows]


def grouped_bars(ax: plt.Axes, rows: list, xlabel: str, divider_after: int = -1) -> list:
    x = np.arange(len(rows))
    w = 0.38
    bars = [ax.bar(x - w / 2, [r[2] for r in rows], w, color=FROZEN, edgecolor=EDGE, linewidth=0.8,
                   hatch=FROZEN_HATCH, label=FROZEN_LABEL),
            ax.bar(x + w / 2, [r[3] for r in rows], w, color=FINETUNED, edgecolor=EDGE, linewidth=0.8,
                   label=FINETUNED_LABEL)]
    for c in bars:
        ax.bar_label(c, labels=[f"{b.get_height():.1f}" for b in c], padding=1.5, fontsize=7.5, color=INK)
    ax.set_xticks(x, [f"{r[0]}\n(n={r[1]})" for r in rows], fontsize=8.5)
    if divider_after >= 0:
        ax.axvline(divider_after + 0.5, color="#bdbdbd", lw=0.8, ls=(0, (3, 2)), zorder=0)
    ax.set_xlabel(xlabel, labelpad=6)
    ax.set_ylabel(YLABEL)
    sns.despine(ax=ax)
    ax.grid(axis="x", visible=False)
    ax.tick_params(axis="x", length=0)
    ax.tick_params(axis="y", length=3, width=0.8, color=SPINE)
    ax.set_axisbelow(True)
    return bars


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out-dir", type=Path, default=Path(__file__).resolve().parent / "figures")
    args = ap.parse_args()
    groups, durations = accuracies(CAPABILITY_GROUPS), accuracies(VIDEO_DURATIONS)

    apply_style()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.8, 3.0), sharey=True,
                                   gridspec_kw={"width_ratios": [len(groups) + 0.6, len(durations)]})
    handles = grouped_bars(ax1, groups, XLABEL_LEFT, divider_after=0)
    grouped_bars(ax2, durations, XLABEL_RIGHT)
    ax2.tick_params(axis="y", labelleft=True)
    top = max(max(r[2], r[3]) for r in groups + durations)
    ax1.set_ylim(0, np.ceil((top + 4) / 5) * 5)
    fig.tight_layout(rect=(0, 0.075, 1, 1), w_pad=2.0)
    fig.legend(handles=handles, loc="lower center", ncol=2, bbox_to_anchor=(0.5, -0.005), handlelength=2.4,
               handleheight=1.1, columnspacing=2.0, borderpad=0.5)
    fig.align_xlabels([ax1, ax2])

    for sub in ("pdf", "jpg"):
        (args.out_dir / sub).mkdir(parents=True, exist_ok=True)
    fig.savefig(args.out_dir / "pdf" / "video_index_native.pdf")
    # quality 100 and no chroma subsampling: JPEG's defaults smear text and thin hatch lines
    fig.savefig(args.out_dir / "jpg" / "video_index_native.jpg", dpi=600,
                pil_kwargs={"quality": 100, "subsampling": 0, "optimize": True})
    print("wrote", args.out_dir / "pdf" / "video_index_native.pdf", "and", args.out_dir / "jpg" / "video_index_native.jpg")


if __name__ == "__main__":
    main()
