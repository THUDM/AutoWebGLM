() => {
    var items = Array.prototype.slice.call(
        document.querySelectorAll("canvas")
    );

    var vw = Math.max(document.documentElement.clientWidth || 0, window.innerWidth || 0);
    var vh = Math.max(document.documentElement.clientHeight || 0, window.innerHeight || 0);
    
    items = items.map(element => {
        // var img = element.toDataURL("image/png");
        var bb = element.getClientRects();
        var rect = {
            left: -1,
            top: -1,
            right: -1,
            bottom: -1,
            width: 0,
            height: 0,
        };
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
        }
        
        return {
            rects: rect,
            tag: element.tagName.toLowerCase?.() || "",
            text: element.textContent.trim().replace(/\s{2,}/g, ' '),
            // img: img
        };
    });

    return items;
}