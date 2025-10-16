// API Configuration  
const API_BASE_URL = 'http://127.0.0.1:8000/api/v1';

// State Management
let currentFile = null;
let documents = [];
let questions = [];
let papers = [];
let authToken = null;

console.log('🔧 AutoQ v2.0 - Question Type Bug Fixed! Cache cleared.');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
    setupNavigation();
    autoLogin();
});

// Auto Login with default user
async function autoLogin() {
    try {
        const formData = new FormData();
        formData.append('username', 'default');
        formData.append('password', 'default123');
        
        const response = await fetch(`${API_BASE_URL}/auth/login`, {
            method: 'POST',
            body: formData
        });
        
        if (response.ok) {
            const data = await response.json();
            authToken = data.access_token;
            console.log('✅ Auto-logged in');
            loadDocuments();
        } else {
            console.warn('⚠️ Auto-login failed, some features may not work');
            loadDocuments();
        }
    } catch (error) {
        console.error('Auto-login error:', error);
        loadDocuments();
    }
}

// Get auth headers
function getHeaders() {
    const headers = {};
    if (authToken) {
        headers['Authorization'] = `Bearer ${authToken}`;
    }
    return headers;
}

// Event Listeners
function setupEventListeners() {
    // File upload
    const fileInput = document.getElementById('fileInput');
    const uploadArea = document.getElementById('uploadArea');
    const uploadBtn = document.getElementById('uploadBtn');

    fileInput.addEventListener('change', handleFileSelect);
    uploadArea.addEventListener('click', () => fileInput.click());
    uploadBtn.addEventListener('click', uploadDocument);

    // Drag and drop
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.style.background = '#e0e7ff';
    });

    uploadArea.addEventListener('dragleave', () => {
        uploadArea.style.background = '';
    });

    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.style.background = '';
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            fileInput.files = files;
            handleFileSelect({ target: fileInput });
        }
    });

    // Generate questions
    document.getElementById('generateBtn').addEventListener('click', generateQuestions);

    // Download questions as PDF
    const downloadQuestionsBtn = document.getElementById('downloadQuestionsBtn');
    if (downloadQuestionsBtn) {
        downloadQuestionsBtn.addEventListener('click', downloadQuestionsAsPDF);
    }

    // Download questions as Word
    const downloadWordBtn = document.getElementById('downloadWordBtn');
    if (downloadWordBtn) {
        downloadWordBtn.addEventListener('click', downloadQuestionsAsWord);
    }

    // Create paper
    document.getElementById('createPaperBtn').addEventListener('click', createPaper);
}

// Delete Document
async function deleteDocument(documentId) {
    if (!confirm('Are you sure you want to delete this document?')) {
        return;
    }
    
    showLoading(true);
    try {
        const response = await fetch(`${API_BASE_URL}/documents/${documentId}`, {
            method: 'DELETE',
            headers: getHeaders()
        });
        
        if (!response.ok) throw new Error('Delete failed');
        
        // Remove from array
        documents = documents.filter(doc => doc.id !== documentId);
        displayDocuments();
        updateDocumentSelect();
        
        alert('✅ Document deleted successfully!');
    } catch (error) {
        console.error('Delete error:', error);
        alert('❌ Delete failed. Please try again.');
    } finally {
        showLoading(false);
    }
}

// Navigation
function setupNavigation() {
    const navLinks = document.querySelectorAll('.nav-link');
    const sections = document.querySelectorAll('.section');

    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const targetId = link.getAttribute('href').substring(1);

            // Update active link
            navLinks.forEach(l => l.classList.remove('active'));
            link.classList.add('active');

            // Show target section
            sections.forEach(section => {
                if (section.id === targetId) {
                    section.classList.remove('hidden');
                } else {
                    section.classList.add('hidden');
                }
            });
        });
    });
}

// File Handling
function handleFileSelect(event) {
    const file = event.target.files[0];
    if (!file) return;

    if (file.type !== 'application/pdf') {
        alert('Please select a PDF file');
        return;
    }

    currentFile = file;
    const fileInfo = document.getElementById('fileInfo');
    const uploadBtn = document.getElementById('uploadBtn');

    fileInfo.innerHTML = `
        <div>
            <strong>📄 ${file.name}</strong>
            <p style="color: var(--gray); font-size: 0.875rem;">
                Size: ${(file.size / 1024 / 1024).toFixed(2)} MB
            </p>
        </div>
    `;
    fileInfo.classList.remove('hidden');
    uploadBtn.classList.remove('hidden');
}

