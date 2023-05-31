import os
import sys
import bpy
import json
import math
import argparse
import mathutils

def ensure_directory_exists(path):
    dirname = os.path.dirname(path)
    exists = os.path.exists(dirname)
    if not exists:
        os.makedirs(dirname)

def convert_gltf_to_usd(input_path, output_path):

    print("convert_gltf_to_usd")
    print("input_path is " + input_path)
    print("output_path is " + output_path)

    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    bpy.ops.import_scene.gltf(filepath=input_path,filter_glob='*.glb;*.gltf')
    
    ensure_directory_exists(output_path)
    bpy.ops.wm.usd_export(filepath=output_path, export_animation=True)

def convert_usd_to_gltf(input_path, output_path):

    print("convert_usd_to_gltf")
    print("input_path is " + input_path)
    print("output_path is " + output_path)

    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    bpy.ops.wm.usd_import(filepath=input_path, import_textures_dir="//textures")

    ensure_directory_exists(output_path)
    bpy.ops.export_scene.gltf(filepath=output_path, export_animations=True)

def parse_args():
    parser = argparse.ArgumentParser(description='Perform the roundtrip')
    parser.add_argument('-i', '--input_gltf_path', help='Input glTF model path')
    parser.add_argument('-u', '--usd_path', help='Path for intermediate USD model')
    parser.add_argument('-o', '--output_gltf_path', help='Output glTF model path')

    argv = sys.argv
    if "--" not in argv:
        argv = []
    else:
        argv = argv[argv.index("--") + 1:]
    args = parser.parse_args(argv)
    return args


def run_single():
    args = parse_args()

    input_gltf_path = os.path.abspath(args.input_gltf_path)
    usd_path = os.path.abspath(args.usd_path)
    output_gltf_path = os.path.abspath(args.output_gltf_path)

    convert_gltf_to_usd(input_gltf_path, usd_path)
    convert_usd_to_gltf(usd_path, output_gltf_path)

    euler = ( math.radians(90), 0, 0)
    camera_setup = compute_camera_setup(input_gltf_path, euler)

    create_render(input_gltf_path, "./render_before", camera_setup)
    create_render(output_gltf_path, "./render_after", camera_setup)


def run_single_model_variant(input_gltf_path, usd_path, output_gltf_path, model_name):

    print("run_single_model_variant")
    print("input_gltf_path  "+ input_gltf_path)
    print("usd_path         "+ usd_path)
    print("output_gltf_path "+ output_gltf_path)
    print("model_name       "+ model_name)

    convert_gltf_to_usd(input_gltf_path, usd_path)
    convert_usd_to_gltf(usd_path, output_gltf_path)

    render_output_directory = "./Data/renders"
    ensure_directory_exists(render_output_directory)

    euler = ( math.radians(90), 0, 0)
    camera_setup = compute_camera_setup(input_gltf_path, euler)

    input_render_name = os.path.join(render_output_directory, model_name + "_input");
    create_render(input_gltf_path, input_render_name, camera_setup)

    output_render_name = os.path.join(render_output_directory, model_name + "_output");
    create_render(output_gltf_path, output_render_name, camera_setup)


  
def run_single_model(input_gltf_path, usd_path, output_gltf_path, model_name, variants):
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

    full_input_gltf_path = os.path.join(input_gltf_path, model_name, variant_name, variant_file_name)
    full_usd_path = os.path.join(usd_path, model_name, variant_name, base_file_name + ".usd")
    full_output_gltf_path = os.path.join(output_gltf_path, model_name, variant_name, base_file_name + ".glb")
    run_single_model_variant(full_input_gltf_path, full_usd_path, full_output_gltf_path, model_name)



def run_model_index(input_gltf_path, usd_path, output_gltf_path):
    model_index_file_path = os.path.join(input_gltf_path, "model-index.json")
    with open(model_index_file_path, 'r') as model_index_file:
        model_index_data = json.load(model_index_file)
        for model_entry in model_index_data:
            model_name = model_entry["name"]
            variants = model_entry["variants"]
            run_single_model(input_gltf_path, usd_path, output_gltf_path, model_name, variants)



