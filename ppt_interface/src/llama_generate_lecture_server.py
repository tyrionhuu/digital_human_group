import transformers
import torch
import xml.etree.ElementTree as ET

torch.cuda.set_device(3)
model_choice = 70

# Set the correct model path based on the choice
if model_choice == 8:
    model_id = "/data/share_weight/Meta-Llama-3-8B-Instruct"
elif model_choice == 70:
    model_id = "/data/share_weight/Meta-Llama-3.1-70B-Instruct"
else:
    raise ValueError("Please choose an existing model to use")

def load_xml(input_file):
    tree = ET.parse(input_file)
    root = tree.getroot()
    return root

def generate_lecture_for_slides(root, model, output_file):
    lectures = []
    # Iterate over each slide in the presentation
    for slide in root:
        slide_content = ET.tostring(slide, encoding='unicode', method='xml').strip()

        # Construct messages in a chat-like format
        messages = [
            {
                "role": "system",
                "content": "You are a lecturer who is tasked to write a lecture note for each slide in a presentation.",
            },
            {
                "role": "user",
                "content": slide_content
            },
        ]

        # Convert the messages into a single prompt
        formatted_messages = format_messages_for_llama(messages)

        # Call the model with the formatted prompt
        inputs = model.tokenizer(formatted_messages, return_tensors="pt", truncation=True, max_length=1024).to(model.device)
        output = model.generate(**inputs, max_new_tokens=2048)

        response = model.tokenizer.decode(output[0], skip_special_tokens=True).strip()
        lectures.append(response)
        print(f"Lecture for slide: {response}")

    # Save the lectures to a file
    with open(output_file, 'w') as f:
        for lecture, slide in zip(lectures, root):
            slide_title = slide.find('title').text
            f.write(f"Slide: {slide_title}\n")
            f.write(lecture)
            f.write("\n\n")
    return lectures

def format_messages_for_llama(messages):
    """
    Formats the chat-like messages into a single string that can be processed by LLaMA.
    """
    formatted = ""
    for message in messages:
        formatted += f"<|start_header_id|>{message['role']}<|end_header_id|>\n\n{message['content']}<|eot_id|>\n"
    return formatted

def merge_lecture(model, lectures_file, output_file):
    with open(lectures_file, 'r') as f:
        lectures = f.read()
    messages = [
        {
            "role": "system",
            "content": "You are a lecturer who is tasked to take in all the lecture notes of a presentation and create a thorough lecture for all the slides.",
        },
        {
            "role": "user",
            "content": lectures
        },
    ]
    formatted_messages = format_messages_for_llama(messages)
    inputs = model.tokenizer(formatted_messages, return_tensors="pt", truncation=True, max_length=1024).to(model.device)
    output = model.generate(**inputs, max_new_tokens=4096)

    response = model.tokenizer.decode(output[0], skip_special_tokens=True).strip()
    print(f"Merged lecture: {response}")

    with open(output_file, 'w+') as f:
        f.write(response)

def main(input_file):
    # Load the tokenizer and model
    model = transformers.AutoModelForCausalLM.from_pretrained(model_id)
    tokenizer = transformers.AutoTokenizer.from_pretrained(model_id)

    # If CUDA is available, load the model onto the GPU
    if torch.cuda.is_available():
        model = model.cuda()

    # Combine model and tokenizer in a usable object
    model.tokenizer = tokenizer

    # Load the XML file
    root = load_xml(input_file)

    # Generate the lecture for each slide
    intermediate_file = '../output/intermediate_lectures.txt'
    output_file = '../output/merged_lecture.txt'
    lectures = generate_lecture_for_slides(root, model, intermediate_file)

    # Merge the lecture notes into a single document
    merge_lecture(model, intermediate_file, output_file)

if __name__ == "__main__":
    input_file = '../test/test.xml'  # Modify the path as needed
    main(input_file)
