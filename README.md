# Clinical Psychologist Interviewer 𝚿

![Clinical Psychologist Interviewer 𝚿 Icon](appendix/icon.jpeg)

**Clinical Psychologist Interviewer 𝚿** is an advanced AI platform designed to simulate clinical interviews. It leverages state-of-the-art NLP and speech technologies to emulate a clinical psychologist, offering insightful assessments and generating detailed clinical reports. This platform is ideal for educational, research, and preliminary assessment purposes but should not replace professional medical advice.

## Features and Technologies

**Key Features**:
- **Simulated Interviews**: Conducts interviews with preset psychological questions.
- **Natural Language Processing**: Understands and generates contextually relevant questions.
- **Audio Interaction**: Converts text questions to speech and transcribes audio responses to text.
- **Report Generation**: Automatically creates comprehensive clinical reports after each session.
- **Document Upload for Reports**: Generates reports from uploaded TXT, PDF, or DOCX files.
- **Multi-language Support**: Conducts interviews and generates reports in the user's preferred language.

**Technologies Used**:
- Gradio: For the user interface.
- LangChain: To create NLP chains for interview and report generation.
- OpenAI: For language models and text-to-speech conversion.
- FAISS: Document retrieval.
- PyPDF2 and python-docx: File handling.
- ReportLab: PDF generation.

## User Interface

The user interface, built with Gradio, provides an intuitive and interactive experience with two primary tabs: **Interview** and **Upload Document**.

### Interview Tab

1. **Initial Setup**: The session begins with an introductory message in both text and audio formats.
2. **Interaction**: Users can type or record responses. The AI processes these inputs to generate relevant follow-up questions, converting them into speech.
3. **Session Conclusion**: After a set number of questions, the session concludes with a closing message.
4. **Report Generation**: A detailed clinical report is generated and can be downloaded as a PDF.

### Upload Document Tab

1. **File Upload**: Users upload TXT, PDF, or DOCX files.
2. **Language Preference**: The user specifies the preferred language for the report.
3. **Report Creation**: The system analyzes the document content and generates a clinical report.
4. **Download Report**: The generated report is available for download in PDF format.

## How to Run

To run the application:
1. **Clone the Repository**: 
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```
2. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3. **Configure OpenAI API Key**:
    Set your OpenAI API key in `ai_config.py`.
4. **Launch the Application**:
    ```bash
    python app.py
    ```
5. **Access the Application**:
    Navigate to the local URL provided by Gradio.

## Core Functionalities

### Initial Setup and Response Handling

The platform begins with an initial setup where an introductory message is provided. As users interact, their inputs are processed to generate appropriate follow-up questions. These questions are then converted into speech using OpenAI’s text-to-speech technology.

### Audio Interaction and Conversion

The interaction includes converting text questions to speech and transcribing user audio responses back into text, ensuring the conversation remains fluid and engaging.

### Report Generation

Upon completion of the interview session, a comprehensive clinical report is created, detailing observations and insights based on user responses. This report can be downloaded as a PDF.

### Document-Based Report Generation

Users can generate reports from existing documents by uploading TXT, PDF, or DOCX files. The system processes the content and creates a detailed clinical report in the specified language.

## Important Details

- **Temporary Files**: The platform manages temporary audio files efficiently, ensuring they are cleaned up after use.
- **Language and Model Support**: Multiple language support and model configurations ensure accurate and contextually relevant interactions.

## License and Contributions

The project is licensed under the MIT License. For detailed terms, refer to the LICENSE file. Contributions are welcome, whether it’s identifying issues or submitting pull requests for new features, bug fixes, or documentation improvements.

## Disclaimer

This platform is a simulation and should not replace professional medical advice. Always seek advice from a qualified healthcare provider for medical concerns.

---

**Clinical Psychologist Interviewer 𝚿** stands as a testament to the potential of advanced AI technologies in simulating clinical psychology interviews and generating detailed reports. For technical details, refer to the in-code documentation. This platform offers a valuable tool for educational and research purposes by providing an enriching and interactive user experience.
