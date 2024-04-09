(items) => {
    function getRandomColor() {
        var letters = '0123456789ABCDEF';
        var color = '#';
        for (var i = 0; i < 6; i++) {
            color += letters[Math.floor(Math.random() * 16)];
        }
        return color;
    }

    items.filter(
        item => item.id != ""
    ).forEach((item) => {
        const bbox = item.rects;
        const id_string = `dom-marker-id-${index}`;
        
        index = item.id;

        outerElement = document.createElement("div");
        outerElement.classList.add("our-dom-marker");
        // var borderColor = getRandomColor();
        var borderColor = "#FFFF00";
        outerElement.style.outline = `2px dashed ${borderColor}`; 
        outerElement.style.position = "fixed";
        outerElement.style.left = bbox.left - 2 + "px";
        outerElement.style.top = bbox.top - 2 + "px";
        outerElement.style.width = bbox.width + 4 + "px";
        outerElement.style.height = bbox.height + 4 + "px";
        outerElement.style.pointerEvents = "none";
        outerElement.style.boxSizing = "border-box";
        outerElement.style.zIndex = 2147483647;

        innerElement = document.createElement("div");
        innerElement.classList.add("our-dom-marker");
        innerElement.style.outline = `2px dashed #222288`;
        innerElement.style.position = "fixed";
        innerElement.style.left = bbox.left + "px";
        innerElement.style.top = bbox.top + "px";
        innerElement.style.width = bbox.width + "px";
        innerElement.style.height = bbox.height + "px";
        innerElement.style.pointerEvents = "none";
        innerElement.style.boxSizing = "border-box";
        innerElement.style.zIndex = 2147483647;
    
        // Add floating label at the corner
        var label = document.createElement("span");
        var topPosition = 25;
        if (bbox.top < 25) topPosition = bbox.top;
        label.textContent = index;
        label.style.position = "absolute";
        label.style.top = `-${topPosition}px`;
        label.style.left = "0px";
        label.style.background = borderColor;
        label.style.color = "black";
        label.style.padding = "2px 4px";
        label.style.fontSize = "16px";
        label.style.borderRadius = "2px";
        label.style.fontWeight = "bold";
        outerElement.appendChild(label);
    
        document.body.appendChild(outerElement);
        document.body.appendChild(innerElement);
    })
    return items;
}