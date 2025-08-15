import jsonschema
from typing import Dict, Any, List

def validate_resume_schema(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate resume data against the strict JSON schema
    """
    
    schema = {
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
    
    try:
        jsonschema.validate(data, schema)
        return {
            "valid": True,
            "errors": [],
            "warnings": []
        }
    except jsonschema.ValidationError as e:
        return {
            "valid": False,
            "errors": [str(e)],
            "warnings": []
        }
    except Exception as e:
        return {
            "valid": False,
            "errors": [f"Validation error: {str(e)}"],
            "warnings": []
        }

