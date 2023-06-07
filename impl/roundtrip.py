import sys
sys.path.append(".")

import os
import bpy
import argparse

from roundtrip_runner import run_single_model_variant
from roundtrip_runner import run_model_index

def parse_args():
    parser = argparse.ArgumentParser(description='Perform the roundtrip')
    parser.add_argument('-i', '--input_gltf_path', help='Input glTF model path')
    parser.add_argument('-u', '--usd_path', help='Path for intermediate USD model')
    parser.add_argument('-o', '--output_gltf_path', help='Output glTF model path')
    parser.add_argument('-m', '--model_name', help='Model name (using default input/output directories, and assuming the variant "glTF-Binary")')

    argv = sys.argv
    if "--" not in argv:
        argv = []
    else:
        argv = argv[argv.index("--") + 1:]
    args = parser.parse_args(argv)
    return args

def main():
    bpy.context.preferences.view.show_splash = False

    args = parse_args()
    model_name = args.model_name

    input_gltf_directory = os.path.abspath("./Data/input_gltf")
    usd_directory = os.path.abspath("./Data/usd")
    output_gltf_directory = os.path.abspath("./Data/output_gltf")

    if not (model_name is None):
        default_variant = "glTF-Binary"
        default_extension = ".glb" # TODO glTF will require a different export call
        full_input_gltf_path = os.path.join(input_gltf_directory, model_name, default_variant, model_name + default_extension)
        full_usd_path = os.path.join(usd_directory, model_name, default_variant, model_name + ".usd")
        full_output_gltf_path = os.path.join(output_gltf_directory, model_name, default_variant, model_name + default_extension)
        run_single_model_variant(full_input_gltf_path, full_usd_path, full_output_gltf_path, model_name)
    else:
        input_gltf_path = args.input_gltf_path
        usd_path = args.usd_path
        output_gltf_path = args.output_gltf_path

        if (input_gltf_path is None or usd_path is None or output_gltf_path is None):
            run_model_index(input_gltf_directory, usd_directory, output_gltf_directory)
        else: 
           model_name = "model"
           full_input_gltf_path = os.path.abspath(args.input_gltf_path)
           full_usd_path = os.path.abspath(args.usd_path)
           full_output_gltf_path = os.path.abspath(args.output_gltf_path)
           run_single_model_variant(full_input_gltf_path, full_usd_path, full_output_gltf_path, model_name)

    #bpy.ops.wm.quit_blender()

if __name__ == "__main__":
    main()
