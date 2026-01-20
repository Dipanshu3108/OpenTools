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
            <div class="audio-extractor">
                <div class="input-section">
                    <div class="input-row">
                        <div class="input-group">
                            <label for="video-file">Video File</label>
                            <div class="file-input-wrapper">
                                <input type="file" id="video-file" accept="video/*" class="file-input">
                                <label for="video-file" class="file-input-label">
                                    <svg class="upload-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                        <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                                        <polyline points="17 8 12 3 7 8"></polyline>
                                        <line x1="12" y1="3" x2="12" y2="15"></line>
                                    </svg>
                                    <span class="file-input-text">Choose a video file</span>
                                    <span class="file-input-filename"></span>
                                </label>
                            </div>
                        </div>
                    </div>
                    
                    <div class="button-group">
                        <button id="extract-audio-btn" class="extract-btn" onclick="extractAudio()">Extract Audio</button>
                        <button id="download-audio-btn" class="download-btn" onclick="downloadAudio()" style="display: none;">Download Audio</button>
                    </div>
                </div>
                
                <div id="audio-preview" class="audio-preview" style="display: none;">
                    <h4 id="audio-title" style="margin: 0 0 10px 0; font-size: 14px; color: #1a202c;">Extracted Audio</h4>
                    
                    <div class="audio-player-container">
                        <audio id="audio-player" controls style="width: 100%; margin-bottom: 10px;"></audio>
                        <div class="audio-info">
                            <span id="audio-filename" style="font-size: 12px; color: #666;"></span>
                            <span id="audio-size" style="font-size: 12px; color: #666; margin-left: 10px;"></span>
                        </div>
                    </div>
                </div>
                
                <div id="audio-loading" class="loading" style="display: none;">
                    <div class="spinner"></div>
                    <p>Extracting audio...</p>
                </div>
                
                <div id="audio-error-message" class="error-message" style="display: none;"></div>
            </div>
        `
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
    } else if (toolName === "YouTube Video Downloader") {
        content = `
            <div class="youtube-downloader">
                <div class="input-section">
                    <div class="input-row">
                        <div class="input-group">
                            <label for="youtube-url">URL</label>
                            <input type="url" id="youtube-url" placeholder="https://www.youtube.com/watch?v=..." class="url-input">
                        </div>
                        <div class="input-group">
                            <label for="start-time">Start Time*</label>
                            <input type="text" id="start-time" placeholder="HH:MM:SS" class="time-input">
                        </div>
                        <div class="input-group">
                            <label for="end-time">End Time*</label>
                            <input type="text" id="end-time" placeholder="HH:MM:SS" class="time-input">
                        </div>
                    </div>
                    
                    <div class="button-group">
                        <button id="extract-btn" class="extract-btn" onclick="extractVideoInfo()">Extract Video Info</button>
                        <button id="download-btn" class="download-btn" onclick="downloadVideo()">Download Video</button>
                    </div>
                </div>
                
                <div id="video-preview" class="video-preview" style="display: none;">
                    <h4 id="video-title" style="margin: 0 0 10px 0; font-size: 14px; color: #1a202c;">Video Title</h4>
                    
                    <div class="thumbnail-container">
                        <img id="video-thumbnail" src="" alt="Video thumbnail" class="video-thumbnail">
                        <div class="play-overlay">
                            <div class="play-icon">▶️</div>
                            <div class="play-text">Preview Only<br>(Cannot Play)</div>
                        </div>
                    </div>
                </div>
                
                <div id="loading" class="loading" style="display: none;">
                    <div class="spinner"></div>
                    <p>Processing...</p>
                </div>
                
                <div id="error-message" class="error-message" style="display: none;"></div>
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

