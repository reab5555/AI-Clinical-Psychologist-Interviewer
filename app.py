import gradio as gr
import tempfile
import os
from pathlib import Path
from io import BytesIO
from settings import (
    respond,
    generate_random_string,
    reset_interview,
    generate_interview_report,
    generate_report_from_file,
    interview_history,
    question_count,
    language,
)
from ai_config import convert_text_to_speech, transcribe_audio, n_of_questions
from prompt_instructions import get_interview_initial_message

# Global variables
temp_audio_files = []
initial_audio_path = None


def reset_interview_action():
    global question_count, interview_history
    question_count = 0
    interview_history.clear()
    initial_message = get_interview_initial_message()

    # Generate new audio for the initial message
    initial_audio_buffer = BytesIO()
    convert_text_to_speech(initial_message, initial_audio_buffer)
    initial_audio_buffer.seek(0)

    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_file:
        temp_audio_path = temp_file.name
        temp_file.write(initial_audio_buffer.getvalue())

    temp_audio_files.append(temp_audio_path)

    return (
        [(None, initial_message)],  # Reset chatbot
        temp_audio_path,  # New audio
        gr.File(visible=False),  # Hide PDF output
        gr.Textbox(visible=True),  # Show message input
        "Interview reset. You can start a new interview now."  # Status message
    )


# Initialize Gradio interface
def create_app():
    global initial_audio_path
    initial_message = get_interview_initial_message()

    # Generate the audio for the initial message and save to a temporary file
    initial_audio_buffer = BytesIO()
    convert_text_to_speech(initial_message, initial_audio_buffer)
    initial_audio_buffer.seek(0)

    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_file:
        initial_audio_path = temp_file.name
        temp_file.write(initial_audio_buffer.getvalue())

    temp_audio_files.append(initial_audio_path)

    with gr.Blocks(title="Clinical Psychologist Interviewer 𝚿") as demo:
        gr.Image(value="appendix/icon.jpeg", label='icon', width=20, scale=1, show_label=False,
                 show_download_button=False, show_share_button=False)
        gr.Markdown(
            """
            # Clinical Psychologist Interviewer 𝚿
            This chatbot conducts clinical interviews based on psychological knowledge.
            Please note that this is a simulation and should not be used as a substitute for professional medical advice.

            The interviewer will prepare a clinical report based on the interview.
            """
        )

        with gr.Tab("Interview"):
            audio_output = gr.Audio(
                label="Sarah",
                scale=1,
                value=initial_audio_path,
                autoplay=True,
                visible=True,
                show_download_button=False,
            )

            reset_button = gr.Button("Reset Interview", size='sm')
            chatbot = gr.Chatbot(value=[(None, f"{initial_message}")], label=f"Clinical Interview 𝚿📋")
            with gr.Row():
                msg = gr.Textbox(label="Type your message here...", scale=3)
                audio_input = gr.Audio(sources=(["microphone"]), label="Record your message", type="filepath", scale=2)
            send_button = gr.Button("Send")
            pdf_output = gr.File(label="Download Report", visible=False)

            def user(user_message, audio, history):
                print(audio)
                if audio is not None:
                    user_message = transcribe_audio(audio)
                    print(user_message)

                return "", None, history + [[user_message, None]]

            def bot_response(chatbot, message):
                global question_count, temp_audio_files
                question_count += 1

                # Use the last user message from the chatbot history
                last_user_message = chatbot[-1][0] if chatbot else message

                response, audio_buffer = respond(chatbot, last_user_message)

                # Add all bot responses to the chatbot history
                for bot_message in response:
                    chatbot.append((None, bot_message[1]))

                if isinstance(audio_buffer, BytesIO):
                    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_file:
                        temp_audio_path = temp_file.name
                        temp_file.write(audio_buffer.getvalue())
                    temp_audio_files.append(temp_audio_path)
                    audio_output = temp_audio_path
                else:
                    audio_output = audio_buffer

                if question_count >= n_of_questions():
                    conclusion_message = "Thank you for participating in this interview. We have reached the end of our session. I hope this conversation has been helpful. Take care!"
                    chatbot.append((None, conclusion_message))

                    conclusion_audio_buffer = BytesIO()
                    convert_text_to_speech(conclusion_message, conclusion_audio_buffer)
                    conclusion_audio_buffer.seek(0)

                    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_file:
                        temp_audio_path = temp_file.name
                        temp_file.write(conclusion_audio_buffer.getvalue())
                    temp_audio_files.append(temp_audio_path)
                    audio_output = temp_audio_path

                    # Generate report automatically
                    report_content, pdf_path = generate_interview_report(interview_history, language)

                    # Add report to the chat
                    chatbot.append((None, f"Interview Report:\n\n{report_content}"))

                    return chatbot, audio_output, gr.File(visible=True, value=pdf_path), gr.Textbox(visible=False)

                return chatbot, audio_output, gr.File(visible=False), gr.Textbox(visible=True)

            msg.submit(user, [msg, audio_input, chatbot], [msg, audio_input, chatbot], queue=False).then(
                bot_response, [chatbot, msg], [chatbot, audio_output, pdf_output, msg]
            )

            send_button.click(user, [msg, audio_input, chatbot], [msg, audio_input, chatbot], queue=False).then(
                bot_response, [chatbot, msg], [chatbot, audio_output, pdf_output, msg]
            )

            reset_button.click(
                reset_interview_action,
                inputs=[],
                outputs=[chatbot, audio_output, pdf_output, msg, audio_input]
            )

        with gr.Tab("Upload Document"):
            file_input = gr.File(label="Upload a TXT, PDF, or DOCX file")
            language_input = gr.Textbox(label="Preferred Language for Report",
                                        placeholder="Enter language")
            generate_button = gr.Button("Generate Report")
            report_output = gr.Textbox(label="Generated Report", lines=100)
            pdf_output = gr.File(label="Download Report", visible=True)

            def generate_report_and_pdf(file, language):
                report_content, pdf_path = generate_report_from_file(file, language)
                return report_content, pdf_path, gr.File(visible=True)

            generate_button.click(
                generate_report_and_pdf,
                inputs=[file_input, language_input],
                outputs=[report_output, pdf_output, pdf_output]
            )

    return demo


# Clean up function
def cleanup():
    global temp_audio_files, initial_audio_path
    for audio_file in temp_audio_files:
        if os.path.exists(audio_file):
            os.unlink(audio_file)
    temp_audio_files.clear()

    if initial_audio_path and os.path.exists(initial_audio_path):
        os.unlink(initial_audio_path)


if __name__ == "__main__":
    app = create_app()
    try:
        app.launch()
    finally:
        cleanup()