#!/usr/bin/env python3
"""
D23 Pin Catalog Extraction Script
Outputs pins.json with full catalog metadata. Images use a placeholder path;
drop real images into images/<pin-id>.png to replace them.

Note: The DSSH PDF is fully rasterized (no selectable text). All metadata is
sourced from the verified spec catalog tables for all three stores.

Usage:
    python extract.py --catalogs ./catalogs/ --output ./pins.json
"""

import argparse
import json
import os
from datetime import datetime
from collections import defaultdict


PLACEHOLDER = "images/placeholder.png"


def slugify(text):
    import re
    t = text.lower().strip()
    t = re.sub(r"[^\w\s-]", "", t)
    t = re.sub(r"[\s_-]+", "-", t)
    t = re.sub(r"-+", "-", t)
    return t[:60].rstrip("-")


def make_pin(set_id, catalog_number, name, edition_size, edition_notes=None):
    if catalog_number is not None:
        pin_id = f"{set_id}-{catalog_number}"
    else:
        pin_id = f"{set_id}-{slugify(name)}"
    return {
        "id": pin_id,
        "catalog_number": catalog_number,
        "name": name,
        "edition_size": edition_size,
        "edition_notes": edition_notes,
        "image_path": PLACEHOLDER,
    }


def make_set(id, store, drop_date, drop_day_label, set_name, set_description,
             set_type, features, dimensions, retail_price, retail_note,
             purchase_limit, ship_only, pins):
    return {
        "id": id,
        "store": store,
        "drop_date": drop_date,
        "drop_day_label": drop_day_label,
        "set_name": set_name,
        "set_description": set_description,
        "set_type": set_type,
        "features": features,
        "dimensions": dimensions,
        "retail_price": retail_price,
        "retail_display": f"${retail_price:,.2f}" if retail_price else None,
        "retail_note": retail_note,
        "purchase_limit": purchase_limit,
        "ship_only": ship_only,
        "available_dates": [drop_date],
        "pins": pins,
    }


# ---------------------------------------------------------------------------
# MOG SETS
# ---------------------------------------------------------------------------

def build_mog_sets():
    sets = []
    FRI, FRI_L = "2026-08-14", "Friday, August 14"
    SAT, SAT_L = "2026-08-15", "Saturday, August 15"
    SUN, SUN_L = "2026-08-16", "Sunday, August 16"
    MOG = "MOG"

    # --- Friday ---
    sid = "mog-alice-mystery"
    s = make_set(
        sid, MOG, FRI, FRI_L,
        "Alice in Wonderland Mystery Set", None, "mystery",
        "Soft Enamel, Marbleized Fill, 3D Border, Laser Print", '1.9″–2.0″H',
        34.95, "per box", "Limit six (6) boxes per guest", False,
        [make_pin(sid, 1, "Mystery Box", 400)],
    )
    s["pins"].extend([make_pin(sid, None, n, 400) for n in [
        "Doorknob", "Mad Hatter", "Queen of Hearts", "March Hare",
        "Red Rose", "Alice", "Caterpillar", "Dinah",
        "White Rabbit", "King of Hearts", "Tweedledee & Tweedledum", "Cheshire Cat"]])
    sets.append(s)

    sid = "mog-alice-75th"
    sets.append(make_set(
        sid, MOG, FRI, FRI_L,
        "Alice in Wonderland 75th Anniversary",
        "Celebrate the 75th Anniversary of Alice in Wonderland with this comic-inspired pin series.",
        "individual",
        "Hard Enamel, Translucent Fills, Marbleized Fill, Laser Print", '3.25″–4.15″H',
        52.95, None, None, False,
        [
            make_pin(sid, 2, "Alice", 400),
            make_pin(sid, 3, "Queen of Hearts", 400),
            make_pin(sid, 4, "White Rabbit", 400),
            make_pin(sid, 5, "Cheshire Cat", 400),
            make_pin(sid, 6, "The Flowers", 400),
        ],
    ))

    sid = "mog-princess-windows"
    sets.append(make_set(
        sid, MOG, FRI, FRI_L,
        "Disney Princess Dream Windows",
        "Celebrate timeless Disney Princess stories with these enchanting stained glass pins.",
        "individual",
        "Hard Enamel, Stained Glass, Laser Print", '3.8″–4.0″H',
        42.95, None, None, False,
        [
            make_pin(sid, 7, "Snow White", 400),
            make_pin(sid, 8, "Cinderella", 400),
            make_pin(sid, 9, "Aurora", 400),
            make_pin(sid, 10, "Ariel", 400),
            make_pin(sid, 11, "Belle", 400),
            make_pin(sid, 12, "Jasmine", 400),
            make_pin(sid, 13, "Pocahontas", 400),
            make_pin(sid, 14, "Mulan", 400),
            make_pin(sid, 15, "Tiana", 400),
            make_pin(sid, 16, "Rapunzel", 400),
            make_pin(sid, 17, "Merida", 400),
            make_pin(sid, 18, "Moana", 400),
            make_pin(sid, 19, "Raya", 400),
        ],
    ))

    sid = "mog-ducktales-mystery"
    s = make_set(
        sid, MOG, FRI, FRI_L,
        "DuckTales the Movie: Treasure of the Lost Lamp Mystery Set", None, "mystery",
        None, '1.2″–1.8″H', 34.95, "per box", "Limit eight (8) boxes per guest", False, [],
    )
    s["pins"] = [
        make_pin(sid, 20, "Mystery Box (Regular)", 400),
        {**make_pin(sid, None, "Mystery Box (Chaser)", 300), "edition_notes": "chaser",
         "id": f"{sid}-chaser"},
    ]
    sets.append(s)

    sid = "mog-treasure-seekers"
    sets.append(make_set(
        sid, MOG, FRI, FRI_L,
        "Disney Treasure Seekers", None, "individual",
        None, None, 34.95, None, None, False,
        [
            make_pin(sid, 21, "Ariel", 400),
            make_pin(sid, 22, "Scrooge McDuck", 400),
            make_pin(sid, 23, "Jim Hawkins", 400),
            make_pin(sid, 24, "Peter Pan", 400),
            make_pin(sid, 25, "Abu", 400),
            make_pin(sid, 26, "Penny", 400),
        ],
    ))

    sid = "mog-squad-goals"
    sets.append(make_set(
        sid, MOG, FRI, FRI_L,
        "Disney Squad Goals", None, "individual",
        None, None, 69.95, None, None, False,
        [
            make_pin(sid, 27, "The Little Mermaid", 400),
            make_pin(sid, 28, "Treasure Planet", 400),
            make_pin(sid, 29, "The Princess and the Frog", 400),
            make_pin(sid, 30, "Big Hero 6", 400),
            make_pin(sid, 31, "Raya and the Last Dragon", 400),
            make_pin(sid, 32, "Lilo & Stitch", 400),
            make_pin(sid, 33, "A Goofy Movie", 400),
            make_pin(sid, 34, "Moana", 400),
            make_pin(sid, 35, "Robin Hood", 400),
            make_pin(sid, 36, "Snow White and the Seven Dwarfs", 400),
        ],
    ))

    sid = "mog-pov"
    sets.append(make_set(
        sid, MOG, FRI, FRI_L,
        "POV: Another Point of View",
        "Rotating double-sided spinner pins featuring heroes and villains.",
        "individual",
        "Rotating Double-Sided Jumbo Pin, Hard Enamel, 3D Cast Frame, Gemstones, Specialty Fills (Glitter, Marbleized, Translucent)",
        '5″–5.5″H', 79.95, None, None, False,
        [
            make_pin(sid, 37, "Moana and Te Kā", 400),
            make_pin(sid, 38, "Belle and Beast", 400),
            make_pin(sid, 39, "Snow White and Evil Queen", 400),
            make_pin(sid, 40, "Ariel and Ursula", 400),
            make_pin(sid, 41, "Aurora and Maleficent", 400),
            make_pin(sid, 42, "Aladdin and Genie", 400),
            make_pin(sid, 43, "Alice and the Queen of Hearts", 400),
            make_pin(sid, 44, "Cinderella and Prince Charming", 400),
            make_pin(sid, 45, "Rapunzel and Flynn Rider", 400),
            make_pin(sid, 46, "Sorcerer's Apprentice Mickey and Yen Sid", 400),
        ],
    ))

    sid = "mog-dining-character"
    sets.append(make_set(
        sid, MOG, FRI, FRI_L,
        "Dining with Character",
        "Detailed dining scenes on commemorative plate-inspired pins.",
        "individual",
        "Jumbo Hard Enamel Pin, Specialty Fills (Glitter, Marbleized, Translucent), Laser Print",
        '4.5″H', 79.95, None, None, False,
        [
            make_pin(sid, 47, "The Emperor's New Groove", 400),
            make_pin(sid, 48, "Sleeping Beauty", 400),
            make_pin(sid, 49, "Alice in Wonderland", 400),
            make_pin(sid, 50, "The Princess and the Frog", 400),
            make_pin(sid, 51, "Winnie the Pooh", 400),
            make_pin(sid, 52, "The Little Mermaid", 400),
            make_pin(sid, 53, "Mickey and the Beanstalk", 400),
            make_pin(sid, 54, "Lady and the Tramp", 400),
            make_pin(sid, 55, "Beauty and the Beast", 400),
            make_pin(sid, 56, "Ratatouille", 400),
        ],
    ))

    sid = "mog-world-princess-ultra"
    sets.append(make_set(
        sid, MOG, FRI, FRI_L,
        "World Princess Week Ultra Jumbo",
        "Gathering beloved heroines from across Disney's animated legacy, this majestic pin celebrates the optimism, courage, and timeless stories of the Disney Princesses.",
        "ultra_jumbo",
        "Ultra Jumbo Hard Enamel Pin, Stained Glass, Laser Print, Pin On Pin",
        '16″W × 9″H', 1200.00, None, None, False,
        [make_pin(sid, 57, "World Princess Week", 150)],
    ))

    # --- Saturday ---
    sid = "mog-sea-mystery"
    s = make_set(
        sid, MOG, SAT, SAT_L,
        "S.E.A. Mystery Set",
        "Collect all 15 pins plus trading cards to reveal a hidden image.",
        "mystery", None, None, 39.95, "per box", None, False,
        [make_pin(sid, 58, "Mystery Box", 500)],
    )
    s["pins"].extend([make_pin(sid, None, n, 500) for n in [
        "Mary Oceaneer", "Duncan the Parrot", "Alberta Falls", "Albert Falls",
        "Pin 5", "Dr. Kon Chunosuke", "Camellia Falco", "S.E.A. Member",
        "Harrison Hightower III", "Barnabas T. Bullion", "Lord Henry Mystic", "Albert",
        "Pin 13", "Shiriki Utundu"]])
    sets.append(s)

    sid = "mog-parks-to-ports"
    sets.append(make_set(
        sid, MOG, SAT, SAT_L,
        "Around the World with Disney: Parks to Ports", None, "individual",
        None, None, 36.95, None, None, False,
        [
            make_pin(sid, 59, "Disneyland", 400),
            make_pin(sid, 60, "Magic Kingdom", 400),
            make_pin(sid, 61, "Tokyo Disneyland", 400),
            make_pin(sid, 62, "Disneyland Paris", 400),
            make_pin(sid, 63, "Hong Kong Disneyland", 400),
            make_pin(sid, 64, "Shanghai Disneyland", 400),
            make_pin(sid, 65, "Disney Cruise Line", 400),
        ],
    ))

    sid = "mog-park-stamps-2"
    sets.append(make_set(
        sid, MOG, SAT, SAT_L,
        "Disney Park Stamps — Series 2",
        "Commemorative stamp pin series celebrating the characters and attractions of Disney Parks.",
        "individual",
        "Hard Enamel, Stained Glass, Specialty Fills (Glitter, Translucent, Pearlized), Laser Print",
        '2.5″–3″H', 34.95, None, None, False,
        [
            make_pin(sid, 66, "Ariel", 400),
            make_pin(sid, 67, "Rosita", 400),
            make_pin(sid, 68, "Teddi Barra", 400),
            make_pin(sid, 69, "Hatbox Ghost", 400),
            make_pin(sid, 70, "Albert", 400),
            make_pin(sid, 71, "Scooter", 400),
            make_pin(sid, 72, "Yeti", 400),
            make_pin(sid, 73, "Chuuby", 400),
            make_pin(sid, 74, "Tom Morrow 2.0", 400),
            make_pin(sid, 75, "Dumbo", 400),
            make_pin(sid, 76, "Winnie the Pooh", 400),
            make_pin(sid, 77, "Sonny Eclipse", 400),
            make_pin(sid, 78, "Lagoona Gator", 400),
            make_pin(sid, 79, "The Dapper Dans", 400),
            make_pin(sid, 80, "Jingles", 400),
        ],
    ))

    sid = "mog-panoramas"
    sets.append(make_set(
        sid, MOG, SAT, SAT_L,
        "Disney Attraction Panoramas", None, "individual",
        None, None, 74.95, None, None, False,
        [
            make_pin(sid, 81, "Peter Pan's Flight", 400),
            make_pin(sid, 82, "Jungle Cruise", 400),
            make_pin(sid, 83, "Alice in Wonderland", 400),
            make_pin(sid, 84, "Matterhorn Bobsleds", 400),
            make_pin(sid, 85, "It's a Small World", 400),
            make_pin(sid, 86, "Pirates of the Caribbean", 400),
            make_pin(sid, 87, "Haunted Mansion", 400),
            make_pin(sid, 88, "Big Thunder Mountain Railroad", 400),
        ],
    ))

    sid = "mog-carousel-horses"
    s = make_set(
        sid, MOG, SAT, SAT_L,
        "Disney Royal Carousel Horses",
        "Box set of 6 carousel horse pins with display box.", "box_set",
        None, None, 324.95, "for set of 6", None, False,
        [make_pin(sid, 89, "Box Set", 250)],
    )
    s["pins"].extend([make_pin(sid, None, n, 250) for n in [
        "Mickey", "Minnie", "Donald", "Goofy", "Clarabelle", "Daisy"]])
    sets.append(s)

    # --- Sunday ---
    sid = "mog-avengers-mystery"
    s = make_set(
        sid, MOG, SUN, SUN_L,
        "The Avengers Mystery Set", None, "mystery",
        None, '1.3″–1.7″H', 34.95, "per box", "Limit eight (8) boxes per guest", False, [],
    )
    s["pins"] = [
        make_pin(sid, None, "Mystery Box (Regular)", 400),
        {**make_pin(sid, None, "Mystery Box (Chaser)", 300), "edition_notes": "chaser",
         "id": f"{sid}-chaser"},
        {**make_pin(sid, None, "Mystery Box (Super Chaser)", 200), "edition_notes": "super chaser",
         "id": f"{sid}-super-chaser"},
    ]
    sets.append(s)

    sid = "mog-guardians-boxset"
    sets.append(make_set(
        sid, MOG, SUN, SUN_L,
        "Guardians of the Galaxy Box Set",
        "Each box contains one mystery pin under the tray.", "box_set",
        None, '1″–1.7″H', 74.95, None, None, False,
        [make_pin(sid, 91, "Guardians of the Galaxy Box Set", 400)],
    ))

    sid = "mog-kingdom-hearts-mystery"
    s = make_set(
        sid, MOG, SUN, SUN_L,
        "Kingdom Hearts Mystery Set", None, "mystery",
        None, None, 34.95, "per box", "Limit eight (8) boxes per guest", False, [],
    )
    s["pins"] = [
        make_pin(sid, None, "Mystery Box (Regular)", 500),
        {**make_pin(sid, None, "Mystery Box (Chaser)", 400), "edition_notes": "chaser",
         "id": f"{sid}-chaser"},
        {**make_pin(sid, None, "Mystery Box (Super Chaser)", 300), "edition_notes": "super chaser",
         "id": f"{sid}-super-chaser"},
    ]
    sets.append(s)

    sid = "mog-pixar-soul-mystery"
    s = make_set(
        sid, MOG, SUN, SUN_L,
        "Pixar Soul Mystery Set", None, "mystery",
        None, None, 34.95, "per box", "Limit eight (8) boxes per guest", False, [],
    )
    s["pins"] = [
        make_pin(sid, None, "Mystery Box (Regular)", 400),
        {**make_pin(sid, None, "Mystery Box (Chaser)", 300), "edition_notes": "chaser",
         "id": f"{sid}-chaser"},
        {**make_pin(sid, None, "Mystery Box (Super Chaser)", 200), "edition_notes": "super chaser",
         "id": f"{sid}-super-chaser"},
    ]
    sets.append(s)

    sid = "mog-pixar-soul-boxset"
    sets.append(make_set(
        sid, MOG, SUN, SUN_L,
        "Pixar Soul Box Set", None, "box_set",
        None, None, 49.95, None, None, False,
        [make_pin(sid, 94, "Pixar Soul Box Set", 400)],
    ))

    sid = "mog-muppet-show-50th"
    sets.append(make_set(
        sid, MOG, SUN, SUN_L,
        "The Muppet Show 50th", "Celebrating 50 years of The Muppet Show.", "individual",
        "Pin On Pin, 3D Cast Frame, Specialty Fills (Glitter, Translucent, Marbleized, Pearlized), Laser Print",
        '3.5″W', 54.95, None, None, False,
        [
            make_pin(sid, 95, "Kermit", 400),
            make_pin(sid, 96, "Veterinarian's Hospital", 400),
            make_pin(sid, 97, "At the Dance", 400),
            make_pin(sid, 98, "Swedish Chef", 400),
            make_pin(sid, 99, "Great Gonzo", 400),
            make_pin(sid, 100, "Fozzie's Stand-Up", 400),
            make_pin(sid, 101, "Pigs in Space", 400),
            make_pin(sid, 102, "The Electric Mayhem", 400),
            make_pin(sid, 103, "Muppet Labs", 400),
            make_pin(sid, 104, "Statler and Waldorf", 400),
        ],
    ))

    sid = "mog-portraits-of-evil"
    sets.append(make_set(
        sid, MOG, SUN, SUN_L,
        "Portraits of Evil", None, "individual",
        None, None, 44.95, None, None, False,
        [
            make_pin(sid, 105, "Evil Queen", 400),
            make_pin(sid, 106, "Chernabog", 400),
            make_pin(sid, 107, "Queen of Hearts", 400),
            make_pin(sid, 108, "Maleficent", 400),
            make_pin(sid, 109, "Cruella De Vil", 400),
            make_pin(sid, 110, "Horned King", 400),
            make_pin(sid, 111, "Ursula", 400),
            make_pin(sid, 112, "Gaston", 400),
            make_pin(sid, 113, "Jafar", 400),
            make_pin(sid, 114, "Scar", 400),
            make_pin(sid, 115, "Hades", 400),
            make_pin(sid, 116, "Yzma", 400),
            make_pin(sid, 117, "Mother Gothel", 400),
        ],
    ))

    sid = "mog-colorful-world-mystery"
    sets.append(make_set(
        sid, MOG, SUN, SUN_L,
        "The Colorful World of Disney Mystery Set",
        "23 color-changing UV-reactive pins.", "mystery",
        "UV Reactive Color-Changing", None, 34.95, "per box", None, False,
        [make_pin(sid, 118, "Mystery Box", 500)],
    ))

    return sets


