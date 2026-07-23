# D23 Pin Catalog — Kiro Project Spec

## Project Overview

Build a **mobile-first interactive pin catalog web app** for Disney D23 pin releases across three stores: Mickey's of Glendale (MOG), The Walt Disney Company Store (TWDC Store), and the Disney Studio Store Hollywood (DSSH). The app lets a collector browse upcoming drops by store and date, view pin images and full metadata, and maintain a personal **ISO list** (In Search Of) with a running total cost.

The deliverable is two things:
1. A **Python extraction script** that parses catalog PDFs (one per store) and outputs a structured `pins.json` data file with base64-encoded images.
2. A **single-file static web app** (`index.html`) that loads `pins.json` and runs entirely in the browser — no backend, no build step, deployable to GitHub Pages or any static host.

---

## Input: Catalog PDFs

PDFs are placed in a `/catalogs/` directory. Each store uses a different number of PDFs and a different internal layout:

```
/catalogs/
  mog/mog.pdf           # Single PDF, Fri+Sat+Sun (35 pages)
  twdc/twdc_fri.pdf     # Friday August 14 only
  twdc/twdc_sat.pdf     # Saturday August 15 only
  twdc/twdc_sun.pdf     # Sunday August 16 only
  dssh/dssh.pdf         # Single PDF, Fri+Sat+Sun
```

**Store + date detection — infer from PDF content, not filenames:**
- MOG: page header = `MICKEY'S OF GLENDALE PIN STORE | FRIDAY, AUGUST 14`
- TWDC: cover page = `FRIDAY, AUGUST 14, 2026`; body pages = `FRIDAY PIN PRODUCT CATALOG`
- DSSH: body pages = `RELEASING FRIDAY AUGUST 14`

**Per-store layout differences — critical for parser design:**

*MOG:* Catalog numbers as bold numerals. Labels on left: `FEATURES:`, `DIMENSIONS:`, `RETAIL:`, `EDITION SIZE:`. Pin names below images. Light lavender background.

*TWDC:* No catalog numbers. Set header = `EDITION: LE400  RETAIL: $42.95` (combined). Purchase limit in orange italic. Pin dimensions listed as `[Name] DIMS: 3"x2.5"` in a block at page bottom. Framed Pin Sets use a distinct layout: large `FRAMED PIN SET` header + stacked `EDITION: LE3 / RETAIL: $X / DIMS: WxH` + set name as caption below photo. Warm brick-texture background.

*DSSH:* Dark navy background. Per-page header = `RELEASING FRIDAY AUGUST 14`. Metadata on a single pipe-delimited line per set: `$29.95 | LE 400 | 1.69"W X 2.25"H | 3D LASER PRINT & CUSTOM BACKING CARD`. No separate `FEATURES:` label — finish details are in the metadata line. Pin name + dims below each image. Purchase limit at top of each page. Gold decorative border.

---

## Phase 1: PDF Extraction Script (`extract.py`)

### Goal
Parse each catalog PDF and output a single `pins.json` file containing all pins across all three stores.

### Requirements

**Text extraction:**
Use `pdfplumber` for layout-aware text parsing. For each page, extract:
- Store name (from the header, e.g. `MICKEY'S OF GLENDALE PIN STORE`)
- Drop date (from the header, e.g. `FRIDAY, AUGUST 14`)
- Set name (bold/large text at top of each section)
- Set description (body text below set name)
- Features (after `FEATURES:` label)
- Dimensions (after `DIMENSIONS:` label)
- Retail price (after `RETAIL:` label — capture the dollar amount)
- Edition size (after `EDITION SIZE:` or `EDITION:` label)
- Purchase limits (e.g. "Limit six (6) boxes per guest")
- Individual pin numbers and names (numeric catalog number + character/title name)
- Whether it's a mystery set, box set, or individual pin (infer from "Mystery boxes contain", "Box Set", etc.)

**Image extraction:**
Use `PyMuPDF (fitz)` to extract embedded raster images from each page. Match each image to its nearest pin by spatial proximity (compare image bounding box Y-coordinate to pin number Y-coordinate on the same page). Save each image as a PNG file in an `/images/` directory, named by pin ID (e.g. `images/mog-alice-75th-2.png`). Reference the relative path in `pins.json` via the `image_path` field.

Filter out decorative/background images by minimum size threshold: ignore any extracted image smaller than 80×80px.

**Output format — `pins.json`:**
```json
{
  "generated_at": "ISO-8601 timestamp",
  "stores": ["MOG", "TWDC", "DSSH"],
  "sets": [
    {
      "id": "mog-alice-75th",
      "store": "MOG",
      "drop_date": "2026-08-14",
      "drop_day_label": "Friday, August 14",
      "set_name": "Alice in Wonderland 75th Anniversary",
      "set_description": "Celebrate the 75th Anniversary of Alice in Wonderland with this comic-inspired pin series...",
      "set_type": "individual",
      "features": "Hard Enamel, Translucent Fills, Marbleized Fill, Laser Print",
      "dimensions": "3.25″–4.15″H",
      "retail_price": 52.95,
      "retail_display": "$52.95",
      "retail_note": null,
      "purchase_limit": null,
      "ship_only": false,
      "available_dates": ["2026-08-14"],
      "pins": [
        {
          "id": "mog-alice-75th-2",
          "catalog_number": 2,
          "name": "Alice",
          "edition_size": 400,
          "edition_notes": null,
          "image_path": "images/mog-alice-75th-2.png"
        },
        {
          "id": "mog-alice-75th-3",
          "catalog_number": 3,
          "name": "Queen of Hearts",
          "edition_size": 400,
          "edition_notes": null,
          "image_path": "images/mog-alice-75th-3.png"
        }
      ]
    }
  ]
}
```

