# 🔧 QUICK FIX - Question Generation Error

## The Problem
Backend is returning **422 Unprocessable Entity** - this means the request format is wrong.

## ✅ SOLUTION

The issue is likely that **question_types** values don't match what the backend expects.

### Step 1: Check What Backend Expects

The backend expects these **exact** values:
- `"mcq"` - Multiple Choice
- `"true_false"` - True/False  
- `"short_answer"` - Short Answer
- `"long_answer"` - Long Answer
- `"fill_blank"` - Fill in the Blank
- `"programming"` - Programming

### Step 2: Restart Backend with Better Errors

I've added detailed error logging. Now when you restart:

```powershell
cd c:\Users\karis\OneDrive\Desktop\A20\CascadeProjects\AutoQ
.\start_backend.bat
```

The backend terminal will show **EXACTLY** what field is wrong!

### Step 3: Try Again

1. **Refresh browser** (F5)
2. **Generate questions**
3. **Look at backend terminal** - it will show the exact error like:
   ```
   ❌ Validation Error: question_types -> 0: value is not a valid enumeration member
   ```

### Step 4: Check Browser Console

1. Press **F12**
2. Go to **Console** tab
3. Try generating questions
4. Look for the error message - it will now show the actual problem!

---

## 🎯 Most Likely Causes

### Cause 1: Document Not Selected
**Error:** `document_id: field required`
**Fix:** Select a document from dropdown before clicking Generate

### Cause 2: No Question Types Selected  
**Error:** `question_types: field required`
**Fix:** Check at least one question type checkbox

### Cause 3: Invalid Question Type Value
**Error:** `question_types -> 0: value is not a valid enumeration member`
**Fix:** The HTML checkbox values must match backend enum exactly

---

## 🔍 Debug Steps

### 1. Open Browser Console (F12)
Look for errors when you click "Generate Questions"

### 2. Check Network Tab
1. Press F12
2. Go to "Network" tab
3. Click "Generate Questions"
4. Find the `/api/v1/questions/generate` request
5. Click on it
6. Look at "Response" tab - shows exact error

### 3. Check Backend Terminal
The terminal running `start_backend.bat` will show:
```
📝 Generate request received:
   Document ID: 1
   Num questions: 10
   Question types: ['mcq', 'short_answer']
   Difficulty mix: Easy=0.3, Medium=0.5, Hard=0.2
```

If you don't see this, the request isn't reaching the backend!

---

## 🚀 Quick Test

Try this in browser console (F12 → Console):

```javascript
// Test if backend is running
fetch('http://127.0.0.1:8000/health')
  .then(r => r.json())
  .then(d => console.log('✅ Backend:', d))
  .catch(e => console.error('❌ Backend not running:', e));

// Test question generation
fetch('http://127.0.0.1:8000/api/v1/questions/generate', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    document_id: 1,
    num_questions: 5,
    question_types: ["mcq", "short_answer"],
    difficulty_easy: 0.3,
    difficulty_medium: 0.5,
    difficulty_hard: 0.2
  })
})
.then(r => r.json())
.then(d => console.log('✅ Response:', d))
.catch(e => console.error('❌ Error:', e));
```

---

## 📋 Checklist Before Generating

- [ ] Backend running (http://localhost:8000/docs loads)
- [ ] Frontend running (http://localhost:3001 loads)
- [ ] Document uploaded
- [ ] Document shows "✓ Processed" (not "⏳ Processing")
- [ ] Document selected in dropdown
- [ ] At least one question type checked
- [ ] Number of questions is between 1-100

---

## 💡 Pro Tip

The new error handler will show messages like:

**Before:** `❌ Question generation failed: [object Object]`

**After:** `❌ Question generation failed: Validation error: body -> question_types -> 0: value is not a valid enumeration member; expected 'mcq', 'true_false', 'short_answer', 'long_answer', 'fill_blank', or 'programming'`

Much better! 🎉

---

## Still Not Working?

1. **Close ALL terminals**
2. **Restart backend:**
   ```powershell
   cd c:\Users\karis\OneDrive\Desktop\A20\CascadeProjects\AutoQ
   .\start_backend.bat
   ```
3. **Restart frontend (new terminal):**
   ```powershell
   cd c:\Users\karis\OneDrive\Desktop\A20\CascadeProjects\AutoQ\simple-frontend
   python -m http.server 3001
   ```
4. **Hard refresh browser:** `Ctrl+Shift+R`
5. **Try again and check backend terminal for detailed error**
