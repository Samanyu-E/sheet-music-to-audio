**Open Source Tools Used**

1. **Audiveris**
   - Purpose: Used for Optical Music Recognition (OMR) from scanned sheet music.
   - Source: https://github.com/Audiveris/audiveris
   - License: GNU AFFERO GENERAL PUBLIC LICENSE Version 3
   - Copyright (C) 2007 Free Software Foundation, Inc.

2. **FluidR3 GM SoundFont**
   - Purpose: General MIDI SoundFont used for audio synthesis from MIDI files.
   - Source: https://member.keymusician.com/Member/FluidR3_GM/
   - License: MIT license
   - Copyright (c) 2000-2002, 2008, 2013 Frank Wen

_________________________________________________________________________________________________________________________________________

**License Compliance Notes:**

- This project **does not modify** the source code of Audiveris.
- The Audiveris tool is used externally via its command-line interface (`audiveris.bat`). Audiveris files used under omr/ directory.
- The FluidR3 SoundFont is used solely for MIDI-to-audio conversion via FluidSynth. FluidR3 SoundFont files used under soundfont/ directory.
- All third-party components retain their original licenses, terms, and copyright.
- This NOTICE file, the `LICENSE` file (MIT), and `licenses/` directory (if included) provide full attribution.

_________________________________________________________________________________________________________________________________________

MIT License applies to all other original components in this repository written by Samanyu Earna.
