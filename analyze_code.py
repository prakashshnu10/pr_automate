import os
import openai


# Initialize the Azure OpenAI client
openai.api_key = '82d7d9dfc84f443d8b2af93e957624bf'
openai.api_base = 'https://llm-sermo-nu10.openai.azure.com/'
openai.api_type = "azure"
openai.api_version = "2024-02-15-preview"

def get_code_analysis(code):
    response = openai.ChatCompletion.create(
        engine="sermo",
        messages=[
            {"role": "system", "content": "You are a code analysis assistant."},
            {"role": "user", "content": f"Analyze the following code:\n\n{code}\n\nProvide insights and suggestions and can you optimize the time complexity and tell the before time complexity and after time complexity"}
        ],
        max_tokens=200
    )
    return response.choices[0].message['content'].strip()

def main():

    file_path = "hello.py"
    
    # Check if the file exists
    if not os.path.exists(file_path):
        print(f"File {file_path} does not exist. Please provide the correct file path.")
        return

    try:
        # Read the code from the file
        with open(file_path, "r") as file:
            code = file.read()

        print("Code from file:")
        print(code)

        analysis = get_code_analysis(code)
        with open("analysis.txt", "w") as analysis_file:
            analysis_file.write("Code Analysis:\n")
            analysis_file.write(analysis)

    except Exception as e:
        print(f"An error occurred while reading the file: {e}")

if __name__ == "__main__":
    main()
