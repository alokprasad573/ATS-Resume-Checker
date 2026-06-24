import io
import logging

logger = logging.getLogger('ats_resume_scorer')

def generate_combined_pdf(html_docs: dict[str, str]) -> bytes:
    # Try WeasyPrint first
    try:
        from weasyprint import HTML
        logger.info("Attempting PDF generation using WeasyPrint")
        documents = []
        
        # Render all HTML strings to WeasyPrint Document objects
        for name, html_str in html_docs.items():
            doc = HTML(string=html_str).render()
            documents.append(doc)
        
        # Merge them into the first document
        first_doc = documents[0]
        for other_doc in documents[1:]:
            for page in other_doc.pages:
                first_doc.pages.append(page)
                
        # Write combined PDF bytes
        return first_doc.write_pdf()
    except (ImportError, OSError, Exception) as e:
        logger.warning(f"WeasyPrint PDF generation failed/unavailable, falling back to xhtml2pdf: {e}")
        
        try:
            from xhtml2pdf import pisa
            from pypdf import PdfWriter
            
            merger = PdfWriter()
            for name, html_str in html_docs.items():
                pdf_buf = io.BytesIO()
                pisa_status = pisa.CreatePDF(html_str, dest=pdf_buf)
                if pisa_status.err:
                    raise RuntimeError(f"xhtml2pdf failed rendering document '{name}'")
                pdf_buf.seek(0)
                merger.append(pdf_buf)
                
            out_buf = io.BytesIO()
            merger.write(out_buf)
            return out_buf.getvalue()
        except Exception as fallback_err:
            logger.error(f"Fallback PDF generation with xhtml2pdf failed: {fallback_err}")
            raise RuntimeError(f"PDF generation failed: {fallback_err}") from fallback_err