def setup_environment():
    light_name = "city.exr"
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
    camera = bpy.data.cameras.new("Camera")
    camera_object = bpy.data.objects.new("Camera Object", camera)
    bpy.context.scene.collection.objects.link(camera_object)
    camera_object.location = (0, 0, 0)
    camera_object.rotation_euler = (0, 0, 0)
    bpy.context.scene.camera = camera_object


def fit_active_camera(margin_factor=1.1):     
    
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.view3d.camera_to_view_selected()
    bpy.ops.object.select_all(action="DESELECT")

    camera_object = bpy.context.scene.camera
    mat = camera_object.rotation_euler.to_matrix()
    camera_direction = mat @ mathutils.Vector((0.0, 0.0, 1.0))
    camera_object.location += camera_direction * margin_factor

def compute_number_of_frames():
    number_of_frames = 0
    actions = bpy.data.actions
    if actions:
        for action in actions:
            number_of_frames = max(number_of_frames, action.frame_range[1])
            print("frame range");
            print(action.frame_range);
    return math.ceil(number_of_frames)

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



def render_single_frame(output_file_name_prefix):
    full_file_prefix = os.path.abspath(output_file_name_prefix)
    bpy.context.scene.frame_set(0)
    bpy.context.scene.render.resolution_x = 512
    bpy.context.scene.render.resolution_y = 512
    bpy.context.scene.render.filepath = full_file_prefix + ".png"
    bpy.ops.render.render(write_still=True)


def compute_camera_setup(input_gltf_path, euler=(0,0,0)):
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    bpy.ops.import_scene.gltf(filepath=input_gltf_path,filter_glob='*.glb;*.gltf')
    init_camera()

    camera_object = bpy.context.scene.camera
    camera_object.rotation_euler = euler

    fit_active_camera(margin_factor=1.1)

    camera_setup = {
        "location": tuple(camera_object.location), 
        "rotation_euler": tuple(camera_object.rotation_euler) 
    }
    return camera_setup

def apply_camera_setup(camera_setup):
    camera_object = bpy.context.scene.camera
    print(camera_setup)
    camera_object.location = camera_setup['location']
    camera_object.rotation_euler = camera_setup['rotation_euler']


def create_render(input_gltf_path, output_file_name_prefix, camera_setup):

    print("create_render")
    print("input_gltf_path is " + input_gltf_path)
    print("output_file_name_prefix is " + output_file_name_prefix)

    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    bpy.ops.import_scene.gltf(filepath=input_gltf_path,filter_glob='*.glb;*.gltf')
    setup_environment()
    init_camera()
    apply_camera_setup(camera_setup)
    render_single_frame(output_file_name_prefix);






def main():
    bpy.context.preferences.view.show_splash = False
    #run_single()
    #run_model_index()

    input_gltf_path = os.path.abspath("./Data/input_gltf")
    usd_path = os.path.abspath("./Data/usd")
    output_gltf_path = os.path.abspath("./Data/output_gltf")

 
    #variant_name = "glTF-Binary"
    #model_name = "DamagedHelmet"
    #variant_file_name = model_name + ".glb";
    #full_input_gltf_path = os.path.join(input_gltf_path, model_name, variant_name, variant_file_name)
    #full_usd_path = os.path.join(usd_path, model_name, variant_name, model_name + ".usd")
    #full_output_gltf_path = os.path.join(output_gltf_path, model_name, variant_name, model_name + ".glb")
    #run_single_model_variant(full_input_gltf_path, full_usd_path, full_output_gltf_path, model_name)

    run_model_index(input_gltf_path, usd_path, output_gltf_path)

    #bpy.ops.wm.quit_blender()

if __name__ == "__main__":
    main()
