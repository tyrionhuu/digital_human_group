from llama_cpp import Llama
import xml.etree.ElementTree as ET


def load_xml(input_file):
    tree = ET.parse(input_file)
    root = tree.getroot()
    return root


def generate_lecture_for_slides(root, model, output_file):
    lectures = []
    # Iterate over each slide in the presentation
    for slide in root:
        # Extract slide content
        slide_content = ET.tostring(slide, encoding='unicode', method='xml').strip()

        # Skip if slide content is empty
        if not slide_content:
            print("Empty slide, skipping...")
            continue

        # Debug: Print the slide content for review
        print(f"Slide content: {slide_content}")

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

        # Debug: Print the formatted prompt for the model
        print(f"Formatted message: {formatted_messages}")

        try:
            # Call the model with the formatted prompt
            output = model(
                formatted_messages,
                max_tokens=2048,
                stop="<|eot_id|>",
                echo=False
            )

            # Debug: Print the model output to ensure it's correct
            print(f"Model output: {output}")

            # Get the model's response if available
            response = output['choices'][0]['text'].strip() if 'choices' in output and len(
                output['choices']) > 0 else "No output"
            lectures.append(response)
            print(f"Lecture for slide: {response}")

        except Exception as e:
            print(f"Error generating lecture for slide: {e}")
            continue

    # Save the lectures to a file
    with open(output_file, 'w') as f:
        for lecture, slide in zip(lectures, root):
            slide_title = slide.find('title').text if slide.find('title') is not None else "Untitled Slide"
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
    # Read all the lecture notes from the file
    with open(lectures_file, 'r') as f:
        lectures = f.read()

    # Prepare the prompt for merging lecture notes
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

    # Generate the merged lecture
    output = model(
        format_messages_for_llama(messages),
        max_tokens=4096,
        stop="<|eot_id|>",
        echo=False
    )

    # Get the model's response
    response = output['choices'][0]['text'].strip()
    print(f"Merged lecture: {response}")

    # Save the merged lecture to the output file
    with open(output_file, 'w+') as f:
        f.write(response)


def main(input_file):
    # Load the LLaMA model
    model_path = '../../models/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf'
    llama = Llama(model_path, n_ctx=4096)

    # Load the XML file
    root = load_xml(input_file)

    # Generate the lecture for each slide
    intermediate_file = '../output/intermediate_lectures.txt'
    output_file = '../output/merged_lecture.txt'
    lectures = generate_lecture_for_slides(root, llama, intermediate_file)

    # Merge the lecture notes into a single document
    merge_lecture(llama, intermediate_file, output_file)


if __name__ == "__main__":
    input_file = '../test/test.xml'  # Modify the path as needed
    main(input_file)
