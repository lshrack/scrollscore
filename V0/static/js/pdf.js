function renderPDF(url, canvasContainer, options) {
    options = options || { scale: 1 };
        
    function renderPage(page) {
        var viewport = page.getViewport({ scale: 1.5 });
        //var wrapper = document.createElement("div");
        var wrapper = document.getElementById("wrapper" + page.pageNumber.toString());
        wrapper.className = "canvas-wrapper";
        var canvas = document.createElement('canvas');
        var ctx = canvas.getContext('2d');
        var renderContext = {
        canvasContext: ctx,
        viewport: viewport
        };
        
        canvas.height = viewport.height;
        canvas.width = viewport.width;
        wrapper.appendChild(canvas)
        console.log("HI")
        canvasContainer.appendChild(wrapper);
        
        page.render(renderContext);
    }

    function renderPages(pdfDoc) {
        for(var num = 1; num <= pdfDoc.numPages; num++)
            pdfDoc.getPage(num).then(page => renderPage(page));
    }

    pdfjsLib.disableWorker = true;
    pdfjsLib.getDocument(url).promise.then(renderPages);
}   

console.log("hi, I'm in pdf.js")