// Upload Document
async function uploadDocument() {
    if (!currentFile) return;

    showLoading(true);

    const formData = new FormData();
    formData.append('file', currentFile);

    try {
        // Upload file
        const response = await fetch(`${API_BASE_URL}/documents/upload`, {
            method: 'POST',
            headers: getHeaders(),
            body: formData
        });

        if (!response.ok) throw new Error('Upload failed');

        const data = await response.json();
        
        // Process document
        await processDocument(data.id);

        alert('✅ Document uploaded and processed successfully!');
        currentFile = null;
        document.getElementById('fileInput').value = '';
        document.getElementById('fileInfo').classList.add('hidden');
        document.getElementById('uploadBtn').classList.add('hidden');
        
        loadDocuments();
    } catch (error) {
        console.error('Upload error:', error);
        alert('❌ Upload failed. Please try again.');
    } finally {
        showLoading(false);
    }
}

// Process Document
async function processDocument(documentId) {
    try {
        const response = await fetch(`${API_BASE_URL}/documents/${documentId}/process`, {
            method: 'POST',
            headers: getHeaders()
        });

        if (!response.ok) throw new Error('Processing failed');

        return await response.json();
    } catch (error) {
        console.error('Processing error:', error);
        throw error;
    }
}

// Load Documents
async function loadDocuments() {
    try {
        const response = await fetch(`${API_BASE_URL}/documents/`, {
            headers: getHeaders()
        });
        if (!response.ok) throw new Error('Failed to load documents');

        documents = await response.json();
        displayDocuments();
        updateDocumentSelect();
    } catch (error) {
        console.error('Load documents error:', error);
        // Show empty state if no documents
        displayDocuments();
    }
}

// Display Documents
function displayDocuments() {
    const list = document.getElementById('documentsList');

    if (documents.length === 0) {
        list.innerHTML = '<p class="empty-state">No documents uploaded yet. Upload your first PDF to get started!</p>';
        return;
    }

    list.innerHTML = documents.map(doc => `
        <div class="document-item">
            <div style="flex: 1;">
                <h4>📄 ${doc.filename}</h4>
                <p style="color: var(--gray); margin: 0.5rem 0;">
                    Uploaded: ${new Date(doc.created_at).toLocaleDateString()}
                </p>
                <span class="document-status ${doc.is_processed ? 'status-processed' : 'status-processing'}">
                    ${doc.is_processed ? '✓ Processed' : '⏳ Processing'}
                </span>
            </div>
            <button class="btn btn-danger" onclick="deleteDocument(${doc.id})" style="padding: 0.5rem 1rem; margin-left: 1rem;">
                🗑️ Delete
            </button>
        </div>
    `).join('');
}

// Update Document Select
function updateDocumentSelect() {
    const select = document.getElementById('documentSelect');
    const processedDocs = documents.filter(doc => doc.is_processed);

    select.innerHTML = '<option value="">Choose a document...</option>' +
        processedDocs.map(doc => `
            <option value="${doc.id}">${doc.filename}</option>
        `).join('');
}

