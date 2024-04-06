() => {
    var items = Array.prototype.slice.call(
        document.querySelectorAll('*')
    ).map(function(element) {
        var vw = Math.max(document.documentElement.clientWidth || 0, window.innerWidth || 0);
        var vh = Math.max(document.documentElement.clientHeight || 0, window.innerHeight || 0);
        
        var rects = [...element.getClientRects()].filter(bb => {
            var center_x = bb.left + bb.width / 2;
            var center_y = bb.top + bb.height / 2;
            var elAtCenter = document.elementFromPoint(center_x, center_y);
        
            if (!elAtCenter) return false;
            return elAtCenter === element || element.contains(elAtCenter) 
        }).map(bb => {
            const rect = {
                left: Math.max(0, bb.left),
                top: Math.max(0, bb.top),
                right: Math.min(vw, bb.right),
                bottom: Math.min(vh, bb.bottom)
            };
            return {
                ...rect,
                width: rect.right - rect.left,
                height: rect.bottom - rect.top
            }
        });
        // var rects = [];
        var area = rects.reduce((acc, rect) => acc + rect.width * rect.height, 0);
    
        const tagName = element.tagName.toLowerCase?.() || "";
        let isClickable = ((element.onclick != null) || window.getComputedStyle(element).cursor == "pointer");
        
        // Insert area elements that provide click functionality to an img.
        if (tagName === "img") {
            let mapName = element.getAttribute("usemap");
            if (mapName) {
                const imgClientRects = element.getClientRects();
                mapName = mapName.replace(/^#/, "").replace('"', '\\"');
                const map = document.querySelector(`map[name=\"${mapName}\"]`);
                if (map && (imgClientRects.length > 0)) isClickable = true;
            }
        }
    
        if (!isClickable) {
            const role = element.getAttribute("role");
            const clickableRoles = [
                "button",
                "tab",
                "link",
                "checkbox",
                "menuitem",
                "menuitemcheckbox",
                "menuitemradio",
                "radio",
            ];
            if (role != null && clickableRoles.includes(role.toLowerCase())) {
                isClickable = true;
            } else {
                const contentEditable = element.getAttribute("contentEditable");
                if (
                contentEditable != null &&
                ["", "contenteditable", "true"].includes(contentEditable.toLowerCase())
                ) {
                isClickable = true;
                }
            }
        }
    
        // Check for jsaction event listeners on the element.
        if (!isClickable && element.hasAttribute("jsaction")) {
            const jsactionRules = element.getAttribute("jsaction").split(";");
            for (let jsactionRule of jsactionRules) {
                const ruleSplit = jsactionRule.trim().split(":");
                if ((ruleSplit.length >= 1) && (ruleSplit.length <= 2)) {
                const [eventType, namespace, actionName] = ruleSplit.length === 1
                    ? ["click", ...ruleSplit[0].trim().split("."), "_"]
                    : [ruleSplit[0], ...ruleSplit[1].trim().split("."), "_"];
                if (!isClickable) {
                    isClickable = (eventType === "click") && (namespace !== "none") && (actionName !== "_");
                }
                }
            }
        }
    
        if (!isClickable) {
            const clickableTags = [
                "input",
                "textarea",
                "select",
                "button",
                "a",
                "iframe",
                "video",
                "object",
                "embed",
                "details"
            ];
        isClickable = clickableTags.includes(tagName);
            }
        
        if (!isClickable) {
            if (tagName === "label")
                isClickable = (element.control != null) && !element.control.disabled;
            else if (tagName === "img")
                isClickable = ["zoom-in", "zoom-out"].includes(element.style.cursor);
        }

        // An element with a class name containing the text "button" might be clickable. However, real
        // clickables are often wrapped in elements with such class names. So, when we find clickables
        // based only on their class name, we mark them as unreliable.
        const className = element.getAttribute("class");
        if (!isClickable && className && className.toLowerCase().includes("button")) {
            isClickable = true;
        }
    
        // Elements with tabindex are sometimes useful, but usually not. We can treat them as second
        // class citizens when it improves UX, so take special note of them.
        const tabIndexValue = element.getAttribute("tabindex");
        const tabIndex = tabIndexValue ? parseInt(tabIndexValue) : -1;
        if (!isClickable && !(tabIndex < 0) && !isNaN(tabIndex)) {
            isClickable = true;
        }
    
        const idValue = element.getAttribute("id");
        const id = idValue ? idValue.toLowerCase() : "";
        if (isClickable && area == 0) {
            const textValue = element.textContent.trim().replace(/\s{2,}/g, ' ');
            clickable_msg = `${tagName}[id=${id}] ${isClickable} (${area}) ${textValue}`
        }
    
        return {
            element: element,
            include: isClickable,
            area,
            rects,
            text: element.textContent.trim().replace(/\s{2,}/g, ' ')
        };
    }).filter(item =>
        item.include && (item.area >= 1)
    );

    items = items.filter(x => !items.some(y => x.element.contains(y.element) && !(x == y)))

    items.forEach(item => {
        item.element.classList.add('possible-clickable-element');
    });
}