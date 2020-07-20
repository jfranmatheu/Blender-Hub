def check_folders():
    from os.path import exists
    from bhub_io import bhub_dir, blender_dir, autosave_dir, thumbnails_dir, config_dir, styles_dir
    from os import mkdir
    if not exists(bhub_dir):
        bhub_dir.mkdir(parents=True)
    if not exists(blender_dir):
        mkdir(blender_dir)
    if not exists(autosave_dir):
        mkdir(autosave_dir)
    if not exists(thumbnails_dir):
        mkdir(thumbnails_dir)
    if not exists(config_dir):
        mkdir(config_dir)
    if not exists(styles_dir):
        mkdir(styles_dir)


def check_projects():
    from bhub_io import projects_list
    import json
    from os.path import exists
    if not exists(projects_list):
        with open(projects_list, 'x') as file:
            data = {}
            json.dump(data, file)
        return

    with open(projects_list, "w+") as file:
        raw_data = file.read()
        if not raw_data:
            return
        data = json.load(file)
        changes = False
        if data and isinstance(data, dict):
            for name, props in data.items():
                # print("Name:", name)
                # for k, v in props.items():
                #    print("\t-", v)
                if not exists(props['file_path']):  # AUTOLIMPIEZA?
                    # props['invalid'] = True
                    del data[name]
                else:
                    if props['blender'] == '':
                        with open(props['file_path']) as blend:
                            v = blend.read(12)[-3:]
                            props['blender'] = v[0] + '.' + v[1:]
                        changes = True
                    if props['dirty']:
                        from bhub_io import generate_preview
                        generate_preview(props['file_path'], props['blender'], True)
                        props['dirty'] = False
                        changes = True
            if changes:
                json.dump(data, file, ensure_ascii=False, indent=4)


def load_style():
    from bhub_io import stylesheet
    from styles import loadStylesheet
    from os.path import exists
    if not exists(stylesheet):
        with open(stylesheet, 'x'):
            loadStylesheet()
            return
    with open(stylesheet, 'r') as file:
        active_style = file.readline()
        if not active_style or active_style == '':
            loadStylesheet()
        else:
            loadStylesheet(active_style)
