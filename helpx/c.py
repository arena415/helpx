# File: encode_examples.py

import base64

# Path to your original examples.txt
input_file = 'examples.txt'

# Path to save the Base64-encoded content
output_file = 'examples.b64'

# Read the original file
with open(input_file, 'rb') as f:
    file_content = f.read()

# Encode the content to Base64
encoded_content = base64.b64encode(file_content)

# Write the encoded content to the output file
with open(output_file, 'wb') as f:
    f.write(encoded_content)

print(f"Encoded '{input_file}' to '{output_file}' successfully.")

