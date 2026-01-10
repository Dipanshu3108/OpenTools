function selectTool(tool) {
    // If the tool is already selected, do nothing
    if (tool.classList.contains('selected')) return;

    const selectedSlot = document.getElementById("selectedSlot");
    const toolsContainer = document.getElementById("toolsContainer");
    const preview = document.getElementById("preview");
    const previewTitle = document.getElementById("previewTitle");
    const previewContent = document.getElementById("previewContent");

    // Remove previous selected tool and put it back in the container
    const prevTool = selectedSlot.querySelector(".tool");
    if (prevTool) {
        // Remove close button and description
        const closeBtn = prevTool.querySelector('.tool-close');
        const description = prevTool.querySelector('.tool-description');
        if (closeBtn) closeBtn.remove();
        if (description) description.remove();
        
        prevTool.classList.remove("selected");
        toolsContainer.appendChild(prevTool);
    }

    // Hide placeholder
    const placeholder = selectedSlot.querySelector(".placeholder");
    if (placeholder) {
        placeholder.style.display = "none";
    }

    // Add description and close button to the tool
    const toolName = tool.dataset.name || tool.querySelector("h3").innerText;
    const toolDesc = tool.dataset.description || "Tool description will appear here";
    
    // Create description element
    const descriptionEl = document.createElement('div');
    descriptionEl.className = 'tool-description';
    descriptionEl.textContent = toolDesc;
    tool.appendChild(descriptionEl);
    
    // Create close button
    const closeBtn = document.createElement('div');
    closeBtn.className = 'tool-close';
    closeBtn.onclick = (e) => {
        e.stopPropagation();
        closeTool();
    };
    tool.appendChild(closeBtn);

    // Move clicked tool to selected slot with smooth transition
    tool.classList.add("selected");
    selectedSlot.appendChild(tool);
    selectedSlot.classList.add("has-tool");

    // Update and show preview
    previewTitle.innerText = toolName;
    
    // Example content based on tool
    let content = "";
    if (toolName === "Video Editor") {
        content = `
            <div class="tool-settings">
                <p>Upload your video file to start editing. You can trim, crop, and add filters.</p>
                <div style="margin-top: 20px; padding: 20px; border: 2px dashed #cbd5e0; border-radius: 10px; text-align: center;">
                    <p>Drop video here or click to upload</p>
                </div>
            </div>
        `;
    } else if (toolName === "Audio Extractor") {
        content = `
            <div class="tool-settings">
                <p>Extract high-quality audio from any video format (MP4, AVI, MOV).</p>
                <ul style="margin: 15px 0; padding-left: 20px;">
                    <li>Output Format: MP3, WAV, AAC</li>
                    <li>Bitrate: 128kbps - 320kbps</li>
                </ul>
            </div>
        `;
    } else if (toolName === "Frame Grabber") {
        content = `
            <div class="tool-settings">
                <p>Extract frames from your video at specific timestamps.</p>
                <ul style="margin: 15px 0; padding-left: 20px;">
                    <li>Support for all video formats</li>
                    <li>High-quality image export</li>
                    <li>Batch frame extraction</li>
                </ul>
            </div>
        `;
    } else {
        content = `<p>Configuration options for ${toolName} will appear here. This area will contain buttons, inputs, and sliders to control the tool's functionality.</p>`;
    }
    
    previewContent.innerHTML = content;
    preview.classList.add("active");
}

function closeTool() {
    const selectedSlot = document.getElementById("selectedSlot");
    const toolsContainer = document.getElementById("toolsContainer");
    const preview = document.getElementById("preview");
    const placeholder = selectedSlot.querySelector(".placeholder");

    // Get the selected tool
    const selectedTool = selectedSlot.querySelector(".tool");
    if (!selectedTool) return;

    // Remove close button and description
    const closeBtn = selectedTool.querySelector('.tool-close');
    const description = selectedTool.querySelector('.tool-description');
    if (closeBtn) closeBtn.remove();
    if (description) description.remove();

    // Remove selected class and move back to container
    selectedTool.classList.remove("selected");
    toolsContainer.appendChild(selectedTool);
    selectedSlot.classList.remove("has-tool");

    // Show placeholder again
    if (placeholder) {
        placeholder.style.display = "block";
    }

    // Hide preview
    preview.classList.remove("active");
}
