import transformers
import torch
import xml.etree.ElementTree as ET

model = 8

## Here you paste your cloned repos location
if model == 8:
    model_id = "/data/share_weight/Meta-Llama-3-8B-Instruct"
elif model == 70:
    model_id = "/data/share_weight/Meta-Llama-3.1-70B-Instruct"
else:
    print("Please choose a existing model to use")


def load_xml(input_file):
    tree = ET.parse(input_file)
    root = tree.getroot()
    return root


def generate_lecture_for_slides(root, model,output_file):
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
        output = model(
            formatted_messages,
            max_tokens=2048,
            stop="<|eot_id|>",
            echo=False)

        response = output['choices'][0]['text'].strip()
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


def merge_lecture(model, lectures_file):
    with open(lectures_file, 'r') as f:
        lectures = f.read()
    messages = [
        {
            "role": "system",
            "content": "You are a lecturer who is tasked to take in all the lectures notes of a presentation and create a throughout lecture for all the slides.",
        },
        {
            "role": "user",
            "content": lectures
        },
    ]
    output = model(
        format_messages_for_llama(messages),
        max_tokens=4096,
        stop="<|eot_id|>",
        echo=False)
    response = output['choices'][0]['text'].strip()
    print(f"Merged lecture: {response}")


def main(input_file):
    # Load LLaMA model
    model_path = '../../models/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf'
    llama = transformers.pipeline(
        'text-generation',
        model=model_path,
        device=0 if torch.cuda.is_available() else -1
    )
    # Load the XML file
    root = load_xml(input_file)
    # Generate the lecture for each slide
    lectures = generate_lecture_for_slides(root, llama, '../output/lectures.txt')
    merge_lecture(llama, '../output/lectures.txt')

if __name__ == "__main__":
    input_file = '../test/test.xml'  # Modify the path as needed
    main(input_file)