# ---------------------------------------------------------------------------
# TWDC SETS
# ---------------------------------------------------------------------------

def build_twdc_sets():
    sets = []
    FRI, FRI_L = "2026-08-14", "Friday, August 14"
    SAT, SAT_L = "2026-08-15", "Saturday, August 15"
    SUN, SUN_L = "2026-08-16", "Sunday, August 16"
    T = "TWDC"
    PL1 = "Purchase limit of ONE (1) of each limited edition pin per person"
    PL5 = "Purchase limit of FIVE BOXES (5) per person. 2 pins per box"

    # --- FRIDAY ---
    sid = "twdc-disney-stamp-classic"
    sets.append(make_set(sid, T, FRI, FRI_L,
        "The Ultimate Disney Stamp — Classic Era", None, "individual",
        "Gold base metal, pin on pin, hard enamel, glitter and laser printed background details",
        None, 34.95, None, PL1, False,
        [make_pin(sid, None, n, 500) for n in [
            "Yensid & Sorcerer Mickey", "Blue Fairy & Jiminy", "Dumbo & Timothy",
            "Donald & Aracuan Bird", "Alice & White Rabbit", "Chip & Dale",
            "Maleficent Dragon & Prince Phillip", "Merlin & Archimedes",
            "Robin Hood & Little John", "Pooh & Piglet"]],
    ))

    sid = "twdc-disney-stamp-renaissance"
    sets.append(make_set(sid, T, FRI, FRI_L,
        "The Ultimate Disney Stamp — Renaissance Era", None, "individual",
        "Gold base metal, pin on pin, hard enamel, glitter and laser printed background details",
        None, 34.95, None, PL1, False,
        [make_pin(sid, None, n, 500) for n in [
            "Todd & Copper", "Dodger & Oliver", "Ariel & Scuttle", "Bernard & Bianca",
            "Belle & Maurice", "Hercules & Phil", "Mulan & Mushu", "Kronk & Yzma",
            "Lilo & Stitch", "Tiana & Charlotte"]],
    ))

    sid = "twdc-disney-stamp-modern"
    sets.append(make_set(sid, T, FRI, FRI_L,
        "The Ultimate Disney Stamp — Modern Era", None, "individual",
        "Gold base metal, pin on pin, hard enamel, glitter and laser printed background details",
        None, 34.95, None, PL1, False,
        [make_pin(sid, None, n, 500) for n in [
            "Rapunzel & Pascal", "Wreck-It Ralph & Vanellope", "Anna & Olaf",
            "Baymax & Hiro", "Judy & Nick", "Moana & Hei Hei", "Elsa & Bruni",
            "Raya & Tuk Tuk", "Valentino & Star", "Gazelle & Tiger"]],
    ))

    sid = "twdc-reel-of-magic"
    sets.append(make_set(sid, T, FRI, FRI_L,
        "Reel of Magic", None, "individual",
        "Hinge pin, gold metal base, translucent pattern backgrounds, clear epoxy, hard enamel, laser printed details",
        '3.47″×3.5″', 52.95, None, PL1, False,
        [make_pin(sid, None, n, 500) for n in [
            "The Little Mermaid", "Beauty and the Beast", "Aladdin", "The Lion King",
            "Pocahontas", "The Hunchback of Notre Dame", "Mulan", "Tarzan",
            "Emperor's New Groove", "Atlantis", "Hercules"]],
    ))

    sid = "twdc-royal-chambers"
    sets.append(make_set(sid, T, FRI, FRI_L,
        "Royal Chambers", None, "individual",
        "Throne scene pin-on-pin", None, 45.95, None, PL1, False,
        [make_pin(sid, None, n, 400) for n in [
            "Evil Queen", "Prince Charming", "Queen of Hearts",
            "King Stefan & Queen Leah", "King Arthur", "Triton", "Gaston",
            "Sultan", "Zeus", "Emperor", "Kuzco", "King Magnifico",
            "King Candy", "Elsa"]],
    ))

    sid = "twdc-role-models"
    sets.append(make_set(sid, T, FRI, FRI_L,
        "Role Models", None, "individual", "Pin-on-pin", None, 45.95, None, PL1, False,
        [make_pin(sid, None, n, 400) for n in [
            "Rafiki & Simba", "Jiminy & Pinocchio", "Tala & Moana", "Mei Mei & Ming",
            "Merlin & Arthur", "Grandmother Willow & Pocahontas", "Phil & Hercules",
            "Fairy Godmother & Cinderella", "Timothy Mouse & Dumbo", "Ancestor & Mulan",
            "Auguste Gusteau & Remy", "Hector & Miguel", "Tadashi & Hiro", "Carl & Russel"]],
    ))

    sid = "twdc-disney-d-mystery"
    s = make_set(sid, T, FRI, FRI_L,
        "Disney D's Mystery Pin Box", None, "mystery", None, None, 32.95, "per box", PL5, False,
        [make_pin(sid, None, "Mystery Box", 400)],
    )
    s["pins"].extend([make_pin(sid, None, n, 400) for n in [
        "Mickey", "Minnie", "Goofy", "Daisy", "Pluto", "Chip & Dale", "Donald", "Blank D"]])
    sets.append(s)

    sid = "twdc-princess-mystery"
    s = make_set(sid, T, FRI, FRI_L,
        "Disney Princess Mystery Pin Box", None, "mystery", None, None, 32.95, "per box", PL5, False,
        [make_pin(sid, None, "Mystery Box", 400)],
    )
    s["pins"].extend([make_pin(sid, None, n, 400) for n in [
        "Ariel", "Moana", "Tiana", "Belle", "Rapunzel", "Pocahontas", "Jasmine", "Cinderella"]])
    sets.append(s)

    # Framed — All days combined into one set
    framed_all = [
        # Friday
        ("Color Shades of Magic", 6000, '22.31″×30.50″', FRI, True),
        ("The Songs We Grew Up With", 2500, '26″×26″', FRI, False),
        ("Friends From Around the World", 1500, '16.50″×12.25″', FRI, False),
        ("35 Years of Mermaid Emotions", 1000, '21″×10.5″', FRI, False),
        ("Spirit of Family", 900, '21″×10″', FRI, False),
        ("Pixar Animation Studios", 900, '21″×9.5″', FRI, False),
        ("Encanto Tiles", 700, '12.5″×12.5″', FRI, False),
        ("Villains", 500, '12″×8.50″', FRI, False),
        ("The Ultimate Disney Fan Event 2024", 400, '14.75″×11″', FRI, False),
        # Saturday
        ("Star Wars Stamps", 3000, '28.50″×12.50″', SAT, False),
        ("A Day at the Studio Lot", 2500, '17″×19″', SAT, False),
        ("Seasons of Friendship", 1500, '14″×17.50″', SAT, False),
        ("Princess Ballerinas", 1000, '21.5″×12.50″', SAT, False),
        ("Villains Premier Season", 1000, '24.50″×10″', SAT, False),
        ("D23 15th Anniversary Cakes", 900, '13″×16″', SAT, False),
        ("Princess & Friends", 500, '14″×8.50″', SAT, False),
        ("Mickey's City Outfits", 500, '15″×9.50″', SAT, False),
        ("Be My Valentine", 500, '18.25″×7.25″', SAT, False),
        # Sunday
        ("Pixar Stamps", 3000, '28.50″×12.50″', SUN, False),
        ("Hugs Are the Best", 2000, '17″×19″', SUN, False),
        ("Fairytale Dancing", 1000, '14″×14″', SUN, False),
        ("A Villain's Darkness", 750, '14″×14″', SUN, False),
        ("Holiday Princess Party", 500, '17.75″×10.50″', SUN, False),
        ("Minnie's City Outfits", 500, '16″×9.50″', SUN, False),
        ("Classic Friends", 500, '15″×9.50″', SUN, False),
        ("Holiday Snowflakes", 400, '14″×10.50″', SUN, False),
    ]

    framed_pins = []
    for name, price, dims, day, ship in framed_all:
        sid = slugify(f"twdc-framed-{name}")
        p = make_pin(sid, None, f"{name} (Framed)", 3)
        # Store price in a custom field so the web app can show per-pin pricing
        p["retail_price"] = float(price)
        p["retail_display"] = f"${price:,.2f}"
        p["dimensions"] = dims
        p["ship_only"] = ship
        p["drop_date"] = day
        framed_pins.append(p)

    framed_set = {
        "id": "twdc-framed",
        "store": T,
        "drop_date": FRI,
        "drop_day_label": FRI_L,
        "set_name": "Framed",
        "set_description": "Limited edition framed pin displays. All LE3.",
        "set_type": "framed_set",
        "features": None,
        "dimensions": None,
        "retail_price": None,
        "retail_display": "Varies",
        "retail_note": None,
        "purchase_limit": None,
        "ship_only": False,
        "available_dates": [FRI, SAT, SUN],
        "pins": framed_pins,
    }
    sets.append(framed_set)

    # --- SATURDAY ---
    sid = "twdc-pixar-stamp-1"
    sets.append(make_set(sid, T, SAT, SAT_L,
        "The Ultimate Pixar Stamp — Series 1", None, "individual",
        "Gold base metal, pin on pin, hard enamel, glitter and laser printed background details",
        None, 34.95, None, PL1, False,
        [make_pin(sid, None, n, 500) for n in [
            "Buzz & Woody", "Heimlich & Flik", "Jessie & Bullseye", "Sulley & Boo",
            "Nemo & Crush", "Mr Incredible & Frozone", "Lightning McQueen & Mater",
            "Linguini & Remy", "WALL-E & EVE", "Carl & Ellie"]],
    ))

    sid = "twdc-pixar-stamp-2"
    sets.append(make_set(sid, T, SAT, SAT_L,
        "The Ultimate Pixar Stamp — Series 2", None, "individual",
        "Gold base metal, pin on pin, hard enamel, glitter and laser printed background details",
        None, 34.95, None, PL1, False,
        [make_pin(sid, None, n, 500) for n in [
            "Gus the Cloud & Peck the Stork", "Lotso & Mr Pricklepants",
            "Young Boy & Papa", "Queen Elinor & Merida", "Mike & Squishy",
            "Joy & Bing Bong", "Arlo & Spot", "Dory & Hank",
            "Miguel & Dante", "Edna Mode & Jack-Jack"]],
    ))

    sid = "twdc-pixar-stamp-3"
    sets.append(make_set(sid, T, SAT, SAT_L,
        "The Ultimate Pixar Stamp — Series 3", None, "individual",
        "Gold base metal, pin on pin, hard enamel, glitter and laser printed background details",
        None, 34.95, None, PL1, False,
        [make_pin(sid, None, n, 500) for n in [
            "Bonnie & Forky", "Ian & Barley", "Joe & 22", "Luca & Alberto",
            "Dug & Carl", "Meilin & Ming", "Ember & Wade", "Paula & Xeni",
            "Anxiety & Sadness", "Elio & Glordon"]],
    ))

    sid = "twdc-game-changers"
    sets.append(make_set(sid, T, SAT, SAT_L,
        "Game Changers", None, "individual", "Pin-on-pin, tall bookmark format",
        None, 39.95, None, PL1, False,
        [make_pin(sid, None, n, 400) for n in [
            "Ariel", "Belle", "Jasmine", "Pocahontas", "Esmeralda", "Megara",
            "Mulan", "Tiana", "Rapunzel", "Merida", "Moana", "Anna", "Elsa",
            "Raya", "Vanellope", "Mirabel"]],
    ))

    sid = "twdc-welcome-home"
    sets.append(make_set(sid, T, SAT, SAT_L,
        "Welcome Home", None, "individual", "Pin-on-pin, home/building scenes",
        None, 42.95, None, PL1, False,
        [make_pin(sid, None, n, 400) for n in [
            "Carl & Ellie's Home", "Mulan's Family Home", "Geppetto's Workshop",
            "Robinsons Family Lab", "Snow White's Cottage", "Belle's Cottage",
            "Lilo's Home", "The Incredibles' Home", "Tinkerbell's Home",
            "White Rabbit's Home", "Winnie the Pooh's Home", "Casa Madrigal",
            "Roger & Anita's Home", "Lady & Tramp's Home"]],
    ))

    sid = "twdc-epic-rivals"
    sets.append(make_set(sid, T, SAT, SAT_L,
        "Disney Epic Rivals", None, "box_set",
        "Mini-jumbo pin-on-pin, comes in custom box", None, 79.95, None, None, False,
        [make_pin(sid, None, n, 500) for n in [
            "Hades & Hercules", "Maleficent & 3 Fairies", "Lucifer & Mice",
            "Alice & Cheshire Cat", "Vanessa & Ariel"]],
    ))

    sid = "twdc-villains-sidekicks-mystery"
    s = make_set(sid, T, SAT, SAT_L,
        "Villains & Sidekicks Mystery Pin Box", None, "mystery",
        None, None, 32.95, "per box", PL5, False,
        [make_pin(sid, None, "Mystery Box", 400)],
    )
    s["pins"].extend([make_pin(sid, None, n, 400) for n in [
        "Hades, Pain, & Panic", "Maleficent & Diablo",
        "Ursula & Flotsam & Jetsam", "Cruella, Jasper, & Horace",
        "Mother Gothel & The Stabbington Brothers", "Gaston & LeFou",
        "Scar, Shenzi, Banzai, & Ed", "Lady Tremaine & Lucifer"]])
    sets.append(s)

    sid = "twdc-muppet-babies-mystery"
    s = make_set(sid, T, SAT, SAT_L,
        "Muppet Babies Mystery Pin Box", None, "mystery",
        None, None, 32.95, "per box", PL5, False,
        [make_pin(sid, None, "Mystery Box", 400)],
    )
    s["pins"].extend([make_pin(sid, None, n, 400) for n in [
        "Baby Kermit", "Baby Piggy", "Baby Fozzie", "Baby Gonzo",
        "Baby Animal", "Baby Scooter", "Baby Bunsen & Beaker", "Baby Rowlf"]])
    sets.append(s)


    # --- SUNDAY ---
    sid = "twdc-elements-fire"
    sets.append(make_set(sid, T, SUN, SUN_L,
        "Elements of Nature — Fire", None, "individual",
        "Gold metal base, pin-on-pin oval frame", None, 42.95, None, PL1, False,
        [make_pin(sid, None, n, 400) for n in [
            "Maleficent Dragon", "Chernabog", "Scar", "Ember", "Mushu", "Lotso"]],
    ))
    sid = "twdc-elements-water"
    sets.append(make_set(sid, T, SUN, SUN_L,
        "Elements of Nature — Water", None, "individual",
        "Gold metal base, pin-on-pin oval frame", None, 42.95, None, PL1, False,
        [make_pin(sid, None, n, 400) for n in [
            "Moana", "Sorcerer's Apprentice", "Simba & Friends", "Nemo & Dory",
            "Nokk & Elsa", "Wade"]],
    ))
    sid = "twdc-elements-wind"
    sets.append(make_set(sid, T, SUN, SUN_L,
        "Elements of Nature — Wind", None, "individual",
        "Silver metal base, pin-on-pin oval frame", None, 42.95, None, PL1, False,
        [make_pin(sid, None, n, 400) for n in [
            "Pocahontas", "Gale & Olaf", "Pooh & Piglet", "Bernard & Bianca",
            "Band Concert", "Wolf & Pigs"]],
    ))
    sid = "twdc-elements-earth"
    sets.append(make_set(sid, T, SUN, SUN_L,
        "Elements of Nature — Earth", None, "individual",
        "Silver metal base, pin-on-pin oval frame", None, 42.95, None, PL1, False,
        [make_pin(sid, None, n, 400) for n in [
            "Grandma Willow", "Mufasa & Simba", "Gaetan 'Mole' Moliere",
            "Sprite", "Flik & Dot", "Te Fiti"]],
    ))
    sid = "twdc-cat-astrophe"
    sets.append(make_set(sid, T, SUN, SUN_L,
        "Cat-astrophe", None, "individual", "Antique gold base, hard enamel",
        None, 34.95, None, PL1, False,
        [make_pin(sid, None, n, 400) for n in [
            "Yzma", "Toulouse", "Sergeant Tibbs", "Snowball", "Oliver",
            "Mr. Mittens", "Marie & Berlioz", "Madam Mim", "Machiavelli",
            "Lucifer", "Figaro", "Dinah", "Mochi", "Cheshire"]],
    ))
    sid = "twdc-table-for-one"
    sets.append(make_set(sid, T, SUN, SUN_L,
        "Table for One", None, "individual", "Villain dining scene pin-on-pin",
        None, 45.95, None, PL1, False,
        [make_pin(sid, None, n, 400) for n in [
            "Evil Queen", "Maleficent", "Captain Hook", "Cruella de Vil",
            "Ursula", "King Candy", "Hades", "Mother Gothel", "Yzma",
            "Ernesto de la Cruz", "Hans", "King Magnifico", "Madam Mim",
            "Prince John", "Dr. Facilier"]],
    ))
    sid = "twdc-enchanted-gowns"
    sets.append(make_set(sid, T, SUN, SUN_L,
        "Enchanted Gowns", None, "individual", "Gold base, glitter, small jewels",
        None, 34.95, None, PL1, False,
        [make_pin(sid, None, n, 400) for n in [
            "Snow White", "Cinderella", "Aurora", "Ariel", "Jasmine", "Belle",
            "Pocahontas", "Mulan", "Tiana", "Rapunzel", "Anna", "Elsa"]],
    ))
    sid = "twdc-pooh-mystery"
    s = make_set(sid, T, SUN, SUN_L,
        "Winnie the Pooh Mystery Pin Box", None, "mystery",
        None, None, 32.95, "per box", PL5, False,
        [make_pin(sid, None, "Mystery Box", 400)],
    )
    s["pins"].extend([make_pin(sid, None, n, 400) for n in [
        "Pooh with Flowers", "Birthday Pooh", "Pooh & Piglet", "Bedtime Pooh",
        "King Pooh", "Rainy Day Pooh", "Adventurer Pooh", "Pirate Pooh"]])
    sets.append(s)
    sid = "twdc-star-wars-galactic-mystery"
    s = make_set(sid, T, SUN, SUN_L,
        "Star Wars Galactic Pals Mystery Pin Box", None, "mystery",
        None, None, 32.95, "per box", PL5, False,
        [make_pin(sid, None, "Mystery Box", 400)],
    )
    s["pins"].extend([make_pin(sid, None, n, 400) for n in [
        "Porg", "Loth-Cat", "Gamorrean", "Ortolan", "Wookiee",
        "Tauntaun", "Ewok", "Rodian", "Huttlet"]])
    sets.append(s)

    return sets


