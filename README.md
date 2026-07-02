# MagicItalic

This is a [Glyphs.app](http://glyphsapp.com/) filter for slanting upright shapes into italics, with correction for optical contrast, shape and stem thickness (cursify/italify/obliquify).

Unlike a plain shear, it applies Glyphs’ built-in slant correction algorithm, so verticals, curves and rounds keep believable proportions instead of just leaning sideways.


### Installation

1. One-click install *Magic Italic* from *Window > Plugin Manager*
2. Restart Glyphs.


### Usage Instructions

1. Open a glyph for editing.
2. Choose *Filter > Magic Italic.*
3. In the dialog, set your *Italic Angle,* and the amount of *Contrast,* *Shape* and *Thickness Correction* (0–100 each).
4. *Horizontal Stem* and *Vertical Stem* default to the first stems defined in *File > Font Info > Masters.* Enter a number to use a different width for the correction, or leave the asterisk (`*`) to keep using the font’s stem.
5. Enable *Realign Handles* to clean up the curve handles that the slanting leaves behind (see below).
6. Click *Italify* to apply.

#### Realign Handles

Slanting shifts off-curve points, which can leave smooth nodes slightly out of alignment with their handles. *Realign Handles* straightens those handles back onto the tangent, the same way the standalone [Realign Handles](https://github.com/mekkablue/RealignHandles) filter does. It is on by default; uncheck it if you want to fix handles yourself, or if you are applying *Magic Italic* as a *PreFilter* together with a separate *RealignHandles* step.

#### as custom parameter

1. In *File > Font Info > Exports,* in one of the instances, add a *Filter* (or *PreFilter*) custom parameter.
2. As its value, enter `MagicItalic; italicAngle: 10; correctContrast: 20; correctShape: 30; correctThickness: 100; hStem: *; vStem: *; realignHandles: 1;`
3. Adjust the values to your liking. Leave out any key to fall back to the plug-in’s current dialog settings; set `realignHandles: 0` to skip the handle cleanup.


### License

Copyright 2026 Rainer Erich Scheichelbauer (@mekkablue).
Based on sample code by the Glyphs team (glyphsapp.com).

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

See the License file included in this repository for further details.
