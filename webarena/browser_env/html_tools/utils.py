from lxml import html
def get_xpath_top_down(element: html.HtmlElement, id_column: str='temp_id', label_column: str='temp_clickable_label', path: str='', order: int=0, 
                        in_svg: bool=False, temp_id: int=0) -> tuple[int, dict[str, str], dict[str]]:
    used_labels, i2xpath = {}, {}
    # path
    tag = element.tag.lower()
    in_svg = in_svg or (tag == 'svg')
    
    if not in_svg and 'id' in element.attrib:
        node_id = element.attrib['id']
        path = f'//*[@id="{node_id}"]'
    else:
        suffix = f'[{order}]' if order > 0 else ''
        prefix = f'*[name()="{tag}"]' if in_svg else tag
        path = path + '/' + prefix + suffix
    
    # add temp id
    element.attrib[id_column] = str(temp_id)
    ori_label = element.attrib.get(label_column, '')
    if ori_label != '':
        used_labels[ori_label] = True
    
    bid = str(temp_id)
    i2xpath[bid] = path
    i2xpath[path] = bid
    i2xpath[f'xpath/{path}'] = bid
    i2xpath[f'xpath=/{path}'] = bid
    
    temp_id += 1
    
    # traverse node
    children = element.getchildren()
    tag_dict = {}
    id_list = []
    for child in children:
        ctag = child.tag.lower()
        if ctag not in tag_dict:
            tag_dict[ctag] = 0
        tag_dict[ctag] += 1
        id_list.append(tag_dict[ctag])
    
    for cid, child in zip(id_list, children):
        ctag = child.tag.lower()
        cod = cid if tag_dict[ctag] > 1 else 0
        temp_id, i2x, ulabels = get_xpath_top_down(child, id_column, label_column, path, cod, in_svg, temp_id)
        i2xpath.update(i2x)
        used_labels.update(ulabels)
    
    return temp_id, i2xpath, used_labels
        
def print_html_object(obj: str='') -> str:
    tab_cnt = 0
    result, content, sep = '', '', ''
    last_is_left, last_is_right = False, False
    for ch in obj:
        if ch == '<':
            result += '\n'
            if len(content.strip()) > 0:
                result += sep + content.strip() + '\n'
            result += sep + '<'
            
            tab_cnt += 1
            sep = '  ' * tab_cnt
            
            content = ''
            last_is_right = False
            last_is_left = True
        elif ch == '>':
            if last_is_left:
                result += content
            else:
                if last_is_right:
                    result += '\n'
                if len(content.strip()) > 0:
                    result += sep + content.strip() + '\n'
            
            tab_cnt -= 1
            sep = '  ' * tab_cnt
            
            if not last_is_left:
                result += sep
            
            result += '>'
            content = ''
            
            last_is_right = True
            last_is_left = False
        else:
            content += ch
    
    return result

def rect2tuple(rect: str) -> tuple[int, int, int, int]:
    if rect is None or type(rect) != type('str'):
        return None
    rect = rect.strip()
    if rect.count(',') != 3:
        return None
    rect = rect.split(',')
    rect = [float(r) for r in rect]
    return tuple(rect)