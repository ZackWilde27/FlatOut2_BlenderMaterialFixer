# FlatOut2 Material Fixer For Blender

These scripts are for automating a lot of the tedious process of fixing tracks in blender to make renders

<br>

## ddsconverter.py

It's a script that automatically converts all DDS textures in a folder to PNG

It'll ask you for a file, just pick any one of the textures in the folder and it will convert all of them.

You will need Pillow to run the DDS converter, [here's](https://pillow.readthedocs.io/en/stable/installation/basic-installation.html) the instructions for installing it

<br>

## fo2materialfixer.py

It's an addon for Blender, you can either import it in the settings window, or paste the script into blender's text editor and run it from there

It'll add a tab at the top called ```FlatOut Material Fixer```, and from there you've got 5 operators + an operator that automatically does all of them:

- `DDS To PNG`: Goes through every object and finds any using DDS textures, then points them to the corrosponding PNG file in the given textures folder

- `Apply Alpha`: Finds all objects using a material with ```alpha``` in the name, and connects up the alpha to the BSDF automatically

- `Fix Track UVs`: Finds all track geometry, and switches the UVs over to the second one, making them look correct

- `Disconnect Mapping Nodes`: Goes through all materials and disconnects the mapping node linked to the colour texture

- `Set Channel Packed Alpha Mode`: Goes through all materials and sets the colour texture's alpha mode to Channel Packed instead of Straight

- `Fix Everything`: Performs all of the above operators in one go for convenience

<br>

## Where to go from here

After fixing the track, you'll notice that there are still issues, I wanted to mention some of these because they require knowledge about how the game renders to fix

### White Textures
Some surfaces are mysteriously white, like roads, grass, dirt, etc.

<img width="1319" height="746" alt="image" src="https://github.com/user-attachments/assets/3c75f1a5-7820-4d04-ab9c-5823559988b1" />


That's because those surfaces are coloured by either vertex colours or based on the alpha channel

These textures need to be multiplied by a colour to get them looking correct, like grass should be multiplied by green

<img width="559" height="265" alt="image" src="https://github.com/user-attachments/assets/81d654a8-8513-4a3e-b853-df80d9b2a3f5" />

<img width="633" height="569" alt="image" src="https://github.com/user-attachments/assets/7c137ddf-4499-401a-a353-a78cc7e1c712" />

Now to get a more realistic result you could use a noise texture fed into a colour ramp to get variation across the surface, instead of multiplying by a solid colour, but that's for you to decide how you want to go about it

Some textures use their alpha channel to blend between 2 colours, like dirt roads blending between a grass colour and dirt colour. In that case you would feed the alpha channel into a colour ramp to get the colour to multiply by

<br>

### Buildings
What makes the windows shiny while the rest is not?

The alpha channel describes what parts are windows (1.0), and what is not (0.0). Do with that what you will. Personally what I do is connect the alpha to the metallic, and then the inverted alpha into the roughness

<img width="584" height="250" alt="image" src="https://github.com/user-attachments/assets/475d6c8a-625a-4611-9e4e-77b0e4d051c3" />

<img width="1368" height="596" alt="image" src="https://github.com/user-attachments/assets/d23eeaf0-f963-42e6-a6e6-4c237865677c" />

This is true for every object with gloss in the game, the alpha channel controls how glossy parts of the materials get. In the building's case what I do is swap between rough diffuse and shiny metal, but in other cases (like the galaxy mall's floor) you can just feed the inverted alpha into the roughness channel without touching metallic.