# ---------------------------------------------------------------------------
# DSSH SETS
# ---------------------------------------------------------------------------

def build_dssh_sets():
    sets = []
    FRI, FRI_L = "2026-08-14", "Friday, August 14"
    SAT, SAT_L = "2026-08-15", "Saturday, August 15"
    SUN, SUN_L = "2026-08-16", "Sunday, August 16"
    D = "DSSH"
    PL1 = "Limit one (1) per person"
    PL5 = "Limit five (5) boxes per person"

    # --- FRIDAY ---
    sid = "dssh-premiere-el-capitan"
    sets.append(make_set(sid, D, FRI, FRI_L,
        "Premiere Collection — El Capitan 100 Years in Hollywood", None, "box_set",
        "Pin-on-pin + custom box", '5.04″W×3.425″H', 199.95, None, PL1, False,
        [make_pin(sid, None, "El Capitan 100 Years", 200)],
    ))

    sid = "dssh-artist-avengers"
    sets.append(make_set(sid, D, FRI, FRI_L,
        "Artist Series — Avengers: Endgame by Matt Ferguson", None, "individual",
        "3D laser print + custom backing card", '1.69″W×2.25″H', 29.95, None, PL1, False,
        [make_pin(sid, None, n, 400) for n in [
            "Ant-Man", "Iron Man", "Thanos", "Captain America", "Thor"]],
    ))

    sid = "dssh-all-in-a-name"
    sets.append(make_set(sid, D, FRI, FRI_L,
        "It's All in a Name Series", None, "individual",
        "Jumbo, two pin-on-pins, translucent, custom backing card", None, 49.95, None, PL1, False,
        [make_pin(sid, None, n, 400) for n in [
            "Ariel", "Belle", "Marie", "Ursula", "Stitch", "Maleficent",
            "Dumbo", "Kuzco", "Alice", "Aurora", "Hades", "Eeyore", "Goofy", "Moana"]],
    ))

    sid = "dssh-dragons-cuties"
    sets.append(make_set(sid, D, FRI, FRI_L,
        "Disney Dragons Cuties Series", None, "individual",
        "Custom backing card", None, 34.95, None, PL1, False,
        [make_pin(sid, None, n, 300) for n in [
            "Elliott", "Madam Mim", "Maleficent", "Sisu", "The Reluctant Dragon",
            "Queen Narissa", "Hydra", "The Gwythaints", "Blazey", "Mushu"]],
    ))

    sid = "dssh-best-in-show"
    sets.append(make_set(sid, D, FRI, FRI_L,
        "Best in Show Series", None, "individual",
        "Pin-on-pin", '1.27″W×2.0″H', 29.95, None, PL1, False,
        [make_pin(sid, None, n, 400) for n in [
            "Marie", "Lucifer", "Cheshire Cat", "Fifi the Peke", "Dinah", "Max",
            "Nana", "Dodger", "Little Brother", "Pongo", "Pluto", "Berlioz",
            "Toulouse", "Mochi"]],
    ))

    # Throwback Mystery with per-pin LE tiers
    sid = "dssh-throwback-mystery"
    s = make_set(sid, D, FRI, FRI_L,
        "Throwback Mystery Series", None, "mystery",
        None, None, 49.95, "per box", PL5, False, [])
    s["pins"] = [
        make_pin(sid, None, "Kim Possible Cheer", 400),
        make_pin(sid, None, "Ron and Rufus", 400),
        make_pin(sid, None, "Lizzie on Scooter", 400),
        make_pin(sid, None, "Lizzie Frame", 400),
        make_pin(sid, None, "Lizzie Heart", 400),
        make_pin(sid, None, "East High School", 400),
        make_pin(sid, None, "Troy and Gabriella", 400),
        make_pin(sid, None, "Rufus", 400),
    ]
    # Chasers
    for n in ["Kim Possible", "Lizzie Hooray", "Lizzie Flower Crown", "EHS Megaphone"]:
        p = make_pin(sid, None, n, 300)
        p["edition_notes"] = "chaser"
        s["pins"].append(p)
    # Super chasers
    for n in ["So Not the Drama", "Lizzie in Heels"]:
        p = make_pin(sid, None, n, 150)
        p["edition_notes"] = "super chaser"
        s["pins"].append(p)
    sets.append(s)

    # --- SATURDAY ---
    sid = "dssh-vinyl-starter"
    sets.append(make_set(sid, D, SAT, SAT_L,
        "Vinyl Records — Starter Set", None, "box_set",
        "Custom backing", '2.25″W×1.84″H player; 1.88″W×1.88″H vinyls', 89.95, None, None, False,
        [make_pin(sid, None, "Record Player + Sleeping Beauty + Pinocchio", 400)],
    ))

    sid = "dssh-vinyl-records"
    sets.append(make_set(sid, D, SAT, SAT_L,
        "Vinyl Records — Individual Vinyls", None, "individual",
        "Pin-on-pin, custom backing card", None, 32.95, None, PL1, False,
        [make_pin(sid, None, n, 400) for n in [
            "Tangled", "Hoppers", "Pocahontas", "Big Hero 6",
            "Snow White & the Seven Dwarfs", "Mulan", "Frozen", "Cinderella",
            "Dumbo", "Fantasia"]],
    ))

    sid = "dssh-unlocking-magic"
    sets.append(make_set(sid, D, SAT, SAT_L,
        "Unlocking the Magic Series", None, "individual",
        "Hinge pin, glitter fill, custom backing", None, 49.95, None, PL1, False,
        [make_pin(sid, None, n, 400) for n in [
            "The Little Mermaid", "Lilo & Stitch", "Mulan", "Sleeping Beauty",
            "Aladdin", "Rapunzel", "Big Hero 6", "Frozen", "Pinocchio",
            "Moana", "Dumbo", "Cinderella"]],
    ))

    sid = "dssh-duos"
    sets.append(make_set(sid, D, SAT, SAT_L,
        "Duos Series", None, "individual",
        "Stained glass, bookmark format, custom backing", '1.07″W×3.0″H', 74.95, None, PL1, False,
        [make_pin(sid, None, n, 400) for n in [
            "Anna & Elsa", "The Mandalorian & Grogu", "Goofy & Max",
            "Maui & Moana", "Deadpool & Wolverine", "Mr. & Mrs. Incredible",
            "Robin Hood & Little John", "Hercules & Megara", "Baymax & Hiro",
            "Ariel & Prince Eric", "Nick Wilde & Judy Hopps", "Lilo & Stitch"]],
    ))

    sid = "dssh-zootopia-cars"
    sets.append(make_set(sid, D, SAT, SAT_L,
        "Zootopia 10th Anniversary Car Series", None, "individual",
        "Characters driving cars", None, 24.95, None, PL1, False,
        [make_pin(sid, None, n, 300) for n in [
            "Judy Hopps", "Flash", "Finnick", "Nick Wilde", "Dawn Bellwether", "Chief Bogo"]],
    ))

    sid = "dssh-el-capitan-hinge"
    sets.append(make_set(sid, D, SAT, SAT_L,
        "El Capitan Theatre 100th — El Capitan 1926 Hinged Pin", None, "individual",
        "Antique gold", '1.83″W×2.25″H', 29.95, None, PL1, False,
        [make_pin(sid, None, "El Capitan 1926 Hinged Pin", 400)],
    ))

    sid = "dssh-el-capitan-characters"
    sets.append(make_set(sid, D, SAT, SAT_L,
        "El Capitan Theatre 100th — Character Pins", None, "individual",
        "Antique nickel + pin-on-pin", None, 24.95, None, PL1, False,
        [make_pin(sid, None, n, 400) for n in [
            "Mickey", "Minnie", "Oswald the Lucky Rabbit", "Donald", "Daisy",
            "Judy Hopps", "Nick Wilde"]],
    ))

    # --- SUNDAY ---
    sid = "dssh-tapestry"
    sets.append(make_set(sid, D, SUN, SUN_L,
        "Tapestry Series", None, "individual",
        "Pin-on-pin", '1.56″W×2.0″H', 32.95, None, PL1, False,
        [make_pin(sid, None, n, 400) for n in [
            "Miguel", "Alice", "Jasmine", "Jack and Sally", "Elsa", "Merida",
            "Rapunzel", "Briar Rose", "Yzma", "Maleficent", "Ursula", "Mirabel"]],
    ))

    sid = "dssh-duck-series"
    sets.append(make_set(sid, D, SUN, SUN_L,
        "Duck Series", None, "individual",
        "Pin-on-pin rubber duck characters", None, 32.95, None, PL1, False,
        [make_pin(sid, None, n, 400) for n in [
            "Stitch", "Lilo", "Maleficent", "Cruella", "Hades", "Jiminy Cricket",
            "Fairy Godmother", "Flora", "Fauna", "Merryweather", "Mad Hatter", "Panda Mei"]],
    ))

    sid = "dssh-cursive-cuties"
    sets.append(make_set(sid, D, SUN, SUN_L,
        "Cursive Cuties Series", None, "individual",
        "3D color paste, pin-on-pin, translucent fill", '2.5″W×2.5″H', 44.95, None, PL1, False,
        [make_pin(sid, None, n, 400) for n in [
            "Baymax", "Bing Bong", "Bolt", "Cheshire Cat", "Merryweather",
            "Grumpy", "Louis", "Meeko", "Flora", "Cri-Kee", "Mushu",
            "Oswald the Lucky Rabbit", "Scrump", "Fauna"]],
    ))

    sid = "dssh-goofy-movie-cuties"
    sets.append(make_set(sid, D, SUN, SUN_L,
        "A Goofy Movie Cuties Series", None, "individual",
        "Custom backing card", None, 34.95, None, PL1, False,
        [make_pin(sid, None, n, 300) for n in [
            "Goofy", "Max", "P.J. Pete", "Powerline", "Pete",
            "Bobby Zimuruski", "Roxanne", "Stacey"]],
    ))

    return sets


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

