import requests
import json
import gradio as gr

url = "http://localhost:11434/api/generate"
headers = {"Content-Type": "application/json"}
history = []

def generate_response(prompt):
    history.append(prompt)
    final_prompt = "\n".join(history)

    data = {
        "model": "codehappy:7b",
        "prompt": final_prompt,
        "stream": False
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    if response.status_code == 200:
        result = response.json()
        return result.get("response", "No response found.")
    else:
        return f"Error {response.status_code}: {response.text}"


# 🚀 Gradio Interface
interface = gr.Interface(
    fn=generate_response,
    inputs=gr.Textbox(lines=4, placeholder="Enter your Prompt"),
    outputs=gr.Textbox(label="Output", lines=15, placeholder="Response will appear here..."),  # ⬆ bigger output box
    title="HAPPY AssISTANT HERE",
    
)

interface.launch()
