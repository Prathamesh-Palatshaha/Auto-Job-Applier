# Resume Parser with Gemini API

A powerful resume parser that extracts text from PDF resumes and uses Google's Gemini API to structure the data into a clean JSON format.

## Features

- 📄 **PDF Text Extraction**: Extracts text from PDF resume files using PyPDF2
- 🤖 **AI-Powered Parsing**: Uses Google Gemini API to intelligently parse and structure resume data
- 🌐 **REST API**: Flask-based API server for easy integration
- 📊 **Comprehensive Data Extraction**: Extracts name, contact info, skills, experience, projects, education, and more
- 🔧 **Flexible**: Can be used as a Python library or REST API

## JSON Output Format

The parser extracts the following information:

```json
{
  "name": "Full name",
  "email": "Email address",
  "phone": "Phone number",
  "location": "City, State/Country",
  "linkedin": "LinkedIn URL",
  "github": "GitHub URL",
  "summary": "Professional summary",
  "skills": ["Python", "Machine Learning", "..."],
  "experience": [
    {
      "company": "Company name",
      "position": "Job title",
      "duration": "Jan 2020 - Present",
      "description": "Key responsibilities..."
    }
  ],
  "projects": [
    {
      "name": "Project name",
      "description": "Description",
      "technologies": ["Python", "Flask"],
      "link": "https://github.com/..."
    }
  ],
  "education": [
    {
      "institution": "University name",
      "degree": "Bachelor of Science in Computer Science",
      "duration": "2016 - 2020",
      "gpa": "3.8/4.0"
    }
  ],
  "certifications": ["AWS Certified", "..."],
  "experience_years": "5",
  "domain": "Software Development"
}
```

## Installation

### Prerequisites

- Python 3.8 or higher
- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))

### Setup

1. **Clone or download the project**

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Set up your Gemini API key** (optional for API server):
```bash
export GEMINI_API_KEY="your-api-key-here"
```

## Usage

### Option 1: Command Line Interface

Parse a resume directly from the command line:

```bash
python resume_parser.py <pdf_path> <gemini_api_key> [output_json_path]
```

**Example**:
```bash
python resume_parser.py john_doe_resume.pdf YOUR_GEMINI_API_KEY parsed_resume.json
```

### Option 2: Python Library

Use the parser in your Python code:

```python
from resume_parser import ResumeParser

# Initialize parser
parser = ResumeParser(gemini_api_key="YOUR_GEMINI_API_KEY")

# Parse resume
result = parser.parse_resume("resume.pdf", "output.json")

# Access parsed data
print(f"Name: {result['name']}")
print(f"Skills: {', '.join(result['skills'])}")
print(f"Experience: {result['experience_years']} years")
```

### Option 3: REST API

Start the Flask API server:

```bash
# Set API key (optional - can be passed in requests)
export GEMINI_API_KEY="your-api-key-here"

# Start server
python api_server.py
```

The server runs on `http://localhost:5000`

#### API Endpoints

**1. Health Check**
```bash
GET /health
```

**2. Parse Resume (PDF Upload)**
```bash
POST /parse
Content-Type: multipart/form-data

Parameters:
- file: PDF file
- api_key: (optional) Gemini API key
```

**Example with curl**:
```bash
curl -X POST http://localhost:5000/parse \
  -F "file=@resume.pdf" \
  -F "api_key=YOUR_GEMINI_API_KEY"
```

**Example with Python requests**:
```python
import requests

url = "http://localhost:5000/parse"
files = {"file": open("resume.pdf", "rb")}
data = {"api_key": "YOUR_GEMINI_API_KEY"}

response = requests.post(url, files=files, data=data)
result = response.json()
print(result)
```

**3. Parse Resume (Text Input)**
```bash
POST /parse-text
Content-Type: application/json

Body:
{
  "text": "Resume text here...",
  "api_key": "YOUR_GEMINI_API_KEY"
}
```

**Example**:
```bash
curl -X POST http://localhost:5000/parse-text \
  -H "Content-Type: application/json" \
  -d '{"text": "John Doe\nSoftware Engineer...", "api_key": "YOUR_KEY"}'
```

## Project Structure

```
resume-parser/
├── resume_parser.py      # Main parser class
├── api_server.py         # Flask API server
├── requirements.txt      # Python dependencies
├── README.md            # This file
└── example_usage.py     # Usage examples
```

## How It Works

1. **PDF Text Extraction**: The parser uses PyPDF2 to extract raw text from PDF files
2. **Text Processing**: The extracted text is sent to Google's Gemini API with a structured prompt
3. **AI Parsing**: Gemini analyzes the resume text and extracts relevant information
4. **JSON Formatting**: The AI response is parsed and validated as JSON
5. **Output**: Returns a structured JSON object with all resume data

## Customization

You can modify the JSON format by editing the prompt in the `parse_resume_with_gemini` method in `resume_parser.py`. Simply update the JSON structure in the prompt to add or remove fields.

## Error Handling

The parser includes comprehensive error handling for:
- Invalid or corrupted PDF files
- Missing API keys
- Gemini API failures
- JSON parsing errors
- Network issues

## Limitations

- Only supports PDF format (not Word documents or images)
- Requires internet connection for Gemini API
- Quality depends on PDF text extraction (scanned PDFs may not work well)
- Subject to Gemini API rate limits and quotas

## Troubleshooting

**Issue**: "No text could be extracted from the PDF"
- **Solution**: The PDF might be scanned or image-based. Try using OCR tools first.

**Issue**: "Error calling Gemini API"
- **Solution**: Check your API key and internet connection. Ensure you haven't exceeded rate limits.

**Issue**: "Failed to parse Gemini response as JSON"
- **Solution**: The AI might have returned invalid JSON. Check the response and adjust the prompt if needed.

## License

This project is open source and available for personal and commercial use.

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

## Support

For issues or questions, please open an issue in the repository.
