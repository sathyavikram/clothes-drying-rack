# Requirements

## Scope
Implementation of `part_01_leg_tube.py` representing a single round straight hollow tube segment of the leg structure, and assembling the full leg combining these segments. It must measure ~220 mm to fit diagonally within the default 175x175x175 FDM build plate (giving safe margin on $175\sqrt{2} - 25$ OD).

## Decisions
- The tube shape will be exclusively round.
- Joints are implemented as **threaded joints** and a **rounded clamp (female threads)** for segmentation.
- Print orientation must be lying flat on its long face.

## Constraints
- Wall thickness and dimensions must abide by `tech-stack.md` and `params.py` (e.g. 25 mm OD, 2 mm wall thickness).
- Thread geometry must incorporate appropriate FDM clearances (usually 0.2 - 0.4 mm).

## Non-goals
- Modifying hinges or top rod connectors is out of scope.

## Context
Long structural members exceed the build plate and must be split. Strong connections are necessary to maintain stability and structural integrity of the drying rack. Threaded joints provide a strong grip for connection.