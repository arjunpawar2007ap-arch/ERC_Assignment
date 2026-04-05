# Pick and Place — My Solution

## How I Approached This

Going into this I had zero experience with Simscape Multibody. I spent an entire night on this literally didn't sleep just trying to understand what each block does and how things connect. Most of my time went into trial and error, running the simulation, seeing something wrong, and trying to fix it.

## What I Had to Figure Out

The model came with all the blocks but nothing was connected. I had to understand what each block does before I could wire anything. Honestly the hardest part was understanding the difference between physical frame connections (the Simscape lines) and regular signal connections they look similar but work completely differently.

## Blocks I Added

**World Frame** I didn't initially understand why this was needed. Turns out every physical thing in Simscape needs a reference point to know where it exists in space. Without this, nothing works.

**Two Rigid Transforms** — These position the belts in 3D space. I had to configure:
- Transform Belt Out: 180° rotation about +Z, with translation [-0.505, 0, 0.05] m
- Transform Belt In: -90° rotation about +Z, with translation [0, 0.505, 0.05] m

I'll be honest, I initially left the translation as "None" and couldn't figure out why the belts weren't showing up. Took me a while to realize the offset values were stored in the model workspace (belt_out_offset and belt_in_offset) and I had to set translation method to Cartesian.

**Two Goto blocks** — Tagged as "Out" and "In". These route the force block outputs wirelessly to the Forces subsystem.

## How I Figured Out the Wiring

The assignment said the World Frame connects to 4 physical things. I figured out those are: the 6-DOF Joint, Belt Out (through its rigid transform), Belt In (through its rigid transform), and the Gripper.

For the Gripper subsystem, I had the reference image showing the correct wiring. The key thing I learned is that the Rod block needs to connect to BOTH prismatic joints (not just one), and the -1 gain makes the fingers move in opposite directions.

For the force blocks, the PlaB port connects to the belt's End port and FacF connects to the box frame. The bus/On subsystem creates a bus signal with Enable=1 and belt speed, which feeds into the force block's In port. The force block's Out port goes to the Goto blocks.

The Commands block sends signals to everything finger position, gripper angle, post height, post rotation, and belt speeds. Each belt speed signal branches to both the belt's Spd port and the bus/On subsystem.

## What Each Value Represents

- **belt_out_offset [-0.505, 0, 0.05]** — where Belt Out sits in the world (X, Y, Z in meters)
- **belt_in_offset [0, 0.505, 0.05]** — where Belt In sits
- **180° and -90° rotations** — the belts form an L-shape, facing different directions
- **cube_d = 0.06m** — the box is a 6cm cube
- **Initial box position Py=0.6m, Pz=0.13m** — places the box above Belt In's surface

## What Went Wrong and How I Debugged

This is where most of my night went:

1. **Belts not showing in 3D** — forgot to set translation values on the rigid transforms
2. **Gripper head floating separately** — Rod wasn't connected to both prismatic joints inside the Gripper
3. **"Cycle detected in rigidity graph" error** — I had belt End ports connected wrong, creating a physical loop. Had to rewire the force blocks carefully
4. **"Bus Selector" error** — the Goto/From blocks were sending wrong signal types to the Forces block. Fixed by connecting force block Out ports to the Goto blocks
5. **Box falling through the belt** — this is the one I couldn't solve. I checked every connection, changed solver settings (ode15s, tolerances as per the README), verified contact parameters, enabled contact surface visualization everything looks correct but the contact forces just don't engage

## Current Status

The gripper works perfectly post moves up/down, rotates, fingers open and close. Both belts are positioned correctly. All connections are verified. The only remaining issue is the box passing through the belt surface, which I suspect is a compatibility issue between the Contact Forces Library (built for R2020a) and my MATLAB R2025b.

## What I Learned

Before this assignment I didn't know what a rigid transform was or how joints work in simulation. Now I understand how frame trees work, why everything needs to connect back to the World Frame, how prismatic and revolute joints create linear and rotational motion, and how contact forces are supposed to work between surfaces. It was a painful night but I genuinely understand the system now.
