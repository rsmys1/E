import pyperclip
import keyboard
import threading
import time
import pyautogui
from llama_cpp import Llama

model_path = "C:/Users/afaye/models/mistral/mistral-7b-instruct-v0.1.Q4_0.gguf"
llm = Llama(model_path=model_path)

is_typing = False
stop_typing = False
generated_text = ""
index = 0

def get_clipboard_text():
    return pyperclip.paste().strip()

def generate_academic_essay(prompt):
    instruction = f"""
Write a complete argumentative essay following this structure:
- Introduction
- Firstly paragraph
- Secondly paragraph
- Conclusion

Always agree with the topic.

Follow the DUELI academic model (Deakin University). 
Use 50% academic linking words (e.g., therefore, in contrast, furthermore) and 50% simple common ones (e.g., also, for example).
Do not include any headers like 'Body Paragraph 1' or 'Conclusion'.
Begin each paragraph with proper transitions like 'Firstly,' 'Secondly,' and 'In conclusion,'.

Topic: {prompt}

Begin writing now:
"""
    print("📡 إرسال إلى Mistral...")
    response = llm(instruction, max_tokens=600)
    return response['choices'][0]['text'].strip()

def type_text():
    global is_typing, stop_typing, generated_text, index
    while True:
        if is_typing and not stop_typing and index < len(generated_text):
            pyautogui.write(generated_text[index])
            index += 1
            time.sleep(0.03)
        time.sleep(0.05)

def start_generation():
    global is_typing, stop_typing, generated_text, index
    prompt = get_clipboard_text()
    if not prompt:
        print("❌ Clipboard فاضي!")
        return
    generated_text = generate_academic_essay(prompt)
    index = 0
    stop_typing = False
    is_typing = True
    print("✍️ جاري كتابة المقال الأكاديمي...")

def toggle_typing():
    global stop_typing
    stop_typing = not stop_typing
    print("⏸️ تم الإيقاف" if stop_typing else "▶️ استئناف")

keyboard.add_hotkey("F8", start_generation)
keyboard.add_hotkey("F9", toggle_typing)

threading.Thread(target=type_text, daemon=True).start()
print("✅ كاتب المقال الأكاديمي جاهز: F8 للبدء، F9 للإيقاف المؤقت، Esc للخروج")
keyboard.wait("esc")
