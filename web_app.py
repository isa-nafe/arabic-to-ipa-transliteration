from flask import Flask, render_template_string, request, send_file, make_response
from arabic_to_ipa import ArabicToIPATransliterator
import os
import io

app = Flask(__name__)
transliterator = ArabicToIPATransliterator()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Arabic to IPA Transliterator</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        textarea { width: 100%; height: 100px; }
        button { margin-top: 10px; }
        .custom-rules { margin-top: 20px; }
        .custom-rule { margin-bottom: 10px; }
        .file-upload { margin: 20px 0; padding: 10px; border: 1px solid #ccc; }
    </style>
</head>
<body>
    <h1>Arabic to IPA Transliterator</h1>
    
    <!-- Text Input Form -->
    <form method="post">
        <label for="arabic_text">Enter Arabic text:</label><br>
        <textarea name="arabic_text" id="arabic_text">{{ arabic_text }}</textarea><br>
        <button type="submit" name="action" value="transliterate">Transliterate</button>
        
        <div class="custom-rules">
            <h2>Custom Transliteration Rules</h2>
            <div class="custom-rule">
                <input type="text" name="arabic_char" placeholder="Arabic character" maxlength="1">
                <input type="text" name="ipa_char" placeholder="IPA character(s)">
                <button type="submit" name="action" value="add_rule">Add/Modify Rule</button>
            </div>
            <div class="custom-rule">
                <input type="text" name="remove_char" placeholder="Arabic character to remove" maxlength="1">
                <button type="submit" name="action" value="remove_rule">Remove Rule</button>
            </div>
        </div>
    </form>

    <!-- File Upload Form -->
    <div class="file-upload">
        <h2>File Upload</h2>
        <form method="post" enctype="multipart/form-data">
            <input type="file" name="file" accept=".txt">
            <button type="submit" name="action" value="upload_file">Upload and Transliterate</button>
        </form>
    </div>

    {% if ipa_text %}
    <h2>IPA Result:</h2>
    <pre>{{ ipa_text }}</pre>
    <form method="post">
        <input type="hidden" name="ipa_text" value="{{ ipa_text }}">
        <button type="submit" name="action" value="download">Download IPA Result</button>
    </form>
    {% endif %}
    
    {% if message %}
    <p><strong>{{ message }}</strong></p>
    {% endif %}
    
    <h2>Current Transliteration Rules:</h2>
    <pre>{{ current_rules }}</pre>
</body>
</html>
"""

def process_file_content(file):
    """Process uploaded file content and return transliterated text."""
    if file.filename.endswith('.txt'):
        content = file.read().decode('utf-8')
        return transliterator.transliterate(content)
    return None

@app.route('/', methods=['GET', 'POST'])
def index():
    arabic_text = ""
    ipa_text = ""
    message = ""
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'transliterate':
            arabic_text = request.form['arabic_text']
            ipa_text = transliterator.transliterate(arabic_text)
        
        elif action == 'add_rule':
            arabic_char = request.form['arabic_char']
            ipa_char = request.form['ipa_char']
            if arabic_char and ipa_char:
                transliterator.add_rule(arabic_char, ipa_char)
                message = f"Rule added/modified: {arabic_char} -> {ipa_char}"
            else:
                message = "Both Arabic and IPA characters are required to add/modify a rule."
        
        elif action == 'remove_rule':
            remove_char = request.form['remove_char']
            if remove_char:
                transliterator.remove_rule(remove_char)
                message = f"Rule removed for character: {remove_char}"
            else:
                message = "An Arabic character is required to remove a rule."
        
        elif action == 'upload_file':
            if 'file' not in request.files:
                message = "No file uploaded"
            else:
                file = request.files['file']
                if file.filename == '':
                    message = "No file selected"
                else:
                    ipa_text = process_file_content(file)
                    if ipa_text is None:
                        message = "Please upload a .txt file"
                    else:
                        message = f"File '{file.filename}' processed successfully"
        
        elif action == 'download':
            ipa_text = request.form.get('ipa_text', '')
            if ipa_text:
                output = io.BytesIO()
                output.write(ipa_text.encode('utf-8'))
                output.seek(0)
                response = make_response(send_file(
                    output,
                    mimetype='text/plain',
                    as_attachment=True,
                    download_name='transliterated_text.txt'
                ))
                return response
    
    current_rules = "\n".join([f"{k}: {v}" for k, v in sorted(transliterator.arabic_to_ipa.items())])
    return render_template_string(HTML_TEMPLATE, 
                                arabic_text=arabic_text, 
                                ipa_text=ipa_text, 
                                message=message, 
                                current_rules=current_rules)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
