# OCR Document Extraction & RFP Analysis System

A powerful FastAPI-based application that combines Optical Character Recognition (OCR) and Large Language Models (LLM) to extract, process, and structure information from various document types, with specialized capabilities for Request for Proposal (RFP) analysis.

## 🚀 Features

### Document Processing
- **Multi-format Support**: PDF, DOCX, JPG, JPEG, PNG, TXT files
- **OCR Integration**: PaddleOCR for extracting text from scanned documents and images
- **Intelligent Text Extraction**: Handles both native text and scanned documents
- **Fallback Mechanisms**: Automatic OCR fallback when native text extraction fails

### AI-Powered Analysis
- **Structured Data Extraction**: Converts unstructured text into organized JSON format
- **RFP Specialization**: Tailored analysis for Request for Proposal documents
- **Key Information Extraction**:
  - RFP title and summary
  - Eligibility criteria
  - Important dates (submission deadlines, pre-bid meetings, contract awards)
  - Key points and requirements
  - Contact information

### Web Interface
- **Modern UI**: Clean, responsive web interface
- **Drag & Drop**: Easy file upload with drag-and-drop support
- **Real-time Processing**: Instant feedback and results display
- **Cross-platform**: Works on desktop and mobile devices

## 🛠️ Technology Stack

- **Backend**: FastAPI (Python)
- **OCR Engine**: PaddleOCR
- **AI Processing**: OpenAI GPT-4
- **Document Processing**: 
  - PyPDF2 for PDF text extraction
  - python-docx for DOCX files
  - pdf2image for PDF to image conversion
- **Frontend**: HTML5, CSS3, JavaScript
- **Deployment**: Uvicorn ASGI server

## 📋 Prerequisites

- Python 3.8 or higher
- OpenAI API key
- System dependencies for PaddleOCR (see installation section)

## 🔧 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/Prashu01/ocr-docxtract.git
cd ocr-docxtract
```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 3. Install System Dependencies

#### Windows
```bash
# Install Visual C++ Build Tools (if not already installed)
# Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install -y libgl1-mesa-glx libglib2.0-0 libsm6 libxext6 libxrender-dev libgomp1
```

#### macOS
```bash
# Install via Homebrew (if needed)
brew install opencv
```

### 4. Environment Setup
Create a `.env` file in the project root:
```bash
OPENAI_API_KEY=your_openai_api_key_here
```

### 5. Create Required Directories
```bash
mkdir temp
```

## 🚀 Usage

### Starting the Application
```bash
python main.py
```

The application will start on `http://127.0.0.1:8097`

### API Endpoints

#### POST `/upload`
Upload and process documents.

**Request:**
- Content-Type: `multipart/form-data`
- Body: File upload

**Response:**
```json
{
  "structured_data": {
    "title": "RFP Title",
    "summary": "Brief description of the RFP",
    "eligibility_criteria": ["Criteria 1", "Criteria 2"],
    "key_dates": {
      "submission_deadline": "2024-01-15",
      "pre_bid_meeting": "2024-01-10",
      "contract_award": "2024-02-01"
    },
    "key_points": ["Important point 1", "Important point 2"],
    "contact_info": {
      "name": "Contact Person",
      "email": "contact@example.com",
      "phone": "+1-234-567-8900"
    }
  }
}
```

#### GET `/`
Serve the main web interface.

### Web Interface Usage

1. **Upload Files**: Drag and drop files or click to browse
2. **Supported Formats**: PDF, DOCX, JPG, JPEG, PNG, TXT
3. **Processing**: Files are automatically processed with OCR and AI analysis
4. **Results**: Structured data is displayed in an organized format

## 📁 Project Structure

```
ocr-docxtract/
├── main.py                 # FastAPI application entry point
├── document_processor.py   # OCR and text extraction logic
├── ai_processor.py        # LLM processing and structured output
├── requirements.txt       # Python dependencies
├── static/
│   └── index.html        # Web interface
├── temp/                 # Temporary file storage
└── README.md            # This file
```

## 🔍 How It Works

### 1. Document Upload
- Files are uploaded via the web interface or API
- File type validation ensures only supported formats are processed

### 2. Text Extraction
- **Native Text**: Direct extraction from PDF/DOCX files
- **OCR Processing**: PaddleOCR extracts text from images and scanned documents
- **Fallback**: Automatic OCR when native extraction fails

### 3. AI Analysis
- Extracted text is sent to OpenAI GPT-4
- Structured output using Pydantic models
- Specialized prompts for RFP analysis

### 4. Results Delivery
- Structured JSON response
- Web interface displays organized results
- API returns machine-readable data

## ⚙️ Configuration

### Environment Variables
- `OPENAI_API_KEY`: Your OpenAI API key (required)

### Model Configuration
- OCR Language: English (configurable in `document_processor.py`)
- AI Model: GPT-4 (configurable in `ai_processor.py`)
- Temperature: 0.6 (adjustable for response creativity)

## 🐛 Troubleshooting

### Common Issues

1. **PaddleOCR Installation Issues**
   ```bash
   # Try reinstalling with specific version
   pip uninstall paddleocr
   pip install paddleocr==3.0.0
   ```

2. **OpenAI API Errors**
   - Verify API key is correct
   - Check API quota and billing
   - Ensure proper environment variable setup

3. **File Processing Errors**
   - Verify file format is supported
   - Check file size limits
   - Ensure file is not corrupted

### Debug Mode
Enable debug logging by modifying the FastAPI app configuration in `main.py`.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR) for OCR capabilities
- [OpenAI](https://openai.com/) for AI processing
- [FastAPI](https://fastapi.tiangolo.com/) for the web framework

## 📞 Support

For support and questions:
- Create an issue in the repository
- Check the troubleshooting section above
- Review the API documentation at `/docs` when the server is running

---

**Note**: This application requires an active internet connection for OpenAI API calls and may incur costs based on your OpenAI usage.
