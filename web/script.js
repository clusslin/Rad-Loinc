document.addEventListener('DOMContentLoaded', () => {
    // Tab Switching
    const tabs = document.querySelectorAll('.tab-btn');
    const contents = document.querySelectorAll('.tab-content');

    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            tabs.forEach(t => t.classList.remove('active'));
            contents.forEach(c => c.classList.remove('active'));

            tab.classList.add('active');
            const target = tab.getAttribute('data-tab');
            document.getElementById(`${target}-tab`).classList.add('active');
        });
    });

    // Single Form Submission
    const singleForm = document.getElementById('single-form');
    const resultArea = document.getElementById('result-area');

    singleForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const loader = singleForm.querySelector('.btn-loader');
        const btnText = singleForm.querySelector('.btn-text');
        const btn = singleForm.querySelector('button');

        // Show loading state
        btn.disabled = true;
        btnText.textContent = 'Processing...';

        try {
            const formData = new FormData(singleForm);
            const data = Object.fromEntries(formData.entries());

            const response = await fetch('/api/map', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            });

            const result = await response.json();

            displayResult(result);
            resultArea.classList.remove('hidden');

        } catch (error) {
            alert('Error processing request: ' + error.message);
        } finally {
            btn.disabled = false;
            btnText.textContent = '開始轉換';
        }
    });

    function displayResult(result) {
        // LOINC
        const loincCode = document.getElementById('loinc-code');
        const loincName = document.getElementById('loinc-name');
        const loincConf = document.getElementById('loinc-confidence');

        loincCode.textContent = result.loinc_code || 'Not Found';
        loincName.textContent = result.loinc_long_name || 'No matching LOINC code found';
        loincConf.textContent = result.mapping_confidence || 'None';
        loincConf.className = `badge ${result.mapping_confidence ? result.mapping_confidence.toLowerCase() : 'none'}`;

        // ICD
        const icdCode = document.getElementById('icd-code');
        const icdDesc = document.getElementById('icd-desc');
        const icdConf = document.getElementById('icd-confidence');

        icdCode.textContent = result.icd10pcs_code || 'Not Found';
        icdDesc.textContent = result.icd10pcs_description || 'No matching ICD code found';
        icdConf.textContent = result.icd10pcs_mapping_confidence || 'None'; // Note: check backend key
        icdConf.className = `badge ${result.mapping_confidence ? result.mapping_confidence.toLowerCase() : 'none'}`; // Reuse confidence or specific one if available

        // Issues
        const issuesContainer = document.getElementById('issues-container');
        const issuesList = document.getElementById('issues-list');
        issuesList.innerHTML = '';

        if (result.has_issues && result.issues.length > 0) {
            result.issues.forEach(issue => {
                const li = document.createElement('li');
                li.textContent = issue;
                issuesList.appendChild(li);
            });
            issuesContainer.classList.remove('hidden');
        } else {
            issuesContainer.classList.add('hidden');
        }
    }

    // Search Logic
    const searchForm = document.getElementById('search-form');
    const searchResultsArea = document.getElementById('search-results-area');
    const loincResultsList = document.getElementById('loinc-results-list');
    const icdResultsList = document.getElementById('icd-results-list');

    if (searchForm) {
        searchForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            const btn = searchForm.querySelector('button');
            const btnText = btn.querySelector('.btn-text');
            const data = {
                query: document.getElementById('search-query').value,
                strategy: document.getElementById('search-strategy').value,
                code_type: searchForm.querySelector('input[name="code_type"]:checked').value
            };

            btn.disabled = true;
            btnText.textContent = 'Searching...';

            try {
                const response = await fetch('/api/search', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });

                if (!response.ok) throw new Error('Search failed');

                const results = await response.json();
                displaySearchResults(results);
                searchResultsArea.classList.remove('hidden');

            } catch (err) {
                alert(err.message);
            } finally {
                btn.disabled = false;
                btnText.textContent = '搜尋';
            }
        });
    }

    function displaySearchResults(results) {
        loincResultsList.innerHTML = '';
        icdResultsList.innerHTML = '';

        // Render LOINC
        if (results.loinc.length === 0) {
            loincResultsList.innerHTML = '<p>No results found.</p>';
        } else {
            results.loinc.forEach(item => {
                const div = document.createElement('div');
                div.className = 'result-item';
                div.innerHTML = `
                    <div class="result-item-header">
                        <span class="result-code">${item.LOINC_NUM || item.code || 'N/A'}</span>
                        <span class="result-score">${item.score.toFixed(2)} (${item.strategy})</span>
                    </div>
                    <div class="result-body">
                        <p><strong>${item.LONG_COMMON_NAME || item.long_name}</strong></p>
                        <div class="result-details">
                            <span class="tag">${item.COMPONENT || item.component}</span>
                            <span class="tag">${item.METHOD_TYP || item.method}</span>
                        </div>
                    </div>
                `;
                loincResultsList.appendChild(div);
            });
        }

        // Render ICD
        if (results.icd.length === 0) {
            icdResultsList.innerHTML = '<p>No results found.</p>';
        } else {
            results.icd.forEach(item => {
                const div = document.createElement('div');
                div.className = 'result-item';
                div.innerHTML = `
                    <div class="result-item-header">
                        <span class="result-code">${item.ICD10PCS_CODE || item.code || 'N/A'}</span>
                        <span class="result-score">${item.score.toFixed(2)} (${item.strategy})</span>
                    </div>
                    <div class="result-body">
                        <p><strong>${item.DESCRIPTION || item.description}</strong></p>
                        <div class="result-details">
                            <span class="tag">Section: ${item.SECTION || item.section}</span>
                            <span class="tag">Body Part: ${item.BODY_PART || item.body_part}</span>
                        </div>
                    </div>
                `;
                icdResultsList.appendChild(div);
            });
        }
    }

    // AI Assistant Logic
    const btnLoadLLM = document.getElementById('btn-load-llm');
    const badgeLLMStatus = document.getElementById('llm-status-badge');
    const chatInput = document.getElementById('chat-input');
    const btnSendChat = document.getElementById('btn-send-chat');
    const chatContainer = document.getElementById('chat-container');

    let isLLMLoaded = false;

    // Check status on load and tab switch
    async function checkLLMStatus() {
        try {
            const res = await fetch('/api/llm/status');
            const data = await res.json();
            isLLMLoaded = data.status === 'loaded';
            updateLLMUI(isLLMLoaded, data.model);
        } catch (e) {
            console.error('Failed to check LLM status', e);
        }
    }

    function updateLLMUI(loaded, modelName) {
        if (loaded) {
            badgeLLMStatus.className = 'badge high';
            badgeLLMStatus.textContent = 'Loaded: ' + (modelName || 'LLM');
            btnLoadLLM.textContent = 'Unload Model';
            btnLoadLLM.classList.add('danger'); // Add a danger class style if needed
            chatInput.disabled = false;
            btnSendChat.disabled = false;
        } else {
            badgeLLMStatus.className = 'badge none';
            badgeLLMStatus.textContent = 'Unloaded';
            btnLoadLLM.textContent = 'Load Model';
            btnLoadLLM.classList.remove('danger');
            chatInput.disabled = true;
            btnSendChat.disabled = true;
        }
    }

    if (btnLoadLLM) {
        btnLoadLLM.addEventListener('click', async () => {
            btnLoadLLM.disabled = true;
            const originalText = btnLoadLLM.textContent;
            btnLoadLLM.textContent = 'Processing...';

            try {
                if (!isLLMLoaded) {
                    // Load
                    const res = await fetch('/api/llm/load', { method: 'POST' });
                    if (!res.ok) throw new Error((await res.json()).detail);
                    await checkLLMStatus();
                } else {
                    // Unload
                    const res = await fetch('/api/llm/unload', { method: 'POST' });
                    if (!res.ok) throw new Error((await res.json()).detail);
                    await checkLLMStatus();
                }
            } catch (e) {
                alert('Operation failed: ' + e.message);
                updateLLMUI(isLLMLoaded); // Revert
            } finally {
                btnLoadLLM.disabled = false;
            }
        });
    }

    if (btnSendChat) {
        btnSendChat.addEventListener('click', sendMessage);
    }

    // Auto resize textarea
    if (chatInput) {
        chatInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendMessage();
            }
        });
    }

    async function sendMessage() {
        const text = chatInput.value.trim();
        if (!text) return;

        // Add User Message
        appendMessage('user', text);
        chatInput.value = '';
        btnSendChat.disabled = true;

        // Show typing indicator?
        const loadingId = appendMessage('assistant', 'Thinking...');

        try {
            const res = await fetch('/api/llm/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ prompt: text })
            });

            if (!res.ok) throw new Error((await res.json()).detail);

            const data = await res.json();

            // Update assistant message
            const loadingMsg = document.getElementById(loadingId);
            if (loadingMsg) {
                loadingMsg.querySelector('.message-content').innerHTML = formatAIResponse(data.response);
            }

        } catch (e) {
            appendMessage('system', 'Error: ' + e.message);
        } finally {
            btnSendChat.disabled = false;
        }
    }

    function appendMessage(role, text) {
        const div = document.createElement('div');
        div.className = `chat-message ${role}`;
        const id = 'msg-' + Date.now();
        div.id = id;

        const content = document.createElement('div');
        content.className = 'message-content';

        if (role === 'assistant' && text !== 'Thinking...') {
            content.innerHTML = formatAIResponse(text);
        } else {
            content.textContent = text;
        }

        div.appendChild(content);
        chatContainer.appendChild(div);
        chatContainer.scrollTop = chatContainer.scrollHeight;
        return id;
    }

    function formatAIResponse(text) {
        // Basic markdown formatting
        // Convert **bold** to <b>
        let html = text
            .replace(/\*\*(.*?)\*\*/g, '<b>$1</b>')
            .replace(/\n/g, '<br>');
        return html;
    }

    // Check status on init
    checkLLMStatus();

    // Also check when tab becomes active
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            if (tab.getAttribute('data-tab') === 'ai') {
                checkLLMStatus();
            }
        });
    });

    // File Upload Handling
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const fileInfo = document.getElementById('file-info');
    const fileName = document.querySelector('.file-name');
    const processBtn = document.getElementById('process-btn');
    const removeFileBtn = document.querySelector('.remove-file');
    let currentFile = null;

    dropZone.addEventListener('click', () => fileInput.click());

    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.style.borderColor = 'var(--accent)';
        dropZone.style.backgroundColor = '#f0f9ff';
    });

    dropZone.addEventListener('dragleave', (e) => {
        e.preventDefault();
        dropZone.style.borderColor = 'var(--border)';
        dropZone.style.backgroundColor = 'transparent';
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.style.borderColor = 'var(--border)';
        dropZone.style.backgroundColor = 'transparent';

        if (e.dataTransfer.files.length) {
            handleFile(e.dataTransfer.files[0]);
        }
    });

    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length) {
            handleFile(e.target.files[0]);
        }
    });

    function handleFile(file) {
        if (!file.name.match(/\.(xlsx|csv|xls)$/)) {
            alert('Please select an Excel or CSV file.');
            return;
        }
        currentFile = file;
        fileName.textContent = file.name;
        dropZone.classList.add('hidden');
        fileInfo.classList.remove('hidden');
        processBtn.disabled = false;
        document.getElementById('download-section').classList.add('hidden');
    }

    removeFileBtn.addEventListener('click', () => {
        currentFile = null;
        fileInput.value = '';
        dropZone.classList.remove('hidden');
        fileInfo.classList.add('hidden');
        processBtn.disabled = true;
    });

    processBtn.addEventListener('click', async () => {
        if (!currentFile) return;

        const btnText = processBtn.querySelector('.btn-text');

        processBtn.disabled = true;
        btnText.textContent = 'Processing... (This may take a moment)';

        const formData = new FormData();
        formData.append('file', currentFile);

        try {
            const response = await fetch('/api/process_file', {
                method: 'POST',
                body: formData,
            });

            if (response.ok) {
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const downloadLink = document.getElementById('download-link');
                const downloadSection = document.getElementById('download-section');

                downloadLink.href = url;
                downloadLink.download = 'mapped_results_' + currentFile.name;
                downloadSection.classList.remove('hidden');

            } else {
                const err = await response.json();
                alert('Error: ' + (err.detail || 'Unknown error'));
            }
        } catch (error) {
            alert('Error uploading file: ' + error.message);
        } finally {
            processBtn.disabled = false;
            btnText.textContent = '開始批次轉換';
        }
    });
});
