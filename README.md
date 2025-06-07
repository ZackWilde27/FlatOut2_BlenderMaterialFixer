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

It'll add a tab at the top called ```FlatOut Material Fixer```, and from there you've got 3 tools:

- DDSToPNG: Goes through every object and finds any using DDS textures, then points them to the corrosponding PNG file in the given textures folder

- ApplyAlpha: Finds all objects using a material with ```alpha``` in the name, and connects up the alpha to the BSDF automatically

- FixTrackUVs: Finds all track geometry, and switches the UVs over to the second one, making them look correct
