import os
import re
import tempfile
import requests
from typing import Dict, List, Any
import mammoth
import PyPDF2
from docx import Document
from io import BytesIO

class ResumeParser:
    """
    Service for parsing resumes from various formats
    """
    
    def __init__(self):
        self.section_patterns = {
            'contact': r'(contact|personal|info)',
            'summary': r'(summary|profile|objective|about)',
            'experience': r'(experience|work|employment|career|professional)',
            'education': r'(education|academic|school|university|college)',
            'skills': r'(skills|technical|competencies|technologies)',
            'projects': r'(projects|portfolio|work samples)',
            'certifications': r'(certifications?|certificates?|credentials)',
            'awards': r'(awards?|honors?|achievements?|recognition)',
            'publications': r'(publications?|papers?|articles?)',
        }
    
    def parse_file(self, file_path: str) -> Dict[str, Any]:
        """
        Parse resume from file path
        """
        file_ext = os.path.splitext(file_path)[1].lower()
        
        if file_ext == '.pdf':
            return self._parse_pdf(file_path)
        elif file_ext in ['.docx', '.doc']:
            return self._parse_docx(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_ext}")
    
    def parse_google_doc(self, doc_id: str) -> Dict[str, Any]:
        """
        Parse resume from Google Docs
        """
        try:
            # Export Google Doc as plain text
            export_url = f"https://docs.google.com/document/d/{doc_id}/export?format=txt"
            response = requests.get(export_url)
            
            if response.status_code != 200:
                raise Exception("Unable to access Google Doc. Please check sharing permissions.")
            
            text_content = response.text
            return self._parse_text_content(text_content, source="google_docs")
            
        except Exception as e:
            raise Exception(f"Error parsing Google Doc: {str(e)}")
    
    def _parse_pdf(self, file_path: str) -> Dict[str, Any]:
        """
        Parse PDF file
        """
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text_content = ""
                
                for page in pdf_reader.pages:
                    text_content += page.extract_text() + "\n"
                
                # Check text quality
                warnings = []
                if len(text_content.strip()) < 100:
                    warnings.append("Low text extraction quality. Consider uploading DOCX or Google Doc for better results.")
                
                return self._parse_text_content(text_content, source="pdf", warnings=warnings)
                
        except Exception as e:
            raise Exception(f"Error parsing PDF: {str(e)}")
    
    def _parse_docx(self, file_path: str) -> Dict[str, Any]:
        """
        Parse DOCX file
        """
        try:
            # Try mammoth first for better formatting
            with open(file_path, 'rb') as docx_file:
                result = mammoth.extract_raw_text(docx_file)
                text_content = result.value
                
                if not text_content.strip():
                    # Fallback to python-docx
                    doc = Document(file_path)
                    text_content = "\n".join([paragraph.text for paragraph in doc.paragraphs])
                
                return self._parse_text_content(text_content, source="docx")
                
        except Exception as e:
            raise Exception(f"Error parsing DOCX: {str(e)}")
    
    def _parse_text_content(self, text_content: str, source: str = "unknown", warnings: List[str] = None) -> Dict[str, Any]:
        """
        Parse and structure text content into resume sections
        """
        if warnings is None:
            warnings = []
        
        lines = text_content.split('\n')
        sections = self._identify_sections(lines)
        
        # Extract structured data
        structured_data = {
            'rawText': text_content,
            'source': source,
            'contact': self._extract_contact_info(sections.get('contact', [])),
            'summary': self._extract_summary(sections.get('summary', [])),
            'experience': self._extract_experience(sections.get('experience', [])),
            'education': self._extract_education(sections.get('education', [])),
            'skills': self._extract_skills(sections.get('skills', [])),
            'projects': self._extract_projects(sections.get('projects', [])),
            'certifications': self._extract_certifications(sections.get('certifications', [])),
            'awards': self._extract_awards(sections.get('awards', [])),
            'publications': self._extract_publications(sections.get('publications', [])),
            'warnings': warnings
        }
        
        return structured_data
    
    def _identify_sections(self, lines: List[str]) -> Dict[str, List[str]]:
        """
        Identify and group lines by resume sections
        """
        sections = {}
        current_section = 'unknown'
        current_lines = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check if line is a section header
            section_found = None
            for section_name, pattern in self.section_patterns.items():
                if re.search(pattern, line, re.IGNORECASE):
                    section_found = section_name
                    break
            
            if section_found:
                # Save previous section
                if current_section and current_lines:
                    sections[current_section] = current_lines
                
                # Start new section
                current_section = section_found
                current_lines = []
            else:
                current_lines.append(line)
        
        # Save last section
        if current_section and current_lines:
            sections[current_section] = current_lines
        
        return sections
    
    def _extract_contact_info(self, lines: List[str]) -> Dict[str, Any]:
        """
        Extract contact information
        """
        contact = {}
        
        # Extract name (usually first non-empty line)
        if lines:
            contact['name'] = lines[0]
        
        # Extract email
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        for line in lines:
            email_match = re.search(email_pattern, line)
            if email_match:
                contact['email'] = email_match.group()
                break
        
        # Extract phone
        phone_pattern = r'(\+?1?[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})'
        for line in lines:
            phone_match = re.search(phone_pattern, line)
            if phone_match:
                contact['phone'] = phone_match.group()
                break
        
        # Extract links (LinkedIn, GitHub, etc.)
        url_pattern = r'https?://[^\s]+'
        links = []
        for line in lines:
            urls = re.findall(url_pattern, line)
            for url in urls:
                if 'linkedin' in url.lower():
                    links.append({'label': 'LinkedIn', 'url': url})
                elif 'github' in url.lower():
                    links.append({'label': 'GitHub', 'url': url})
                else:
                    links.append({'label': 'Website', 'url': url})
        
        if links:
            contact['links'] = links
        
        return contact
    
    def _extract_summary(self, lines: List[str]) -> str:
        """
        Extract summary/objective
        """
        return ' '.join(lines) if lines else ""
    
    def _extract_experience(self, lines: List[str]) -> List[Dict[str, Any]]:
        """
        Extract work experience
        """
        experiences = []
        current_exp = None
        
        for line in lines:
            # Check if line contains dates (likely a job entry)
            date_pattern = r'\b(19|20)\d{2}\b|\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\b|\bPresent\b'
            if re.search(date_pattern, line, re.IGNORECASE):
                # Save previous experience
                if current_exp:
                    experiences.append(current_exp)
                
                # Start new experience
                current_exp = {
                    'company': '',
                    'role': '',
                    'startDate': '',
                    'endDate': '',
                    'bullets': []
                }
                
                # Try to parse company and role from line
                parts = line.split('|')
                if len(parts) >= 2:
                    current_exp['role'] = parts[0].strip()
                    current_exp['company'] = parts[1].strip()
                else:
                    current_exp['company'] = line.strip()
            
            elif line.startswith('•') or line.startswith('-') or line.startswith('*'):
                # This is a bullet point
                if current_exp:
                    bullet_text = line.lstrip('•-* ').strip()
                    current_exp['bullets'].append({'text': bullet_text})
        
        # Save last experience
        if current_exp:
            experiences.append(current_exp)
        
        return experiences
    
    def _extract_education(self, lines: List[str]) -> List[Dict[str, Any]]:
        """
        Extract education information
        """
        education = []
        
        for line in lines:
            if any(keyword in line.lower() for keyword in ['university', 'college', 'school', 'bachelor', 'master', 'phd']):
                education.append({
                    'institution': line.strip(),
                    'degree': '',
                    'endDate': ''
                })
        
        return education
    
    def _extract_skills(self, lines: List[str]) -> Dict[str, List[str]]:
        """
        Extract skills
        """
        skills = {
            'languages': [],
            'frameworks': [],
            'tools': [],
            'other': []
        }
        
        all_skills = []
        for line in lines:
            # Split by common delimiters
            skill_items = re.split(r'[,;|•\-\*]', line)
            all_skills.extend([skill.strip() for skill in skill_items if skill.strip()])
        
        # Categorize skills (basic categorization)
        for skill in all_skills:
            skill_lower = skill.lower()
            if any(lang in skill_lower for lang in ['python', 'java', 'javascript', 'c++', 'c#', 'go', 'rust']):
                skills['languages'].append(skill)
            elif any(fw in skill_lower for fw in ['react', 'angular', 'vue', 'django', 'flask', 'spring']):
                skills['frameworks'].append(skill)
            elif any(tool in skill_lower for tool in ['git', 'docker', 'kubernetes', 'aws', 'azure']):
                skills['tools'].append(skill)
            else:
                skills['other'].append(skill)
        
        return skills
    
    def _extract_projects(self, lines: List[str]) -> List[Dict[str, Any]]:
        """
        Extract projects
        """
        projects = []
        current_project = None
        
        for line in lines:
            # Check if line looks like a project title
            if line and not line.startswith(('•', '-', '*')):
                if current_project:
                    projects.append(current_project)
                
                current_project = {
                    'name': line.strip(),
                    'description': '',
                    'bullets': []
                }
            elif line.startswith(('•', '-', '*')) and current_project:
                bullet_text = line.lstrip('•-* ').strip()
                current_project['bullets'].append(bullet_text)
        
        if current_project:
            projects.append(current_project)
        
        return projects
    
    def _extract_certifications(self, lines: List[str]) -> List[Dict[str, Any]]:
        """
        Extract certifications
        """
        certifications = []
        for line in lines:
            if line.strip():
                certifications.append({
                    'name': line.strip(),
                    'issuer': '',
                    'year': ''
                })
        return certifications
    
    def _extract_awards(self, lines: List[str]) -> List[Dict[str, Any]]:
        """
        Extract awards
        """
        awards = []
        for line in lines:
            if line.strip():
                awards.append({
                    'name': line.strip(),
                    'issuer': '',
                    'year': ''
                })
        return awards
    
    def _extract_publications(self, lines: List[str]) -> List[Dict[str, Any]]:
        """
        Extract publications
        """
        publications = []
        for line in lines:
            if line.strip():
                publications.append({
                    'title': line.strip(),
                    'venue': '',
                    'year': '',
                    'link': ''
                })
        return publications

