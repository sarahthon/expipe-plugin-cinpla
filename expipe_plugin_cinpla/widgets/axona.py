from expipe_plugin_cinpla.imports import *
from expipe_plugin_cinpla.scripts import axona
from .utils import SelectFilesButton, MultiInput, Templates


def axona_view(project):
    axona_path = SelectFilesButton()
    user = ipywidgets.Text(placeholder='*User', value=PAR.USERNAME)
    location = ipywidgets.Text(placeholder='*Location', value=PAR.LOCATION)
    action_id = ipywidgets.Text(placeholder='Action id')
    entity_id = ipywidgets.Text(placeholder='Entity id')
    message = ipywidgets.Text(placeholder='Message')
    tag = ipywidgets.Text(placeholder='Tags (; to separate)')
    templates = Templates(project)
    depth = MultiInput(['Key', 'Probe', 'Depth', 'Unit'], 'Add depth')
    register_depth = ipywidgets.Checkbox(description='Register depth', value=False)
    register_depth_from_adjustment = ipywidgets.Checkbox(
        description='Find adjustments', value=True)

    load_input = ipywidgets.Checkbox(description='Load .inp', value=False)
    set_zero_cluster_to_noise = ipywidgets.Checkbox(description='Zero cluster noise', value=True)
    load_cut = ipywidgets.Checkbox(description='Load .cut', value=True)
    overwrite = ipywidgets.Checkbox(description='Overwrite', value=False)
    register = ipywidgets.Button(description='Register')

    fields = ipywidgets.VBox([
        user,
        location,
        action_id,
        entity_id,
        message,
        tag,
        register
    ])
    checks = ipywidgets.HBox([axona_path, register_depth, overwrite, load_cut, load_input])
    main_box = ipywidgets.VBox([
            checks,
            ipywidgets.HBox([fields, templates])
        ])


    def on_register_depth(change):
         if change['name'] == 'value':
             if change['owner'].value:
                 children = list(checks.children)
                 children = children[:2] + [register_depth_from_adjustment] + children[2:]
                 checks.children = children
             else:
                children = list(checks.children)
                del(children[2])
                checks.children = children


    def on_register_depth_from_adjustment(change):
         if change['name'] == 'value':
             if not change['owner'].value:
                 children = list(fields.children)
                 children = children[:5] + [depth] + children[5:]
                 fields.children = children
             else:
                 children = list(fields.children)
                 del(children[5])
                 fields.children = children

    register_depth.observe(on_register_depth)
    register_depth_from_adjustment.observe(on_register_depth_from_adjustment)


    def on_register(change):
        tags = tag.value.split(';')
        axona.register_axona_recording(
            project=project,
            action_id=action_id.value,
            axona_filename=axona_path.files,
            depth=depth.value,
            user=user.value,
            overwrite=overwrite.value,
            templates=templates.value,
            entity_id=entity_id.value,
            location=location.value,
            message=message.value,
            tag=tags,
            get_inp=get_inp.value,
            no_cut=no_cut.value,
            cluster_group=[],
            set_zero_cluster_to_noise=set_zero_cluster_to_noise.value,
            register_depth=register_depth.value,
            correct_depth_answer=True)

    register.on_click(on_register)
    return main_box