def apply_image_mappings(all_sets):
    """Map real image files to pins where available."""
    twdc_sun_dir = "images/twdc/sun"
    twdc_sat_dir = "images/twdc/sat"
    twdc_fri_dir = "images/twdc/fri"
    mappings = {
        # =====================================================================
        # MOG FRIDAY
        # =====================================================================
        # Alice Mystery (p02 — 12 individual pulls, no box image)
        "mog-alice-mystery-doorknob": "images/mog/fri/mog_p02_0108.png",
        "mog-alice-mystery-mad-hatter": "images/mog/fri/mog_p02_0110.png",
        "mog-alice-mystery-queen-of-hearts": "images/mog/fri/mog_p02_0112.png",
        "mog-alice-mystery-march-hare": "images/mog/fri/mog_p02_0114.png",
        "mog-alice-mystery-red-rose": "images/mog/fri/mog_p02_0116.png",
        "mog-alice-mystery-alice": "images/mog/fri/mog_p02_0118.png",
        "mog-alice-mystery-caterpillar": "images/mog/fri/mog_p02_0120.png",
        "mog-alice-mystery-dinah": "images/mog/fri/mog_p02_0122.png",
        "mog-alice-mystery-white-rabbit": "images/mog/fri/mog_p02_0124.png",
        "mog-alice-mystery-king-of-hearts": "images/mog/fri/mog_p02_0126.png",
        "mog-alice-mystery-tweedledee-tweedledum": "images/mog/fri/mog_p02_0128.png",
        "mog-alice-mystery-cheshire-cat": "images/mog/fri/mog_p02_0130.png",
        # Alice 75th Anniversary (p03 — 5 pins)
        "mog-alice-75th-2": "images/mog/fri/mog_p03_0175.png",
        "mog-alice-75th-3": "images/mog/fri/mog_p03_0177.png",
        "mog-alice-75th-4": "images/mog/fri/mog_p03_0179.png",
        "mog-alice-75th-5": "images/mog/fri/mog_p03_0181.png",
        "mog-alice-75th-6": "images/mog/fri/mog_p03_0183.png",
        # Princess Dream Windows (p04-p06 — 13 pins)
        "mog-princess-windows-7": "images/mog/fri/mog_p04_0232.png",
        "mog-princess-windows-8": "images/mog/fri/mog_p04_0234.png",
        "mog-princess-windows-9": "images/mog/fri/mog_p04_0236.png",
        "mog-princess-windows-10": "images/mog/fri/mog_p04_0230.png",
        "mog-princess-windows-11": "images/mog/fri/mog_p04_0228.png",
        "mog-princess-windows-12": "images/mog/fri/mog_p05_0283.png",
        "mog-princess-windows-13": "images/mog/fri/mog_p05_0285.png",
        "mog-princess-windows-14": "images/mog/fri/mog_p05_0287.png",
        "mog-princess-windows-15": "images/mog/fri/mog_p05_0281.png",
        "mog-princess-windows-16": "images/mog/fri/mog_p05_0289.png",
        "mog-princess-windows-17": "images/mog/fri/mog_p06_0335.png",
        "mog-princess-windows-18": "images/mog/fri/mog_p06_0337.png",
        "mog-princess-windows-19": "images/mog/fri/mog_p06_0339.png",
        # Treasure Seekers (p07 — 6 pins)
        "mog-treasure-seekers-21": "images/mog/fri/mog_p07_0392.png",
        "mog-treasure-seekers-22": "images/mog/fri/mog_p07_0394.png",
        "mog-treasure-seekers-23": "images/mog/fri/mog_p07_0396.png",
        "mog-treasure-seekers-24": "images/mog/fri/mog_p07_0398.png",
        "mog-treasure-seekers-25": "images/mog/fri/mog_p07_0400.png",
        "mog-treasure-seekers-26": "images/mog/fri/mog_p07_0402.png",
        # Squad Goals (p08-p09 — 10 pins)
        "mog-squad-goals-27": "images/mog/fri/mog_p08_0447.png",
        "mog-squad-goals-28": "images/mog/fri/mog_p08_0453.png",
        "mog-squad-goals-29": "images/mog/fri/mog_p08_0455.png",
        "mog-squad-goals-30": "images/mog/fri/mog_p08_0449.png",
        "mog-squad-goals-31": "images/mog/fri/mog_p08_0451.png",
        "mog-squad-goals-32": "images/mog/fri/mog_p09_0500.png",
        "mog-squad-goals-33": "images/mog/fri/mog_p09_0506.png",
        "mog-squad-goals-34": "images/mog/fri/mog_p09_0508.png",
        "mog-squad-goals-35": "images/mog/fri/mog_p09_0502.png",
        "mog-squad-goals-36": "images/mog/fri/mog_p09_0504.png",
        # POV: Another Point of View (p10-p11 — 10 pins, 2 photos each = front/back of spinner)
        # p10: pairs (593,595), (597,599), (601,603), (605,607), (609,611)
        # p11: pairs (696,698), (700,702), (704,706), (708,710), (712,714)
        "mog-pov-37": "images/mog/fri/mog_p10_0593.png",
        "mog-pov-38": "images/mog/fri/mog_p10_0605.png",
        "mog-pov-39": "images/mog/fri/mog_p10_0601.png",
        "mog-pov-40": "images/mog/fri/mog_p10_0609.png",
        "mog-pov-41": "images/mog/fri/mog_p10_0597.png",
        "mog-pov-42": "images/mog/fri/mog_p11_0700.png",
        "mog-pov-43": "images/mog/fri/mog_p11_0696.png",
        "mog-pov-44": "images/mog/fri/mog_p11_0704.png",
        "mog-pov-45": "images/mog/fri/mog_p11_0708.png",
        "mog-pov-46": "images/mog/fri/mog_p11_0712.png",
        # Dining with Character (p12-p14 — 10 pins)
        "mog-dining-character-47": "images/mog/fri/mog_p12_0750.png",
        "mog-dining-character-48": "images/mog/fri/mog_p12_0754.png",
        "mog-dining-character-49": "images/mog/fri/mog_p12_0756.png",
        "mog-dining-character-50": "images/mog/fri/mog_p12_0752.png",
        "mog-dining-character-51": "images/mog/fri/mog_p13_0798.png",
        "mog-dining-character-52": "images/mog/fri/mog_p13_0792.png",
        "mog-dining-character-53": "images/mog/fri/mog_p13_0794.png",
        "mog-dining-character-54": "images/mog/fri/mog_p13_0796.png",
        "mog-dining-character-55": "images/mog/fri/mog_p14_0822.png",
        "mog-dining-character-56": "images/mog/fri/mog_p14_0824.png",
        # World Princess Week Ultra Jumbo (p15)
        "mog-world-princess-ultra-57": "images/mog/fri/mog_p15_0837.png",

        # =====================================================================
        # MOG SATURDAY
        # =====================================================================
        # S.E.A. Mystery — 14 individual pulls (mystery box uses placeholder)
        "mog-sea-mystery-mary-oceaneer": "images/mog/sat/mog_sea_mystery_01.png",
        "mog-sea-mystery-duncan-the-parrot": "images/mog/sat/mog_sea_mystery_02.png",
        "mog-sea-mystery-alberta-falls": "images/mog/sat/mog_sea_mystery_03.png",
        "mog-sea-mystery-albert-falls": "images/mog/sat/mog_sea_mystery_04.png",
        "mog-sea-mystery-pin-5": "images/mog/sat/mog_sea_mystery_05.png",
        "mog-sea-mystery-dr-kon-chunosuke": "images/mog/sat/mog_sea_mystery_06.png",
        "mog-sea-mystery-camellia-falco": "images/mog/sat/mog_sea_mystery_07.png",
        "mog-sea-mystery-sea-member": "images/mog/sat/mog_sea_mystery_08.png",
        "mog-sea-mystery-harrison-hightower-iii": "images/mog/sat/mog_sea_mystery_09.png",
        "mog-sea-mystery-barnabas-t-bullion": "images/mog/sat/mog_sea_mystery_10.png",
        "mog-sea-mystery-lord-henry-mystic": "images/mog/sat/mog_sea_mystery_11.png",
        "mog-sea-mystery-albert": "images/mog/sat/mog_sea_mystery_12.png",
        "mog-sea-mystery-pin-13": "images/mog/sat/mog_sea_mystery_13.png",
        "mog-sea-mystery-shiriki-utundu": "images/mog/sat/mog_sea_mystery_14.png",
        # Parks to Ports (p19-p20 — 7 pins)
        "mog-parks-to-ports-59": "images/mog/sat/mog_p19_1010.png",
        "mog-parks-to-ports-60": "images/mog/sat/mog_p19_1012.png",
        "mog-parks-to-ports-61": "images/mog/sat/mog_p19_1008.png",
        "mog-parks-to-ports-62": "images/mog/sat/mog_p19_1014.png",
        "mog-parks-to-ports-63": "images/mog/sat/mog_p20_1043.png",
        "mog-parks-to-ports-64": "images/mog/sat/mog_p20_1045.png",
        "mog-parks-to-ports-65": "images/mog/sat/mog_p20_1047.png",
        # Park Stamps Series 2 (custom named files + p21 + p22 — 15 pins)
        "mog-park-stamps-2-66": "images/mog/sat/mog_park_stamps_row1_01.png",
        "mog-park-stamps-2-67": "images/mog/sat/mog_park_stamps_row1_02.png",
        "mog-park-stamps-2-68": "images/mog/sat/mog_park_stamps_row1_03.png",
        "mog-park-stamps-2-69": "images/mog/sat/mog_park_stamps_row1_04.png",
        "mog-park-stamps-2-70": "images/mog/sat/mog_p21_1078.png",
        "mog-park-stamps-2-71": "images/mog/sat/mog_park_stamps_row2_01.png",
        "mog-park-stamps-2-72": "images/mog/sat/mog_park_stamps_row2_02.png",
        "mog-park-stamps-2-73": "images/mog/sat/mog_park_stamps_row2_03.png",
        "mog-park-stamps-2-74": "images/mog/sat/mog_p22_1162.png",
        "mog-park-stamps-2-75": "images/mog/sat/mog_p22_1150.png",
        "mog-park-stamps-2-76": "images/mog/sat/mog_p22_1160.png",
        "mog-park-stamps-2-77": "images/mog/sat/mog_p22_1152.png",
        "mog-park-stamps-2-78": "images/mog/sat/mog_p22_1154.png",
        "mog-park-stamps-2-79": "images/mog/sat/mog_p22_1156.png",
        "mog-park-stamps-2-80": "images/mog/sat/mog_p22_1158.png",
        # Panoramas Gate-fold (p23-p24 — 8 pins, 2 images each)
        "mog-panoramas-81": "images/mog/sat/mog_p23_1235.png",
        "mog-panoramas-82": "images/mog/sat/mog_p23_1239.png",
        "mog-panoramas-83": "images/mog/sat/mog_p23_1243.png",
        "mog-panoramas-84": "images/mog/sat/mog_p23_1247.png",
        "mog-panoramas-85": "images/mog/sat/mog_p24_1326.png",
        "mog-panoramas-86": "images/mog/sat/mog_p24_1330.png",
        "mog-panoramas-87": "images/mog/sat/mog_p24_1334.png",
        "mog-panoramas-88": "images/mog/sat/mog_p24_1322.png",
        # Carousel Horses (p25)
        "mog-carousel-horses-89": "images/mog/sat/mog_p25_1357.png",
        "mog-carousel-horses-mickey": "images/mog/sat/mog_p25_carousel_01.png",
        "mog-carousel-horses-minnie": "images/mog/sat/mog_p25_carousel_02.png",
        "mog-carousel-horses-donald": "images/mog/sat/mog_p25_carousel_03.png",
        "mog-carousel-horses-goofy": "images/mog/sat/mog_p25_carousel_04.png",
        "mog-carousel-horses-clarabelle": "images/mog/sat/mog_p25_carousel_05.png",
        "mog-carousel-horses-daisy": "images/mog/sat/mog_p25_carousel_06.png",

        # =====================================================================
        # TWDC FRIDAY
        # =====================================================================
        # Disney Stamp Classic Era (PDF layout: left column top-to-bottom, then right column)
        "twdc-disney-stamp-classic-dumbo-timothy": f"{twdc_fri_dir}/fri_stamp_p2_007.png",
        "twdc-disney-stamp-classic-donald-aracuan-bird": f"{twdc_fri_dir}/fri_stamp_p2_011.png",
        "twdc-disney-stamp-classic-alice-white-rabbit": f"{twdc_fri_dir}/fri_stamp_p2_013.png",
        "twdc-disney-stamp-classic-chip-dale": f"{twdc_fri_dir}/fri_stamp_p2_015.png",
        "twdc-disney-stamp-classic-blue-fairy-jiminy": f"{twdc_fri_dir}/fri_stamp_p2_017.png",
        "twdc-disney-stamp-classic-pooh-piglet": f"{twdc_fri_dir}/fri_stamp_p2_009.png",
        "twdc-disney-stamp-classic-robin-hood-little-john": f"{twdc_fri_dir}/fri_stamp_p2_025.png",
        "twdc-disney-stamp-classic-merlin-archimedes": f"{twdc_fri_dir}/fri_stamp_p2_023.png",
        "twdc-disney-stamp-classic-maleficent-dragon-prince-phillip": f"{twdc_fri_dir}/fri_stamp_p2_021.png",
        "twdc-disney-stamp-classic-yensid-sorcerer-mickey": f"{twdc_fri_dir}/fri_stamp_p2_019.png",
        # Disney Stamp Renaissance Era (same layout pattern as Classic)
        "twdc-disney-stamp-renaissance-ariel-scuttle": f"{twdc_fri_dir}/fri_stamp_p3_030.png",
        "twdc-disney-stamp-renaissance-tiana-charlotte": f"{twdc_fri_dir}/fri_stamp_p3_032.png",
        "twdc-disney-stamp-renaissance-bernard-bianca": f"{twdc_fri_dir}/fri_stamp_p3_034.png",
        "twdc-disney-stamp-renaissance-belle-maurice": f"{twdc_fri_dir}/fri_stamp_p3_036.png",
        "twdc-disney-stamp-renaissance-hercules-phil": f"{twdc_fri_dir}/fri_stamp_p3_038.png",
        "twdc-disney-stamp-renaissance-dodger-oliver": f"{twdc_fri_dir}/fri_stamp_p3_040.png",
        "twdc-disney-stamp-renaissance-todd-copper": f"{twdc_fri_dir}/fri_stamp_p3_042.png",
        "twdc-disney-stamp-renaissance-mulan-mushu": f"{twdc_fri_dir}/fri_stamp_p3_044.png",
        "twdc-disney-stamp-renaissance-kronk-yzma": f"{twdc_fri_dir}/fri_stamp_p3_046.png",
        "twdc-disney-stamp-renaissance-lilo-stitch": f"{twdc_fri_dir}/fri_stamp_p3_048.png",
        # Disney Stamp Modern Era (same layout pattern as Classic)
        "twdc-disney-stamp-modern-anna-olaf": f"{twdc_fri_dir}/fri_stamp_p4_053.png",
        "twdc-disney-stamp-modern-gazelle-tiger": f"{twdc_fri_dir}/fri_stamp_p4_055.png",
        "twdc-disney-stamp-modern-baymax-hiro": f"{twdc_fri_dir}/fri_stamp_p4_057.png",
        "twdc-disney-stamp-modern-judy-nick": f"{twdc_fri_dir}/fri_stamp_p4_059.png",
        "twdc-disney-stamp-modern-moana-hei-hei": f"{twdc_fri_dir}/fri_stamp_p4_061.png",
        "twdc-disney-stamp-modern-wreck-it-ralph-vanellope": f"{twdc_fri_dir}/fri_stamp_p4_065.png",
        "twdc-disney-stamp-modern-rapunzel-pascal": f"{twdc_fri_dir}/fri_stamp_p4_063.png",
        "twdc-disney-stamp-modern-elsa-bruni": f"{twdc_fri_dir}/fri_stamp_p4_067.png",
        "twdc-disney-stamp-modern-raya-tuk-tuk": f"{twdc_fri_dir}/fri_stamp_p4_069.png",
        "twdc-disney-stamp-modern-valentino-star": f"{twdc_fri_dir}/fri_stamp_p4_071.png",
        # Reel of Magic (2 top images, then 2 rows of 5 and 4)
        "twdc-reel-of-magic-the-little-mermaid": f"{twdc_fri_dir}/fri_reel_top1_01.png",
        "twdc-reel-of-magic-beauty-and-the-beast": f"{twdc_fri_dir}/fri_reel_top1_02.png",
        "twdc-reel-of-magic-aladdin": f"{twdc_fri_dir}/fri_reel_row1_01.png",
        "twdc-reel-of-magic-the-lion-king": f"{twdc_fri_dir}/fri_reel_row1_02.png",
        "twdc-reel-of-magic-pocahontas": f"{twdc_fri_dir}/fri_reel_row1_03.png",
        "twdc-reel-of-magic-the-hunchback-of-notre-dame": f"{twdc_fri_dir}/fri_reel_row1_04.png",
        "twdc-reel-of-magic-mulan": f"{twdc_fri_dir}/fri_reel_row2_01.png",
        "twdc-reel-of-magic-tarzan": f"{twdc_fri_dir}/fri_reel_row2_02.png",
        "twdc-reel-of-magic-emperors-new-groove": f"{twdc_fri_dir}/fri_reel_row2_03.png",
        "twdc-reel-of-magic-atlantis": f"{twdc_fri_dir}/fri_reel_row2_04.png",
        "twdc-reel-of-magic-hercules": f"{twdc_fri_dir}/fri_reel_row1_05.png",
        # Royal Chambers (PDF layout: 1 featured, then right col 10-14, left col 2-7, bottom 8-9)
        "twdc-royal-chambers-evil-queen": f"{twdc_fri_dir}/fri_royal_p6_089.png",
        "twdc-royal-chambers-emperor": f"{twdc_fri_dir}/fri_royal_p6_091.png",
        "twdc-royal-chambers-kuzco": f"{twdc_fri_dir}/fri_royal_p6_093.png",
        "twdc-royal-chambers-king-magnifico": f"{twdc_fri_dir}/fri_royal_p6_095.png",
        "twdc-royal-chambers-king-candy": f"{twdc_fri_dir}/fri_royal_p6_097.png",
        "twdc-royal-chambers-elsa": f"{twdc_fri_dir}/fri_royal_p6_099.png",
        "twdc-royal-chambers-prince-charming": f"{twdc_fri_dir}/fri_royal_p6_101.png",
        "twdc-royal-chambers-queen-of-hearts": f"{twdc_fri_dir}/fri_royal_p6_103.png",
        "twdc-royal-chambers-king-stefan-queen-leah": f"{twdc_fri_dir}/fri_royal_p6_105.png",
        "twdc-royal-chambers-king-arthur": f"{twdc_fri_dir}/fri_royal_p6_107.png",
        "twdc-royal-chambers-triton": f"{twdc_fri_dir}/fri_royal_p6_109.png",
        "twdc-royal-chambers-gaston": f"{twdc_fri_dir}/fri_royal_p6_111.png",
        "twdc-royal-chambers-sultan": f"{twdc_fri_dir}/fri_royal_p6_113.png",
        "twdc-royal-chambers-zeus": f"{twdc_fri_dir}/fri_royal_p6_115.png",
        # Role Models (same layout pattern as Royal Chambers)
        "twdc-role-models-rafiki-simba": f"{twdc_fri_dir}/fri_royal_p7_120.png",
        "twdc-role-models-ancestor-mulan": f"{twdc_fri_dir}/fri_royal_p7_126.png",
        "twdc-role-models-auguste-gusteau-remy": f"{twdc_fri_dir}/fri_royal_p7_124.png",
        "twdc-role-models-hector-miguel": f"{twdc_fri_dir}/fri_royal_p7_128.png",
        "twdc-role-models-tadashi-hiro": f"{twdc_fri_dir}/fri_royal_p7_136.png",
        "twdc-role-models-carl-russel": f"{twdc_fri_dir}/fri_royal_p7_130.png",
        "twdc-role-models-jiminy-pinocchio": f"{twdc_fri_dir}/fri_royal_p7_132.png",
        "twdc-role-models-tala-moana": f"{twdc_fri_dir}/fri_royal_p7_134.png",
        "twdc-role-models-mei-mei-ming": f"{twdc_fri_dir}/fri_royal_p7_122.png",
        "twdc-role-models-merlin-arthur": f"{twdc_fri_dir}/fri_royal_p7_138.png",
        "twdc-role-models-grandmother-willow-pocahontas": f"{twdc_fri_dir}/fri_royal_p7_140.png",
        "twdc-role-models-phil-hercules": f"{twdc_fri_dir}/fri_royal_p7_142.png",
        "twdc-role-models-fairy-godmother-cinderella": f"{twdc_fri_dir}/fri_royal_p7_144.png",
        "twdc-role-models-timothy-mouse-dumbo": f"{twdc_fri_dir}/fri_royal_p7_146.png",
        # Disney D's Mystery
        "twdc-disney-d-mystery-mystery-box": f"{twdc_fri_dir}/fri_disney_ds_box.png",
        "twdc-disney-d-mystery-mickey": f"{twdc_fri_dir}/fri_disney_ds_01.png",
        "twdc-disney-d-mystery-minnie": f"{twdc_fri_dir}/fri_disney_ds_02.png",
        "twdc-disney-d-mystery-goofy": f"{twdc_fri_dir}/fri_disney_ds_03.png",
        "twdc-disney-d-mystery-daisy": f"{twdc_fri_dir}/fri_disney_ds_04.png",
        "twdc-disney-d-mystery-pluto": f"{twdc_fri_dir}/fri_disney_ds_05.png",
        "twdc-disney-d-mystery-chip-dale": f"{twdc_fri_dir}/fri_disney_ds_06.png",
        "twdc-disney-d-mystery-donald": f"{twdc_fri_dir}/fri_disney_ds_07.png",
        "twdc-disney-d-mystery-blank-d": f"{twdc_fri_dir}/fri_disney_ds_08.png",
        # Disney Princess Mystery
        "twdc-princess-mystery-mystery-box": f"{twdc_fri_dir}/fri_princess_mystery_box.png",
        "twdc-princess-mystery-ariel": f"{twdc_fri_dir}/fri_princess_mystery_01.png",
        "twdc-princess-mystery-moana": f"{twdc_fri_dir}/fri_princess_mystery_02.png",
        "twdc-princess-mystery-tiana": f"{twdc_fri_dir}/fri_princess_mystery_03.png",
        "twdc-princess-mystery-belle": f"{twdc_fri_dir}/fri_princess_mystery_04.png",
        "twdc-princess-mystery-rapunzel": f"{twdc_fri_dir}/fri_princess_mystery_05.png",
        "twdc-princess-mystery-pocahontas": f"{twdc_fri_dir}/fri_princess_mystery_06.png",
        "twdc-princess-mystery-jasmine": f"{twdc_fri_dir}/fri_princess_mystery_07.png",
        "twdc-princess-mystery-cinderella": f"{twdc_fri_dir}/fri_princess_mystery_08.png",
        # Framed — Friday
        "twdc-framed-color-shades-of-magic-color-shades-of-magic-framed": f"{twdc_fri_dir}/fri_framed_color_shades.png",
        "twdc-framed-the-songs-we-grew-up-with-the-songs-we-grew-up-with-framed": f"{twdc_fri_dir}/fri_framed_songs.png",
        "twdc-framed-friends-from-around-the-world-friends-from-around-the-world-framed": f"{twdc_fri_dir}/fri_framed_friends_world.png",
        "twdc-framed-35-years-of-mermaid-emotions-35-years-of-mermaid-emotions-framed": f"{twdc_fri_dir}/fri_framed_mermaid_emotions.png",
        "twdc-framed-spirit-of-family-spirit-of-family-framed": f"{twdc_fri_dir}/fri_framed_spirit_family.png",
        "twdc-framed-pixar-animation-studios-pixar-animation-studios-framed": f"{twdc_fri_dir}/fri_framed_pixar_studios.png",
        "twdc-framed-encanto-tiles-encanto-tiles-framed": f"{twdc_fri_dir}/fri_framed_encanto_tiles.png",
        "twdc-framed-villains-villains-framed": f"{twdc_fri_dir}/fri_framed_villains.png",
        "twdc-framed-the-ultimate-disney-fan-event-2024-the-ultimate-disney-fan-event-2024-framed": f"{twdc_fri_dir}/fri_framed_fan_event.png",
        # =====================================================================
        # TWDC SATURDAY
        # =====================================================================
        # Pixar Stamp Series 1
        "twdc-pixar-stamp-1-buzz-woody": f"{twdc_sat_dir}/sat_pixar_p2_01.png",
        "twdc-pixar-stamp-1-heimlich-flik": f"{twdc_sat_dir}/sat_pixar_p2_02.png",
        "twdc-pixar-stamp-1-jessie-bullseye": f"{twdc_sat_dir}/sat_pixar_p2_03.png",
        "twdc-pixar-stamp-1-sulley-boo": f"{twdc_sat_dir}/sat_pixar_p2_04.png",
        "twdc-pixar-stamp-1-nemo-crush": f"{twdc_sat_dir}/sat_pixar_p2_05.png",
        "twdc-pixar-stamp-1-mr-incredible-frozone": f"{twdc_sat_dir}/sat_pixar_p2_06.png",
        "twdc-pixar-stamp-1-lightning-mcqueen-mater": f"{twdc_sat_dir}/sat_pixar_p2_07.png",
        "twdc-pixar-stamp-1-linguini-remy": f"{twdc_sat_dir}/sat_pixar_p2_08.png",
        "twdc-pixar-stamp-1-wall-e-eve": f"{twdc_sat_dir}/sat_pixar_p2_09.png",
        "twdc-pixar-stamp-1-carl-ellie": f"{twdc_sat_dir}/sat_pixar_p2_10.png",
        # Pixar Stamp Series 2
        "twdc-pixar-stamp-2-gus-the-cloud-peck-the-stork": f"{twdc_sat_dir}/sat_pixar_p3_01.png",
        "twdc-pixar-stamp-2-lotso-mr-pricklepants": f"{twdc_sat_dir}/sat_pixar_p3_02.png",
        "twdc-pixar-stamp-2-young-boy-papa": f"{twdc_sat_dir}/sat_pixar_p3_03.png",
        "twdc-pixar-stamp-2-queen-elinor-merida": f"{twdc_sat_dir}/sat_pixar_p3_04.png",
        "twdc-pixar-stamp-2-mike-squishy": f"{twdc_sat_dir}/sat_pixar_p3_05.png",
        "twdc-pixar-stamp-2-joy-bing-bong": f"{twdc_sat_dir}/sat_pixar_p3_06.png",
        "twdc-pixar-stamp-2-arlo-spot": f"{twdc_sat_dir}/sat_pixar_p3_07.png",
        "twdc-pixar-stamp-2-dory-hank": f"{twdc_sat_dir}/sat_pixar_p3_08.png",
        "twdc-pixar-stamp-2-miguel-dante": f"{twdc_sat_dir}/sat_pixar_p3_09.png",
        "twdc-pixar-stamp-2-edna-mode-jack-jack": f"{twdc_sat_dir}/sat_pixar_p3_10.png",
        # Pixar Stamp Series 3
        "twdc-pixar-stamp-3-bonnie-forky": f"{twdc_sat_dir}/sat_pixar_p4_01.png",
        "twdc-pixar-stamp-3-ian-barley": f"{twdc_sat_dir}/sat_pixar_p4_02.png",
        "twdc-pixar-stamp-3-joe-22": f"{twdc_sat_dir}/sat_pixar_p4_03.png",
        "twdc-pixar-stamp-3-luca-alberto": f"{twdc_sat_dir}/sat_pixar_p4_04.png",
        "twdc-pixar-stamp-3-dug-carl": f"{twdc_sat_dir}/sat_pixar_p4_05.png",
        "twdc-pixar-stamp-3-meilin-ming": f"{twdc_sat_dir}/sat_pixar_p4_06.png",
        "twdc-pixar-stamp-3-ember-wade": f"{twdc_sat_dir}/sat_pixar_p4_07.png",
        "twdc-pixar-stamp-3-paula-xeni": f"{twdc_sat_dir}/sat_pixar_p4_08.png",
        "twdc-pixar-stamp-3-anxiety-sadness": f"{twdc_sat_dir}/sat_pixar_p4_09.png",
        "twdc-pixar-stamp-3-elio-glordon": f"{twdc_sat_dir}/sat_pixar_p4_10.png",
        # Game Changers
        "twdc-game-changers-ariel": f"{twdc_sat_dir}/sat_game_changers_01.png",
        "twdc-game-changers-belle": f"{twdc_sat_dir}/sat_game_changers_02.png",
        "twdc-game-changers-jasmine": f"{twdc_sat_dir}/sat_game_changers_03.png",
        "twdc-game-changers-pocahontas": f"{twdc_sat_dir}/sat_game_changers_04.png",
        "twdc-game-changers-esmeralda": f"{twdc_sat_dir}/sat_game_changers_05.png",
        "twdc-game-changers-megara": f"{twdc_sat_dir}/sat_game_changers_06.png",
        "twdc-game-changers-mulan": f"{twdc_sat_dir}/sat_game_changers_07.png",
        "twdc-game-changers-tiana": f"{twdc_sat_dir}/sat_game_changers_08.png",
        "twdc-game-changers-rapunzel": f"{twdc_sat_dir}/sat_game_changers_09.png",
        "twdc-game-changers-merida": f"{twdc_sat_dir}/sat_game_changers_10.png",
        "twdc-game-changers-moana": f"{twdc_sat_dir}/sat_game_changers_11.png",
        "twdc-game-changers-anna": f"{twdc_sat_dir}/sat_game_changers_12.png",
        "twdc-game-changers-elsa": f"{twdc_sat_dir}/sat_game_changers_13.png",
        "twdc-game-changers-raya": f"{twdc_sat_dir}/sat_game_changers_14.png",
        "twdc-game-changers-vanellope": f"{twdc_sat_dir}/sat_game_changers_15.png",
        "twdc-game-changers-mirabel": f"{twdc_sat_dir}/sat_game_changers_16.png",
        # Welcome Home (partial — strip images mapped to first pins in each strip)
        "twdc-welcome-home-carl-ellies-home": f"{twdc_sat_dir}/sat_home_strip1_01.png",
        "twdc-welcome-home-mulans-family-home": f"{twdc_sat_dir}/sat_home_strip1_02.png",
        "twdc-welcome-home-geppettos-workshop": f"{twdc_sat_dir}/sat_home_strip1_03.png",
        "twdc-welcome-home-robinsons-family-lab": f"{twdc_sat_dir}/sat_home_strip1_04.png",
        "twdc-welcome-home-snow-whites-cottage": f"{twdc_sat_dir}/sat_home_strip2_01.png",
        "twdc-welcome-home-belles-cottage": f"{twdc_sat_dir}/sat_home_strip2_02.png",
        "twdc-welcome-home-lilos-home": f"{twdc_sat_dir}/sat_home_strip2_03.png",
        "twdc-welcome-home-the-incredibles-home": f"{twdc_sat_dir}/sat_home_strip3_01.png",
        "twdc-welcome-home-tinkerbells-home": f"{twdc_sat_dir}/sat_home_strip4_01.png",
        "twdc-welcome-home-white-rabbits-home": f"{twdc_sat_dir}/sat_home_strip5_01.png",
        "twdc-welcome-home-winnie-the-poohs-home": f"{twdc_sat_dir}/sat_home_strip5_02.png",
        "twdc-welcome-home-casa-madrigal": f"{twdc_sat_dir}/sat_home_single_108.png",
        "twdc-welcome-home-roger-anitas-home": f"{twdc_sat_dir}/sat_home_single_110.png",
        "twdc-welcome-home-lady-tramps-home": f"{twdc_sat_dir}/sat_home_single_112.png",
        # Disney Epic Rivals
        "twdc-epic-rivals-hades-hercules": f"{twdc_sat_dir}/sat_epic_rivals_181.png",
        "twdc-epic-rivals-maleficent-3-fairies": f"{twdc_sat_dir}/sat_epic_rivals_183.png",
        "twdc-epic-rivals-lucifer-mice": f"{twdc_sat_dir}/sat_epic_rivals_187.png",
        "twdc-epic-rivals-alice-cheshire-cat": f"{twdc_sat_dir}/sat_epic_rivals_173.png",
        "twdc-epic-rivals-vanessa-ariel": f"{twdc_sat_dir}/sat_epic_rivals_175.png",
        # Villains & Sidekicks Mystery
        "twdc-villains-sidekicks-mystery-mystery-box": f"{twdc_sat_dir}/sat_villains_mystery_card.png",
        "twdc-villains-sidekicks-mystery-hades-pain-panic": f"{twdc_sat_dir}/sat_villains_mystery_05.png",
        "twdc-villains-sidekicks-mystery-maleficent-diablo": f"{twdc_sat_dir}/sat_villains_mystery_01.png",
        "twdc-villains-sidekicks-mystery-ursula-flotsam-jetsam": f"{twdc_sat_dir}/sat_villains_mystery_07.png",
        "twdc-villains-sidekicks-mystery-cruella-jasper-horace": f"{twdc_sat_dir}/sat_villains_mystery_04.png",
        "twdc-villains-sidekicks-mystery-mother-gothel-the-stabbington-brothers": f"{twdc_sat_dir}/sat_villains_mystery_06.png",
        "twdc-villains-sidekicks-mystery-gaston-lefou": f"{twdc_sat_dir}/sat_villains_mystery_09.png",
        "twdc-villains-sidekicks-mystery-scar-shenzi-banzai-ed": f"{twdc_sat_dir}/sat_villains_mystery_02.png",
        "twdc-villains-sidekicks-mystery-lady-tremaine-lucifer": f"{twdc_sat_dir}/sat_villains_mystery_08.png",
        # Muppet Babies Mystery
        "twdc-muppet-babies-mystery-mystery-box": f"{twdc_sat_dir}/sat_muppet_mystery_card.png",
        "twdc-muppet-babies-mystery-baby-kermit": f"{twdc_sat_dir}/sat_muppet_mystery_04.png",
        "twdc-muppet-babies-mystery-baby-piggy": f"{twdc_sat_dir}/sat_muppet_mystery_06.png",
        "twdc-muppet-babies-mystery-baby-fozzie": f"{twdc_sat_dir}/sat_muppet_mystery_08.png",
        "twdc-muppet-babies-mystery-baby-gonzo": f"{twdc_sat_dir}/sat_muppet_mystery_07.png",
        "twdc-muppet-babies-mystery-baby-animal": f"{twdc_sat_dir}/sat_muppet_mystery_01.png",
        "twdc-muppet-babies-mystery-baby-scooter": f"{twdc_sat_dir}/sat_muppet_mystery_03.png",
        "twdc-muppet-babies-mystery-baby-bunsen-beaker": f"{twdc_sat_dir}/sat_muppet_mystery_02.png",
        "twdc-muppet-babies-mystery-baby-rowlf": f"{twdc_sat_dir}/sat_muppet_mystery_05.png",
        # Framed — Saturday
        "twdc-framed-star-wars-stamps-star-wars-stamps-framed": f"{twdc_sat_dir}/sat_framed_starwars_stamps.png",
        "twdc-framed-a-day-at-the-studio-lot-a-day-at-the-studio-lot-framed": f"{twdc_sat_dir}/sat_framed_studio_lot.png",
        "twdc-framed-seasons-of-friendship-seasons-of-friendship-framed": f"{twdc_sat_dir}/sat_framed_seasons_friendship.png",
        "twdc-framed-princess-ballerinas-princess-ballerinas-framed": f"{twdc_sat_dir}/sat_framed_princess_ballerinas.png",
        "twdc-framed-villains-premier-season-villains-premier-season-framed": f"{twdc_sat_dir}/sat_framed_villains_premier.png",
        "twdc-framed-d23-15th-anniversary-cakes-d23-15th-anniversary-cakes-framed": f"{twdc_sat_dir}/sat_framed_d23_cakes.png",
        "twdc-framed-princess-friends-princess-friends-framed": f"{twdc_sat_dir}/sat_framed_princess_friends.png",
        "twdc-framed-mickeys-city-outfits-mickeys-city-outfits-framed": f"{twdc_sat_dir}/sat_framed_mickeys_city.png",
        "twdc-framed-be-my-valentine-be-my-valentine-framed": f"{twdc_sat_dir}/sat_framed_be_my_valentine.png",

        # =====================================================================
        # TWDC SUNDAY
        # =====================================================================
        # Elements of Nature — Fire
        "twdc-elements-fire-maleficent-dragon": f"{twdc_sun_dir}/elements_fire_01.png",
        "twdc-elements-fire-chernabog": f"{twdc_sun_dir}/elements_fire_02.png",
        "twdc-elements-fire-scar": f"{twdc_sun_dir}/elements_fire_03.png",
        "twdc-elements-fire-ember": f"{twdc_sun_dir}/elements_fire_04.png",
        "twdc-elements-fire-mushu": f"{twdc_sun_dir}/elements_fire_05.png",
        "twdc-elements-fire-lotso": f"{twdc_sun_dir}/elements_fire_06.png",
        # Elements of Nature — Water
        "twdc-elements-water-moana": f"{twdc_sun_dir}/elements_water_01.png",
        "twdc-elements-water-sorcerers-apprentice": f"{twdc_sun_dir}/elements_water_02.png",
        "twdc-elements-water-simba-friends": f"{twdc_sun_dir}/elements_water_03.png",
        "twdc-elements-water-nemo-dory": f"{twdc_sun_dir}/elements_water_04.png",
        "twdc-elements-water-nokk-elsa": f"{twdc_sun_dir}/elements_water_05.png",
        "twdc-elements-water-wade": f"{twdc_sun_dir}/elements_water_06.png",
        # Elements of Nature — Wind
        "twdc-elements-wind-pocahontas": f"{twdc_sun_dir}/elements_wind_01.png",
        "twdc-elements-wind-gale-olaf": f"{twdc_sun_dir}/elements_wind_02.png",
        "twdc-elements-wind-pooh-piglet": f"{twdc_sun_dir}/elements_wind_03.png",
        "twdc-elements-wind-bernard-bianca": f"{twdc_sun_dir}/elements_wind_04.png",
        "twdc-elements-wind-band-concert": f"{twdc_sun_dir}/elements_wind_05.png",
        "twdc-elements-wind-wolf-pigs": f"{twdc_sun_dir}/elements_wind_06.png",
        # Elements of Nature — Earth
        "twdc-elements-earth-grandma-willow": f"{twdc_sun_dir}/elements_earth_01.png",
        "twdc-elements-earth-mufasa-simba": f"{twdc_sun_dir}/elements_earth_02.png",
        "twdc-elements-earth-gaetan-mole-moliere": f"{twdc_sun_dir}/elements_earth_03.png",
        "twdc-elements-earth-sprite": f"{twdc_sun_dir}/elements_earth_04.png",
        "twdc-elements-earth-flik-dot": f"{twdc_sun_dir}/elements_earth_05.png",
        "twdc-elements-earth-te-fiti": f"{twdc_sun_dir}/elements_earth_06.png",
        # Cat-astrophe
        "twdc-cat-astrophe-yzma": f"{twdc_sun_dir}/catastrophe_01.png",
        "twdc-cat-astrophe-toulouse": f"{twdc_sun_dir}/catastrophe_02.png",
        "twdc-cat-astrophe-sergeant-tibbs": f"{twdc_sun_dir}/catastrophe_03.png",
        "twdc-cat-astrophe-snowball": f"{twdc_sun_dir}/catastrophe_04.png",
        "twdc-cat-astrophe-oliver": f"{twdc_sun_dir}/catastrophe_06.png",
        "twdc-cat-astrophe-mr-mittens": f"{twdc_sun_dir}/catastrophe_07.png",
        "twdc-cat-astrophe-marie-berlioz": f"{twdc_sun_dir}/catastrophe_08.png",
        "twdc-cat-astrophe-madam-mim": f"{twdc_sun_dir}/catastrophe_05.png",
        "twdc-cat-astrophe-machiavelli": f"{twdc_sun_dir}/catastrophe_09.png",
        "twdc-cat-astrophe-lucifer": f"{twdc_sun_dir}/catastrophe_10.png",
        "twdc-cat-astrophe-figaro": f"{twdc_sun_dir}/catastrophe_11.png",
        "twdc-cat-astrophe-dinah": f"{twdc_sun_dir}/catastrophe_12.png",
        "twdc-cat-astrophe-mochi": f"{twdc_sun_dir}/catastrophe_14.png",
        "twdc-cat-astrophe-cheshire": f"{twdc_sun_dir}/catastrophe_13.png",
        # Table for One
        "twdc-table-for-one-evil-queen": f"{twdc_sun_dir}/table_for_one_01.png",
        "twdc-table-for-one-maleficent": f"{twdc_sun_dir}/table_for_one_02.png",
        "twdc-table-for-one-captain-hook": f"{twdc_sun_dir}/table_for_one_03.png",
        "twdc-table-for-one-cruella-de-vil": f"{twdc_sun_dir}/table_for_one_04.png",
        "twdc-table-for-one-ursula": f"{twdc_sun_dir}/table_for_one_05.png",
        "twdc-table-for-one-king-candy": f"{twdc_sun_dir}/table_for_one_06.png",
        "twdc-table-for-one-hades": f"{twdc_sun_dir}/table_for_one_07.png",
        "twdc-table-for-one-mother-gothel": f"{twdc_sun_dir}/table_for_one_08.png",
        "twdc-table-for-one-yzma": f"{twdc_sun_dir}/table_for_one_09.png",
        "twdc-table-for-one-ernesto-de-la-cruz": f"{twdc_sun_dir}/table_for_one_10.png",
        "twdc-table-for-one-hans": f"{twdc_sun_dir}/table_for_one_11.png",
        "twdc-table-for-one-king-magnifico": f"{twdc_sun_dir}/table_for_one_12.png",
        "twdc-table-for-one-madam-mim": f"{twdc_sun_dir}/table_for_one_13.png",
        "twdc-table-for-one-prince-john": f"{twdc_sun_dir}/table_for_one_14.png",
        "twdc-table-for-one-dr-facilier": f"{twdc_sun_dir}/table_for_one_15.png",
        # Enchanted Gowns
        "twdc-enchanted-gowns-snow-white": f"{twdc_sun_dir}/enchanted_gowns_01.png",
        "twdc-enchanted-gowns-cinderella": f"{twdc_sun_dir}/enchanted_gowns_02.png",
        "twdc-enchanted-gowns-aurora": f"{twdc_sun_dir}/enchanted_gowns_03.png",
        "twdc-enchanted-gowns-ariel": f"{twdc_sun_dir}/enchanted_gowns_04.png",
        "twdc-enchanted-gowns-jasmine": f"{twdc_sun_dir}/enchanted_gowns_05.png",
        "twdc-enchanted-gowns-belle": f"{twdc_sun_dir}/enchanted_gowns_06.png",
        "twdc-enchanted-gowns-pocahontas": f"{twdc_sun_dir}/enchanted_gowns_07.png",
        "twdc-enchanted-gowns-mulan": f"{twdc_sun_dir}/enchanted_gowns_08.png",
        "twdc-enchanted-gowns-tiana": f"{twdc_sun_dir}/enchanted_gowns_09.png",
        "twdc-enchanted-gowns-rapunzel": f"{twdc_sun_dir}/enchanted_gowns_10.png",
        "twdc-enchanted-gowns-anna": f"{twdc_sun_dir}/enchanted_gowns_11.png",
        "twdc-enchanted-gowns-elsa": f"{twdc_sun_dir}/enchanted_gowns_12.png",
        # Winnie the Pooh Mystery — box + individual pulls
        "twdc-pooh-mystery-mystery-box": f"{twdc_sun_dir}/winnie_pooh_box.png",
        "twdc-pooh-mystery-pooh-with-flowers": f"{twdc_sun_dir}/winnie_pooh_01.png",
        "twdc-pooh-mystery-birthday-pooh": f"{twdc_sun_dir}/winnie_pooh_02.png",
        "twdc-pooh-mystery-pooh-piglet": f"{twdc_sun_dir}/winnie_pooh_03.png",
        "twdc-pooh-mystery-bedtime-pooh": f"{twdc_sun_dir}/winnie_pooh_04.png",
        "twdc-pooh-mystery-king-pooh": f"{twdc_sun_dir}/winnie_pooh_05.png",
        "twdc-pooh-mystery-rainy-day-pooh": f"{twdc_sun_dir}/winnie_pooh_06.png",
        "twdc-pooh-mystery-adventurer-pooh": f"{twdc_sun_dir}/winnie_pooh_07.png",
        "twdc-pooh-mystery-pirate-pooh": f"{twdc_sun_dir}/winnie_pooh_08.png",
        # Star Wars Galactic Pals — box + individual pulls
        "twdc-star-wars-galactic-mystery-mystery-box": f"{twdc_sun_dir}/galactic_pals_box.png",
        "twdc-star-wars-galactic-mystery-porg": f"{twdc_sun_dir}/galactic_pals_01.png",
        "twdc-star-wars-galactic-mystery-loth-cat": f"{twdc_sun_dir}/galactic_pals_02.png",
        "twdc-star-wars-galactic-mystery-gamorrean": f"{twdc_sun_dir}/galactic_pals_03.png",
        "twdc-star-wars-galactic-mystery-ortolan": f"{twdc_sun_dir}/galactic_pals_04.png",
        "twdc-star-wars-galactic-mystery-wookiee": f"{twdc_sun_dir}/galactic_pals_05.png",
        "twdc-star-wars-galactic-mystery-tauntaun": f"{twdc_sun_dir}/galactic_pals_06.png",
        "twdc-star-wars-galactic-mystery-ewok": f"{twdc_sun_dir}/galactic_pals_07.png",
        "twdc-star-wars-galactic-mystery-rodian": f"{twdc_sun_dir}/galactic_pals_08.png",
        "twdc-star-wars-galactic-mystery-huttlet": f"{twdc_sun_dir}/galactic_pals_09.png",
        # Framed sets
        "twdc-framed-pixar-stamps-pixar-stamps-framed": f"{twdc_sun_dir}/framed_pixar_stamps.png",
        "twdc-framed-hugs-are-the-best-hugs-are-the-best-framed": f"{twdc_sun_dir}/framed_hugs_are_the_best.png",
        "twdc-framed-fairytale-dancing-fairytale-dancing-framed": f"{twdc_sun_dir}/framed_fairytale_dancing.png",
        "twdc-framed-a-villains-darkness-a-villains-darkness-framed": f"{twdc_sun_dir}/framed_villains_darkness.png",
        "twdc-framed-holiday-princess-party-holiday-princess-party-framed": f"{twdc_sun_dir}/framed_holiday_princess_party.png",
        "twdc-framed-minnies-city-outfits-minnies-city-outfits-framed": f"{twdc_sun_dir}/framed_minnies_city_outfits.png",
        "twdc-framed-classic-friends-classic-friends-framed": f"{twdc_sun_dir}/framed_classic_friends.png",
        "twdc-framed-holiday-snowflakes-holiday-snowflakes-framed": f"{twdc_sun_dir}/framed_holiday_snowflakes.png",
    }

    mapped = 0
    for s in all_sets:
        for pin in s["pins"]:
            if pin["id"] in mappings:
                pin["image_path"] = mappings[pin["id"]]
                mapped += 1

    # Assign box_image_path to individual pulls in mystery sets
    for s in all_sets:
        if s["set_type"] != "mystery":
            continue
        # Find the mystery box pin's image
        box_img = None
        for pin in s["pins"]:
            if "mystery-box" in pin["id"] or pin["name"] == "Mystery Box":
                box_img = pin.get("image_path")
                break
        if box_img and box_img != PLACEHOLDER:
            for pin in s["pins"]:
                if pin["name"] != "Mystery Box":
                    pin["box_image_path"] = box_img

    # Assign secondary image to Reel of Magic pins
    reel_secondary = "images/twdc/fri/fri_reel_top2_01.png"
    for s in all_sets:
        if s["id"] == "twdc-reel-of-magic":
            for pin in s["pins"]:
                pin["box_image_path"] = reel_secondary

    # Assign secondary (back side) images to POV spinner pins
    pov_back_images = {
        "mog-pov-37": "images/mog/fri/mog_p10_0595.png",
        "mog-pov-38": "images/mog/fri/mog_p10_0607.png",
        "mog-pov-39": "images/mog/fri/mog_p10_0603.png",
        "mog-pov-40": "images/mog/fri/mog_p10_0611.png",
        "mog-pov-41": "images/mog/fri/mog_p10_0599.png",
        "mog-pov-42": "images/mog/fri/mog_p11_0702.png",
        "mog-pov-43": "images/mog/fri/mog_p11_0698.png",
        "mog-pov-44": "images/mog/fri/mog_p11_0706.png",
        "mog-pov-45": "images/mog/fri/mog_p11_0710.png",
        "mog-pov-46": "images/mog/fri/mog_p11_0714.png",
    }
    for s in all_sets:
        if s["id"] == "mog-pov":
            for pin in s["pins"]:
                if pin["id"] in pov_back_images:
                    pin["box_image_path"] = pov_back_images[pin["id"]]

    # Assign sea_card_969 as secondary image for all S.E.A. individual pins
    # Except pin 6 (uses 967) and pin 12 (uses 965)
    for s in all_sets:
        if s["id"] == "mog-sea-mystery":
            for pin in s["pins"]:
                if pin["name"] != "Mystery Box":
                    pin["box_image_path"] = "images/mog/sat/mog_sea_card_969.png"
            # Override specific pins
            for pin in s["pins"]:
                if pin["id"] == "mog-sea-mystery-dr-kon-chunosuke":
                    pin["box_image_path"] = "images/mog/sat/mog_sea_card_967.png"
                elif pin["id"] == "mog-sea-mystery-albert":
                    pin["box_image_path"] = "images/mog/sat/mog_sea_card_965.png"

    # Assign secondary (gate-fold) images to Panoramas pins
    panorama_back = {
        "mog-panoramas-81": "images/mog/sat/mog_p23_1237.png",
        "mog-panoramas-82": "images/mog/sat/mog_p23_1241.png",
        "mog-panoramas-83": "images/mog/sat/mog_p23_1245.png",
        "mog-panoramas-84": "images/mog/sat/mog_p23_1249.png",
        "mog-panoramas-85": "images/mog/sat/mog_p24_1324.png",
        "mog-panoramas-86": "images/mog/sat/mog_p24_1328.png",
        "mog-panoramas-87": "images/mog/sat/mog_p24_1332.png",
        "mog-panoramas-88": "images/mog/sat/mog_p24_1320.png",
    }
    for s in all_sets:
        if s["id"] == "mog-panoramas":
            for pin in s["pins"]:
                if pin["id"] in panorama_back:
                    pin["box_image_path"] = panorama_back[pin["id"]]

    # Assign box image to Epic Rivals pins
    epic_rivals_box = "images/twdc/sat/sat_epic_rivals_185.png"
    for s in all_sets:
        if s["id"] == "twdc-epic-rivals":
            for pin in s["pins"]:
                pin["box_image_path"] = epic_rivals_box

    return mapped


