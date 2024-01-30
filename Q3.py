import os
import pickle
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string

# Function to perform text preprocessing
def preprocess_text(text):
    text = text.lower()
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]
    tokens = [token for token in tokens if token not in string.punctuation]
    tokens = [token for token in tokens if token.strip()]
    return tokens

# Function to build the positional index
def build_positional_index(directory):
    positional_index = {}

    for filename in os.listdir(directory):
        with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
            text = file.read()
            tokens = preprocess_text(text)

            for i, token in enumerate(tokens):
                if token not in positional_index:
                    positional_index[token] = {}

                if filename not in positional_index[token]:
                    positional_index[token][filename] = []

                positional_index[token][filename].append(i)

    return positional_index

# Save and load positional index using Python's pickle module
def save_positional_index(positional_index, filename):
    with open(filename, 'wb') as file:
        pickle.dump(positional_index, file)

def load_positional_index(filename):
    with open(filename, 'rb') as file:
        positional_index = pickle.load(file)
    return positional_index

# Function to perform phrase queries using positional index
# Function to perform phrase queries using positional index
def phrase_query(positional_index, query):
    query_tokens = preprocess_text(query)
    result = set()

    if all(token in positional_index for token in query_tokens):
        first_token = query_tokens[0]

        for filename in positional_index[first_token]:
            positions = positional_index[first_token][filename]

            for position in positions:
                for i in range(1, len(query_tokens)):
                    current_position = position + i
                    if (
                        filename in positional_index[query_tokens[i]]
                        and current_position not in positional_index[query_tokens[i]][filename]
                    ):
                        break
                else:
                    result.add(filename)

    return result


# User input for dataset directory
directory = '/Users/sarvajeethuk/Downloads/IR/Assignment-1/Processed_Files'
positional_index = build_positional_index(directory)
save_positional_index(positional_index, 'positional_index.pkl')

# Load the positional index
loaded_positional_index = load_positional_index('positional_index.pkl')

# User input for queries and number of queries
num_queries = int(input("Enter the number of queries: "))

for _ in range(num_queries):
    query = input("Enter the phrase query: ")

    # Perform phrase query
    result = phrase_query(loaded_positional_index, query)

    # Display the result
    print(f"\nNumber of documents retrieved for query using positional index: {len(result)}")
    print(f"Names of documents retrieved for query using positional index: {list(result)}")
