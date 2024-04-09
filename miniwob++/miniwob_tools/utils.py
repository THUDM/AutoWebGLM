from PIL import Image
import numpy as np
import copy

from .configs import testcases, mwpp_attrs, not_clickable_tag, miniwob_attrs, special_classes

def save_pixel_array(arr: np.ndarray, fp: str):
    im = Image.fromarray(arr)
    im.save(fp)
    
def get_dom_list(dom_list: list) -> str:
    prompt='{:3} {:3} {:5} {:15} {:15} {:5} {:12} {:30}'
    parts = []
    parts.append(prompt.format('ref', 'lab', 'tag', 'text', 'value', 'id', 'flags', 'classes'))
    parts.append('--------------------------------------------------------------------------------------------')
    ndom_list = update_dom_list(dom_list)
    for elem in ndom_list:
        if elem.get('invisible', False):
            continue
        parts.append(prompt.format(str(elem['ref']), elem.get('label', ''), elem['tag'][:5], elem['text'][:15], elem['value'][:15], elem['id'][:5], str(elem['flags']), elem['classes'][:30]))
        
    return parts

def update_dom_list(dom_list: list) -> list:
    def _dfs(elem: dict, dom_list: list, args: dict={}) -> None:
        cur_args = copy.deepcopy(args)
        cur_args['tag'] = elem.get('tag', '')
        for key in ['top', 'left', 'width', 'height']:
            if key not in elem:
                elem[key] = args.get(key, '-1')
            cur_args.update({key: elem[key]})
        
        # judge position
        if float(elem['top']) > 200 or float(elem['top']) + float(elem['height']) < 55:
            elem['invisible'] = True
        
        if 'height' in args and 'top' in args and args.get('tag', '') == 'select':
            mid_point = float(elem['top']) + float(elem['height']) * 0.5
            if (mid_point > float(args['top']) + float(args['height'])
                or mid_point < float(args['top'])):
                elem['invisible'] = True
        
        # determine if it is hidden
        if args.get('hidden', False) or elem['classes'].count('ui-helper-hidden-accessible') > 0:
            elem['hidden'] = True
            elem['invisible'] = True
            cur_args['hidden'] = True
        
        for dom in dom_list:
            if dom['parent'] != elem['ref']:
                continue
            _dfs(dom, dom_list, cur_args)
    
    if len(dom_list) == 0:
        return []

    new_dom_list = copy.deepcopy(dom_list)
    _dfs(new_dom_list[0], new_dom_list)
    return new_dom_list

def process_dom_list(dom_list):
    dom_list = copy.deepcopy(dom_list)
    for elem in dom_list:
        for k in ['left', 'top', 'width', 'height']:
            elem[k] = str(float(elem[k]))
        for k in ['bg_color', 'fg_color', 'flags']:
            elem[k] = [str(v) for v in elem[k]]
    return dom_list

def get_html(dom_list: list) -> str:
    def get_json_tree(elem: dict, dom_list: list) -> dict:
        elem['children'] = []
        for dom in dom_list:
            if dom['parent'] != elem['ref']:
                continue
            get_json_tree(dom, dom_list)
            elem['children'].append(dom)
        return elem
    
    def convert(elem: dict) -> str:
        invisible = elem.get('invisible', False)
        
        obs_list = []
        ref = str(elem.get('ref', None))
        id = elem.get('id', '')
        tag = elem.get('tag', '')
        text = elem.get('text', '')
        classes = elem.get('classes', '')
        flags = elem.get('flags', [])
        
        elem['classes'] = ' '.join([v for v in classes.split(' ') if v.count('ui-') == 0 or v.count('ui-spinner-up') > 0  or v.count('ui-spinner-down') > 0])
                
        attr_str = f' ref="{ref}"'
        if tag.find('_') != -1:
            tag, typ = tag.split('_')
            attr_str += f' type="{typ}"'

        for key in mwpp_attrs['basic']:
            val = elem.get(key, '')
            if len(val) != 0:
                attr_str += f' {key}="{val}"'
        for key in mwpp_attrs['position']:
            if key in elem:
                val = str(float(elem[key]))
                attr_str += f' {key}="{val}"'
        
        color_col = []
        for key, tkey in mwpp_attrs['color'].items():
            if key in elem:
                color_col.append(f'{tkey}: {elem[key]}')
        
        if len(color_col) != 0:
            attr_str += ' style="{}"'.format('; '.join(color_col))
            
        is_click_shades = tag == 'span' and float(elem['width']) == 12 and float(elem['height']) == 12
        if classes.count('color') > 0 or is_click_shades:
            colors = list(elem.get('bg_color', []))
            attr_str += ' rgba="rgb({})"'.format(','.join([str(round(float(color), 2)) for color in colors[:-1]]))
            
        if classes.count('SVG_CLASS') > 0 and tag != 'svg':
            positions = [float(x) for x in [elem['width'], elem['height']]]
            attr_str += ' size="size({})"'.format(','.join([str(round(pos, 1)) for pos in positions]))
        
        special_class = 0
        for spec in special_classes:
            special_class += classes.count(spec)
        
        if not invisible and (
            tag not in not_clickable_tag
            or special_class > 0
            or (classes.count('email-') > 0 and flags[3] == 1)
            or id.count('ui-id') > 0
            or text.lower().count('submit') > 0
            or text.lower().count('search') > 0
            or False):
            obs_list.append(ref)
                
        child_dom = [text]
        for child in elem.get('children', []):
            cdom, cobs = convert(child)
            child_dom.append(cdom)
            obs_list.extend(cobs)
        
        child_str = ' '.join(child_dom)
        
        if invisible:
            attr_str = ''  
         
        dom = f'<{tag}{attr_str}> {child_str} </{tag}>'
        return dom, obs_list
    
    ndom_list = update_dom_list(dom_list)
    root = get_json_tree(ndom_list[0], ndom_list)
    return convert(root)

def get_page_height(dom_list: list) -> tuple[float, float]:
    pg_top, pg_bot = 150, 0
    ndom_list = update_dom_list(dom_list)
    for ix, elem in enumerate(ndom_list):
        ref = elem['ref']
        if ref <= 2 or elem.get('hidden', False):
            continue
        top = float(elem['top'])
        height = float(elem['height'])
        if top < pg_top:
            pg_top = top
        if top + height > pg_bot:
            pg_bot = top + height
    
    pg_height = pg_bot - pg_top
    cur_pos = pg_top - 50
    return round(abs(cur_pos / 150), 2), round(pg_height / 150, 2)

def get_position_bar(dom_list: list) -> list:
    position, page_height = get_page_height(dom_list)
    left_bar = '-' * int(position)
    right_bar = '-' * int(max(page_height - position, 1))
    position_bar = f'[0{left_bar}|{round(position, 1)}{right_bar}{round(page_height, 1)}]'
    return position_bar

def get_position_info(dom_list: list) -> list:
    position, page_height = get_page_height(dom_list)
    return f"{position} / {page_height}"