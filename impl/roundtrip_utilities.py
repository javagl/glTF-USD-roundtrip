import sys
sys.path.append(".")

import os
import math
from blender_utilities import compute_camera_setup
from blender_utilities import create_single_render
from io_utilities import ensure_directory_exists

def compute_camera_setups(input_gltf_path):
    """
    compute_camera_setups Computes camera setups for rendering the given model

    The details are not specified

    :return: The camera setups
    """ 
    euler_front = ( math.radians(90), 0, 0)
    camera_setup_front = compute_camera_setup(input_gltf_path, euler_front)

    euler_top = ( 0, 0, 0)
    camera_setup_top = compute_camera_setup(input_gltf_path, euler_top)

    euler_right = ( math.radians(90), 0, math.radians(90))
    camera_setup_right = compute_camera_setup(input_gltf_path, euler_right)

    camera_setups = {
        "front": camera_setup_front,
        "top": camera_setup_top,
        "right": camera_setup_right
    }
    return camera_setups


def create_single_render_views(input_gltf_path, model_name, render_output_directory, render_name_suffix, camera_setups):
    """
    create_single_render_views Creates a single rendering of the given glTF model for multiple views

    The details are not specified, but this will generate a single
    rendered image, from different camera angles (views), of the
    given glTF model

    :param input_gltf_path: The input glTF
    :param model_name: The model name, used for constructing the final image file name
    :param render_output_directory: The relative output directory of the image files
    :param render_name_suffix: A suffix for the image file names (inserted before the file extension)
    :param camera_setups: The camera setups
    """ 
    ensure_directory_exists(render_output_directory)
    render_file_name_prefix = os.path.join(render_output_directory, model_name)

    for camera_setup_name in camera_setups:
        camera_setup = camera_setups[camera_setup_name]

        full_render_name_prefix = render_file_name_prefix + "_" + camera_setup_name + render_name_suffix
        create_single_render(input_gltf_path, full_render_name_prefix, camera_setup)