**Set type values:**
- `"individual"` — buy one pin at a time, known contents
- `"mystery"` — blind box, randomly selected contents. Each possible pull gets its own entry in the `pins` array (with name, image, and per-pin edition size) so collectors can ISO specific pulls.
- `"box_set"` — predetermined group sold together
- `"ultra_jumbo"` — large-format single piece (MOG only)
- `"framed_set"` — framed multi-pin display, always LE3, TWDC only; price in the thousands

**Additional set-level fields:**
- `ship_only` (boolean, default `false`) — `true` for sets that cannot be picked up in person (e.g. TWDC "Color Shades of Magic"). When `true`, the web app displays a shipping-only notice.
- `available_dates` (array of ISO-8601 date strings) — lists all drop dates a set is available on. Most sets have a single date. Sets that appear on multiple days (e.g. Walt Disney Imagineering Pin Boards) list all dates here.

**Edge cases to handle:**
- Mystery sets where the edition size varies by rarity tier (e.g. `400 (8 pins), 300 (5 chaser pins)`) — each pull gets its own pin entry with its specific `edition_size` (e.g. a chaser pin has `edition_size: 300`). Use `edition_notes` on the pin to label the tier (e.g. `"chaser"`)
- Sets that span multiple PDF pages (same set name repeats with only the features header, no new description) — merge all pins under one set object
- Box sets priced as a unit — set `retail_note: "per box"` or `"for set of 6"` as appropriate
- The World Princess Week Ultra Jumbo ($1,200, LE 150) should be `set_type: "ultra_jumbo"`
- Pin boards (items 119–120) appear on multiple drop days but are the same product — deduplicate by catalog number and populate `available_dates` with all dates the item appears on. Use the first occurrence's drop date as `drop_date`.
- `catalog_number` is nullable — TWDC and DSSH pins have no catalog numbers and should use `null`
- DSSH Throwback Mystery Series has per-pin LE tiers (LE400 / LE300 / LE150). Each pull's pin entry gets its own `edition_size` matching its tier, with `edition_notes` indicating the tier label (e.g. `"chaser"`, `"super chaser"`)

**CLI usage:**
```bash
python extract.py --catalogs ./catalogs/ --output ./pins.json
```
Print a summary table on completion: store, date, sets parsed, pins parsed, images extracted.

---

## Phase 2: Web App (`index.html`)

### Design Direction

**Reference:** Mirror the visual design language of the official Disneyland app (see provided screenshots). The app should feel native to the Disney mobile ecosystem — a guest picking this up should feel right at home.

**Color tokens:**
```css
--color-bg:           #EDF2F8;   /* light blue-gray page background */
--color-surface:      #FFFFFF;   /* white cards */
--color-navy:         #00264C;   /* primary Disney navy — headers, active pills, primary buttons */
--color-navy-light:   #1A3A5C;   /* hover/pressed state */
--color-accent:       #0063D3;   /* interactive blue — links, secondary buttons */
--color-green:        #2D7A47;   /* confirmed/available badge */
--color-gold:         #F5A800;   /* LE badge, ultra-jumbo highlight only */
--color-text-primary: #0A1929;   /* near-black body text */
--color-text-secondary: #5A6A7A; /* metadata, captions */
--color-border:       #D8E3EE;   /* subtle card borders */
--color-hero-gradient-start: #B8D4EF; /* light blue gradient top */
--color-hero-gradient-end:   #EDF2F8; /* fades into page bg */
```

**Typography:**
Load `Plus Jakarta Sans` from Google Fonts (weights 400, 600, 700). This closely matches the rounded, friendly sans-serif used in the Disneyland app. No condensed display font — all type is set in Plus Jakarta Sans with weight doing the hierarchy work.
- Page title / set name: `700`, 20–22px
- Section headers: `700`, 17–18px
- Body / metadata: `400`, 14–15px
- Badges / chips: `600`, 12px, all-caps letter-spacing `0.04em`

**Component patterns (match the Disneyland app exactly):**