// YouTube Video Downloader Functions
function extractVideoInfo() {
    const url = document.getElementById('youtube-url').value.trim();
    const startTime = document.getElementById('start-time').value.trim();
    const endTime = document.getElementById('end-time').value.trim();
    
    if (!url) {
        showError('Please enter a YouTube URL');
        return;
    }
    
    // Show loading
    document.getElementById('loading').style.display = 'block';
    document.getElementById('error-message').style.display = 'none';
    document.getElementById('video-preview').style.display = 'none';
    
    // Disable buttons
    document.getElementById('extract-btn').disabled = true;
    document.getElementById('download-btn').disabled = true;
    
    fetch('/api/youtube/extract', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url: url })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            throw new Error(data.error);
        }
        
        // Hide loading
        document.getElementById('loading').style.display = 'none';
        
        // Show video preview
        document.getElementById('video-preview').style.display = 'block';
        
        // Populate video info - only title and thumbnail
        document.getElementById('video-title').textContent = data.title;
        
        if (data.thumbnail) {
            document.getElementById('video-thumbnail').src = data.thumbnail;
        }
        
    })
    .catch(error => {
        document.getElementById('loading').style.display = 'none';
        showError(error.message);
    })
    .finally(() => {
        document.getElementById('extract-btn').disabled = false;
        document.getElementById('download-btn').disabled = false;
    });
}

function downloadVideo() {
    const url = document.getElementById('youtube-url').value.trim();
    const startTime = document.getElementById('start-time').value.trim();
    const endTime = document.getElementById('end-time').value.trim();
    
    if (!url) {
        showError('Please enter a YouTube URL');
        return;
    }
    
    // Show loading
    document.getElementById('loading').style.display = 'block';
    document.getElementById('error-message').style.display = 'none';
    
    // Disable buttons
    document.getElementById('extract-btn').disabled = true;
    document.getElementById('download-btn').disabled = true;
    document.getElementById('download-btn').textContent = 'Downloading...';
    
    fetch('/api/youtube/download', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
            url: url,
            start_time: startTime || null,
            end_time: endTime || null
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            throw new Error(data.error);
        }
        
        // Hide loading
        document.getElementById('loading').style.display = 'none';
        
        // Show success message
        showSuccess('Download completed! File is being saved to your Downloads folder.');
        
        // Automatically trigger file download using fetch + blob for better control
        const filename = data.filename;
        fetch(`/api/youtube/get-file/${encodeURIComponent(filename)}`)
            .then(response => {
                if (!response.ok) throw new Error('Failed to download file');
                return response.blob();
            })
            .then(blob => {
                // Create download link from blob
                const url = window.URL.createObjectURL(blob);
                const downloadLink = document.createElement('a');
                downloadLink.href = url;
                downloadLink.download = filename;
                document.body.appendChild(downloadLink);
                downloadLink.click();
                document.body.removeChild(downloadLink);
                window.URL.revokeObjectURL(url);
                
                // Now delete the file from server since download is complete
                fetch(`/api/youtube/delete-file/${encodeURIComponent(filename)}`, {
                    method: 'DELETE'
                })
                .then(res => res.json())
                .then(delData => {
                    console.log('Server file cleanup:', delData.message || delData.error);
                })
                .catch(err => {
                    console.warn('Could not delete server file:', err);
                });
            })
            .catch(err => {
                console.error('Download error:', err);
                showError('Failed to save file to your computer');
            });
        
        // Re-enable buttons
        document.getElementById('extract-btn').disabled = false;
        document.getElementById('download-btn').disabled = false;
        document.getElementById('download-btn').textContent = 'Download Video';
        
    })
    .catch(error => {
        document.getElementById('loading').style.display = 'none';
        showError(error.message);
        document.getElementById('extract-btn').disabled = false;
        document.getElementById('download-btn').disabled = false;
        document.getElementById('download-btn').textContent = 'Download Video';
    });
}

function showError(message) {
    const errorDiv = document.getElementById('error-message');
    errorDiv.textContent = message;
    errorDiv.style.display = 'block';
    errorDiv.className = 'error-message';
}

function showSuccess(message) {
    const errorDiv = document.getElementById('error-message');
    errorDiv.textContent = message;
    errorDiv.style.display = 'block';
    errorDiv.className = 'success-message';
}