def standardize_features(all_sets):
    """Normalize feature strings to consistent, filterable terms."""
    # Map raw feature fragments to standardized names
    rules = [
        ("hard enamel", "Hard Enamel"),
        ("soft enamel", "Soft Enamel"),
        ("pin on pin", "Pin on Pin"),
        ("pin-on-pin", "Pin on Pin"),
        ("3d", "Pin on Pin"),
        ("laser print", "Laser Print"),
        ("stained glass", "Stained Glass"),
        ("glitter", "Glitter"),
        ("translucent", "Translucent"),
        ("marbleized", "Marbleized"),
        ("pearlized", "Pearlized"),
        ("hinge pin", "Hinged"),
        ("jumbo", "Jumbo"),
        ("gemstone", "Gemstones"),
        ("custom backing", "Custom Backing Card"),
        ("uv-reactive", "UV Reactive"),
        ("foam pin board", "Foam Pin Board"),
        ("debossed", "Debossed"),
        ("antique gold", "Antique Gold"),
        ("antique nickel", "Antique Nickel"),
        ("gold base", "Gold Base"),
        ("gold metal", "Gold Base"),
        ("silver metal", "Silver Base"),
        ("clear epoxy", "Clear Epoxy"),
        ("spinner", "Spinner"),
        ("rotating", "Spinner"),
    ]

    for s in all_sets:
        if not s.get("features"):
            continue
        raw = s["features"].lower()
        found = []
        for fragment, standard in rules:
            if fragment in raw and standard not in found:
                found.append(standard)
        s["features"] = ", ".join(found) if found else s["features"]


