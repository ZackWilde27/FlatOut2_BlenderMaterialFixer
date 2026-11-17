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
