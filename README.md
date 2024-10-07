# PDF Query Program

This project is a web-based application that allows users to upload PDF files and ask queries. The program responds with relevant answers extracted from the uploaded PDFs using a natural language processing model.

## Features

- **Upload PDFs:** Users can upload PDF files to the application.
- **Ask Queries:** Users can ask questions related to the contents of the uploaded PDF.
- **Intelligent Responses:** The system will provide relevant answers based on the PDF content using a Hugging Face NLP model.
- **Web Interface:** The program includes an `index.html` file that serves as a simple, user-friendly webpage for interacting with the application.

## Technologies Used

- **Python:** Backend is written in Python, which handles PDF parsing and querying.
- **Hugging Face Models:** Used for natural language processing and answering queries from the PDF content.
- **HTML/CSS:** The web interface is designed using `index.html`.
- **AWS EC2:** The application is deployed on an AWS EC2 instance, with the API running on port 8000.

## Setup Instructions

### Requirements

- Python 3.x
- pip (Python package manager)
- Hugging Face library (`transformers`)
- Flask or FastAPI (for the web framework)
- PyPDF2 (for PDF parsing)
- Basic HTML/CSS knowledge

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/acktron/pdf_query.git
   cd pdf_query
2. Install the required Python packages:
   pip install -r requirements.txt
3. Run the application:
   python pdf_search_api.py
   This will start the web server on localhost:8000.
