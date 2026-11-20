# Bits and Bots — curriculum

**Code real things. Start with blocks, finish with Python.**

Source-controlled teaching materials for the "Bits and Bots" coding club. The materials themselves are adapted from the [Micro:bit Educational Foundation](https://microbit.org) and formatted into lesson plans, handouts, and presentations.

## Getting started

Prerequisites: 
- Python 3
- Pandoc (3.x recommended) 
- a TeX distribution with XeLaTeX
- [Space Grotesk](https://floriankarsten.github.io/space-grotesk/) typeface 
- Node.js 22+
- npm

_For reproducible builds use the pinned versions in `package.json` and `.github/workflows/build.yml` (the system Pandoc/TeX versions are not fully pinned locally)._

```sh
npm install --no-audit --no-fund
make all
```

Outputs go to `build/`. `make pdf`, `make slides`, `make html-slides`, `make clean`, `make check` are also available. `make pdf` requires `xelatex`; `make slides` requires a Chromium-compatible browser available to [Marp](https://marp.app).

## Layout

- `sessions/`: session stubs.
- `config/`: Pandoc defaults and common metadata.
- `themes/`: Marp CSS and brand assets.
- `templates/`: reusable Markdown authoring templates.
- `scripts/`: build/check scripts.
- `shared/`: equipment, attribution and safeguarding-adjacent teaching checklists.

## Authoring conventions

Use UTF-8 Markdown, relative links and images, descriptive filenames, and YAML front matter. Put assets next to the session using them. Keep slides brief; use activity sheets for detailed instructions. Do not store children's names, photos, work, or other personal data in this public-ready repo.

## Copyright, licensing and branding

### Educational materials

Unless otherwise stated, the original educational materials published by Bits and Bots, including lesson plans, activity sheets, challenge cards and presentations, are licensed under the [Creative Commons Attribution-ShareAlike 4.0 International licence (CC BY-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/).

You are welcome to copy, share, adapt and redistribute these materials, including for commercial purposes, provided you:

- Give appropriate credit to Bits and Bots and any other credited contributors.
- Link to the applicable licence and indicate whether changes were made.
- Distribute adaptations under CC BY-SA 4.0 or another licence permitted by its ShareAlike terms.
- Do not suggest that Bits and Bots endorses or is affiliated with your activities without permission.

### Bits and Bots branding

The **Bits and Bots** name, robot logo and other identifying brand artwork are excluded from the Creative Commons licence. All rights in these branding elements are reserved by their respective rights holders.

You may refer to Bits and Bots when providing appropriate attribution or accurately identifying the source of materials.

However, permission is not granted to use the Bits and Bots name or logo to brand another club, course, organisation, product or service, or to suggest official affiliation, sponsorship or endorsement.

Requests for permission to use the branding can be made through [bitsandbots.codes](https://bitsandbots.codes).

### Third-party materials

Some educational resources incorporate or adapt materials from the Micro:bit Educational Foundation. Their copyright notices, attribution requirements and applicable licences remain in effect.

Where third-party material is used, its source and any modifications will be identified where reasonably practicable.
