import re
from typing import Dict, Any, List

class LaTeXRenderer:
    """
    Service for rendering optimized resume JSON to LaTeX
    """
    
    def __init__(self):
        self.latex_escape_chars = {
            '&': r'\&',
            '%': r'\%',
            '$': r'\$',
            '#': r'\#',
            '_': r'\_',
            '{': r'\{',
            '}': r'\}',
            '~': r'\textasciitilde{}',
            '^': r'\textasciicircum{}',
            '\\': r'\textbackslash{}'
        }
    
    def render(self, optimized_json: Dict[str, Any], template_name: str = "default_user_template") -> str:
        """
        Render optimized JSON to LaTeX using the specified template
        """
        
        # Get the LaTeX template
        template = self._get_template(template_name)
        
        # Extract data from JSON
        contact = optimized_json.get('contact', {})
        experience = optimized_json.get('experience', [])
        projects = optimized_json.get('projects', [])
        education = optimized_json.get('education', [])
        skills = optimized_json.get('skills', {})
        
        # Build template variables
        template_vars = {
            'NAME': self._escape_latex(contact.get('name', '')),
            'CONTACT_LINE': self._build_contact_line(contact),
            'SKILLS_BLOCK': self._build_skills_block(skills),
            'EXPERIENCE_BLOCK': self._build_experience_block(experience),
            'PROJECTS_BLOCK': self._build_projects_block(projects),
            'EDUCATION_BLOCK': self._build_education_block(education)
        }
        
        # Replace placeholders in template
        rendered_latex = template
        for var_name, var_value in template_vars.items():
            placeholder = '{{' + var_name + '}}'
            rendered_latex = rendered_latex.replace(placeholder, var_value)
        
        return rendered_latex
    
    def _escape_latex(self, text: str) -> str:
        """
        Escape special LaTeX characters in user data only.
        Does NOT escape LaTeX control sequences - only user-provided text.
        """
        if not text:
            return ""
        
        # Convert to string if not already
        text = str(text)
        
        # Normalize unicode characters to LaTeX-safe sequences
        # Handle smart quotes and dashes
        text = text.replace('"', '``').replace('"', "''")  # Smart quotes to LaTeX
        text = text.replace(''', "'").replace(''', "'")    # Smart single quotes
        text = text.replace('—', '---').replace('–', '--')  # Em/en dashes
        
        # Escape LaTeX special characters in correct order
        # Do backslash first to avoid double-escaping
        text = text.replace('\\', r'\textbackslash{}')
        text = text.replace('&', r'\&')
        text = text.replace('%', r'\%')
        text = text.replace('$', r'\$')
        text = text.replace('#', r'\#')
        text = text.replace('_', r'\_')
        text = text.replace('{', r'\{')
        text = text.replace('}', r'\}')
        text = text.replace('~', r'\textasciitilde{}')
        text = text.replace('^', r'\textasciicircum{}')
        
        return text
    
    def _escape_latex_url(self, url: str) -> str:
        """
        Escape URLs for LaTeX hyperlinks.
        Handles special characters in URLs properly.
        """
        if not url:
            return ""
        
        # Strip whitespace and newlines
        url = url.strip().replace('\n', '').replace('\r', '')
        
        # Basic URL escaping - mainly handle underscores and special chars
        url = url.replace('_', r'\_')
        url = url.replace('%', r'\%')
        url = url.replace('#', r'\#')
        
        return url
    
    def _build_contact_line(self, contact: Dict[str, Any]) -> str:
        """
        Build the contact line with email, phone, and links
        """
        contact_parts = []
        
        # Add email
        if contact.get('email'):
            email = self._escape_latex(contact['email'])
            contact_parts.append(f"\\href{{mailto:{email}}}{{{email}}}")
        
        # Add phone
        if contact.get('phone'):
            phone = self._escape_latex(contact['phone'])
            contact_parts.append(phone)
        
        # Add location
        if contact.get('location'):
            location = self._escape_latex(contact['location'])
            contact_parts.append(location)
        
        # Add links
        if contact.get('links'):
            for link in contact['links']:
                label = self._escape_latex(link.get('label', link.get('url', '')))
                url = link.get('url', '')
                if url:
                    # Use proper URL escaping for hyperlinks
                    escaped_url = self._escape_latex_url(url)
                    contact_parts.append(f"\\href{{{escaped_url}}}{{{label}}}")
        
        return " | ".join(contact_parts)
    
    def _build_skills_block(self, skills: Dict[str, List[str]]) -> str:
        """
        Build the skills block matching the exact template format
        """
        if not skills:
            return ""
        
        skills_lines = []
        
        # Add section header
        skills_lines.append("% skills section")
        skills_lines.append("\\section*{Skills}")
        
        # Define skill categories and their display names to match template
        skill_categories = {
            'languages': 'Programming Languages',
            'frameworks': 'Frameworks', 
            'tools': 'Tools',
            'other': 'Analysis',  # Changed to match template style
            'cad': 'CAD'  # Add CAD category to match template
        }
        
        # Consolidate skills into appropriate categories for the template format
        consolidated_skills = {}
        
        # Map existing skills to template categories
        if skills.get('tools'):
            # Split tools into CAD and other tools
            cad_tools = []
            other_tools = []
            for tool in skills['tools']:
                if any(cad_term in tool.lower() for cad_term in ['nx', 'catia', 'solidworks', 'autocad', 'fusion', 'inventor']):
                    cad_tools.append(tool)
                else:
                    other_tools.append(tool)
            
            if cad_tools:
                consolidated_skills['cad'] = cad_tools
            if other_tools:
                consolidated_skills['tools'] = other_tools
        
        # Add other categories as they are
        for category in ['languages', 'frameworks', 'other']:
            if skills.get(category):
                consolidated_skills[category] = skills[category]
        
        # Build skills lines in template format
        for category, display_name in skill_categories.items():
            skill_list = consolidated_skills.get(category, [])
            if skill_list:
                escaped_skills = [self._escape_latex(skill) for skill in skill_list]
                skills_line = f"\\textbf{{{display_name}:}} {', '.join(escaped_skills)} \\\\"
                skills_lines.append(skills_line)
        
        return "\n".join(skills_lines)
    
    def _build_experience_block(self, experience: List[Dict[str, Any]]) -> str:
        """
        Build the experience block matching the exact template format
        """
        if not experience:
            return ""
        
        experience_blocks = []
        
        # Add section header
        experience_blocks.append("% experience section")
        experience_blocks.append("\\section*{Experience}")
        
        for exp in experience:
            company = self._escape_latex(exp.get('company', ''))
            role = self._escape_latex(exp.get('role', ''))
            location = self._escape_latex(exp.get('location', ''))
            start_date = self._escape_latex(exp.get('startDate', ''))
            end_date = self._escape_latex(exp.get('endDate') or 'Present')
            
            # Build date range in template format
            date_range = f"{start_date} -- {end_date}" if start_date else end_date
            
            # Build header line in exact template format: Job Title, Company -- City, ST
            header_parts = []
            if role:
                header_parts.append(f"\\textbf{{{role}}}")
            if company:
                if header_parts:
                    header_parts.append(f", {{{company}}}")
                else:
                    header_parts.append(f"\\textbf{{{company}}}")
            if location:
                header_parts.append(f" -- {location}")
            
            header_line = "".join(header_parts)
            if date_range:
                header_line += f" \\hfill {date_range} \\\\"
            else:
                header_line += " \\\\"
            
            experience_blocks.append(header_line)
            
            # Add spacing before bullets (matching template)
            experience_blocks.append("\\vspace{-9pt}")
            
            # Add bullets
            bullets = exp.get('bullets', [])
            if bullets:
                experience_blocks.append("\\begin{itemize}")
                for bullet in bullets:
                    # Handle both string and dictionary bullet formats
                    if isinstance(bullet, dict):
                        bullet_text = bullet.get('text', str(bullet))
                    elif isinstance(bullet, str):
                        bullet_text = bullet
                    else:
                        bullet_text = str(bullet)
                    
                    escaped_bullet = self._escape_latex(bullet_text)
                    experience_blocks.append(f"  \\item {escaped_bullet}")
                experience_blocks.append("\\end{itemize}")
            
            # Add spacing after each job (except the last one)
            experience_blocks.append("")
        
        # Remove the last empty line and add proper spacing before next section
        if experience_blocks and experience_blocks[-1] == "":
            experience_blocks.pop()
        
        return "\n".join(experience_blocks)
    
    def _build_projects_block(self, projects: List[Dict[str, Any]]) -> str:
        """
        Build the projects block matching the exact template format
        """
        if not projects:
            return ""
        
        projects_blocks = []
        
        # Add spacing before section (matching template)
        projects_blocks.append("\\vspace{-18.5pt}")
        projects_blocks.append("")
        projects_blocks.append("% projects section")
        projects_blocks.append("\\section*{Projects}")
        
        for project in projects:
            name = self._escape_latex(project.get('name', ''))
            url = project.get('url', '')
            description = self._escape_latex(project.get('description', ''))
            
            # Build header line in template format: Project Title \hfill github.com/name/project
            header_parts = []
            if name:
                header_parts.append(f"\\textbf{{{name}}}")
            
            header_line = "".join(header_parts)
            if url:
                escaped_url = self._escape_latex_url(url)
                header_line += f" \\hfill \\href{{{escaped_url}}}{{{escaped_url}}} \\\\"
            else:
                header_line += " \\\\"
            
            projects_blocks.append(header_line)
            
            # Add spacing before bullets (matching template)
            projects_blocks.append("\\vspace{-9pt}")
            
            # Add bullets
            bullets = project.get('bullets', [])
            if bullets:
                projects_blocks.append("\\begin{itemize}")
                for bullet in bullets:
                    # Handle both string and dictionary bullet formats
                    if isinstance(bullet, dict):
                        bullet_text = bullet.get('text', str(bullet))
                    elif isinstance(bullet, str):
                        bullet_text = bullet
                    else:
                        bullet_text = str(bullet)
                    
                    escaped_bullet = self._escape_latex(bullet_text)
                    projects_blocks.append(f"  \\item {escaped_bullet}")
                projects_blocks.append("\\end{itemize}")
            elif description:
                # If no bullets but has description, add it as a single bullet
                projects_blocks.append("\\begin{itemize}")
                projects_blocks.append(f"  \\item {description}")
                projects_blocks.append("\\end{itemize}")
            
            projects_blocks.append("")
        
        # Remove the last empty line
        if projects_blocks and projects_blocks[-1] == "":
            projects_blocks.pop()
        
        return "\n".join(projects_blocks)
    
    def _build_education_block(self, education: List[Dict[str, Any]]) -> str:
        """
        Build the education block matching the exact template format
        """
        if not education:
            return ""
        
        education_blocks = []
        
        # Add spacing before section (matching template)
        education_blocks.append("\\vspace{-18.5pt}")
        education_blocks.append("")
        education_blocks.append("% education section")
        education_blocks.append("\\section*{Education}")
        
        for edu in education:
            institution = self._escape_latex(edu.get('institution', ''))
            degree = self._escape_latex(edu.get('degree', ''))
            location = self._escape_latex(edu.get('location', ''))
            end_date = self._escape_latex(edu.get('endDate', ''))
            gpa = self._escape_latex(edu.get('gpa', ''))
            
            # Build education line in template format: School -- Degree \hfill Date
            edu_parts = []
            if institution:
                edu_parts.append(f"\\textbf{{{institution}}}")
            if degree:
                if edu_parts:
                    edu_parts.append(f" -- {degree}")
                else:
                    edu_parts.append(f"\\textbf{{{degree}}}")
            if location and not end_date:  # Only add location if no date (to match template)
                edu_parts.append(f", {location}")
            if gpa:
                edu_parts.append(f" (GPA: {gpa})")
            
            edu_line = "".join(edu_parts)
            if end_date:
                edu_line += f" \\hfill {end_date} \\\\"
            else:
                edu_line += " \\\\"
            
            education_blocks.append(edu_line)
        
        return "\n".join(education_blocks)
    
    def _get_template(self, template_name: str) -> str:
        """
        Get the LaTeX template - using the exact custom template provided by user
        """
        # Custom template matching the exact format and styling requested
        return r"""\documentclass[11pt]{article}       % set main text size
\usepackage[letterpaper,                % set paper size to letterpaper. change to a4paper for resumes outside of North America
top=0.5in,                          % specify top page margin
bottom=0.5in,                       % specify bottom page margin
left=0.5in,                         % specify left page margin
right=0.5in]{geometry}              % specify right page margin
                       
\usepackage{XCharter}               % set font. comment this line out if you want to use the default LaTeX font Computer Modern
\usepackage[T1]{fontenc}            % output encoding
\usepackage[utf8]{inputenc}         % input encoding
\usepackage{enumitem}               % enable lists for bullet points: itemize and \item
\usepackage[hidelinks]{hyperref}    % format hyperlinks
\usepackage{titlesec}               % enable section title customization
\raggedright                        % disable text justification
\pagestyle{empty}                   % disable page numbering

% ensure PDF output will be all-Unicode and machine-readable
\input{glyphtounicode}
\pdfgentounicode=1

% format section headings: bolding, size, white space above and below
\titleformat{\section}{\bfseries\large}{}{0pt}{}[\vspace{1pt}\titlerule\vspace{-6.5pt}]

% format bullet points: size, white space above and below, white space between bullets
\renewcommand\labelitemi{$\vcenter{\hbox{\small$\bullet$}}$}
\setlist[itemize]{itemsep=-2pt, leftmargin=12pt, topsep=7pt}

% resume starts here
\begin{document}

% name
\centerline{\Huge {{NAME}}}

\vspace{5pt}

% contact information
\centerline{{{CONTACT_LINE}}}

\vspace{-10pt}

{{SKILLS_BLOCK}}

\vspace{-6.5pt}

{{EXPERIENCE_BLOCK}}

{{PROJECTS_BLOCK}}

{{EDUCATION_BLOCK}}

\end{document}"""

