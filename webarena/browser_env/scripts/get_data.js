(packet) => {
    function int2str(index) {
        var str = "";
        while (index >= 0) {
            str = String.fromCharCode(65 + index % 26) + str;
            index = Math.floor(index / 26) - 1;
        }
        return str;
    };

    selector = packet.selector
    index = packet.startIndex
    var items = Array.prototype.slice.call(
        document.querySelectorAll(selector)
    );

    var vw = Math.max(document.documentElement.clientWidth || 0, window.innerWidth || 0);
    var vh = Math.max(document.documentElement.clientHeight || 0, window.innerHeight || 0);
    
    items = items.filter(
        x => !items.some(y => x.contains(y) && !(x == y))
    ).map(element => {
        var bb = element.getClientRects();
        var rect = {
            left: 0,
            top: 0,
            right: 0,
            bottom: 0,
            width: 0,
            height: 0
        };
        var keep = false;
        var text = "", id = -1;
        if (bb.length > 0) {
            bb = bb[0];
            rect = {
                left: Math.max(0, bb.left),
                top: Math.max(0, bb.top),
                right: Math.min(vw, bb.right),
                bottom: Math.min(vh, bb.bottom)
            };
            rect = {
                ...rect,
                width: rect.right - rect.left,
                height: rect.bottom - rect.top
            };
            if (rect.width > 0 || rect.height > 0) {
                keep = true;
                if (index >= 0) { 
                    id = int2str(index++);
                    element.setAttribute("data-testid", id);
                }
                var childNodes = element.childNodes;
                
                for (var i = 0; i < childNodes.length; i++) {
                    if (childNodes[i].nodeType == Node.TEXT_NODE) {
                        text += childNodes[i].textContent;
                    }
                }
            }
        }
        
        return {
            keep: true,
            id,
            rects: rect,
            tag: element.tagName.toLowerCase?.() || "",
            text,//: element.innerText?.trim().replace(/\s{2,}/g, " ") || ""
        };
    }).filter(x => x.keep);

    return [items, index];
}