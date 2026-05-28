# Mission

## Purpose

Design a full-scale, 3D-printable clothes drying rack intended for home use and commercial distribution — optimized for printability, repeatability, and customer assembly without specialist tools.

## Problem Statement

Commercially available drying racks are often flimsy, take up permanent floor space, or lack the capacity for large items (sheets, blankets). This project delivers a custom, heavy-duty, collapsible rack that can be printed on demand and sold direct-to-consumer, with each part individually replaceable.

## Core Requirements

| Requirement | Specification |
|---|---|
| Footprint (extended) | 80 in length × 51 in height |
| Portability | Fully collapsible / foldable for flat storage |
| Durability | Heavy-duty — must support wet laundry loads |
| Stability | Locking hinges to prevent accidental collapse |
| Drying capacity | 3 retractable rods (shirts, pants, sheets, blankets) |
| Safety | Anti-slip feet on all ground contact points |
| Fabrication | FDM 3D-printed parts, consumer printer compatible |

## Design Principles

1. **Print-first** — every part must fit on a 180 × 180 × 180 mm build volume (or be intentionally split).
2. **Minimal hardware** — prefer snap fits, friction fits, and printed joints; use bolts/nuts only where strength demands it.
3. **Customer repair** — any broken part must be individually re-printable and sold as a spare; no full-rack reprint required.
4. **Batch consistency** — tolerances and print settings must produce identical results across multiple printers and print runs.
5. **Tool-free assembly** — a customer must be able to assemble the complete rack with no tools beyond a rubber mallet for press fits.

## Out of Scope

- Non-FDM fabrication methods (injection moulding, CNC, laser cut)
- Motorized or automated features
