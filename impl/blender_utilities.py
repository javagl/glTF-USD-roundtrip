import sys
sys.path.append(".")

import os
import bpy
import math

def set_up_environment(light_name="city.exr"):
    """
    set_up_environment Sets up the lighting in a scene.

    It looks up up the (built-in) environment map for the given light 
    name, and sets it as the environment background. 

    :param light_name: The light name.
    """     
    lights = bpy.context.preferences.studio_lights
    for light in lights:
        if light.name == light_name:
            break
    if (light is None):
        print('Light setup ' + light_name + ' not found')
        return

    world = bpy.context.scene.world
    world.use_nodes = True
    environment_node = world.node_tree.nodes.new("ShaderNodeTexEnvironment")
    environment_node.image = bpy.data.images.load(light.path)
    
    node_tree = bpy.context.scene.world.node_tree 
    node_tree.links.new(environment_node.outputs['Color'], node_tree.nodes['Background'].inputs['Color'])


def init_camera():
    """
    init_camera Adds a default camera to the scene.

    It will add a camera with an unspecified location and
    rotation, and set it as the active camera object of
    the scene
    """     
    camera = bpy.data.cameras.new("Camera")
    camera_object = bpy.data.objects.new("Camera Object", camera)
    bpy.context.scene.collection.objects.link(camera_object)
    camera_object.location = (0, 0, 0)
    camera_object.rotation_euler = (0, 0, 0)
    bpy.context.scene.camera = camera_object



def find_3d_area():
    for area in bpy.context.window.screen.areas:
        if area.type == 'VIEW_3D':
            return area

        

def fit_active_camera():     
    """
    fit_active_camera Fit the active camera to view all objects.

    This will use the "camera_to_view_selected" function from
    blender to set up the camera
    """     
    bpy.ops.object.select_all(action='SELECT')
    bpy.context.scene.camera.select_set(False)
    bpy.ops.view3d.camera_to_view_selected()
    bpy.ops.object.select_all(action="DESELECT")


def compute_number_of_frames():
    """
    compute_number_of_frames Computes the number of frames of all actions.
    This will examine all actions in the current data, and return the
    maximum frame range that appears in any of them.

    :return: The number of frames of all actions
    """     
    number_of_frames = 0
    actions = bpy.data.actions
    if actions:
        for action in actions:
            number_of_frames = max(number_of_frames, action.frame_range[1])
            #print("frame range");
            #print(action.frame_range);
    return math.ceil(number_of_frames)


def render_single_frame(output_file_name_prefix, sizeX=512, sizeY=512):
    """
    render_single_frame Renders a single frame to a file

    :param output_file_name_prefix: A prefix for the output file.
    The file will be converted into an absolute path, and the
    extension ".png" (including the dot) will be appended.
    :param sizeX: The size in x-direction, in pixels
    :param sizeY: The size in y-direction, in pixels
    """     

    full_file_prefix = os.path.abspath(output_file_name_prefix)
    bpy.context.scene.frame_set(0)
    bpy.context.scene.render.resolution_x = sizeX
    bpy.context.scene.render.resolution_y = sizeY
    bpy.context.scene.render.filepath = full_file_prefix + ".png"
    bpy.ops.render.render(write_still=True)


def compute_camera_setup(input_gltf_path, euler=(0,0,0)):
    """
    compute_camera_setup Computes a camera setup for rendering
    the given glTF.

    This will compute dictionary containing "location" and
    "rotation_euler" properties that can be assigned to 
    a camera, so that the given glTF is fully visible

    :param input_gltf_path: The input glTF
    :param euler: The initial euler angles of the camera
    """     
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    bpy.ops.import_scene.gltf(filepath=input_gltf_path,filter_glob='*.glb;*.gltf')
    init_camera()

    camera_object = bpy.context.scene.camera
    camera_object.rotation_euler = euler

    fit_active_camera()

    camera_setup = {
        "location": tuple(camera_object.location), 
        "rotation_euler": tuple(camera_object.rotation_euler) 
    }
    return camera_setup

def apply_camera_setup(camera_setup):
    """
    apply_camera_setup Applies the given setup to the active camera

    This will set the "location" and "rotation_euler" properties 
    from the given dictionary as the corresponding properties
    of the active camera

    :param camera_setup: The camera setup
    """     
    camera_object = bpy.context.scene.camera
    #print(camera_setup)
    camera_object.location = tuple(camera_setup['location'])
    camera_object.rotation_euler = tuple(camera_setup['rotation_euler'])


def create_single_render(input_gltf_path, output_file_name_prefix, camera_setup):
    """
    create_render Creates a single, rendered image of the given glTF.

    This will load the given glTF, apply the given camera setup,
    and create a rendered image that is written to the specified
    path. The path will be made absolute, and ".png" (including
    the dot) will be appended.

    :param input_gltf_path: The input glTF
    :param output_file_name_prefix: The output file name prefix
    :param camera_setup: The camera setup
    """     
    print("create_render")
    print("input_gltf_path is " + input_gltf_path)
    print("output_file_name_prefix is " + output_file_name_prefix)

    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    bpy.ops.import_scene.gltf(filepath=input_gltf_path,filter_glob='*.glb;*.gltf')
    set_up_environment()
    init_camera()
    apply_camera_setup(camera_setup)
    render_single_frame(output_file_name_prefix)

# TODO
def render_all_frames(output_file_name_prefix):
    full_file_prefix = os.path.abspath(output_file_name_prefix)

    bpy.context.scene.render.resolution_x = 512
    bpy.context.scene.render.resolution_y = 512

    number_of_frames = compute_number_of_frames()
    for frame in range(0, number_of_frames):    
        bpy.context.scene.frame_set(frame)
        bpy.context.scene.render.filepath = full_file_prefix + str(frame).zfill(4) + ".png"
        bpy.ops.render.render(write_still=True)

    bpy.context.scene.frame_set(0)


