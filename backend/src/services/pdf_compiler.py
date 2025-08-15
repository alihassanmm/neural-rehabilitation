import os
import tempfile
import subprocess
import os
import base64
import json
from typing import Dict, Any, Optional, Tuple, List

class PDFCompiler:
    """
    Service for compiling LaTeX to PDF using Tectonic engine
    """
    
    def __init__(self):
        self.temp_dir = tempfile.gettempdir()
        # Set environment for reproducibility
        self.env = os.environ.copy()
        self.env.update({
            'TECTONIC_UNTRUSTED_MODE': '1',
            'TECTONIC_CACHE_DIR': '/tmp/.tectonic-cache',
            'TECTONIC_BUNDLE_URL': 'https://data1.fullyjustified.net/tlextras-2023.2r0.tar'
        })
    
    def compile_from_base64(self, base64_tex: str, include_log: bool = False) -> Tuple[bytes, Optional[str], List[str]]:
        """
        Compile LaTeX from Base64 encoded string to PDF
        Returns (pdf_bytes, log_content, warnings)
        """
        try:
            # Decode Base64 to UTF-8
            tex_string = base64.b64decode(base64_tex).decode('utf-8')
            # Normalize to Unix newlines
            tex_string = tex_string.replace('\r\n', '\n').replace('\r', '\n')
            
            return self.compile(tex_string, include_log)
        except Exception as e:
            raise ValueError(f"Failed to decode Base64 LaTeX: {str(e)}")
    
    def compile(self, tex_string: str, include_log: bool = False) -> Tuple[bytes, Optional[str], List[str]]:
        """
        Compile LaTeX string to PDF - simplified and stable version
        Returns (pdf_bytes, log_content, warnings)
        """
        
        # Create temporary files
        with tempfile.NamedTemporaryFile(mode='w', suffix='.tex', delete=False, encoding='utf-8') as tex_file:
            tex_file.write(tex_string)
            tex_file_path = tex_file.name
        
        try:
            # Get the directory and base name
            tex_dir = os.path.dirname(tex_file_path)
            tex_basename = os.path.splitext(os.path.basename(tex_file_path))[0]
            pdf_path = os.path.join(tex_dir, f"{tex_basename}.pdf")
            log_path = os.path.join(tex_dir, f"{tex_basename}.log")
            
            # Use pdflatex for reliable compilation
            compile_command = [
                'pdflatex',
                '-interaction=nonstopmode',
                '-output-directory', tex_dir,
                tex_file_path
            ]
            
            # Run compilation
            result = subprocess.run(
                compile_command,
                capture_output=True,
                text=True,
                cwd=tex_dir
            )
            
            # Read log file if it exists
            log_content = None
            if os.path.exists(log_path):
                with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
                    log_content = f.read()
            elif result.stdout:
                log_content = result.stdout
            
            # Parse warnings from log
            warnings = self._parse_warnings(log_content or "")
            
            # Check if PDF was created
            if not os.path.exists(pdf_path):
                error_msg = f"pdflatex compilation failed (return code: {result.returncode})"
                if log_content:
                    # Extract key error information
                    error_lines = []
                    for line in log_content.split('\n'):
                        if 'error' in line.lower() or line.startswith('!') or 'undefined' in line.lower():
                            error_lines.append(line.strip())
                    if error_lines:
                        error_msg += f"\nKey errors: {'; '.join(error_lines[:3])}"
                raise RuntimeError(error_msg)
            
            # Read PDF bytes
            with open(pdf_path, 'rb') as pdf_file:
                pdf_bytes = pdf_file.read()
            
            # Clean up temporary files
            self._cleanup_files([tex_file_path, pdf_path, log_path])
            
            return pdf_bytes, log_content if include_log else None, warnings
            
        except Exception as e:
            # Clean up on error
            self._cleanup_files([tex_file_path])
            raise e
    
    def _check_tectonic(self) -> bool:
        """Check if Tectonic is available"""
        try:
            result = subprocess.run(['tectonic', '--version'], capture_output=True, text=True)
            return result.returncode == 0
        except FileNotFoundError:
            return False
    
    def _parse_warnings(self, log_content: str) -> List[str]:
        """Parse warnings from compilation log"""
        warnings = []
        
        if not log_content:
            return warnings
        
        lines = log_content.split('\n')
        for line in lines:
            line = line.strip()
            
            # Look for common warning patterns
            if 'LaTeX Font Warning' in line:
                warnings.append(f"Font Warning: {line}")
            elif 'Overfull \\hbox' in line:
                warnings.append(f"Layout Warning: {line}")
            elif 'Token not allowed in a PDF string' in line:
                warnings.append(f"PDF String Warning: {line}")
            elif 'Package hyperref Warning' in line:
                warnings.append(f"Hyperref Warning: {line}")
            elif line.startswith('Warning:'):
                warnings.append(line)
        
        return warnings
    
    def _cleanup_files(self, file_paths: List[str]):
        """Clean up temporary files"""
        for file_path in file_paths:
            try:
                if os.path.exists(file_path):
                    os.unlink(file_path)
            except OSError:
                pass  # Ignore cleanup errors

