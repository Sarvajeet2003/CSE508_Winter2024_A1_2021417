import os
import pickle
from collections import defaultdict
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

# Function to build the unigram inverted index
def build_inverted_index(directory):
    inverted_index = defaultdict(list)

    for filename in os.listdir(directory):
        with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
            text = file.read()
            tokens = preprocess_text(text)

            for i, token in enumerate(tokens):
                inverted_index[token].append((filename, i))

    return inverted_index

# Save and load inverted index using Python's pickle module
def save_inverted_index(inverted_index, filename):
    with open(filename, 'wb') as file:
        pickle.dump(inverted_index, file)

def load_inverted_index(filename):
    with open(filename, 'rb') as file:
        inverted_index = pickle.load(file)
    return inverted_index

# Function to perform boolean queries
def boolean_query(inverted_index, query_tokens, operators):
    result = set()

    # Combine tokens with the operators
    final_query = ""
    for i in range(len(query_tokens)):
        final_query += query_tokens[i]
        if i < len(operators):
            final_query += f" {operators[i]} "

    # Perform boolean operation
    if 'AND' in operators:
        result = set(inverted_index[query_tokens[0]])
        for token in query_tokens[1:]:
            result.intersection_update(set(inverted_index[token]))

    elif 'OR' in operators:
        result = set()
        for token in query_tokens:
            result.update(set(inverted_index[token]))

    elif 'AND NOT' in operators:
        result = set(inverted_index[query_tokens[0]])
        for token in query_tokens[1:]:
            result.difference_update(set(inverted_index[token]))

    elif 'OR NOT' in operators:
        all_documents = set()
        for token in query_tokens:
            all_documents.update(set(inverted_index[token]))
        result = all_documents.difference_update(set(inverted_index[query_tokens[1]]))

    return result, final_query

# User input for dataset directory
directory = '/Users/sarvajeethuk/Downloads/IR/Assignment-1/Processed_Files'
inverted_index = build_inverted_index(directory)
save_inverted_index(inverted_index, 'inverted_index.pkl')

# Load the inverted index
loaded_inverted_index = load_inverted_index('inverted_index.pkl')

# User input for query, operators, and number of queries
num_queries = int(input("Enter the number of queries: "))

for _ in range(num_queries):
    query = input("Enter the query: ")
    operators = input("Enter the boolean operators separated by commas (e.g., OR, AND NOT): ").split(', ')

    # Tokenize and preprocess the query
    query_tokens = preprocess_text(query)

    # Perform boolean query
    result, final_query = boolean_query(loaded_inverted_index, query_tokens, operators)

    # Display the result
    print(f"\nQuery: {final_query}")
    print(f"Number of documents retrieved: {len(result)}")
    print(f"Documents retrieved: {list(result)}")
