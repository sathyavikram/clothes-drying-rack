# Roadmap

Phases are intentionally small — each should produce at least one runnable FreeCAD Python script and a renderable part before moving on.

---

## Phase 1 — Frame & Legs (structural skeleton)

**Goal:** Establish the full-size skeleton of the rack.

- [ ] Define global parameter constants (overall length 80 in, height 51 in, tube/rod OD, wall thickness)
- [ ] Model a single leg profile (extrusion cross-section + length)
- [ ] Model the top horizontal cross-bar
- [ ] Model the lower cross-brace / spreader bar
- [ ] Assemble the two A-frame leg panels (left + right)
- [ ] Validate dimensions with a top/front/side render

---

## Phase 2 — Hinge & Locking Mechanism

**Goal:** Make the frame collapsible and lockable.

- [ ] Design the pivot-hinge body (pin bore, leaf geometry)
- [ ] Design the locking latch / detent that holds the rack open at full extension
- [ ] Integrate hinge mounting holes into leg parts from Phase 1
- [ ] Print-test tolerance on hinge pin fit (rotating fit: +0.3 mm)
- [ ] Validate open ↔ folded motion in FreeCAD assembly

---

## Phase 3 — Retractable Drying Rods

**Goal:** Add 3 rods that slide out for use and retract for storage.

- [ ] Design rod cross-section and length (distribute across 80 in span)
- [ ] Design rod channel / bracket that mounts to the cross-bar
- [ ] Design end-stop to prevent rod pull-out
- [ ] Design friction or click detent for "extended" position
- [ ] Model all 3 rod + bracket sets
- [ ] Validate sliding fit clearance (+0.4 mm) with test coupon

---

## Phase 4 — Anti-Slip Feet

**Goal:** Secure the rack against sliding on hard floors.

- [ ] Design printed foot cup (press-fits onto leg bottom)
- [ ] Size inner bore to accept standard 20 mm rubber furniture pad
- [ ] Add ribbing / texture to outer base for secondary grip if pad is omitted
- [ ] Attach foot cups to leg bottoms in assembly

---

## Phase 5 — Full Assembly & Integration

**Goal:** Combine all sub-assemblies into a single coherent model.

- [ ] Write top-level `assembly.py` that imports all part scripts
- [ ] Verify no intersecting geometry between parts
- [ ] Check all mating interfaces (hinge ↔ leg, rod ↔ bracket, foot ↔ leg)
- [ ] Confirm collapsed footprint fits intended storage space

---

## Phase 6 — Export & Print Readiness

**Goal:** Produce print-ready files and internal documentation.

- [ ] Export all parts as STL (print orientation optimized)
- [ ] Export assembly as STEP
- [ ] Document hardware BOM with quantities and supplier links
- [ ] Archive reference renders (isometric, front, side, detail shots)
- [ ] Create QC test coupon STL for batch validation

---

## Phase 7 — Commercial Readiness

**Goal:** Package the design for print-to-sell distribution.

- [ ] Write customer-facing assembly guide (`docs/assembly-guide/`) with numbered steps and annotated renders
- [ ] Create per-part spare-parts listing (part name, print time, material weight, price guidance)
- [ ] Produce QC checklist (`docs/qc-checklist/`) for use before shipping each unit
- [ ] Photograph or render a completed rack for product listing assets
- [ ] Update README with ordering / customization instructions for buyers
