# D23 Pin Catalog

A mobile-first interactive pin catalog web app for Disney D23 2026 pin releases across three stores: Mickey's of Glendale (MOG), The Walt Disney Company Store (TWDC), and Disney Studio Store Hollywood (DSSH).

## Quick Start

### Prerequisites

```bash
pip install pdfplumber pymupdf
```

### Generate the catalog data

```bash
python extract.py --catalogs ./catalogs/ --output ./pins.json
```

This builds `pins.json` from the known catalog data. All pin images currently point to a placeholder — drop real images into `images/<pin-id>.png` to replace them.

### Run the web app

The app uses `fetch()` to load `pins.json`, so it needs to be served (not opened as `file://`):

```bash
python -m http.server 8000
```

Then open [http://localhost:8000](http://localhost:8000) in your browser.

## Project Structure

```
├── catalogs/           # Source PDFs
│   ├── mog/mog.pdf
│   ├── twdc/twdc_fri.pdf, twdc_sat.pdf, twdc_sun.pdf
│   └── dssh/dssh.pdf
├── images/             # Pin images (placeholder for now)
├── extract.py          # Builds pins.json from catalog data
├── pins.json           # Generated catalog (91 sets, 533 pins)
├── index.html          # The web app (single file, no build step)
└── README.md
```

## Features

- **Catalog view** — browse all pins, filter by store and drop date
- **ISO List** — save pins to your "In Search Of" list with quantities and running total
- **Search** — find pins by name, set, or character
- **Export** — copy your ISO list as formatted text for Discord/Threads
- **Offline** — once loaded, works with no network connection
- **Mobile-first** — designed for 390px+ viewports, bottom tab navigation

## Adding Images

To add real pin images, name them using the pin's `id` field from `pins.json`:

```
images/mog-alice-75th-2.png      # Alice from the 75th Anniversary set
images/dssh-duos-anna--elsa.png  # Anna & Elsa from DSSH Duos
```

The app uses `loading="lazy"` so images load as you scroll.
