import tkinter as tk
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

# Load pre-trained model and tokenizer
model = GPT2LMHeadModel.from_pretrained('gpt2')
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')

# Cache for tokenized prompts
cached_prompts = {}

def tokenize_code(code_snippet):
    if code_snippet in cached_prompts:
        return cached_prompts[code_snippet]
    else:
        prompt = f"Generate documentation for the following code:\n\n{code_snippet}\n\nDocumentation:"
        tokenized_prompt = tokenizer.encode(prompt, return_tensors='pt')
        cached_prompts[code_snippet] = tokenized_prompt
        return tokenized_prompt

def generate_documentation(code_snippet):
    # Tokenize the code snippet
    input_ids = tokenize_code(code_snippet)

    # Set attention mask
    attention_mask = torch.ones(input_ids.shape, dtype=torch.long, device=model.device)

    # Generate text based on the prompt
    output = model.generate(
        input_ids=input_ids,
        attention_mask=attention_mask,
        pad_token_id=tokenizer.eos_token_id,
        max_length=len(input_ids[0]) + 200,  # Adjust max length if needed
        num_return_sequences=1,
        temperature=1.0,
        do_sample=True,
        max_new_tokens=500  # Adjust max new tokens if needed
    )

    # Decode the generated text
    generated_text = tokenizer.decode(output[0], skip_special_tokens=True)

    return generated_text

def generate_button_click():
    code_snippet = code_text.get("1.0", tk.END).strip()
    if code_snippet:
        documentation = generate_documentation(code_snippet)
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, documentation)
    else:
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, "Please enter a code snippet.")

# Create the main window
root = tk.Tk()
root.title("Code Documentation Generator")

# Create input text area for code snippet
code_text = tk.Text(root, height=20, width=80)
code_text.pack()

# Create button to generate documentation
generate_button = tk.Button(root, text="Generate Documentation", command=generate_button_click)
generate_button.pack()

# Create output text area for generated documentation
output_text = tk.Text(root, height=20, width=80)
output_text.pack()

# Start the GUI event loop
root.mainloop()