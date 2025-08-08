document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.getElementById('resume');
    const buttons = [
        document.getElementById('uploadBtn'),
        document.getElementById('analyzeBtn'),
        document.getElementById('findJobsBtn')
    ];
    if (fileInput) {
        fileInput.addEventListener('change', function() {
            const enabled = fileInput.files.length > 0;
            uploadBtn.disabled = !enabled;
            buttons.forEach(btn => btn.disabled = !enabled);
        });
    }
    // Modal logic
    const uploadBtn = document.getElementById('uploadBtn');
    const modal = document.getElementById('credentialsModal');
    const closeModalBtn = document.getElementById('closeModalBtn');
    const credentialsForm = document.getElementById('credentialsForm');

    if (uploadBtn) {
        uploadBtn.addEventListener('click', function(e) {
            modal.style.display = 'flex';
        });
    }
    if (closeModalBtn) {
        closeModalBtn.addEventListener('click', function() {
            modal.style.display = 'none';
        });
    }
    let extractedText = '';
    if (credentialsForm) {
        credentialsForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            modal.style.display = 'none';
            // Extract text from PDF
            const file = fileInput.files[0];
            const formData = new FormData();
            formData.append('resume', file);
            try {
                const response = await fetch('/extract_text', {
                    method: 'POST',
                    body: formData
                });
                const data = await response.json();
                if (data.text) {
                    extractedText = data.text;
                    const statusDiv = document.getElementById('statusMessage');
                    statusDiv.textContent = 'Text has been successfully extracted.';
                    statusDiv.style.display = 'block';
                }
            } catch (err) {
                const statusDiv = document.getElementById('statusMessage');
                statusDiv.textContent = 'Failed to extract text.';
                statusDiv.style.display = 'block';
            }
            // Send credentials and extractedText to backend
            const name = document.getElementById('name').value;
            const email = document.getElementById('email').value;
            if (extractedText && name && email) {
                try {
                    const saveResponse = await fetch('/save_resume', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            name: name,
                            email: email,
                            content: extractedText
                        })
                    });
                    const saveData = await saveResponse.json();
                    if (saveData.message) {
                        const statusDiv = document.getElementById('statusMessage');
                        statusDiv.textContent = 'Resume and credentials saved successfully.';
                        statusDiv.style.display = 'block';
                    } else if (saveData.error) {
                        const statusDiv = document.getElementById('statusMessage');
                        statusDiv.textContent = 'Error saving to database: ' + saveData.error;
                        statusDiv.style.display = 'block';
                    }
                } catch (err) {
                    const statusDiv = document.getElementById('statusMessage');
                    statusDiv.textContent = 'Failed to save resume and credentials.';
                    statusDiv.style.display = 'block';
                }
            }
        });
    }

    // Handle Analyze button click
    const analyzeBtn = document.getElementById('analyzeBtn');
    const analysisModal = document.getElementById('analysisModal');
    const closeAnalysisBtn = document.getElementById('closeAnalysisBtn');
    const analysisResults = document.getElementById('analysisResults');

    if (analyzeBtn) {
        analyzeBtn.addEventListener('click', async function(e) {
            e.preventDefault();
            if (!extractedText) {
                alert('Please upload and extract your resume first.');
                return;
            }
            analysisResults.innerHTML = '<p>Analyzing resume, please wait...</p>';
            analysisModal.style.display = 'flex';
            try {
                const response = await fetch('/resume_agent', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ content: extractedText })
                });
                const data = await response.json();
                let html = '';
                html += `<strong>Summary:</strong> <span>${data.summary}</span><br><br>`;
                html += `<strong>Matching Roles:</strong><ul>`;
                data.roles.forEach(role => { html += `<li>${role}</li>`; });
                html += `</ul><br>`;
                html += `<strong>Career Insight:</strong> <span>${data.career_insight}</span><br><br>`;
                html += `<strong>Keywords to Include:</strong><ul>`;
                data.keywords.forEach(kw => { html += `<li>${kw}</li>`; });
                html += `</ul>`;
                analysisResults.innerHTML = html;
            } catch (err) {
                analysisResults.innerHTML = '<p>Failed to analyze resume.</p>';
            }
        });
    }
    if (closeAnalysisBtn) {
        closeAnalysisBtn.addEventListener('click', function() {
            analysisModal.style.display = 'none';
        });
    }
});