// Audio Extractor Functions
function extractAudio() {
    const videoFile = document.getElementById('video-file').files[0];
    
    if (!videoFile) {
        showAudioError('Please select a video file');
        return;
    }
    
    // Show loading
    document.getElementById('audio-loading').style.display = 'block';
    document.getElementById('audio-error-message').style.display = 'none';
    document.getElementById('audio-preview').style.display = 'none';
    
    // Disable buttons
    document.getElementById('extract-audio-btn').disabled = true;
    document.getElementById('download-audio-btn').style.display = 'none';
    
    // Create FormData for file upload
    const formData = new FormData();
    formData.append('video_file', videoFile);
    
    fetch('/api/audio/extract', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            throw new Error(data.error);
        }
        
        // Hide loading
        document.getElementById('audio-loading').style.display = 'none';
        
        // Show audio preview
        document.getElementById('audio-preview').style.display = 'block';
        
        // Set audio source
        const audioPlayer = document.getElementById('audio-player');
        audioPlayer.src = `/api/audio/get-file/${encodeURIComponent(data.filename)}`;
        
        // Update info
        document.getElementById('audio-filename').textContent = data.filename;
        document.getElementById('audio-size').textContent = formatFileSize(data.size);
        
        // Show download button
        document.getElementById('download-audio-btn').style.display = 'inline-block';
        
        // Store filename for download
        document.getElementById('download-audio-btn').dataset.filename = data.filename;
        
    })
    .catch(error => {
        document.getElementById('audio-loading').style.display = 'none';
        showAudioError(error.message);
    })
    .finally(() => {
        document.getElementById('extract-audio-btn').disabled = false;
    });
}

function downloadAudio() {
    const filename = document.getElementById('download-audio-btn').dataset.filename;
    
    if (!filename) {
        showAudioError('No audio file available for download');
        return;
    }
    
    // Trigger download
    fetch(`/api/audio/get-file/${encodeURIComponent(filename)}`)
        .then(response => {
            if (!response.ok) throw new Error('Failed to download file');
            return response.blob();
        })
        .then(blob => {
            const url = window.URL.createObjectURL(blob);
            const downloadLink = document.createElement('a');
            downloadLink.href = url;
            downloadLink.download = filename;
            document.body.appendChild(downloadLink);
            downloadLink.click();
            document.body.removeChild(downloadLink);
            window.URL.revokeObjectURL(url);
            
            // Show success message
            showAudioSuccess('Audio downloaded successfully!');
            
            // Delete file from server
            fetch(`/api/audio/delete-file/${encodeURIComponent(filename)}`, {
                method: 'DELETE'
            })
            .then(res => res.json())
            .then(delData => {
                console.log('Server file cleanup:', delData.message || delData.error);
            })
            .catch(err => {
                console.warn('Could not delete server file:', err);
            });
        })
        .catch(err => {
            console.error('Download error:', err);
            showAudioError('Failed to download audio file');
        });
}

function showAudioError(message) {
    const errorDiv = document.getElementById('audio-error-message');
    errorDiv.textContent = message;
    errorDiv.style.display = 'block';
    errorDiv.className = 'error-message';
}

function showAudioSuccess(message) {
    const errorDiv = document.getElementById('audio-error-message');
    errorDiv.textContent = message;
    errorDiv.style.display = 'block';
    errorDiv.className = 'success-message';
}

function formatFileSize(bytes) {
    if (!bytes) return '0 B';
    
    const sizes = ['B', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(1024));
    return (bytes / Math.pow(1024, i)).toFixed(1) + ' ' + sizes[i];
}

function formatDuration(seconds) {
    if (!seconds) return 'Unknown';
    
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    
    if (hours > 0) {
        return `${hours}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    } else {
        return `${minutes}:${secs.toString().padStart(2, '0')}`;
    }
}

function formatNumber(num) {
    if (!num) return '0';
    
    if (num >= 1000000) {
        return (num / 1000000).toFixed(1) + 'M';
    } else if (num >= 1000) {
        return (num / 1000).toFixed(1) + 'K';
    } else {
        return num.toString();
    }
}
