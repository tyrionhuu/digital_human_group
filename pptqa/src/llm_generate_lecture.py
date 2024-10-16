import ollama
import xml.etree.ElementTree as ET
import os

# Get the current directory where the script is located
current_dir = os.path.dirname(os.path.abspath(__file__))
    
def load_xml(input_file):
    tree = ET.parse(input_file)
    root = tree.getroot()
    return root


def generate_lecture_for_slides(root, model_name, output_file):
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
        
        # Call the model with the formatted prompt
        response = ollama.chat(
            model=model_name,
            messages=messages
        )

        # Debug: Print the model output to ensure it's correct
        print(f"Model output: {response}")

        # Get the model's response if available
        output_text = response['message']['content']
        lectures.append(output_text)
        print(f"Lecture for slide: {output_text}")
        # try:
        #     # Call the model with the formatted prompt
        #     response = ollama.chat(
        #         model=model_name,
        #         messages=formatted_prompt
        #     )

        #     # Debug: Print the model output to ensure it's correct
        #     print(f"Model output: {response}")

        #     # Get the model's response if available
        #     output_text = response['message']['content']
        #     lectures.append(output_text)
        #     print(f"Lecture for slide: {output_text}")

        # except Exception as e:
        #     print(f"Error generating lecture for slide: {e}")
        #     continue

    # Save the lectures to a file
    with open(output_file, 'w') as f:
        for lecture, slide in zip(lectures, root):
            slide_title = slide.find('title').text if slide.find('title') is not None else "Untitled Slide"
            f.write(f"Slide: {slide_title}\n")
            f.write(lecture)
            f.write("\n\n")
    return lectures



def merge_lecture(model_name, lectures_file, output_file):
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
    response = ollama.chat(
                model=model_name,
                messages=messages
            )
    # Get the model's response
    merged_lecture = response['message']['content']
    print(f"Merged lecture: {merged_lecture}")

    # Save the merged lecture to the output file
    with open(output_file, 'w+') as f:
        f.write(merged_lecture)


def main(input_file):
    # Specify the model name to use in Ollama
    model_name = 'llama3.1:8b'

    # Load the XML file
    root = load_xml(input_file)

    # Generate the lecture for each slide
    intermediate_file = os.path.join(current_dir, '../output/intermediate_lectures.txt')
    output_file = os.path.join(current_dir, '../output/merged_lecture.txt')
    
    generate_lecture_for_slides(root, model_name, intermediate_file)

    # Merge the lecture notes into a single document
    merge_lecture(model_name, intermediate_file, output_file)


if __name__ == "__main__":
    # Specify the input file path relative to the current script's directory
    input_file = os.path.join(current_dir, '../test/ML-Topic1A.xml')
    
    main(input_file)
