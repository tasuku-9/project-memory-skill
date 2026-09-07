# Figures Log

Last updated: {{DATE}}

This file tracks every visual asset, figure, and table used in this project. It records where the asset is saved, where it came from, how it was generated or transformed, and where it appears (or is intended to appear).

## How to use this file

Each entry links a visual output to its asset, original source, data source, generation method, and purpose. Traceability supports retrieval and reproduction; it does not guarantee either when files or methods are missing.

## Asset storage rule

Save durable copies of user-provided images, photos, screenshots, generated images, figures, diagrams, and other visual assets under `figures/` by default, unless the project has chosen another asset directory in `CONTEXT_MANIFEST.md`.

Use stable filenames based on the figure ID, for example:

- `figures/FIG-001.png`
- `figures/FIG-001-source.png`
- `figures/FIG-001-final.svg`
- `figures/inbox/IMG-{{DATE}}-001.png`

Copy original bytes only when the host exposes them. Verify that each saved file exists and is non-empty before setting Storage to `saved`. List project-root-relative paths, one backticked path or Markdown link per line under Asset path(s). Do not overwrite a different original with the same filename.

If original bytes cannot be retrieved, set Storage to `unavailable`, leave saved paths empty, and explain the reason in Notes. Use `pending` for an unfinished save; never present a proposed path or a recreation as the saved original.

Accessible transient bytes may be copied immediately to avoid loss. Use `figures/inbox/` for assets that are not yet formal figures. Canonical entries and interpretation follow Conversation capture in `DOCS_GUIDE.md`; do not interrupt ongoing discussion with holding-status reports.

Preserve the original supplied image when a processed, cropped, annotated, or regenerated version is created. Record both the original path and the derived/final path.

## Figures

### FIG-001

<!-- Copy this block for each figure -->

**Title**: 
**Type**: chart / diagram / photo / screenshot / schematic
**Status**: draft / final / superseded by FIG-xxx
**Storage**: pending / saved / unavailable

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