// Generate Questions
async function generateQuestions() {
    const documentId = document.getElementById('documentSelect').value;
    const numQuestions = document.getElementById('numQuestions').value;
    
    // Get only question type checkboxes (not difficulty)
    const questionTypes = Array.from(document.querySelectorAll('.question-type:checked'))
        .map(cb => cb.value);

    if (!documentId) {
        alert('Please select a document');
        return;
    }

    if (questionTypes.length === 0) {
        alert('Please select at least one question type');
        return;
    }
    
    console.log('📝 Sending request:', {
        document_id: parseInt(documentId),
        num_questions: parseInt(numQuestions),
        question_types: questionTypes
    });

    showLoading(true);

    try {
        const response = await fetch(`${API_BASE_URL}/questions/generate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                ...getHeaders()
            },
            body: JSON.stringify({
                document_id: parseInt(documentId),
                num_questions: parseInt(numQuestions),
                question_types: questionTypes,
                difficulty_easy: 0.3,
                difficulty_medium: 0.5,
                difficulty_hard: 0.2
            })
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            console.error('Generation failed:', errorData);
            
            // Better error message handling
            let errorMsg = 'Generation failed';
            if (errorData.detail) {
                if (typeof errorData.detail === 'string') {
                    errorMsg = errorData.detail;
                } else if (Array.isArray(errorData.detail)) {
                    errorMsg = errorData.detail.map(e => e.msg || JSON.stringify(e)).join(', ');
                }
            }
            throw new Error(errorMsg);
        }

        const data = await response.json();
        questions = data || [];
        
        if (questions.length === 0) {
            throw new Error('No questions were generated. Please try with a different document or settings.');
        }
        
        displayQuestions();
        
        // Show download buttons
        const downloadBtn = document.getElementById('downloadQuestionsBtn');
        const downloadWordBtn = document.getElementById('downloadWordBtn');
        if (downloadBtn && questions.length > 0) {
            downloadBtn.classList.remove('hidden');
        }
        if (downloadWordBtn && questions.length > 0) {
            downloadWordBtn.classList.remove('hidden');
        }
        
        alert(`✅ Generated ${questions.length} questions successfully!`);
    } catch (error) {
        console.error('Generation error:', error);
        // Show detailed error message
        const errorMsg = error.message || 'Unknown error occurred';
        alert(`❌ Question generation failed: ${errorMsg}`);
    } finally {
        showLoading(false);
    }
}

// Download Questions as PDF
async function downloadQuestionsAsPDF() {
    if (questions.length === 0) {
        alert('No questions to download!');
        return;
    }
    
    showLoading(true);
    
    try {
        // Check if answer key should be included
        const includeAnswers = document.getElementById('includeAnswers').checked;
        
        // Create a temporary paper with questions
        const response = await fetch(`${API_BASE_URL}/papers/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                ...getHeaders()
            },
            body: JSON.stringify({
                title: `Generated Questions - ${new Date().toLocaleDateString()}`,
                total_marks: questions.reduce((sum, q) => sum + (q.suggested_marks || 1), 0),
                duration_minutes: 60,
                question_ids: questions.map(q => q.id)
            })
        });

        if (!response.ok) throw new Error('Failed to create paper');

        const paper = await response.json();
        
        // Download PDF
        const exportResponse = await fetch(`${API_BASE_URL}/papers/${paper.id}/export`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                ...getHeaders()
            },
            body: JSON.stringify({
                format: 'pdf',
                include_answers: includeAnswers
            })
        });
        
        if (!exportResponse.ok) throw new Error('Download failed');

        const blob = await exportResponse.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        
        // Use document name or date for filename
        const docSelect = document.getElementById('documentSelect');
        const docName = docSelect.options[docSelect.selectedIndex]?.text || 'Questions';
        const cleanName = docName.replace(/[^a-z0-9]/gi, '_').substring(0, 50);
        a.download = `${cleanName}_Questions.pdf`;
        
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
        
        alert('✅ Questions PDF downloaded successfully!');
    } catch (error) {
        console.error('Download error:', error);
        alert('❌ Download failed. Please try again.');
    } finally {
        showLoading(false);
    }
}

