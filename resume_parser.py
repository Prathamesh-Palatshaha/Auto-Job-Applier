"""
Resume Parser - Extracts text from PDF resumes and structures data using Gemini API
"""

import PyPDF2
import json
import os
import sys
from typing import Dict, Any
import hashlib
import time
import google.generativeai as genai

class ResumeParser:
    def __init__(self, gemini_api_key: str):
        """
        Initialize the Resume Parser with Gemini API key
        
        Args:
            gemini_api_key: Your Google Gemini API key
        """
        if not gemini_api_key:
            raise ValueError("GEMINI_API_KEY not found in environment.")
        
        genai.configure(api_key=gemini_api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """
        Extract text content from a PDF file
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Extracted text as a string
        """
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                
                # Extract text from all pages
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                
                return text.strip()
        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {str(e)}")
    
    def parse_resume_with_gemini(self, resume_text: str) -> Dict[str, Any]:
        """
        Parse resume text using Gemini API to extract structured information
        
        Args:
            resume_text: Raw text extracted from resume
            
        Returns:
            Dictionary with structured resume data
        """
        prompt = f"""
You are a resume parser. Analyze the following resume text and extract information in the exact JSON format specified below.

Resume Text:
{resume_text}

Extract and return ONLY a valid JSON object with the following structure (no other text):
{{
  "name": "Full name of the candidate",
  "email": "Email address",
  "phone": "Phone number",
  "location": "City, State/Country",
  "linkedin": "LinkedIn profile URL if available",
  "github": "GitHub profile URL if available",
  "summary": "Brief professional summary or objective",
  "skills": ["List of technical and professional skills"],
  "experience": [
    {{
      "company": "Company name",
      "position": "Job title",
      "duration": "Start date - End date or Present",
      "description": "Key responsibilities and achievements"
    }}
  ],
  "projects": [
    {{
      "name": "Project name",
      "description": "Brief project description",
      "technologies": ["Technologies used"],
      "link": "Project URL if available"
    }}
  ],
  "education": [
    {{
      "institution": "University/College name",
      "degree": "Degree and major",
      "duration": "Start year - End year",
      "gpa": "GPA if mentioned"
    }}
  ],
  "certifications": ["List of certifications"],
  "experience_years": "Total years of professional experience (calculate from experience section)",
  "domain": "Primary domain/industry (e.g., Software Development, Data Science, Marketing, etc.)"
}}

Important:
- If any field is not found, use empty string "" for strings, empty array [] for arrays
- For experience_years, calculate based on work experience dates
- For domain, infer from skills, experience, and job titles
- Ensure all JSON is properly formatted and valid
"""

        try:
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Remove markdown code blocks if present
            if response_text.startswith('```'):
                lines = response_text.split('\n')
                response_text = '\n'.join(lines[1:-1])
                if response_text.startswith('json'):
                    response_text = response_text[4:].strip()
            
            # Parse JSON
            parsed_data = json.loads(response_text)
            return parsed_data
            
        except json.JSONDecodeError as e:
            raise Exception(f"Failed to parse Gemini response as JSON: {str(e)}\nResponse: {response_text}")
        except Exception as e:
            raise Exception(f"Error calling Gemini API: {str(e)}")
    
    # def parse_resume(self, pdf_path: str, output_path: str = None) -> Dict[str, Any]:
    #     """
    #     Complete pipeline: Extract text from PDF and parse with Gemini
        
    #     Args:
    #         pdf_path: Path to the PDF resume file
    #         output_path: Optional path to save the JSON output
            
    #     Returns:
    #         Dictionary with structured resume data
    #     """
    #     print(f"📄 Extracting text from: {pdf_path}")
    #     resume_text = self.extract_text_from_pdf(pdf_path)
        
    #     if not resume_text:
    #         raise Exception("No text could be extracted from the PDF")
        
    #     print(f"✓ Extracted {len(resume_text)} characters")
    #     print(f"\n🤖 Parsing resume with Gemini API...")
        
    #     parsed_data = self.parse_resume_with_gemini(resume_text)
        
    #     print(f"✓ Successfully parsed resume for: {parsed_data.get('name', 'Unknown')}")
        
    #     # Save to file if output path is provided
    #     if output_path:
    #         with open(output_path, 'w', encoding='utf-8') as f:
    #             json.dump(parsed_data, f, indent=2, ensure_ascii=False)
    #         print(f"✓ Saved parsed data to: {output_path}")
        
    #     return parsed_data

    def parse_resume(self, pdf_path: str, output_path: str = None) -> Dict[str, Any]:
        """
        Cached resume parsing.
        If cached JSON exists and PDF not modified, load from cache.
        Otherwise call Gemini and overwrite cache.
        """

        cache_dir = "parsed_cache"
        os.makedirs(cache_dir, exist_ok=True)

        filename = os.path.basename(pdf_path)
        cache_file = os.path.join(cache_dir, filename.replace(".pdf", ".json"))

        pdf_modified_time = os.path.getmtime(pdf_path)

        # --- Check Cache ---
        if os.path.exists(cache_file):
            with open(cache_file, "r", encoding="utf-8") as f:
                cached_data = json.load(f)

            cached_time = cached_data.get("_pdf_modified_time")

            if cached_time == pdf_modified_time:
                print(f"⚡ Loaded cached resume for: {filename}")
                return cached_data["data"]

        # --- If No Cache or Modified ---
        print(f"📄 Extracting text from: {pdf_path}")
        resume_text = self.extract_text_from_pdf(pdf_path)

        print(f"✓ Extracted {len(resume_text)} characters")
        print(f"\n🤖 Parsing resume with Gemini API...")

        parsed_data = self.parse_resume_with_gemini(resume_text)

        print(f"✓ Successfully parsed resume for: {parsed_data.get('name', 'Unknown')}")

        # Save cache with metadata
        cache_payload = {
            "_pdf_modified_time": pdf_modified_time,
            "data": parsed_data
        }

        with open(cache_file, "w", encoding="utf-8") as f:
            json.dump(cache_payload, f, indent=2, ensure_ascii=False)

        print(f"💾 Cached parsed resume to: {cache_file}")

        return parsed_data


def main():
    """
    Example usage of the Resume Parser
    """
    # Check if API key is provided
    if len(sys.argv) < 3:
        print("Usage: python resume_parser.py <pdf_path> <gemini_api_key> [output_json_path]")
        print("\nExample:")
        print("  python resume_parser.py resume.pdf YOUR_GEMINI_API_KEY output.json")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    api_key = sys.argv[2]
    output_path = sys.argv[3] if len(sys.argv) > 3 else None
    
    # Validate PDF exists
    if not os.path.exists(pdf_path):
        print(f"Error: PDF file not found at {pdf_path}")
        sys.exit(1)
    
    try:
        # Initialize parser
        parser = ResumeParser(gemini_api_key=api_key)
        
        # Parse resume
        result = parser.parse_resume(pdf_path, output_path)
        
        # Display results
        print("\n" + "="*60)
        print("PARSED RESUME DATA")
        print("="*60)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
