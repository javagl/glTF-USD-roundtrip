import sys
sys.path.append(".")

import bpy
from io_utilities import ensure_directory_exists

def convert_gltf_to_usd(input_path, output_path):
    """
    convert_gltf_to_usd Converts a glTF to a USD

    The exact configurations (i.e. details of the import/export calls)
    are not specified.

    :param input_path: The input glTF
    :param output_path: The output USD
    """ 
    print("convert_gltf_to_usd")
    print("input_path is " + input_path)
    print("output_path is " + output_path)

    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    bpy.ops.import_scene.gltf(filepath=input_path,filter_glob='*.glb;*.gltf')
    
    ensure_directory_exists(output_path)
    bpy.ops.wm.usd_export(filepath=output_path, export_animation=True)

def convert_usd_to_gltf(input_path, output_path):
    """
    convert_usd_to_gltf Converts a glTF to a USD

    The exact configurations (i.e. details of the import/export calls)
    are not specified.
    
    :param input_path: The input USD
    :param output_path: The output glTF
    """ 
    print("convert_usd_to_gltf")
    print("input_path is " + input_path)
    print("output_path is " + output_path)

    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    bpy.ops.wm.usd_import(filepath=input_path, import_textures_dir="//textures")

    ensure_directory_exists(output_path)
    bpy.ops.export_scene.gltf(filepath=output_path, export_animations=True, export_frame_range=False)

