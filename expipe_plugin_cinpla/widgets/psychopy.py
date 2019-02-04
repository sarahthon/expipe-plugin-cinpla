from expipe_plugin_cinpla.imports import *
from expipe_plugin_cinpla.scripts import tracking
from .utils import SelectDirectoryButton, MultiInput, SearchSelectMultiple, SelectFileButton, \
    required_values_filled, none_if_empty, split_tags, SearchSelect, ParameterSelectList
import ast

from ..scripts.psychopy import psychopy


def process_psychopy_view(project):
    openephys_path = SelectDirectoryButton(description='*Select OpenEphys path')
    json_path = SelectDirectoryButton(description='*Select JSON path')
    action_id = SearchSelect(project.actions, description='*Actions', layout={'width': 'initial'})
    run = ipywidgets.Button(description='Process', layout={'width': '100%', 'height': '100px'})
    run.style.button_color = 'pink'

    main_box = ipywidgets.VBox([
            ipywidgets.HBox([openephys_path, action_id]), run
        ], layout={'width': '100%'})
    main_box.layout.display = 'flex'

    def on_run(change):
        if not required_values_filled(openephys_path, action_id):
            return

        psychopy(
            project=project,
            action_id=action_id.value,
            jsonpath=json_path)

    run.on_click(on_run)
    return main_box