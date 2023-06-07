import sys
sys.path.append(".")

import os
import json
from blender_conversions import convert_gltf_to_usd
from blender_conversions import convert_usd_to_gltf
from roundtrip_utilities import create_single_render_views
from roundtrip_utilities import compute_camera_setups

def run_single_conversion(input_gltf_path, usd_path, output_gltf_path):

    print("run_single_conversion")
    print("input_gltf_path  "+ input_gltf_path)
    print("usd_path         "+ usd_path)
    print("output_gltf_path "+ output_gltf_path)

    convert_gltf_to_usd(input_gltf_path, usd_path)
    convert_usd_to_gltf(usd_path, output_gltf_path)
    

def run_single_renders(input_gltf_path, output_gltf_path, model_name):

    print("run_single_renders")
    print("input_gltf_path  "+ input_gltf_path)
    print("output_gltf_path "+ output_gltf_path)
    print("model_name       "+ model_name)
    
    render_output_directory = "./Data/renders"
    camera_setups = compute_camera_setups(input_gltf_path)
    create_single_render_views(input_gltf_path, model_name, render_output_directory, "_input", camera_setups)
    create_single_render_views(output_gltf_path, model_name, render_output_directory, "_output", camera_setups)

def run_single_model_variant(input_gltf_path, usd_path, output_gltf_path, model_name):
    try:
        run_single_conversion(input_gltf_path, usd_path, output_gltf_path)
        run_single_renders(input_gltf_path, output_gltf_path, model_name)
    except RuntimeError as e:
        print("ERROR: " + str(e))


  
def run_single_model(input_gltf_directory, usd_directory, output_gltf_directory, model_name, variants):
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
    model_index_file_path = os.path.join(input_gltf_directory, "model-index.json")
    with open(model_index_file_path, 'r') as model_index_file:
        model_index_data = json.load(model_index_file)
        for model_entry in model_index_data:
            model_name = model_entry["name"]
            variants = model_entry["variants"]
            run_single_model(input_gltf_directory, usd_directory, output_gltf_directory, model_name, variants)

