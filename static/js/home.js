document.addEventListener('DOMContentLoaded', function() {
    const generateKeysBtn = document.getElementById('generateKeysBtn');
    if (generateKeysBtn) {
        generateKeysBtn.addEventListener('click', generateKeys);
    }
});

async function generateKeys() {
    const btn = document.getElementById('generateKeysBtn');
    const loading = document.getElementById('loading');
    const result = document.getElementById('result');
    const privateKeyDisplay = document.getElementById('privateKeyDisplay');
    const publicKeyDisplay = document.getElementById('publicKeyDisplay');
    const downloadButtons = document.getElementById('downloadButtons');
    
    // Show loading state
    btn.disabled = true;
    loading.style.display = 'block';
    result.style.display = 'none';
    privateKeyDisplay.style.display = 'none';
    publicKeyDisplay.style.display = 'none';
    downloadButtons.style.display = 'none';
    
    try {
        const response = await fetch('/generate-keys', {
            method: 'POST'
        });
        
        const data = await response.json();
        
        if (response.ok) {
            // Display keys
            document.getElementById('privateKeyContent').textContent = data.private_key;
            document.getElementById('publicKeyContent').textContent = data.public_key;
            
            privateKeyDisplay.style.display = 'block';
            publicKeyDisplay.style.display = 'block';
            downloadButtons.style.display = 'flex';
            
            showResult('✅ RSA key pair generated successfully!', 'success');
        } else {
            showResult(`Error: ${data.error}`, 'error');
        }
    } catch (error) {
        showResult(`Network error: ${error.message}`, 'error');
    } finally {
        btn.disabled = false;
        loading.style.display = 'none';
    }
}

function showResult(message, type) {
    const result = document.getElementById('result');
    result.textContent = message;
    result.className = `result ${type}`;
    result.style.display = 'block';
}

function downloadKey(filename, content) {
    const blob = new Blob([content], { type: 'text/plain' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    a.remove();
    window.URL.revokeObjectURL(url);
} 