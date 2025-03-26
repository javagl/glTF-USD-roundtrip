import sys
sys.path.append(".")

import os
import json
from blender_conversions import convert_gltf_to_usd
from blender_conversions import convert_usd_to_gltf
from roundtrip_utilities import create_single_render_views
from roundtrip_utilities import compute_camera_setups

def run_single_conversion(input_gltf_path, usd_path, output_gltf_path):
    """
    run_single_conversion Converts the given glTF into a USD, and the
    resulting USD into a glTF.

    :param input_gltf_path: The actual path of the input glTF file
    :param usd_path: The actual path of the output USD file
    :param output_gltf_path: The actual path of the output glTF file. 
    """

    print("run_single_conversion")
    print("input_gltf_path  "+ input_gltf_path)
    print("usd_path         "+ usd_path)
    print("output_gltf_path "+ output_gltf_path)

    convert_gltf_to_usd(input_gltf_path, usd_path)
    convert_usd_to_gltf(usd_path, output_gltf_path)
    

def run_single_renders(input_gltf_path, output_gltf_path, model_name):
    """
    run_single_renders Creates renders of the given glTF models and
    writes them as images into the "./Data/renders" directory.

    Many details are (intentionally) not specified here. 

    :param input_gltf_path: The actual path of the input glTF file
    :param output_gltf_path: The actual path of the output glTF file. 
    :param model_name: The model name, from the "model-index.json"
    """

    print("run_single_renders")
    print("input_gltf_path  "+ input_gltf_path)
    print("output_gltf_path "+ output_gltf_path)
    print("model_name       "+ model_name)
    
    render_output_directory = "./Data/renders"
    camera_setups = compute_camera_setups(input_gltf_path)
    create_single_render_views(input_gltf_path, model_name, render_output_directory, "_input", camera_setups)
    create_single_render_views(output_gltf_path, model_name, render_output_directory, "_output", camera_setups)


def run_single_model_variant(input_gltf_path, usd_path, output_gltf_path, model_name):
    """
    run_single_model_variant Runs the conversion and the creation of the rendered images
    for the specified files.

    This will try to run "run_single_conversion" and "run_single_renders",
    printing an error message is something bad happens.
    
    :param input_gltf_path: The actual path of the input glTF file
    :param usd_path: The actual path of the output USD file
    :param output_gltf_path: The actual path of the output glTF file. 
    :param model_name: The model name, from the "model-index.json"
    """
    try:
        run_single_conversion(input_gltf_path, usd_path, output_gltf_path)
        run_single_renders(input_gltf_path, output_gltf_path, model_name)
    except RuntimeError as e:
        print("ERROR: " + str(e))

  
def run_single_model(input_gltf_directory, usd_directory, output_gltf_directory, model_name, variants):
    """
    run_single_model Runs the conversion and the creation of the rendered images
    for the specified model. 

    This will try to find a suitable "variant" for the input of the conversion, trying
    the options "glTF-Binary", "glTF", and "glTF-Embedded". If neither variant is found,
    then an error will be printed.

    Otherwise, this will just run "run_single_model_variant" for that variant.

    :param input_gltf_directory: The directory that contains the "model-index.json" and the glTF files
    :param usd_directory: The directory that will store the USD versions of the files.
    :param output_gltf_directory: The directory that will store the output glTF files
    :param model_name: The "name" of the model, from the "model-index.json"
    :param variants: The "variants" dictionary from the "model-index.json"
    """
    
    if "glTF-Binary" in variants:
        variant_name = "glTF-Binary"
    elif "glTF" in variants:   
        variant_name ="glTF"
    elif "glTF_Embedded" in variants:   
        variant_name = "glTF-Embedded"
    else:
        print("No suitable input variant found for model "+model_name)
        return

    variant_file_name = variants[variant_name]

    base_file_name = variant_file_name
    base_file_name = base_file_name.replace(".gltf", "")
    base_file_name = base_file_name.replace(".glb", "")

    full_input_gltf_path = os.path.join(input_gltf_directory, model_name, variant_name, variant_file_name)
    full_usd_path = os.path.join(usd_directory, model_name, variant_name, base_file_name + ".usd")
    full_output_gltf_path = os.path.join(output_gltf_directory, model_name, variant_name, base_file_name + ".glb")
    run_single_model_variant(full_input_gltf_path, full_usd_path, full_output_gltf_path, model_name)


def run_model_index(input_gltf_directory, usd_directory, output_gltf_directory):
    """
    run_model_index Runs the conversion and the creation of the rendered images
    for all models that are found in the "model-index.json" in 
    the input_gltf_directory. 
    
    The "model-index-json" is assumed to be in the format that is used 
    in the https://github.com/KhronosGroup/glTF-Sample-Assets.

    This will essentially just call "run_single_model" for each model.

    :param input_gltf_directory: The directory that contains the "model-index.json" and the glTF files
    :param usd_directory: The directory that will store the USD versions of the files.
    :param output_gltf_directory: The directory that will store the output glTF files
    """     
    model_index_file_path = os.path.join(input_gltf_directory, "model-index.json")
    with open(model_index_file_path, 'r') as model_index_file:
        model_index_data = json.load(model_index_file)
        for model_entry in model_index_data:
            model_name = model_entry["name"]
            variants = model_entry["variants"]
            run_single_model(input_gltf_directory, usd_directory, output_gltf_directory, model_name, variants)

