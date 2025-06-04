/**
 * yt-dlp JSON Extractor Frontend Application
 */
class YtDlpExtractor {
    constructor() {
        this.apiBaseUrl = '/api';
        this.currentMetadata = null;
        
        // DOM elements
        this.form = document.getElementById('extractForm');
        this.urlInput = document.getElementById('videoUrl');
        this.loadingIndicator = document.getElementById('loadingIndicator');
        this.errorContainer = document.getElementById('errorContainer');
        this.errorText = document.getElementById('errorText');
        this.resultContainer = document.getElementById('resultContainer');
        this.jsonOutput = document.getElementById('jsonOutput');
        this.metadataPreview = document.getElementById('metadataPreview');
        this.downloadBtn = document.getElementById('downloadBtn');
        this.btnText = document.querySelector('.btn-text');
        this.btnLoading = document.querySelector('.btn-loading');
        
        this.init();
    }
    
    init() {
        this.form.addEventListener('submit', this.handleSubmit.bind(this));
        this.downloadBtn.addEventListener('click', this.downloadJson.bind(this));
        
        // Auto-focus URL input
        this.urlInput.focus();
    }
    
    async handleSubmit(event) {
        event.preventDefault();
        
        const url = this.urlInput.value.trim();
        if (!url) {
            this.showError('Please enter a video URL');
            return;
        }
        
        await this.extractMetadata(url);
    }
    
    async extractMetadata(url) {
        this.showLoading(true);
        this.hideError();
        this.hideResult();
        
        try {
            const response = await fetch(`${this.apiBaseUrl}/extract`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ url: url })
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.currentMetadata = data.data;
                this.showResult(data.data);
            } else {
                this.showError(data.error || 'Failed to extract metadata');
            }
            
        } catch (error) {
            console.error('Network error:', error);
            this.showError('Network error: Unable to connect to server');
        } finally {
            this.showLoading(false);
        }
    }
    
    showResult(metadata) {
        // Create metadata preview
        this.createMetadataPreview(metadata);
        
        // Show full JSON
        this.jsonOutput.textContent = JSON.stringify(metadata, null, 2);
        
        // Show result container
        this.resultContainer.style.display = 'block';
        this.resultContainer.scrollIntoView({ behavior: 'smooth' });
    }
    
    createMetadataPreview(metadata) {
        const preview = document.createElement('div');
        preview.className = 'preview-grid';
        
        const fields = [
            { key: 'title', label: 'Title', icon: '📹' },
            { key: 'uploader', label: 'Channel', icon: '👤' },
            { key: 'duration', label: 'Duration', icon: '⏱️', format: this.formatDuration },
            { key: 'view_count', label: 'Views', icon: '👁️', format: this.formatNumber },
            { key: 'upload_date', label: 'Upload Date', icon: '📅', format: this.formatDate },
            { key: 'like_count', label: 'Likes', icon: '👍', format: this.formatNumber }
        ];
        
        fields.forEach(field => {
            if (metadata[field.key] !== undefined) {
                const value = field.format ? 
                    field.format(metadata[field.key]) : 
                    metadata[field.key];
                
                preview.innerHTML += `
                    <div class="preview-item">
                        <span class="preview-icon">${field.icon}</span>
                        <div class="preview-content">
                            <strong>${field.label}:</strong>
                            <span>${value}</span>
                        </div>
                    </div>
                `;
            }
        });
        
        this.metadataPreview.innerHTML = '';
        this.metadataPreview.appendChild(preview);
    }
    
    formatDuration(seconds) {
        if (!seconds) return 'Unknown';
        const hours = Math.floor(seconds / 3600);
        const minutes = Math.floor((seconds % 3600) / 60);
        const secs = seconds % 60;
        
        if (hours > 0) {
            return `${hours}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
        }
        return `${minutes}:${secs.toString().padStart(2, '0')}`;
    }
    
    formatNumber(num) {
        if (!num) return 'Unknown';
        return new Intl.NumberFormat().format(num);
    }
    
    formatDate(dateStr) {
        if (!dateStr) return 'Unknown';
        try {
            const year = dateStr.substring(0, 4);
            const month = dateStr.substring(4, 6);
            const day = dateStr.substring(6, 8);
            return new Date(`${year}-${month}-${day}`).toLocaleDateString();
        } catch {
            return dateStr;
        }
    }
    
    downloadJson() {
        if (!this.currentMetadata) return;
        
        const dataStr = JSON.stringify(this.currentMetadata, null, 2);
        const dataBlob = new Blob([dataStr], { type: 'application/json' });
        const url = URL.createObjectURL(dataBlob);
        
        const link = document.createElement('a');
        link.href = url;
        link.download = `${this.currentMetadata.id || 'video'}_metadata.json`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
    }
    
    showLoading(show) {
        this.loadingIndicator.style.display = show ? 'block' : 'none';
        this.btnText.style.display = show ? 'none' : 'inline';
        this.btnLoading.style.display = show ? 'inline' : 'none';
        this.form.querySelector('button').disabled = show;
    }
    
    showError(message) {
        this.errorText.textContent = message;
        this.errorContainer.style.display = 'block';
        this.errorContainer.scrollIntoView({ behavior: 'smooth' });
    }
    
    hideError() {
        this.errorContainer.style.display = 'none';
    }
    
    hideResult() {
        this.resultContainer.style.display = 'none';
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new YtDlpExtractor();
});
