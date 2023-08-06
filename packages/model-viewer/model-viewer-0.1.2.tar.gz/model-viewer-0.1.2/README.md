# TemporalViewer

TemporalViewer enables the exploration of temporal distribution of the model outputs in Jupyter Notebooks.

## Demo

In Jupyter Notebook:
```Python
import ModelViewer
import json

# Open JSON files
f_steps = open('/Users/soniacq/PTG/TemporalViewer/ModelViewer/data/reasoning_check_status.json')
f_objects = open('/Users/soniacq/PTG/TemporalViewer/ModelViewer/data/detic_image.json')
f_actions = open('/Users/soniacq/PTG/TemporalViewer/ModelViewer/data/egovlp_action_steps.json')
f_metadata = open('/Users/soniacq/PTG/TemporalViewer/ModelViewer/data/ngc_0293_13_additional_metadata_v1.json')
main_camera_path = '/Users/soniacq/PTG/TemporalViewer/ModelViewer/data/ngc_0293_13-main.mp4'
  
# Takes file objects and returns JSON object as dictionaries
data_steps = json.load(f_steps)
data_objects = json.load(f_objects)
data_actions = json.load(f_actions)
data_metadata = json.load(f_metadata)

# create a session
session_info = {'reasoningJSONFile': data_steps, 'boundingBoxJSONFile': data_objects,
                'egovlpActionJSONFile': data_actions, 'recordingMetadata': data_metadata,
                'recordingName': 'ngc_0293_13', 'mainCameraPath': main_camera_path}

ModelViewer.plot_datasets_summary(session_info)
```

## Install

### Option 1: install via pip:
~~~~
pip install model-viewer
~~~~