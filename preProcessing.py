import os
import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Ensure NLTK stopwords are downloaded
import nltk
nltk.download('stopwords')
nltk.download('punkt')

# Define your input and output directories
input_directory = '/Users/sarvajeethuk/Downloads/IR/Assignment-1/text_files'
output_directory = '/Users/sarvajeethuk/Downloads/IR/Assignment-1/Processed_Files'

# Create output directory if it doesn't exist
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Function to perform preprocessing on a single file
def preprocess_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Lowercasing
    content = content.lower()

    # Tokenization
    tokens = word_tokenize(content)

    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]

    # Remove punctuations
    tokens = [token for token in tokens if token not in string.punctuation]

    # Remove blank space tokens
    tokens = [token for token in tokens if token.strip()]

    # Save the preprocessed content to a new file
    output_path = os.path.join(output_directory, os.path.basename(file_path))
    with open(output_path, 'w', encoding='utf-8') as output_file:
        output_file.write(' '.join(tokens))

    return tokens, output_path

# Process all files
all_files = os.listdir(input_directory)
count = 0
for file_name in all_files:
    if count >=5:
        break
    file_path = os.path.join(input_directory, file_name)

    # Before preprocessing
    with open(file_path, 'r', encoding='utf-8') as file:
        original_content = file.read()
    print(f"\nOriginal content of {file_name}:\n{original_content}")

    # After preprocessing
    processed_tokens, output_path = preprocess_file(file_path)
    with open(output_path, 'r', encoding='utf-8') as file:
        preprocessed_content = file.read()
    print(f"\nPreprocessed content of {file_name}:\n{preprocessed_content}")

    print("\n------------------------")
    count = count+1

print("\nPreprocessing completed and files saved in:", output_directory)
