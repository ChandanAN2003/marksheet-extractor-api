import io
import fitz # PyMuPDF
from fastapi import FastAPI, UploadFile, HTTPException, status, File, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from PIL import Image
import pytesseract

# Remove the Windows-specific path for Render deployment. 
# pytesseract will automatically find the executable on Render's Linux server
# because tesseract-ocr is installed via apt-get.
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

from .models.schemas import MarksheetResult
from .services.llm_service import extract_data_with_llm
from .utils.image_processor import resize_image, preprocess_image

app = FastAPI(title="Marksheet Extraction API")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/extract/", response_model=MarksheetResult)
async def extract_marksheet_data(file: UploadFile = File(...)):
    if file.size > 10 * 1024 * 1024:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="File size exceeds the 10 MB limit."
        )

    content_type = file.content_type
    raw_text = ""
    try:
        if content_type in ["image/jpeg", "image/png"]:
            image_data = await file.read()
            img = Image.open(io.BytesIO(image_data))
            
            img = resize_image(img)
            img = preprocess_image(img)
            
            raw_text = pytesseract.image_to_string(img)
            img.close()

        elif content_type == "application/pdf":
            pdf_data = await file.read()
            doc = fitz.open(stream=pdf_data, filetype="pdf")
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                pix = page.get_pixmap(matrix=fitz.Matrix(300 / 72, 300 / 72))
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                
                img = resize_image(img)
                img = preprocess_image(img)
                
                raw_text += pytesseract.image_to_string(img) + "\n\n"
                img.close()
            doc.close()

        else:
            raise HTTPException(
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                detail="Unsupported file format. Please upload a JPG, PNG, or PDF."
            )
        
        # Add this print statement for debugging purposes
        print("--- Raw Text from OCR ---")
        print(raw_text)
        print("-------------------------")
        
        if not raw_text.strip():
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Could not extract any text from the document. The file might be corrupted or of low quality."
            )
        
        extracted_json = extract_data_with_llm(raw_text)
        if not extracted_json:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to process document with LLM. Please try again."
            )
        
        return MarksheetResult.model_validate(extracted_json)

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )