# Figures Log

Last updated: {{DATE}}

This file tracks every visual asset, figure, and table used in this project. It records where the asset is saved, where it came from, how it was generated or transformed, and where it appears (or is intended to appear).

## How to use this file

Each entry links a visual output to its saved asset, original source, data source, generation method, and purpose. This ensures any image, figure, or table can be found, reproduced, updated, or explained during peer review.

## Asset storage rule

Save durable copies of user-provided images, photos, screenshots, generated images, figures, diagrams, and other visual assets under `figures/` by default, unless the project has chosen another asset directory in `CONTEXT_MANIFEST.md`.

Use stable filenames based on the figure ID, for example:

- `figures/FIG-001.png`
- `figures/FIG-001-source.png`
- `figures/FIG-001-final.svg`
- `figures/inbox/IMG-{{DATE}}-001.png`

If the user provides a visual asset during chat, save the original durable copy before relying on it. If it is not yet clear whether the asset will become a formal figure, save it under `figures/inbox/` and record a provisional entry. When it becomes a formal figure, link or rename it to a stable `FIG-xxx` asset path.

Preserve the original supplied image when a processed, cropped, annotated, or regenerated version is created. Record both the original path and the derived/final path.

## Figures

### FIG-001

<!-- Copy this block for each figure -->

**Title**: 
**Type**: chart / diagram / photo / screenshot / schematic
**Status**: draft / final / superseded by FIG-xxx

**Asset path(s)**:
<!-- Saved visual path(s), usually figures/FIG-xxx.ext and/or figures/FIG-xxx-source.ext -->

**Original source**:
<!-- User-provided image, generated preview, screenshot, camera photo, external file path, or script output -->

**Received / created**:
<!-- Date and brief provenance, e.g. supplied by user in chat on YYYY-MM-DD -->

**Data source**: 
<!-- File path, query, or experiment reference (RES-xxx) -->

**Generation method**: 
<!-- Script path, tool, or manual steps to reproduce -->

**Key observation**: 
<!-- What does this figure show? One sentence. -->

**Intended use**: 
<!-- Where will this appear? Paper section, presentation slide, report chapter. -->

**Notes**: 
<!-- Known limitations, caveats, or planned improvements. -->

## Tables

### TBL-001

<!-- Copy this block for each table -->

**Title**: 
**Status**: draft / final / superseded by TBL-xxx

**Data source**: 

**Generation method**: 

**Key observation**: 

**Intended use**: 

**Notes**: 

## Figure index

| ID | Title | Status | Asset path | Original source | Intended section | Data source |
| --- | --- | --- | --- | --- | --- | --- |
| FIG-001 |  |  |  |  |  |  |
| TBL-001 |  |  |  |  |  |  |

## Reproduction checklist

Before submission, verify each figure and table:

- [ ] Data source is accessible and documented
- [ ] Visual asset path exists and uses a stable figure ID
- [ ] Original supplied image is preserved when relevant
- [ ] Generation method is reproducible (script or clear steps)
- [ ] Caption accurately describes content
- [ ] Axes, labels, and units are correct
- [ ] No superseded versions remain in the manuscript
