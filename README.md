# glTF-USD-roundtrip

Internal experiments for conversions between glTF and USD, using Blender.

## Disclaimer

This is just a collection of brainstorming and experiments. Most of this does
not make sense when seen in isolation. I am not a Python expert, and not a
Blender expert, and not a USD expert, and not a glTF expert.

## Summary of goals

The glTF and USD formats serve different purposes and have different application
areas. Nevertheless, there is a certain overlap in these applications. And there
is a demand for converting between these formats. This does raise the question
about the features that can be represented in one format and not the other.

A high-level approach for evaluating the compatibility between glTF and USD
sparked the idea of a "roundtrip": Taking a glTF file, converting it to USD,
converting the result back to glTF, and see what was lost in translation.
(Similarly, one could go the USD-glTF-USD-path). 

### Theoretical approach

Details of this conversion have been discussed on different levels. Intuitively, 
one would like this conversion to be "lossless", but giving a sensible meaning 
to this term is difficult. The [`glTF-USD-roundtrip.md`](glTF-USD-roundtrip.md) 
document contains initial brainstorming about certain features that could
be examined, and how the comparison could be done. It would be necessary
to iterate and refine that, but keeping the structure of that compatibility
analysis manageable could be challenging. 

### Practical approach

The alternative of asking "How can this be done?" is to just do it, and
see what doesn't work. In that vein, this repository contains some 
Python scripts for Blender that perform such a "roundtrip conversion", 
and allow some inspection of the resulting glTF assets.

## Implementation

The [`impl`](impl/) directory contains the implementation of these conversion
scripts. 

## Data directory

The `Data` subdirectory contains the data for the conversion:

- The `input_gltf` is required, and contains the input glTF files, using
  using the same directory structure that is also used in the
  https://github.com/KhronosGroup/glTF-Sample-Assets 
- The `usd` directory will and contain the USD versions of the converted models.
  (This will be created automatically)
- The `output_gltf` directory will contain the glTF versions of the models
  that have been created from the USD versions of the models.
  (This will be created automatically)
- The `renders` directory will contain rendered images of the input- and
  output glTF versions of the models.

## Running the conversion

The [`roundtrip.py`](impl/roundtrip.py) is the entry point, i.e. it contains 
the `main()` function. This can be used to convert a single model, or a bunch 
of models, based on a `model-index.json` file that has the same structure as 
this file in the https://github.com/KhronosGroup/glTF-Sample-Assets repository.

Running this file always starts with

`blender.exe -P blender_conversions.py -P blender_utilities.py -P io_utilities.py -P roundtrip.py -P roundtrip_runner.py -P roundtrip_utilities.py -- `

which is referred to as `runIt` in the following examples. (There actually is 
a `runIt.bat` Windows Batch file that does this, for convenience...)

### Converting a single GLB file

To run the conversion process for a single model, only identified by its **name**,
assuming the default directory layout, the name may be given using the `-m` 
command line argument:

`runIt -m Box` 

Note: For this to work, the model **must** have a `glTF-Binary` variant!

### Converting a single file

To convert a single file (that may not be a GLB file), the input, USD, and output 
file names can be given using the `-i`, `-u`, and `-o` command line arguments:

`runIt -i "./Data/input_gltf/Triangle/glTF-Embedded/Triangle.gltf" -u "./Data/usd/Triangle/glTF-Embedded/Triangle.usd" -o "./Data/output_gltf/Triangle/glTF-Binary/Triangle.glb`

Note: The output file **must** have the extension `.glb`!

### Converting a bunch of files

When running the script without any command line arguments, then it will
look for the `model-index.json` in the `input_gltf` directory, and perform
the conversion for all models that are found in that file.

`runIt`






