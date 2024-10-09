import ollama

res = ollama.chat(
	model="llava",
	messages=[
		{
			'role': 'user',
			'content': 'Describe this image:',
			'images': ['/Users/tyrionhuu/Desktop/1.png']
		}
	]
)

print(res['message']['content'])