import os
import json
import tempfile
import subprocess
from flask import Blueprint, request, jsonify, send_file
from werkzeug.utils import secure_filename
import google.generativeai as genai
from src.services.resume_parser import ResumeParser
from src.services.gemini_optimizer import GeminiOptimizer
from src.services.latex_renderer import LaTeXRenderer
from src.services.pdf_compiler import PDFCompiler
from src.utils.validation import validate_resume_schema
from src.utils.file_utils import allowed_file, extract_google_doc_id

resume_bp = Blueprint('resume', __name__)

# Configure Gemini API
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

@resume_bp.route('/ingest', methods=['POST'])
def ingest_resume():
    """
    Ingest resume from file upload or Google Docs URL
    """
    try:
        resume_parser = ResumeParser()
        
        # Check if file was uploaded
        if 'file' in request.files:
            file = request.files['file']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                
                # Save file temporarily
                with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(filename)[1]) as temp_file:
                    file.save(temp_file.name)
                    
                    # Parse the file
                    resume_data = resume_parser.parse_file(temp_file.name)
                    
                    # Clean up temp file
                    os.unlink(temp_file.name)
                    
                return jsonify({
                    'resumeStructuredDraft': resume_data,
                    'rawTextStats': {
                        'wordCount': len(resume_data.get('rawText', '').split()),
                        'characterCount': len(resume_data.get('rawText', ''))
                    },
                    'warnings': resume_data.get('warnings', [])
                })
        
        # Check if Google Docs URL was provided
        elif request.json and 'googleDocUrl' in request.json:
            google_doc_url = request.json['googleDocUrl']
            doc_id = extract_google_doc_id(google_doc_url)
            
            if not doc_id:
                return jsonify({'error': 'Invalid Google Docs URL'}), 400
            
            # Parse Google Doc
            resume_data = resume_parser.parse_google_doc(doc_id)
            
            return jsonify({
                'resumeStructuredDraft': resume_data,
                'rawTextStats': {
                    'wordCount': len(resume_data.get('rawText', '').split()),
                    'characterCount': len(resume_data.get('rawText', ''))
                },
                'warnings': resume_data.get('warnings', [])
            })
        
        else:
            return jsonify({'error': 'No file or Google Docs URL provided'}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@resume_bp.route('/optimize', methods=['POST'])
def optimize_resume():
    """
    Optimize resume using Gemini AI
    """
    try:
        data = request.json
        resume_draft = data.get('resumeStructuredDraft')
        job_description = data.get('jd', '')
        region = data.get('region', 'US')
        seniority = data.get('seniority', 'mid')
        tone = data.get('tone', 'standard')
        
        if not resume_draft:
            return jsonify({'error': 'Resume structured draft is required'}), 400
        
        # Initialize Gemini optimizer
        optimizer = GeminiOptimizer()
        
        # Optimize resume
        optimized_json = optimizer.optimize_resume(
            resume_draft, job_description, region, seniority, tone
        )
        
        # Validate against schema
        validation_report = validate_resume_schema(optimized_json)
        
        return jsonify({
            'optimizedJson': optimized_json,
            'atsKeywords': optimized_json.get('meta', {}).get('atsKeywords', []),
            'validationReport': validation_report
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@resume_bp.route('/render', methods=['POST'])
def render_latex():
    """
    Render optimized JSON to LaTeX
    """
    try:
        data = request.json
        optimized_json = data.get('optimizedJson')
        template_name = data.get('templateName', 'default_user_template')
        
        if not optimized_json:
            return jsonify({'error': 'Optimized JSON is required'}), 400
        
        # Initialize LaTeX renderer
        renderer = LaTeXRenderer()
        
        # Render to LaTeX
        tex_string = renderer.render(optimized_json, template_name)
        
        # Encode to Base64 for safe transport
        import base64
        base64_tex = base64.b64encode(tex_string.encode('utf-8')).decode('ascii')
        
        return jsonify({
            'texString': tex_string,  # Keep for preview
            'base64Tex': base64_tex   # For compilation
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@resume_bp.route('/compile', methods=['POST'])
def compile_pdf():
    """
    Compile LaTeX to PDF using Base64 transport
    """
    try:
        data = request.json
        base64_tex = data.get('base64Tex')
        tex_string = data.get('texString')  # Fallback for compatibility
        include_log = data.get('includeLog', False)
        
        if not base64_tex and not tex_string:
            return jsonify({'error': 'Base64 LaTeX string is required'}), 400
        
        # Initialize PDF compiler
        compiler = PDFCompiler()
        
        try:
            if base64_tex:
                # Use Base64 method (preferred)
                pdf_bytes, log_content, warnings = compiler.compile_from_base64(base64_tex, include_log)
            else:
                # Fallback to direct string method
                pdf_bytes, log_content, warnings = compiler.compile(tex_string, include_log)
            
            # Check for critical warnings
            critical_warnings = [w for w in warnings if 'Font Warning' in w or 'Overfull' in w]
            
            if critical_warnings:
                # Log warnings but still return PDF
                print(f"PDF compilation warnings: {critical_warnings}")
            
            # Create response with PDF bytes
            from flask import Response
            response = Response(pdf_bytes, mimetype='application/pdf')
            response.headers['Content-Disposition'] = 'attachment; filename=optimized_resume.pdf'
            
            # Add warnings as header if any
            if warnings:
                response.headers['X-Compilation-Warnings'] = str(len(warnings))
            
            return response
            
        except Exception as compile_error:
            # Return structured error with log if available
            error_response = {
                'error': 'PDF compilation failed',
                'details': str(compile_error)
            }
            
            # Try to get log for debugging
            if include_log:
                try:
                    _, log_content, _ = compiler.compile(tex_string or base64.b64decode(base64_tex).decode('utf-8'), True)
                    if log_content:
                        error_response['log'] = log_content[-2000:]  # Last 2000 chars
                except:
                    pass
            
            return jsonify(error_response), 422
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@resume_bp.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint
    """
    return jsonify({'status': 'healthy', 'service': 'ResumeRefiner API'})