def main():
    parser = argparse.ArgumentParser(description="Build D23 pin catalog pins.json")
    parser.add_argument("--catalogs", default="./catalogs", help="Catalogs directory (unused for now)")
    parser.add_argument("--output", default="./pins.json", help="Output path for pins.json")
    args = parser.parse_args()

    output_path = os.path.abspath(args.output)

    print("=" * 60)
    print("D23 Pin Catalog Builder")
    print("=" * 60)

    mog = build_mog_sets()
    twdc = build_twdc_sets()
    dssh = build_dssh_sets()
    all_sets = twdc + mog + dssh

    # Apply image mappings
    mapped = apply_image_mappings(all_sets)
    print(f"\n  Images mapped: {mapped}")

    # Standardize features
    standardize_features(all_sets)

    total_pins = sum(len(s["pins"]) for s in all_sets)

    output = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "stores": ["TWDC", "MOG", "DSSH"],
        "sets": all_sets,
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    # Summary table
    print(f"\n{'Store':<8}{'Date':<20}{'Sets':>5}{'Pins':>6}")
    print("-" * 42)
    stats = defaultdict(lambda: {"sets": 0, "pins": 0})
    for s in all_sets:
        key = (s["store"], s["drop_day_label"])
        stats[key]["sets"] += 1
        stats[key]["pins"] += len(s["pins"])

    for (store, date), v in sorted(stats.items()):
        print(f"{store:<8}{date:<20}{v['sets']:>5}{v['pins']:>6}")
    print("-" * 42)
    print(f"{'TOTAL':<28}{len(all_sets):>5}{total_pins:>6}")
    print("=" * 60)
    print(f"\n✓ Written: {output_path}")
    print(f"  {len(all_sets)} sets, {total_pins} pins")
    print(f"\nNote: All images point to '{PLACEHOLDER}'. Drop real images")
    print(f"  into images/<pin-id>.png to replace the placeholder.")


if __name__ == "__main__":
    main()
