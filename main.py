# This file is without frames and also without main.png files 
import os
import customtkinter as ctk
from gtts import gTTS
import pygame
import tkinter as tk

def generate_response(prompt, model):
    response = os.popen(f"ollama run {model} '{prompt}'").read()
    return response.strip()

def text_to_speech(text, lang='en', tld='com'):
    if text:
        tts = gTTS(text, lang=lang, slow=False, tld=tld)
        tts.save("response.mp3")
        pygame.mixer.init()
        pygame.mixer.music.load("response.mp3")
        pygame.mixer.music.play()
    else:
        print("No text to speak.")

def on_submit():
    prompt = prompt_entry.get("1.0", 'end-1c')
    model = model_combobox.get()  # Get the selected model from the ComboBox
    response = generate_response(prompt, model)
    chat_history.configure(state=ctk.NORMAL)
    chat_history.insert(ctk.END, "🤵: " + prompt + "\n")
    chat_history.insert(ctk.END, "🤖 (" + model + "): " + response + "\n\n")
    chat_history.configure(state=ctk.DISABLED)
    chat_history.yview(ctk.END)
    prompt_entry.delete("1.0", ctk.END)
    global latest_response
    latest_response = response

def on_vocal():
    try:
        text_to_speech(latest_response)
    except NameError:
        print("No response to vocalize")

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()
    app.title("❖ A.I assistant ❖")
    app.geometry("350x650")
    app.resizable(False, False)

    # Create main frame to hold the chat interface
    main_frame = tk.Frame(app, bg="#2427e3")
    main_frame.pack(fill='both', expand=True)

    # Create a frame for model selection label and combobox
    model_frame = tk.Frame(main_frame, bg="#2427e3")
    model_frame.pack(pady=(10, 0))

    # Create the model textbox
    model_textbox = ctk.CTkTextbox(model_frame, width=120, height=10, corner_radius=8, fg_color="white", font=("Trebuchet MS", 12))
    model_textbox.insert("1.0", "✦ Select Model:")
    model_textbox.configure(state=ctk.DISABLED, text_color="black")
    model_textbox.pack(side=tk.LEFT, padx=5)

    # Create the model combobox
    model_combobox = ctk.CTkComboBox(model_frame, values=["Llama3.2", "phi3", "mistral", "qwen2.5", "starcoder2"], font=("Trebuchet MS", 14), fg_color="black")
    model_combobox.set("phi3")  # Set default value
    model_combobox.pack(side=tk.LEFT, padx=5)


    # Add widgets to the main frame
    chat_history_label = ctk.CTkLabel(main_frame, text="Ollama Live Chat 📜", font=("Trebuchet MS", 16), text_color="white", corner_radius=8, fg_color="#158542", bg_color="#2427e3")
    chat_history_label.pack(pady=(5, 0))

    chat_history = ctk.CTkTextbox(main_frame, wrap=ctk.WORD, width=360, height=250, corner_radius=8)
    chat_history.pack(padx=5, pady=5)
    chat_history.configure(state=ctk.DISABLED)

    prompt_entry_label = ctk.CTkLabel(main_frame, text="Your Prompts 💭", font=("Trebuchet MS", 16), text_color="white", corner_radius=8, fg_color="#158542", bg_color="#2427e3")
    prompt_entry_label.pack(pady=(5, 0))

    prompt_entry = ctk.CTkTextbox(main_frame, wrap=ctk.WORD, width=360, height=100, corner_radius=8)
    prompt_entry.pack(padx=5, pady=5)

    # Create a frame for the buttons to align them in the same row
    button_frame = tk.Frame(main_frame, bg="#2427e3")
    button_frame.pack(pady=5)

    submit_button = ctk.CTkButton(button_frame, text="Send Prompt ➤", font=("Trebuchet MS", 12), command=on_submit, corner_radius=8, fg_color="#e37a24", hover_color="#e39424")
    submit_button.pack(side=tk.LEFT, padx=5)

    vocal_button = ctk.CTkButton(button_frame, text="Listen 🔊", font=("Trebuchet MS", 12),  command=on_vocal, corner_radius=8, fg_color="#e37a24", hover_color="#e39424")
    vocal_button.pack(side=tk.LEFT, padx=5)

    # Add copyright label with text wrapping
    copyright_label = ctk.CTkLabel(
        main_frame, 
        text="⚙ To install Ollama visit:\nhttps://ollama.com/download\n🔽 To clone Models run:\nollama pull llama3.2\n\n\n© 2025 Amir Faramarzpour.", 
        text_color="white", 
        font=("Trebuchet MS", 12),
        corner_radius=4, 
        wraplength=380  # Set wrap length to fit within the right frame
    )
    copyright_label.pack(pady=(10, 0))

    app.mainloop()