// Download Questions as Word
async function downloadQuestionsAsWord() {
    if (questions.length === 0) {
        alert('No questions to download!');
        return;
    }
    
    showLoading(true);
    
    try {
        // Check if answer key should be included
        const includeAnswers = document.getElementById('includeAnswers').checked;
        
        // Create a temporary paper with questions
        const response = await fetch(`${API_BASE_URL}/papers/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                ...getHeaders()
            },
            body: JSON.stringify({
                title: `Generated Questions - ${new Date().toLocaleDateString()}`,
                total_marks: questions.reduce((sum, q) => sum + (q.suggested_marks || 1), 0),
                duration_minutes: 60,
                question_ids: questions.map(q => q.id)
            })
        });

        if (!response.ok) throw new Error('Failed to create paper');

        const paper = await response.json();
        
        // Download Word
        const exportResponse = await fetch(`${API_BASE_URL}/papers/${paper.id}/export`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                ...getHeaders()
            },
            body: JSON.stringify({
                format: 'docx',
                include_answers: includeAnswers
            })
        });
        
        if (!exportResponse.ok) throw new Error('Download failed');

        const blob = await exportResponse.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        
        // Use document name or date for filename
        const docSelect = document.getElementById('documentSelect');
        const docName = docSelect.options[docSelect.selectedIndex]?.text || 'Questions';
        const cleanName = docName.replace(/[^a-z0-9]/gi, '_').substring(0, 50);
        a.download = `${cleanName}_Questions.docx`;
        
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
        
        alert('✅ Questions Word document downloaded successfully!');
    } catch (error) {
        console.error('Download error:', error);
        alert('❌ Download failed. Please try again.');
    } finally {
        showLoading(false);
    }
}

// Display Questions
function displayQuestions() {
    const list = document.getElementById('questionsList');

    if (questions.length === 0) {
        list.innerHTML = '<p class="empty-state">No questions generated yet. Select a document and generate questions!</p>';
        return;
    }

    list.innerHTML = questions.map((q, index) => {
        const options = [];
        if (q.option_a) options.push(`A. ${q.option_a}`);
        if (q.option_b) options.push(`B. ${q.option_b}`);
        if (q.option_c) options.push(`C. ${q.option_c}`);
        if (q.option_d) options.push(`D. ${q.option_d}`);
        
        return `
            <div class="question-item">
                <h4>Question ${index + 1}</h4>
                <p class="question-text">${q.question_text}</p>
                <div class="question-meta">
                    <span class="badge badge-primary">${q.question_type}</span>
                    <span class="badge badge-${q.difficulty === 'easy' ? 'success' : q.difficulty === 'medium' ? 'warning' : 'danger'}">
                        ${q.difficulty}
                    </span>
                    <span>Marks: ${q.suggested_marks || 1}</span>
                </div>
                ${options.length > 0 ? `
                    <div style="margin-top: 1rem;">
                        ${options.map(opt => `
                            <p style="margin: 0.25rem 0; color: var(--gray);">
                                ${opt}
                            </p>
                        `).join('')}
                    </div>
                ` : ''}
            </div>
        `;
    }).join('');
}

// Create Paper
async function createPaper() {
    const title = document.getElementById('paperTitle').value;
    const institutionName = document.getElementById('institutionName').value;
    const totalMarks = document.getElementById('totalMarks').value;
    const duration = document.getElementById('duration').value;
    const instructions = document.getElementById('instructions').value;

    if (!title) {
        alert('Please enter a paper title');
        return;
    }

    if (questions.length === 0) {
        alert('Please generate questions first');
        return;
    }

    showLoading(true);

    try {
        const response = await fetch(`${API_BASE_URL}/papers/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                ...getHeaders()
            },
            body: JSON.stringify({
                title: title,
                institution_name: institutionName || null,
                total_marks: parseInt(totalMarks),
                duration_minutes: parseInt(duration),
                instructions: instructions || null,
                question_ids: questions.map(q => q.id)
            })
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            console.error('Paper creation failed:', errorData);
            throw new Error(errorData.detail || 'Paper creation failed');
        }

        const paper = await response.json();
        papers.push(paper);
        
        displayPapers();
        alert('✅ Question paper created successfully!');
        
        // Reset form
        document.getElementById('paperTitle').value = '';
    } catch (error) {
        console.error('Paper creation error:', error);
        alert(`❌ Paper creation failed: ${error.message}`);
    } finally {
        showLoading(false);
    }
}

// Display Papers
function displayPapers() {
    const list = document.getElementById('papersList');

    if (papers.length === 0) {
        list.innerHTML = '<p class="empty-state">No papers created yet. Create your first question paper!</p>';
        return;
    }

    list.innerHTML = papers.map(paper => `
        <div class="paper-item">
            <h4>📋 ${paper.title}</h4>
            <div style="color: var(--gray); margin: 0.5rem 0;">
                <p>Total Marks: ${paper.total_marks} | Duration: ${paper.duration_minutes} minutes</p>
                <p>Questions: ${paper.question_ids ? paper.question_ids.length : 0}</p>
                <p>Created: ${new Date(paper.created_at).toLocaleDateString()}</p>
            </div>
            <button class="btn btn-primary" onclick="downloadPaper(${paper.id})">
                📥 Download PDF
            </button>
        </div>
    `).join('');
}

// Download Paper
async function downloadPaper(paperId) {
    showLoading(true);
    try {
        // Find paper title from papers array
        const paper = papers.find(p => p.id === paperId);
        const paperTitle = paper?.title || 'Question_Paper';
        
        const response = await fetch(`${API_BASE_URL}/papers/${paperId}/export`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                ...getHeaders()
            },
            body: JSON.stringify({
                format: 'pdf',
                include_answers: false
            })
        });
        
        if (!response.ok) throw new Error('Download failed');

        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        
        // Use paper title for filename
        const cleanTitle = paperTitle.replace(/[^a-z0-9 ]/gi, '_').substring(0, 50);
        a.download = `${cleanTitle}.pdf`;
        
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
        
        alert('✅ PDF downloaded successfully!');
    } catch (error) {
        console.error('Download error:', error);
        alert('❌ Download failed. Please try again.');
    } finally {
        showLoading(false);
    }
}

// Loading Overlay
function showLoading(show) {
    const overlay = document.getElementById('loadingOverlay');
    if (show) {
        overlay.classList.remove('hidden');
    } else {
        overlay.classList.add('hidden');
    }
}
