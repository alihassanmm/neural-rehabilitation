import json
import os
import google.generativeai as genai
from typing import Dict, Any, List

class GeminiOptimizer:
    """
    Service for optimizing resumes using Google Gemini AI
    """
    
    def __init__(self):
        # Configure Gemini API
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-pro')
        self.resume_schema = self._get_resume_schema()
    
    def optimize_resume(self, resume_draft: Dict[str, Any], job_description: str = "", 
                      region: str = "US", seniority: str = "mid", tone: str = "standard") -> Dict[str, Any]:
        """
        Optimize resume using Gemini AI with strict JSON schema
        """
        
        # Build the optimization prompt
        prompt = self._build_optimization_prompt(
            resume_draft, job_description, region, seniority, tone
        )
        
        # Generate optimized resume with retries
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = self.model.generate_content(
                    prompt,
                    generation_config=genai.types.GenerationConfig(
                        temperature=0.2,
                        top_p=0.9,
                        max_output_tokens=8192,
                    )
                )
                
                # Extract JSON from response
                optimized_json = self._extract_json_from_response(response.text)
                
                # Validate against schema
                if self._validate_json_structure(optimized_json):
                    return optimized_json
                else:
                    if attempt < max_retries - 1:
                        continue
                    else:
                        raise Exception("Failed to generate valid JSON after multiple attempts")
                        
            except Exception as e:
                if attempt < max_retries - 1:
                    continue
                else:
                    raise Exception(f"Gemini optimization failed: {str(e)}")
        
        raise Exception("Failed to optimize resume after multiple attempts")
    
    def _build_optimization_prompt(self, resume_draft: Dict[str, Any], job_description: str,
                                 region: str, seniority: str, tone: str) -> str:
        """
        Build the optimization prompt for Gemini
        """
        
        prompt = f"""You are an expert resume optimizer. Follow the JSON schema exactly. Do not include any text outside valid JSON. Use active voice and quantifiable impact. Use STAR (Situation, Task, Action, Results), C.A.R. (Challenge, Action, Results), and the XYZ formula ("Accomplished X as measured by Y by doing Z") to craft high-impact, ATS-friendly bullets. Respect the user's region, seniority, tone, and optional job description (JD) for targeting. Maintain truthfulness—do not fabricate roles, dates, or metrics; you may estimate ranges only if user provided partial metrics and clearly mark them as estimates. Minimize industry shorthands unless widely understood. Frontload results for scanability.

TASK:
- Improve and structure the following resume into the prescribed JSON schema.
- If a Job Description (JD) is provided, align content with its requirements and vocabulary without inventing experience.
- Keep dates and employers accurate; enhance bullets using STAR/CAR with XYZ phrasing, quantify impact (%, $, time saved), and surface relevant technologies.
- Honor the tone: {tone}; region: {region}; seniority: {seniority}.
- Extract ATS keywords explicitly (meta.atsKeywords).

INPUTS:
- Resume (normalized): 
{json.dumps(resume_draft, indent=2)}

- Job Description (optional):
{job_description if job_description else "No job description provided"}

OUTPUT:
- Return ONLY valid JSON that conforms to this JSON Schema:
{json.dumps(self.resume_schema, indent=2)}

Constraints:
- bullets[].text length target: 
  - concise: 8–18 words, standard: 12–22 words, detailed: 18–30 words.
- Use consistent tense (past for past roles; present for current role).
- Use region conventions (e.g., UK vs US spelling).
- No LaTeX, no markdown, no commentary—JSON only.

IMPORTANT: Return ONLY the JSON object, no additional text or formatting."""
        
        return prompt
    
    def _extract_json_from_response(self, response_text: str) -> Dict[str, Any]:
        """
        Extract JSON from Gemini response
        """
        # Remove any markdown formatting
        response_text = response_text.strip()
        if response_text.startswith('```json'):
            response_text = response_text[7:]
        if response_text.endswith('```'):
            response_text = response_text[:-3]
        
        # Find JSON object boundaries
        start_idx = response_text.find('{')
        end_idx = response_text.rfind('}')
        
        if start_idx == -1 or end_idx == -1:
            raise Exception("No valid JSON found in response")
        
        json_str = response_text[start_idx:end_idx + 1]
        
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            raise Exception(f"Invalid JSON in response: {str(e)}")
    
    def _validate_json_structure(self, data: Dict[str, Any]) -> bool:
        """
        Basic validation of JSON structure
        """
        required_fields = ['meta', 'contact', 'summary', 'experience', 'skills']
        
        for field in required_fields:
            if field not in data:
                return False
        
        # Validate meta structure
        if not isinstance(data['meta'], dict):
            return False
        
        meta_required = ['region', 'seniority', 'tone', 'atsKeywords']
        for field in meta_required:
            if field not in data['meta']:
                return False
        
        # Validate contact structure
        if not isinstance(data['contact'], dict) or 'name' not in data['contact']:
            return False
        
        # Validate experience structure
        if not isinstance(data['experience'], list):
            return False
        
        for exp in data['experience']:
            if not isinstance(exp, dict):
                return False
            if not all(field in exp for field in ['company', 'role', 'startDate']):
                return False
        
        return True
    
    def _get_resume_schema(self) -> Dict[str, Any]:
        """
        Get the strict JSON schema for resume optimization
        """
        return {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "title": "ResumeOptimizedSchema",
            "type": "object",
            "required": ["meta", "contact", "summary", "experience", "skills"],
            "properties": {
                "meta": {
                    "type": "object",
                    "required": ["region", "seniority", "tone", "atsKeywords"],
                    "properties": {
                        "region": {"type": "string", "enum": ["US", "UK", "EU", "Other"]},
                        "seniority": {"type": "string", "enum": ["entry", "mid", "senior", "exec"]},
                        "tone": {"type": "string", "enum": ["concise", "standard", "detailed"]},
                        "atsKeywords": {"type": "array", "items": {"type": "string"}}
                    }
                },
                "contact": {
                    "type": "object",
                    "required": ["name"],
                    "properties": {
                        "name": {"type": "string"},
                        "title": {"type": "string"},
                        "email": {"type": "string"},
                        "phone": {"type": "string"},
                        "location": {"type": "string"},
                        "links": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "required": ["label", "url"],
                                "properties": {
                                    "label": {"type": "string"},
                                    "url": {"type": "string"}
                                }
                            }
                        }
                    }
                },
                "summary": {"type": "string"},
                "experience": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": ["company", "role", "startDate"],
                        "properties": {
                            "company": {"type": "string"},
                            "role": {"type": "string"},
                            "location": {"type": "string"},
                            "startDate": {"type": "string"},
                            "endDate": {"type": ["string", "null"]},
                            "bullets": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "required": ["text"],
                                    "properties": {
                                        "text": {"type": "string"},
                                        "skills": {"type": "array", "items": {"type": "string"}},
                                        "metric": {"type": "string"}
                                    }
                                }
                            }
                        }
                    }
                },
                "projects": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": ["name"],
                        "properties": {
                            "name": {"type": "string"},
                            "link": {"type": "string"},
                            "description": {"type": "string"},
                            "bullets": {"type": "array", "items": {"type": "string"}}
                        }
                    }
                },
                "education": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": ["institution", "degree"],
                        "properties": {
                            "institution": {"type": "string"},
                            "degree": {"type": "string"},
                            "location": {"type": "string"},
                            "startDate": {"type": "string"},
                            "endDate": {"type": "string"},
                            "gpa": {"type": "string"}
                        }
                    }
                },
                "skills": {
                    "type": "object",
                    "properties": {
                        "languages": {"type": "array", "items": {"type": "string"}},
                        "frameworks": {"type": "array", "items": {"type": "string"}},
                        "tools": {"type": "array", "items": {"type": "string"}},
                        "other": {"type": "array", "items": {"type": "string"}}
                    }
                },
                "certifications": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "issuer": {"type": "string"},
                            "year": {"type": "string"}
                        }
                    }
                },
                "awards": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "issuer": {"type": "string"},
                            "year": {"type": "string"}
                        }
                    }
                },
                "publications": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "title": {"type": "string"},
                            "venue": {"type": "string"},
                            "year": {"type": "string"},
                            "link": {"type": "string"}
                        }
                    }
                },
                "extras": {"type": "string"}
            }
        }

