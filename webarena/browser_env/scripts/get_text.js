() => {
    var items = Array.prototype.slice.call(
        document.querySelectorAll("*")
    );

    var vw = Math.max(document.documentElement.clientWidth || 0, window.innerWidth || 0);
    var vh = Math.max(document.documentElement.clientHeight || 0, window.innerHeight || 0);
    const ignoreTags = ["script", "html"];
    items = items.map(element => {
        const tag = element.tagName.toLowerCase?.() || "";
        var bb = element.getClientRects();
        var keep = false;
        var text = '';

        const domId = element.getAttribute('data-testid');
        var id = domId? parseInt(domId): "-";

        if (bb.length > 0) {
            bb = bb[0];
            var width = Math.min(vw, bb.right) - Math.max(0, bb.left);
            var height = Math.min(vh, bb.bottom) - Math.max(0, bb.top);

            if (width > 0 && height > 0) {
                keep = true;
                var childNodes = element.childNodes;
                
                for (var i = 0; i < childNodes.length; i++) {
                    if (childNodes[i].nodeType == Node.TEXT_NODE) {
                        text += childNodes[i].textContent;
                    }
                }
            }
        }
        
        text = text.trim().replace(/\s{2,}/g, ' ');
        if (ignoreTags.includes(tag)) keep = false;
        if (id == "-" && text.length == 0) keep = false;
        
        return {
            keep,
            tag,
            id,
            text, //:element.innerText?.trim().replace(/\s{2,}/g, " ") || ""
        };
    }).filter(x => x.keep);
 
    return items;
}