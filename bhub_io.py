import os
import time
from os.path import dirname, join, pardir, exists, basename, isfile
import sys
import pathlib
import json
import threading
import subprocess


def run_in_thread(on_exit, popen_args):
    process = subprocess.Popen(popen_args)
    process.wait()
    time.sleep(3)
    print("Thread finish...")
    on_exit()
    return

def popen_and_call(on_exit, popen_args):
    """
    Runs the given args in a subprocess.Popen, and then calls the function
    on_exit when the subprocess completes.
    on_exit is a callable object, and popen_args is a list/tuple of args that
    would give to subprocess.Popen.
    """
    thread = threading.Thread(target=run_in_thread, args=(on_exit, popen_args))
    thread.start()
    # returns immediately after the thread starts
    return thread


def get_datadir() -> pathlib.Path:
    """
    Returns a parent directory path
    where persistent application data can be stored.

    # linux: ~/.local/share
    # macOS: ~/Library/Application Support
    # windows: C:/Users/<USER>/AppData/Roaming
    """

    home = pathlib.Path.home()

    if sys.platform == "win32":
        return home / "AppData/Roaming"
    elif sys.platform == "linux":
        return home / ".local/share"
    elif sys.platform == "darwin":
        return home / "Library/Application Support"


datadir = get_datadir()
bhub_path = datadir / "BlenderHub"
bhub_dir = str(bhub_path)
bf_dir = datadir / "Blender Foundation"
blender_dir = join(bhub_dir, 'Blender')  # join(dirname(__file__), 'blender')
bf_blender_dir = join(str(bf_dir), 'Blender')
recent_files = join(bf_blender_dir, '2.83', 'config', 'recent-files.txt')
autosave_dir = join(bhub_dir, 'autosave')  # join(dirname(__file__), 'autosave')
thumbnails_dir = join(bhub_dir, 'thumbnails')
config_dir = join(bhub_dir, 'config')
projects_list = join(config_dir, 'projects.json')
generator_script = join(dirname(__file__), 'generate_preview.py')
styles_dir = join(bhub_dir, 'styles')
stylesheet = join(config_dir, 'stylesheet')


def launch_blender(file='autosave.blend', use_filepath=False, version='2.83'):
    if not use_filepath:
        if file == '':
            file = 'autosave.blend'
    else:
        if not file.endswith('.blend'):
            file += '.blend'

    ########################
    # Open .blend project. #
    ########################
    file = file if use_filepath else join(autosave_dir, file)
    subprocess.Popen([join(blender_dir, version, 'blender.exe'), file])

    ########################
    # Update project list. #
    ########################
    with open(projects_list, 'r') as json_file:
        raw_data = json_file.read()
        if not raw_data:
            return False
        data = json.loads(raw_data)
        if not data or not isinstance(data, dict):
            data = {}
        else:
            name = basename(file)[:-6]
            new_data = {name: data[name]}
            del data[name]
            data = {**new_data, **data}

    with open(projects_list, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

    return True

    # FREEZE (live communication with Blender, should be used with threads) #
    # subprocess.call([join(blender_dir, version, 'blender.exe'), file])
    # process = subprocess.Popen([join(blender_dir, version, 'blender.exe'), file])
    # stdout, stderr = process.communicate()
    # print("Subprocess has finished.")


# To preview thumbnails.
def register_blend_extension(version="2.83"):
    os.system(join(blender_dir, version, 'blender') + " -r")


FNULL = open(os.devnull, 'w')


def generate_preview(filepath='', version='2.83', wait=False, finish_callback=None):
    # if isfile(filepath):
    if filepath.endswith('.blend'):
        filepath = filepath[:-6]
    img_path = join(thumbnails_dir, basename(filepath) + '.png')
    if isfile(img_path):
        return True, img_path
    if wait:
        subprocess.call([join(blender_dir, version, 'blender'),
                         filepath + '.blend',
                         '--background',
                         '--python',
                         generator_script],
                        stdout=FNULL, stderr=subprocess.STDOUT)
        if finish_callback:
            finish_callback()
    else:
        if finish_callback:
            print("Callback:", finish_callback)
            popen_and_call(finish_callback, [join(blender_dir, version, 'blender'),
                                             filepath + '.blend',
                                             '--background',
                                             '--python',
                                             generator_script])
        else:
            subprocess.Popen([join(blender_dir, version, 'blender'),
                              filepath + '.blend',
                              '--background',
                              '--python',
                              generator_script],
                             stdout=FNULL, stderr=subprocess.STDOUT)
    # print("Thumbnail generated for %s\n\t->%s" % (filepath, join(thumbnails_dir, basename(filepath) + '.png')))
    return False, img_path
    # print("No thumbnail generated for", filepath)
    # return None


def get_thumbnail_path(filepath):
    if not isfile(filepath):
        print("WTF is this file", filepath)
        return None
    if filepath.endswith('.blend'):
        filepath = filepath[:-6]
    img_path = join(thumbnails_dir, basename(filepath) + '.png')
    ok = exists(img_path)
    return ok, img_path


def add_project(filepath='', wait=True, finish_callback=None):
    if not filepath or filepath == '' or not exists(filepath):
        return None
    print("Adding project:", filepath)

    with open(projects_list, 'r') as json_file:
        raw_data = json_file.read()
        # print("Data loaded:", raw_data)
        if not raw_data:
            return None
        data = json.loads(raw_data)
        if not data or not isinstance(data, dict):
            data = {}

    # with open(filepath, 'r') as blend:
    #    v = blend.read(12)[-3:]
    #    blender = v[0] + '.' + v[1:]

    name = basename(filepath)[:-6]
    new_data = {}
    props = {
        'file_path': filepath,
        'dirty': False,
        'blender': '2.83',
        'version': 1.0
    }
    new_data[name] = props
    data = {**new_data, **data}
    # print("New Data:", str(data))

    with open(projects_list, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

    print("Callback:", finish_callback)
    was_created, img_path = generate_preview(filepath, '2.83', wait, finish_callback)
    if was_created:
        if finish_callback:
            finish_callback()
        print("Thumbnail was Found")
    else:
        print("Thumbnail was Generated")

    return True  # [name, props]
