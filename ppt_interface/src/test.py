import ppt_extraction

def main():
    pptx_path = "../test/test.pptx"
    text = ppt_extraction.extract_text_from_pptx(pptx_path)
    print(text)

if __name__ == "__main__":
    main()

