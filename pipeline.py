
import os
import time
import uuid
import openai
import requests
# from prompt_toolkit import prompt
import json
from dotenv import load_dotenv

import urllib3
import bpy
# from tdqm import tdqm
from blenderapi.json2scene import create_blender_scene

load_dotenv()

WAIT_TIME = 180  # in seconds
MESHY_API_KEY = os.getenv('MESHY_API_KEY')
HYPERBOLIC_API_KEY = os.getenv('HYPERBOLIC_API_KEY')
OBJECT_TYPE = "glb" # type to use in blender scene created. Types - glb, obj, stl, fbx
# from rich import print, z

CLIENT = openai.OpenAI(
        api_key=HYPERBOLIC_API_KEY,
        base_url="https://api.hyperbolic.xyz/v1",
        )

def extract_objects(scene_json):
    objects = []
    for obj in scene_json['area_objects_list']:
        objects.append({
            "object_name": obj['object_name'],
            "X": obj['X'],
            "Y": obj['Y'],
            "Z": obj['Z'],
            "scale_X": obj['scale_X'],
            "scale_Y": obj['scale_Y'],
            "scale_Z": obj['scale_Z'],
            "rotation_Z": obj['rotation_Z'],
            "Material": obj['Material']
        })
    return objects

def prompt_llm(system_prompt, user_text):
    chat_completion = CLIENT.chat.completions.create(
        model="meta-llama/Meta-Llama-3-70B-Instruct",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_text},
        ],
        temperature=0.7,
        max_tokens=1024,
    )

    response = chat_completion.choices[0].message.content
    print("Response:\n", response)

    return json.loads(response)


def download_generated_asset(object_url, id, object_type):
        r = requests.get(object_url, allow_redirects=True)
        path = f"./outputs/assets/{id}.{object_type}"
        open(path, 'wb').write(r.content)
        return path


def download_asset_from_meshy(task_id, headers):
    response = requests.get(
        f"https://api.meshy.ai/v2/text-to-3d/{task_id}",
        headers=headers,
    )
    response.raise_for_status()
    print(response.json())
    return response


def meshy_api_call(prompt, object):
    payload = {
        "mode": "preview",
        "prompt": prompt,
        "art_style": "realistic",
    }
    headers = {
        "Authorization": f"Bearer {MESHY_API_KEY}"
    }

    # try:
    response = requests.post(
        "https://api.meshy.ai/v2/text-to-3d",
        headers=headers,
        json=payload,
    )
    response.raise_for_status()
    print(response.json())

    task_id = response.json()["result"]

    # # wait for the task to complete
    retry_count = 0
    while True:

        response = download_asset_from_meshy(task_id, headers)

        if response.json()["status"] == "SUCCEEDED":
            break    
        elif retry_count >= 15:
            print("Job failed after 10 retries")
            return object, False
        
        print("Job is running. Wait for 30 secs")
        time.sleep(30) # Job is running. Again wait for 30 secs
        retry_count+= 1


    obj_file_url = response.json()["model_urls"]["obj"]
    mtl_file_url = response.json()["model_urls"]["mtl"]
    glb_file_url = response.json()["model_urls"]["glb"]

    id = uuid.uuid4()

    # Download the generated asset
    obj_path = download_generated_asset(obj_file_url, id, "obj")
    mtl_path = download_generated_asset(mtl_file_url, id, "mtl")
    glb_path = download_generated_asset(glb_file_url, id, "glb")
    try:
        texture_file_url = response.json()["texture_urls"]["base_color"]
        texture_path = download_generated_asset(texture_file_url, id, "png")
    except:
        texture_path = None
        pass # no texture file


    
    object['object_type'] = OBJECT_TYPE

    object['generated_asset_path'] = {
        "glb_path": glb_path,
        "obj_path": obj_path,
        "mtl_path": mtl_path,
        "texture_path": texture_path
    }

    return object, True
    # except Exception as e:
        # print(e)
        # return object, False
    


def generate_assets(object_data):
    obj_data = []
    # for object in tdqm(object_data):
    for object in object_data:
        text_to_3d_prompt = object_generation_prompt + f"{object['Material']} {object['object_name']}"
        object, asset_generation_status = meshy_api_call(text_to_3d_prompt, object)
        if asset_generation_status is False:
            print(f"Failed to generate asset for {object['object_name']}")
        else:
            obj_data.append(object)
            print(f"Asset generated for {object['object_name']}")
    return obj_data


def open_blender(blender_filename):
    # This will not work on window. 
    # Try - https://stackoverflow.com/questions/43696735/how-can-i-open-a-windows-10-app-with-a-python-script
    os.system(f"blender ./outputs/blender/{blender_filename}.blend &")


system_prompt = ""

with open("./prompts/create_system_prompt.txt", "r") as f:
    system_prompt = f.read()


with open("./prompts/edit_system_prompt.txt", "r") as f:
    edit_system_prompt = f.read()

with open("./prompts/object_generation_prompt.txt", "r") as f:
    object_generation_prompt = f.read()


preview_count = 1
create_stage = True # if current stage is creation

while True:

    if create_stage is True:
        user_text = input("Write a description of your scene: ")
    else:
        user_text = input("Write the edit description you want to make: ")

    if user_text == "exit":
        break

    if create_stage is False:
        # TODO: test this prompt
        user_text = f"Scene JSON - {scene_json} \n {edit_system_prompt} - {user_text}"

    # scene_json = prompt_llm(system_prompt, user_text)

    # use cached response for testing
    with open("./prompts/response.json", "r") as f:
        scene_json = json.load(f)

    # extract object data from scene_json
    object_data = extract_objects(scene_json)

    print("Creating Blender Scene...")

    blender_filename = f"Preview_{preview_count}"

    filename = create_blender_scene(scene_json, blender_filename)

    print(f"Preview Blender Scene Created! & file saved as {blender_filename}")

    open_blender(filename)

    preview_count += 1

    print("Following objects were created - ")
    for obj in object_data:
        print(f"-- {obj['object_name']} --")
    print("Do you want to edit the scene?")
    user_input = input("Yes/No: ")
    if user_input.lower() == "yes":
        create_stage = False # now stage is editing
        print("Following properties can be edited at this stage: ")
        print("- Object Name")
        print("- It's position in the scene")
        print("- It's scale")
        print("- It's material")

    elif user_input.lower() == "no":
        print("Great! Moving on to the next step.")
        
        obj_data = generate_assets(object_data)
        
        print("All assets generated successfully!")

        # update object data with generated assets
        scene_json['area_objects_list'] = obj_data
        filename = create_blender_scene(scene_json, blender_filename, 'generated')
        
        open_blender(filename)

        break
    else:
        print("Invalid input. Please try again.")
