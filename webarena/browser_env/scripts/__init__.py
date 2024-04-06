import os
from pathlib import Path
rootdir = Path(__file__).parent

# marker, gpt-4v-act style
with open(os.path.join(rootdir, 'local_marker.js'), 'r') as f:
    local_marker_script = f.read()
    
with open(os.path.join(rootdir, 'mix_marker.js'), 'r') as f:
    mix_marker_script = f.read()

with open(os.path.join(rootdir, 'get_data.js'), 'r') as f:
    get_rect_script = f.read()

# canva handler
with open(os.path.join(rootdir, 'canva_handler.js'), 'r') as f:
    canva_handler_script = f.read()

# draw label on page
with open(os.path.join(rootdir, 'label_marker.js'), 'r') as f:
    label_marker_script = f.read()
    
# get text from page
with open(os.path.join(rootdir, 'get_text.js'), 'r') as f:
    get_text_script = f.read()

# remove label draw on page
remove_label_mark_script = """
    () => {
        document.querySelectorAll(".our-dom-marker").forEach(item => {
            document.body.removeChild(item);
        });
    }
"""

remove_id_script = """
    () => {
        Array.from(document.getElementsByClassName('possible-clickable-element')).forEach((element) => {
            element.classList.remove('possible-clickable-element');
            element.removeAttribute('data-testid');
        });
    }
"""
