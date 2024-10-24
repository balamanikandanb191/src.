# myapp/views.py

from django.shortcuts import render, redirect
from .models import Document, Bookmark
from transformers import pipeline
import pdfminer.high_level as pdfminer

# Initialize the summarization pipeline
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

# Function to summarize PDF
def summarize_pdf(pdf_path):
    with open(pdf_path, 'rb') as f:
        text = pdfminer.extract_text(f)
    summary = summarizer(text, max_length=150, min_length=30, do_sample=False)
    return summary[0]['summary_text']

# View to handle PDF upload, summarization, and display summary
def index(request):
    summary = ''
    document = None
    if request.method == 'POST' and request.FILES.get('pdf'):
        pdf_file = request.FILES['pdf']
        document = Document.objects.create(title=pdf_file.name, file=pdf_file)
        summary = summarize_pdf(document.file.path)
    
    return render(request, 'index.html', {'summary': summary, 'document': document})

# View to handle bookmarking
def add_bookmark(request, document_id):
    if request.method == 'POST':
        description = request.POST['description']
        page_number = request.POST['page_number']
        document = Document.objects.get(id=document_id)
        Bookmark.objects.create(document=document, description=description, page_number=page_number)
        return redirect('index')