*Page background:* `--color-bg` (#EDF2F8) throughout — never pure white or dark.

*Cards:* White (#FFF) background, `border-radius: 16px`, `box-shadow: 0 2px 12px rgba(0,38,76,0.08)`, `border: 1px solid var(--color-border)`. Generous internal padding (16px).

*Filter pills (store + date selectors):* Stadium/pill shape (`border-radius: 999px`). **Selected state:** `background: var(--color-navy)`, white text, no border. **Unselected state:** white background, `border: 1.5px solid var(--color-navy)`, navy text. Match the exact pill shape from the "Sat, Jul 25 / Sat, Aug 1 / Sat, Sep 12" row in screenshot 1.

*Status badges:* Rounded pill, small. Use the "Booked • Park Reservation" green badge from screenshot 1 as the pattern for set-type badges:
- `INDIVIDUAL` → navy fill
- `MYSTERY BOX` → amber/gold fill, dark text
- `BOX SET` → teal fill (`#0097A7`)
- `ULTRA JUMBO` → gold fill (`--color-gold`), dark text

*Primary buttons:* `background: var(--color-navy)`, white text, `border-radius: 999px` (full pill), `padding: 14px 28px`, `font-weight: 700`. Match the "+ Add Plans" button from screenshot 1.

*Secondary buttons:* White background, `border: 1.5px solid var(--color-navy)`, navy text, same pill shape. Match the "Today's Showtimes" button from screenshot 3.

*Hero/header zone:* A light blue gradient banner at the top of the Catalog view (`linear-gradient(180deg, var(--color-hero-gradient-start), var(--color-hero-gradient-end))`), containing the D23 logo/wordmark, store filter pills, and date chips. This mirrors the blue gradient header zone in screenshot 2.

*Bottom tab bar (mobile):* Fixed, white background, `border-top: 1px solid var(--color-border)`. Three icon-only tabs: Catalog (grid icon), ISO List (bookmark/star icon), Search (magnifying glass). Active tab icon in `--color-navy`, inactive in `--color-text-secondary`. Minimum tap target 56px tall. Mirror the bottom nav from all three screenshots exactly.

*Feature tags:* Small chips inside set cards for "Hard Enamel", "Glitter", etc. White background, navy border, navy text, `border-radius: 6px`, `font-size: 11px`. Not full pills — slightly squared to distinguish from filter pills.

*ISO total footer:* White background bar, `border-top: 1px solid var(--color-border)`, navy bold total on the right, item count in secondary text on the left. Matches the visual weight of the bottom nav.

**Mobile-first breakpoints:**
- Default (≤767px): single-column, full-width cards, bottom tab bar, touch targets min 44px
- `≥768px`: two-column pin grid within set cards, top nav replaces bottom tab bar
- `≥1200px`: three-column pin grid

**Motion:** Subtle only. Bottom sheet slides up with `transform: translateY` + `transition: 200ms ease-out`. No bounce, no elaborate animations. `@media (prefers-reduced-motion: reduce)` disables all transitions.

### App Structure

Three views, navigated via a persistent bottom tab bar on mobile / top nav on desktop:

1. **Catalog** (default view) — browse all pins
2. **ISO List** — your saved want list
3. **Search** — filter/search across all pins

---

### View 1: Catalog

**Top of page:** Store filter tabs (`MOG` | `TWDC` | `DSSH` | `All`). Below that: day filter chips (`Aug 14` | `Aug 15` | `Aug 16` | `All Dates`). Both filters compose (AND logic).

**Set cards:** Each set renders as a card containing:
- Set name (display font, gold accent)
- Drop date badge and store badge
- Set type badge (`MYSTERY BOX` / `BOX SET` / `INDIVIDUAL` / `ULTRA JUMBO`) — color-coded
- Retail price (prominent) + edition size
- Feature tags (small chips: "Hard Enamel", "Glitter", etc. — parsed from the features string)
- A horizontal scroll rail of pin thumbnails (the extracted images). Tapping a thumbnail opens the pin detail sheet.
- A "Add all to ISO" button that adds every individual pin in the set at once

**Pin detail sheet (bottom sheet on mobile, modal on desktop):**
When a pin thumbnail is tapped, slide up a sheet showing:
- Full-size pin image
- Pin name + catalog number
- Parent set name
- All set metadata (store, drop date, features, dimensions, retail, edition size, purchase limit)
- A large "Add to ISO List" button (or "Remove" if already added)
- If it's a mystery set: show a disclaimer "This is a mystery box pull — pin received is random. Price shown is per box."

---

### View 2: ISO List

**Header:** "My ISO List" + total item count badge

**Content:** A list of saved pins, grouped by store then by drop date. Each row shows:
- Pin thumbnail (small, 48px)
- Pin name
- Parent set name
- Drop date + store
- Price
- Quantity stepper (+ / −) — for mystery sets, the user may want to budget for multiple boxes
- Remove button (trash icon)

**Footer (sticky):** Running cost total across all ISO items. Format:
```
12 items across 3 sets  |  Est. Total: $487.40
```
If any items are mystery sets, add a footnote: `* Mystery box prices are per box. Actual pin received may vary.`

**Export button:** "Copy as Text" — generates a plain-text ISO list formatted for sharing in Discord or Threads:

```
📌 MY D23 ISO LIST — MOG Aug 14

□ Alice in Wonderland 75th — Alice (#2) — $52.95 LE400
□ Alice in Wonderland 75th — Queen of Hearts (#3) — $52.95 LE400
□ Disney Squad Goals — Lilo & Stitch (#32) — $69.95 LE400

💰 Est. Total: $175.85
```

**Persistence:** Save the ISO list to `localStorage` under key `d23_iso_list`. It should survive page refreshes.

---

### View 3: Search

A single search input with live filtering across all pin names, set names, and character names. Results render as a flat list of pin cards (image + name + set + price + add-to-ISO button). Show result count. If no results, show a friendly empty state: "No pins found for '[query]'" with a button to clear the search.

---

## Known Catalog Data (MOG — from PDF analysis)

Use this as ground truth for validating extraction accuracy. The script should produce output consistent with this.

### Drop: Friday, August 14 (MOG)

| # | Set | Type | Price | LE |
|---|-----|------|-------|----|
| 1 | Alice in Wonderland Mystery Set | mystery | $34.95/box | 400/style |
| 2–6 | Alice in Wonderland 75th Anniversary | individual | $52.95 | 400 |
| 7–19 | Disney Princess Dream Windows (10 pins: Snow White, Cinderella, Aurora, Ariel, Belle, Jasmine, Pocahontas, Mulan, Tiana, Rapunzel, Merida, Moana, Raya) | individual | $42.95 | 400 |
| 20 | DuckTales the Movie: Treasure of the Lost Lamp Mystery Set | mystery | $34.95/box | 400 regular / 300 chaser |
| 21–26 | Disney Treasure Seekers (Ariel, Scrooge McDuck, Jim Hopkins, Peter Pan, Abu, Penny) | individual | $34.95 | 400 |
| 27–36 | Disney Squad Goals (The Little Mermaid, Treasure Planet, Princess and the Frog, Big Hero 6, Raya, Lilo & Stitch, A Goofy Movie, Moana, Robin Hood, Snow White and the Seven Dwarfs) | individual | $69.95 | 400 |
| 37–46 | POV: Another Point of View (10 spinner pins: Moana/Te Kā, Belle/Beast, Snow White/Evil Queen, Ariel/Ursula, Aurora/Maleficent, Aladdin/Genie, Alice/Queen of Hearts, Cinderella/Prince Charming, Rapunzel/Flynn, Sorcerer Mickey/Yen Sid) | individual | $79.95 | 400 |
| 47–56 | Dining with Character (10 pins: Emperor's New Groove, Sleeping Beauty, Alice in Wonderland, Princess and the Frog, Winnie the Pooh, The Little Mermaid, Mickey and the Beanstalk, Lady and the Tramp, Beauty and the Beast, Ratatouille) | individual | $79.95 | 400 |
| 57 | World Princess Week Ultra Jumbo (16″W × 9″H) | ultra_jumbo | $1,200.00 | 150 |
| 119–120 | Walt Disney Imagineering Pin Boards | individual | $34.95 | — |

### Drop: Saturday, August 15 (MOG)

| # | Set | Type | Price | LE |
|---|-----|------|-------|----|
| 58 | S.E.A. Mystery Set (15 pins + trading cards, collect all for hidden image) | mystery | $39.95/box | 500/style |
| 59–65 | Around the World with Disney: Parks to Ports (Disneyland, Magic Kingdom, Tokyo Disneyland, Disneyland Paris, Hong Kong Disneyland, Shanghai Disneyland, Disney Cruise Line) | individual | $36.95 | 400 |
| 66–80 | Disney Park Stamps: Series 2 (15 pins: Ariel, Rosita, Teddi Barra, Hatbox Ghost, Albert, Scooter, Yeti, Chuuby, Tom Morrow 2.0, Dumbo, Winnie the Pooh, Sonny Eclipse, Lagoona Gator, The Dapper Dans, Jingles) | individual | $34.95 | 400 |
| 81–88 | Disney Attraction Panoramas — Gate-fold (Peter Pan's Flight, Jungle Cruise, Alice in Wonderland, Matterhorn Bobsleds, It's a Small World, Pirates of the Caribbean, Haunted Mansion, Big Thunder Mountain Railroad) | individual | $74.95 | 400 |
| 89 | Disney Royal Carousel Horses — Box set of 6 + display box | box_set | $324.95 | 250 |
| 119–120 | Walt Disney Imagineering Pin Boards | individual | $34.95 | — |

### Drop: Sunday, August 16 (MOG)

| # | Set | Type | Price | LE |
|---|-----|------|-------|----|
| 90 | The Avengers Mystery Set | mystery | $34.95/box | 400 regular / 300 chaser / 200 super chaser |
| 91 | Guardians of the Galaxy Box Set (with mystery pin under tray) | box_set | $74.95 | 400 |
| 92 | Kingdom Hearts Mystery Set | mystery | $34.95/box | 500 regular / 400 chaser / 300 super chaser |
| 93 | Pixar Soul Mystery Set | mystery | $34.95/box | 400 regular / 300 chaser / 200 super chaser |
| 94 | Pixar Soul Box Set | box_set | $49.95 | 400 |
| 95–104 | The Muppet Show 50th (10 pins: Kermit, Veterinarian's Hospital, At the Dance, Swedish Chef, Great Gonzo, Fozzie's Stand-Up, Pigs in Space, The Electric Mayhem, Muppet Labs, Statler and Waldorf) | individual | $54.95 | 400 |
| 105–117 | Portraits of Evil (13 pins: Evil Queen, Chernabog, Queen of Hearts, Maleficent, Cruella De Vil, Horned King, Ursula, Gaston, Jafar, Scar, Hades, Yzma, Mother Gothel) | individual | $44.95 | 400 |
| 118 | The Colorful World of Disney Mystery Set (23 color-changing pins, UV-reactive) | mystery | $34.95/box | 500/style |
| 119–120 | Walt Disney Imagineering Pin Boards | individual | $34.95 | — |

---

## Known Catalog Data (TWDC Store — from PDF analysis)

TWDC pins have no catalog numbers. Sets identified by name only. Individual pin names come from the dimension list at the bottom of each catalog page.

### Drop: Friday, August 14 (TWDC)

| Set | Type | Price | LE | Notes |
|-----|------|-------|----|-------|
| The Ultimate Disney Stamp (classic era: Yensid & Sorcerer Mickey, Blue Fairy & Jiminy, Dumbo & Timothy, Donald & Aracuan Bird, Alice & White Rabbit, Chip & Dale, Maleficent Dragon & Prince Phillip, Merlin & Archimedes, Robin Hood & Little John, Pooh & Piglet) | individual | $34.95 | 500 | Year stamp format 1940–1977 |
| The Ultimate Disney Stamp (renaissance: Todd & Copper, Dodger & Oliver, Ariel & Scuttle, Bernard & Bianca, Belle & Maurice, Hercules & Phil, Mulan & Mushu, Kronk & Yzma, Lilo & Stitch, Tiana & Charlotte) | individual | $34.95 | 500 | Year stamp format 1981–2009 |
| The Ultimate Disney Stamp (modern: Rapunzel & Pascal, Wreck-It Ralph & Vanellope, Anna & Olaf, Baymax & Hiro, Judy & Nick, Moana & Hei Hei, Elsa & Bruni, Raya & Tuk Tuk, Valentino & Star, Gazelle & Tiger) | individual | $34.95 | 500 | Year stamp format 2010–2025 |
| Reel of Magic (The Little Mermaid, Beauty and the Beast, Aladdin, The Lion King, Pocahontas, The Hunchback of Notre Dame, Mulan, Tarzan, Emperor's New Groove, Atlantis, Lilo & Stitch) | individual | $52.95 | 500 | Hinge pin; title becomes stand |
| Royal Chambers (Evil Queen, Prince Charming, Queen of Hearts, King Stefan & Queen Leah, King Arthur, Triton, Gaston, Sultan, Zeus, Emperor, Kuzco, King Magnifico, King Candy, Elsa) | individual | $45.95 | 400 | Throne scene pin-on-pin |
| Role Models (Rafiki & Simba, Jiminy & Pinocchio, Tala & Moana, Mei Mei & Ming, Merlin & Arthur, Grandmother Willow & Pocahontas, Phil & Hercules, Fairy Godmother & Cinderella, Timothy Mouse & Dumbo, Ancestor & Mulan, Auguste Gusteau & Remy, Hector & Miguel, Tadashi & Hiro, Carl & Russel) | individual | $45.95 | 400 | Pin-on-pin |
| Disney D's Mystery Pin Box (Mickey, Minnie, Goofy, Daisy, Pluto, Chip & Dale, Donald, blank D) | mystery | $32.95/box | 400 | 5 box limit, 2 pins/box |
| Disney Princess Mystery Pin Box (Ariel, Moana, Tiana, Belle, Rapunzel, Pocahontas, Jasmine, Cinderella) | mystery | $32.95/box | 400 | 5 box limit, 2 pins/box |
| Color Shades of Magic (Framed) | framed_set | $6,000 | 3 | 22.31"×30.50"; ship-only, no in-person pickup |
| The Songs We Grew Up With (Framed) | framed_set | $2,500 | 3 | 26"×26" |
| Friends From Around the World (Framed) | framed_set | $1,500 | 3 | 16.50"×12.25" |
| 35 Years of Mermaid Emotions (Framed) | framed_set | $1,000 | 3 | 21"×10.5" |
| Spirit of Family (Framed) | framed_set | $900 | 3 | 21"×10" |
| Pixar Animation Studios (Framed) | framed_set | $900 | 3 | 21"×9.5" |
| Encanto Tiles (Framed) | framed_set | $700 | 3 | 12.5"×12.5" |
| Villains (Framed) | framed_set | $500 | 3 | 12"×8.50" |
| The Ultimate Disney Fan Event 2024 (Framed) | framed_set | $400 | 3 | 14.75"×11" |

### Drop: Saturday, August 15 (TWDC)

| Set | Type | Price | LE | Notes |
|-----|------|-------|----|-------|
| The Ultimate Pixar Stamp — Series 1 (Buzz & Woody, Heimlich & Flik, Jessie & Bullseye, Sulley & Boo, Nemo & Crush, Mr Incredible & Frozone, Lightning McQueen & Mater, Linguini & Remy, WALL-E & EVE, Carl & Ellie) | individual | $34.95 | 500 | Year stamps 1995–2009 |
| The Ultimate Pixar Stamp — Series 2 (Gus the Cloud & Peck the Stork, Lotso & Mr Pricklepants, Young Boy & Papa, Queen Elinor & Merida, Mike & Squishy, Joy & Bing Bong, Arlo & Spot, Dory & Hank, Miguel & Dante, Edna Mode & Jack-Jack) | individual | $34.95 | 500 | Year stamps 2009–2018 |
| The Ultimate Pixar Stamp — Series 3 (Bonnie & Forky, Ian & Barley, Joe & 22, Luca & Alberto, Dug & Carl, Meilin & Ming, Ember & Wade, Paula & Xeni, Anxiety & Sadness, Elio & Glordon) | individual | $34.95 | 500 | Year stamps 2019–2025 |
| Game Changers (Ariel, Belle, Jasmine, Pocahontas, Esmeralda, Megara, Mulan, Tiana, Rapunzel, Merida, Moana, Anna, Elsa, Raya, Vanellope, Mirabel) | individual | $39.95 | 400 | Pin-on-pin, tall bookmark format |
| Welcome Home (Carl & Ellie's home, Mulan's family home, Geppetto's Workshop, Robinsons Family Lab, Snow White's Cottage, Belle's Cottage, Lilo's home, The Incredible's home, Tinkerbell's home, White Rabbit's home, Winnie the Pooh's home, Casa Madrigal, Roger & Annita's home, Lady & Tramp's home) | individual | $42.95 | 400 | Pin-on-pin, home/building scenes |
| Disney Epic Rivals (Hades & Hercules, Maleficent & 3 Fairies, Lucifer & Mice, Alice & Cheshire Cat, Vanessa & Ariel) | box_set | $79.95 | 500 | Comes in custom box; mini-jumbo pin-on-pin |
| Villains & Sidekicks Mystery Pin Box | mystery | $32.95/box | 400 | 5 box limit, 2 pins/box |
| Muppet Babies Mystery Pin Box | mystery | $32.95/box | 400 | 5 box limit, 2 pins/box |
| Star Wars Stamps (Framed) | framed_set | $3,000 | 3 | 28.50"×12.50" |
| A Day at the Studio Lot (Framed) | framed_set | $2,500 | 3 | 17"×19" |
| Seasons of Friendship (Framed) | framed_set | $1,500 | 3 | 14"×17.50" |
| Princess Ballerinas (Framed) | framed_set | $1,000 | 3 | 21.5"×12.50" |
| Villains Premier Season (Framed) | framed_set | $1,000 | 3 | 24.50"×10" |
| D23 15th Anniversary Cakes (Framed) | framed_set | $900 | 3 | 13"×16" |
| Princess & Friends (Framed) | framed_set | $500 | 3 | 14"×8.50" |
| Mickey's City Outfits (Framed) | framed_set | $500 | 3 | 15"×9.50" |
| Be My Valentine (Framed) | framed_set | $500 | 3 | 18.25"×7.25" |

### Drop: Sunday, August 16 (TWDC)

| Set | Type | Price | LE | Notes |
|-----|------|-------|----|-------|
| Elements of Nature — Fire (Maleficent Dragon, Chernabog, Scar, Amber, Mushu, Lotso) | individual | $42.95 | 400 | Gold metal base; pin-on-pin oval frame |
| Elements of Nature — Water (Moana, Sorcerer's Apprentice, Simba & friends, Nemo & Dory, Nokk & Elsa, Wade) | individual | $42.95 | 400 | Gold metal base |
| Elements of Nature — Wind (Pocahontas, Gale & Olaf, Pooh & Piglet, Bernard & Bianca, Band Concert, Wolf & Pigs) | individual | $42.95 | 400 | Silver metal base |
| Elements of Nature — Earth (Grandma Willow, Mufasa & Simba, Gaetan 'Mole' Moliere, Sprite, Flik & Dot, Te Fiti) | individual | $42.95 | 400 | Silver metal base |
| Cat-astrophe (Yzma, Toulouse, Sergeant Tibbs, Snowball, Oliver, Mr. Mittens, Marie & Berlioz, Madam Mim, Machiavelli, Lucifer, Figaro, Dinah, Mochi, Cheshire) | individual | $34.95 | 400 | Antique gold base, hard enamel |
| Table for One (Evil Queen, Maleficent, Captain Hook, Cruella de Vil, Ursula, King Candy, Hades, Mother Gothel, Yzma, Ernesto de la Cruz, Hans, King Magnifico, Madam Mim, Prince John, Dr. Facilier) | individual | $45.95 | 400 | Villain dining scene pin-on-pin |
| Enchanted Gowns (Snow White, Cinderella, Aurora, Ariel, Jasmine, Belle, Pocahontas, Mulan, Tiana, Rapunzel, Anna, Elsa) | individual | $34.95 | 400 | Gold base, glitter, small jewels |
| Winnie the Pooh Mystery Pin Box | mystery | $32.95/box | 400 | 5 box limit, 2 pins/box |
| Star Wars Galactic Pals Mystery Pin Box (Porg, Loth-Cat, Gamorrean, Ortolan, Wookiee, Tauntaun, Ewok, Rodian, Huttlet) | mystery | $32.95/box | 400 | 5 box limit, 2 pins/box |
| Pixar Stamps (Framed) | framed_set | $3,000 | 3 | 28.50"×12.50" |
| Hugs Are the Best (Framed) | framed_set | $2,000 | 3 | 17"×19" |
| Fairytale Dancing (Framed) | framed_set | $1,000 | 3 | 14"×14" |
| A Villain's Darkness (Framed) | framed_set | $750 | 3 | 14"×14" |
| Holiday Princess Party (Framed) | framed_set | $500 | 3 | 17.75"×10.50" |
| Minnie's City Outfits (Framed) | framed_set | $500 | 3 | 16"×9.50" |
| Classic Friends (Framed) | framed_set | $500 | 3 | 15"×9.50" |
| Holiday Snowflakes (Framed) | framed_set | $400 | 3 | 14"×10.50" |

---

## Known Catalog Data (DSSH — from PDF analysis)

DSSH metadata appears in a single pipe-delimited header line per set: `$PRICE | LE XXX | W x H | FINISH TYPE`. No catalog numbers. Purchase limit is 1 per person for all individual pins; 5 boxes for mystery sets.

### Drop: Friday, August 14 (DSSH)

| Set | Type | Price | LE | Notes |
|-----|------|-------|----|-------|
| Premiere Collection — El Capitan 100 Years in Hollywood | box_set | $199.95 | 200 | 5.04"W×3.425"H; pin-on-pin + custom box |
| Artist Series — Avengers: Endgame by Matt Ferguson (Ant-Man, Iron Man, Thanos, Captain America, Thor) | individual | $29.95 | 400 | 1.69"W×2.25"H; 3D laser print + custom backing card |
| It's All in a Name Series (Ariel, Belle, Marie, Ursula, Stitch, Maleficent, Dumbo, Kuzco, Alice, Aurora, Hades, Eeyore, Goofy, Moana) | individual | $49.95 | 400 | Jumbo; two pin-on-pins; translucent; custom backing card |
| Disney Dragons Cuties Series (Elliott, Madam Mim, Maleficent, Sisu, The Reluctant Dragon, Queen Narissa, Hydra, The Gwythaints, Blazey, Mushu) | individual | $34.95 | 300 | Custom backing card |
| Best in Show Series (Marie, Lucifer, Cheshire Cat, Fifi the Peke, Dinah, Max, Nana, Dodger, Little Brother, Pongo, Pluto, Berlioz, Toulouse, Mochi) | individual | $29.95 | 400 | 1.27"W×2.0"H; pin-on-pin |
| Throwback Mystery Series (Kim Possible Cheer LE400, Ron and Rufus LE400, Lizzie on Scooter LE400, Lizzie Frame LE400, Lizzie Heart LE400, East High School LE400, Troy and Gabriella LE400, Rufus LE400, Kim Possible LE300, Lizzie Hooray LE300, Lizzie Flower Crown LE300, EHS Megaphone LE300, So Not the Drama LE150, Lizzie in Heels LE150) | mystery | $49.95/box | varies | 5 box limit; 2 pins/box; chaser tiers |

### Drop: Saturday, August 15 (DSSH)

| Set | Type | Price | LE | Notes |
|-----|------|-------|----|-------|
| Vinyl Records — Starter Set (Record player + Sleeping Beauty + Pinocchio) | box_set | $89.95 | 400 | 2.25"W×1.84"H player; 1.88"W×1.88"H vinyls; custom backing |
| Vinyl Records — Individual Vinyls (Tangled, Hoppers, Pocahontas, Big Hero 6, Snow White & the Seven Dwarfs, Mulan, Frozen, Cinderella, Dumbo, Fantasia) | individual | $32.95 | 400 | Pin-on-pin; custom backing card |
| Unlocking the Magic Series (The Little Mermaid, Lilo & Stitch, Mulan, Sleeping Beauty, Aladdin, Rapunzel, Big Hero 6, Frozen, Pinocchio, Moana, Dumbo, Cinderella) | individual | $49.95 | 400 | Hinge pin; glitter fill; custom backing |
| Duos Series (Anna & Elsa, The Mandalorian & Grogu, Goofy & Max, Maui & Moana, Deadpool & Wolverine, Mr. & Mrs. Incredible, Robin Hood & Little John, Hercules & Megara, Baymax & Hiro, Ariel & Prince Eric, Nick Wilde & Judy Hopps, Lilo & Stitch) | individual | $74.95 | 400 | Stained glass; 1.07"W×3.0"H bookmark format; custom backing |
| Zootopia 10th Anniversary Car Series (Judy Hopps, Flash, Finnick, Nick Wilde, Dawn Bellwether, Chief Bogo) | individual | $24.95 | 300 | Characters driving cars |
| El Capitan Theatre 100th — El Capitan 1926 Hinged Pin | individual | $29.95 | 400 | 1.83"W×2.25"H; antique gold |
| El Capitan Theatre 100th — Character Pins (Mickey, Minnie, Oswald the Lucky Rabbit, Donald, Daisy, Judy Hopps, Nick Wilde) | individual | $24.95 | 400 | Antique nickel + pin-on-pin |

### Drop: Sunday, August 16 (DSSH)

| Set | Type | Price | LE | Notes |
|-----|------|-------|----|-------|
| Tapestry Series (Miguel, Alice, Jasmine, Jack and Sally, Elsa, Merida, Rapunzel, Briar Rose, Yzma, Maleficent, Ursula, Mirabel) | individual | $32.95 | 400 | 1.56"W×2.0"H; pin-on-pin |
| Duck Series (Stitch, Lilo, Maleficent, Cruella, Hades, Jiminy Cricket, Fairy Godmother, Flora, Fauna, Merryweather, Mad Hatter, Panda Mei) | individual | $32.95 | 400 | Pin-on-pin rubber duck characters |
| Cursive Cuties Series (Baymax, Bing Bong, Bolt, Cheshire Cat, Merryweather, Grumpy, Louis, Meeko, Flora, Cri-Kee, Mushu, Oswald the Lucky Rabbit, Scrump, Fauna) | individual | $44.95 | 400 | 2.5"W×2.5"H; 3D color paste; pin-on-pin; translucent fill |
| A Goofy Movie Cuties Series (Goofy, Max, P.J. Pete, Powerline, Pete, Bobby Zimuruski, Roxanne, Stacey) | individual | $34.95 | 300 | Custom backing card |

---

## Technical Constraints

- **No backend** — the web app must be a single self-contained `index.html` that can be opened directly from the filesystem or served from any static host
- **No build step required** — use vanilla JS or a CDN-loaded framework (Vue 3 via CDN is acceptable); do not require Node/npm to run the app
- **Offline-capable** — once `pins.json` is loaded, the app should work with no network connection
- **`pins.json` loading** — the app should `fetch('./pins.json')` on load; if it fails (e.g. opened as a local file), fall back to a friendly error: "Catalog data not found. Make sure pins.json is in the same folder as index.html."
- **Image handling** — images are saved as individual PNGs in the `/images/` directory and referenced by relative path in `pins.json`. The web app loads them via standard `<img src>` tags.
- **localStorage** — ISO list persisted under key `d23_iso_list` as a JSON array of pin IDs and quantities
- **Performance** — use native lazy loading (`loading="lazy"`) on pin images so the browser only fetches them as they approach the viewport. `pins.json` itself stays lightweight (metadata only, no embedded images).

---

## File Structure

```
/
├── catalogs/
│   ├── mog/mog.pdf
│   ├── twdc/twdc_fri.pdf
│   ├── twdc/twdc_sat.pdf
│   ├── twdc/twdc_sun.pdf
│   └── dssh/dssh.pdf
├── images/             # Extracted pin images (generated by extract.py)
│   ├── mog-alice-75th-2.png
│   ├── mog-alice-75th-3.png
│   └── ...
├── extract.py          # PDF extraction script
├── pins.json           # Generated output (metadata only, references images/)
├── index.html          # The web app
└── README.md           # How to run the extraction and open the app
```

`README.md` should include:
1. Prerequisites (`pip install pdfplumber pymupdf`)
2. How to run `extract.py`
3. How to open `index.html` (note: must be served, not opened as `file://`, due to fetch() — suggest `python -m http.server 8000`)

---

## Acceptance Criteria

**Extraction:**
- [ ] Running `extract.py` against all 5 PDFs produces a valid `pins.json` consistent with all three Known Data sections above
- [ ] Script correctly auto-detects store (MOG / TWDC / DSSH) and drop date from PDF content, not filename
- [ ] TWDC framed pin sets are parsed as `set_type: "framed_set"` with correct LE3 and prices
- [ ] DSSH pipe-delimited metadata line is parsed correctly (price, LE, dimensions, features all extracted)
- [ ] The TWDC "Color Shades of Magic" set has `ship_only: true` and a note about no in-person pickup
- [ ] DSSH Throwback Mystery Series per-pin LE tiers (400 / 300 / 150) are captured in `edition_notes`
- [ ] Pin images are extracted to the `/images/` directory from all three store PDFs and render clearly in the web app

**Web App:**
- [ ] Catalog view filters correctly by store and drop date (filters compose with AND logic)
- [ ] All three stores appear in the store filter; DSSH shows as "DSSH" or "Studio Store Hollywood"
- [ ] Framed pin sets (LE3) are visually distinguished with a special badge
- [ ] Adding a pin to ISO persists after page refresh
- [ ] Quantity stepper works; total cost updates in real time
- [ ] Copy-as-text export produces correctly formatted output, grouped by store then date
- [ ] App is fully usable on a 390px-wide mobile viewport with no horizontal scroll
- [ ] The MOG $1,200 ultra jumbo pin is visually distinguished from standard pins
- [ ] Mystery set cards show a "blind box" visual cue and per-box price disclaimer
- [ ] ISO list groups items by store → drop date and shows the running total in a sticky footer
- [ ] DSSH Throwback Mystery Series shows chaser tier information in the pin detail sheet
