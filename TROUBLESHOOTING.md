# 🔧 AutoQ Troubleshooting Guide

## Common Issues & Solutions

### ❌ Question Generation Failed

**Error:** `Question generation failed: [object Object]`

**Possible Causes & Solutions:**

#### 1. Document Not Processed
- **Check:** Is the document showing "✓ Processed" status?
- **Solution:** Wait for document processing to complete before generating questions
- **Time:** Processing usually takes 10-30 seconds

#### 2. Document Too Short
- **Error:** "Text is too short to generate questions"
- **Solution:** Upload a PDF with at least 2-3 pages of text content
- **Minimum:** 100 characters required

#### 3. Scanned PDF (Images)
- **Problem:** PDF contains scanned images, not text
- **Solution:** Use text-based PDFs or OCR-processed documents
- **Test:** Try to copy text from the PDF - if you can't, it's an image

#### 4. No Suitable Content
- **Error:** "Could not extract enough content from text"
- **Solution:** Document needs clear sentences, definitions, or facts
- **Best:** Educational content, textbooks, lecture notes work best

#### 5. Backend Not Running
- **Check:** Is backend running on port 8000?
- **Test:** Open http://localhost:8000/docs in browser
- **Solution:** Run `.\start_backend.bat` in AutoQ folder

---

## Quick Fixes

### 🔄 Restart Backend
```powershell
# Stop backend (Ctrl+C in terminal)
# Then restart:
cd c:\Users\karis\OneDrive\Desktop\A20\CascadeProjects\AutoQ
.\start_backend.bat
```

### 🔄 Restart Frontend
```powershell
# Stop frontend (Ctrl+C in terminal)
# Then restart:
cd c:\Users\karis\OneDrive\Desktop\A20\CascadeProjects\AutoQ\simple-frontend
python -m http.server 3001
```

### 🗑️ Clear Browser Cache
1. Press `Ctrl+Shift+Delete`
2. Clear cached files
3. Refresh page (`F5`)

---

## Step-by-Step Debugging

### Test 1: Check Backend
```powershell
# Open in browser:
http://localhost:8000/docs
```
✅ Should show API documentation
❌ If not loading → Backend not running

### Test 2: Check Document Status
1. Go to "Upload" tab
2. Look at uploaded documents
3. Status should be "✓ Processed"
❌ If "⏳ Processing" → Wait longer
❌ If stuck → Re-upload document

### Test 3: Check Browser Console
1. Press `F12` to open Developer Tools
2. Go to "Console" tab
3. Look for error messages
4. Share error details for help

### Test 4: Try Sample Document
1. Create a simple text file with 3-4 paragraphs
2. Save as PDF
3. Upload and test
✅ If works → Original PDF has issues
❌ If fails → System issue

---

## Error Messages Explained

### "Document not found"
- **Cause:** Document ID doesn't exist
- **Fix:** Refresh page and try again

### "Document not yet processed"
- **Cause:** Processing still in progress
- **Fix:** Wait 30 seconds and try again

### "No text available for question generation"
- **Cause:** Document has no extractable text
- **Fix:** Use a different PDF with actual text

### "Failed to analyze text"
- **Cause:** NLP engine error
- **Fix:** Check if spaCy model is installed:
```powershell
cd backend
venv\Scripts\activate
python -m spacy download en_core_web_sm
```

---

## Best Practices

### ✅ DO:
- Use text-based PDFs (not scanned images)
- Upload documents with 5+ pages
- Wait for processing to complete
- Use educational/technical content
- Check document status before generating

### ❌ DON'T:
- Upload image-only PDFs
- Generate questions immediately after upload
- Use very short documents (< 2 pages)
- Upload corrupted/password-protected PDFs
- Generate 50+ questions at once (start with 10)

---

## Performance Tips

### Fast Question Generation:
- **10 questions:** 5-10 seconds
- **20 questions:** 10-15 seconds
- **30 questions:** 15-20 seconds

### If Slow:
1. Reduce number of questions
2. Select fewer question types
3. Check system resources (RAM/CPU)
4. Close other applications

---

## Getting Help

### Check Logs:
1. **Backend logs:** Look at terminal running backend
2. **Browser console:** Press F12 → Console tab
3. **Network tab:** F12 → Network → Look for failed requests

### Report Issue:
Include:
1. Error message (exact text)
2. Browser console errors
3. Backend terminal output
4. Steps to reproduce
5. PDF type/size

---

## System Requirements

### Minimum:
- Python 3.9+
- 4GB RAM
- 10GB storage
- Modern browser (Chrome/Edge/Firefox)

### Recommended:
- Python 3.11+
- 8GB RAM
- 50GB storage
- Chrome browser

---

## Quick Test Checklist

- [ ] Backend running (http://localhost:8000/docs loads)
- [ ] Frontend running (http://localhost:3001 loads)
- [ ] Document uploaded successfully
- [ ] Document shows "✓ Processed" status
- [ ] Document selected in dropdown
- [ ] At least one question type checked
- [ ] Number of questions set (10 is good start)
- [ ] Browser console shows no errors

---

**Still having issues?** Check the backend terminal for detailed error messages!
