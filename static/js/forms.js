document.addEventListener('DOMContentLoaded', function() {
    // Initialize sign form
    const signForm = document.getElementById('uploadForm');
    if (signForm) {
        signForm.addEventListener('submit', handleSignForm);
    }
    
    // Initialize verify form
    const verifyForm = document.getElementById('verifyForm');
    if (verifyForm) {
        verifyForm.addEventListener('submit', handleVerifyForm);
    }
});

async function handleSignForm(e) {
    e.preventDefault();
    
    const formData = new FormData();
    const imageFile = document.getElementById('image').files[0];
    const textFile = document.getElementById('text_file').files[0];
    
    if (!imageFile || !textFile) {
        showResult('Please select both an image and a private key file.', 'error');
        return;
    }
    
    formData.append('image', imageFile);
    formData.append('text_file', textFile);
    
    const submitBtn = document.getElementById('submitBtn');
    const loading = document.getElementById('loading');
    const result = document.getElementById('result');
    
    // Show loading state
    submitBtn.disabled = true;
    loading.style.display = 'block';
    result.style.display = 'none';
    
    try {
        const response = await fetch('/sign', {
            method: 'POST',
            body: formData
        });
        
        if (response.ok) {
            // Handle file download
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `signed_${imageFile.name}`;
            a.click();
            a.remove();
            window.URL.revokeObjectURL(url);
            
            showResult('✅ Image signed and downloaded successfully!', 'success');
        } else {
            const data = await response.json();
            showResult(`Error: ${data.error}`, 'error');
        }
    } catch (error) {
        showResult(`Network error: ${error.message}`, 'error');
    } finally {
        submitBtn.disabled = false;
        loading.style.display = 'none';
    }
}

async function handleVerifyForm(e) {
    e.preventDefault();
    
    const formData = new FormData();
    const imageFile = document.getElementById('image').files[0];
    const publicKeyFile = document.getElementById('public_key').files[0];
    
    if (!imageFile || !publicKeyFile) {
        showResult('Please select both an image and a public key file.', 'error');
        return;
    }
    
    formData.append('image', imageFile);
    formData.append('public_key', publicKeyFile);
    
    const submitBtn = document.getElementById('submitBtn');
    const loading = document.getElementById('loading');
    const result = document.getElementById('result');
    
    // Show loading state
    submitBtn.disabled = true;
    loading.style.display = 'block';
    result.style.display = 'none';
    
    try {
        const response = await fetch('/verify', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (response.ok) {
            if (data.status === 'verified') {
                showResult('✅ Signature verified!', 'success');
            } else if (data.status === 'not_found') {
                showResult('❌ Signature not found', 'warning');
            } else {
                showResult(`Status: ${data.status}`, 'success');
            }
        } else {
            showResult(`Error: ${data.error}`, 'error');
        }
    } catch (error) {
        showResult(`Network error: ${error.message}`, 'error');
    } finally {
        submitBtn.disabled = false;
        loading.style.display = 'none';
    }
}

function showResult(message, type) {
    const result = document.getElementById('result');
    result.textContent = message;
    result.className = `result ${type}`;
    result.style.display = 'block';
} 