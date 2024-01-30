import os
import string
import pickle
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Ensure NLTK stopwords are downloaded
import nltk
nltk.download('stopwords')
nltk.download('punkt')

# Define your input and output directories
input_directory = '/Users/sarvajeethuk/Downloads/IR/Assignment-1/Processed_Files'
output_directory = '/Users/sarvajeethuk/Downloads/IR/Assignment-1/Inverted_Index'

# Create output directory if it doesn't exist
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Function to perform preprocessing and build inverted index
def build_inverted_index(file_path, doc_id):
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

    # Build the inverted index
    for term in set(tokens):
        if term not in inverted_index:
            inverted_index[term] = [doc_id]
        else:
            inverted_index[term].append(doc_id)

# Process all files and build the inverted index
inverted_index = {}
all_files = os.listdir(input_directory)

for doc_id, file_name in enumerate(all_files):
    file_path = os.path.join(input_directory, file_name)
    build_inverted_index(file_path, doc_id)

# Save the inverted index using pickle
pickle_path = os.path.join(output_directory, 'inverted_index.pkl')
with open(pickle_path, 'wb') as pickle_file:
    pickle.dump(inverted_index, pickle_file)

print("Unigram Inverted Index created and saved using pickle.")



import os
import string
import pickle
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Ensure NLTK stopwords are downloaded
import nltk
nltk.download('stopwords')
nltk.download('punkt')

class InvertedIndexElement:
    def __init__(self, c, docId):
        self.character = c
        self.frequency = 1
        self.docIds = [docId]
    
    def increaseFreq(self, by=1):
        self.frequency += by
    
    def addDocId(self, id):
        self.docIds.append(id)

    def printIndexElement(self):
        return str(self.character) + ' ' + str(self.frequency) + ' -> ' + str(self.getDocIds())             
    
    def getDocIds(self):
        return self.docIds

# Function to perform preprocessing on a single file
def preprocess_file(content):
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

    return tokens

# Function to build inverted index from preprocessed files
# Function to build inverted index from preprocessed files
def build_inverted_index(input_directory):
    inverted_index = {}
    all_files = os.listdir(input_directory)

    for doc_id, file_name in enumerate(all_files, start=1):
        file_path = os.path.join(input_directory, file_name)
        
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            tokens = preprocess_file(content)

        for token in set(tokens):
            if token not in inverted_index:
                inverted_index[token] = {doc_id}  # Use doc_id instead of file_name
            else:
                inverted_index[token].add(doc_id)

    return inverted_index, all_files  # Return all_files as well
# Function to execute boolean operations on the inverted index
# Function to execute boolean operations on the inverted index
def execute_query(query, inverted_index, all_files):
    stack = []

    for term in query:
        if term == 'AND':
            operand2 = stack.pop() if stack else set()
            operand1 = stack.pop() if stack else set()
            result = operand1 & operand2
            stack.append(result)
        elif term == 'OR':
            operand2 = stack.pop() if stack else set()
            operand1 = stack.pop() if stack else set()
            result = operand1 | operand2
            stack.append(result)
        elif term == 'NOT':
            operand = stack.pop() if stack else set()
            result = set(range(1, len(all_files) + 1)) - operand
            stack.append(result)
        elif term == 'AND NOT':
            operand2 = stack.pop() if stack else set()
            operand1 = stack.pop() if stack else set(range(1, len(all_files) + 1))
            result = operand1 - operand2
            stack.append(result)
        elif term == 'OR NOT':
            operand2 = stack.pop() if stack else set()
            operand1 = stack.pop() if stack else set(range(1, len(all_files) + 1))
            result = operand1 | (set(range(1, len(all_files) + 1)) - operand2)
            stack.append(result)
        else:
            stack.append(set(inverted_index.get(term, set())))

    return stack.pop()

# Function to preprocess a query
def preprocess_query(query):
    return preprocess_file(' '.join(query))

# Function to insert boolean operators between preprocessed queries
def insert_boolean_operators(preprocessed_queries, operators):
    merged_query = []

    for i in range(len(preprocessed_queries)):
        merged_query.append(preprocessed_queries[i])
        if i < len(operators):
            merged_query.append(operators[i])

    return merged_query

# Function to print the output format
def print_output(query_number, result_set, all_files, original_query):
    print(f"Query {query_number}: {' '.join(original_query)}")
    print(f"Number of documents retrieved for query {query_number}: {len(result_set)}")
    print(f"Names of the documents retrieved for query {query_number}: {', '.join([all_files[i-1] for i in result_set])}\n")

# Define your input and output directories
input_directory = '/Users/sarvajeethuk/Downloads/IR/Assignment-1/Processed_Files'
output_directory = '/Users/sarvajeethuk/Downloads/IR/Assignment-1/Inverted_Index'

# Build inverted index
inverted_index, all_files = build_inverted_index(input_directory)

# Save the inverted index using pickle with the correct file extension
with open(os.path.join(output_directory, 'invertedIndexPickle.pkl'), 'wb') as dbfile:
    pickle.dump(inverted_index, dbfile)

# Input for queries and boolean operators
num_queries = int(input("Enter the number of queries: "))
queries = []
operators = []

for i in range(num_queries):
    query = input("Enter query: ").split()
    preprocessed_query = preprocess_query(query)
    queries.append(preprocessed_query)

    if i < num_queries - 1:
        op = input("Enter boolean operator (AND, OR, NOT, AND NOT, OR NOT): ")
        operators.append(op)

# Merge queries and operators
merged_queries = insert_boolean_operators(queries, operators)

# Execute merged queries and print output
result_set = execute_query(merged_queries, inverted_index, all_files)
print_output(1, result_set, all_files, merged_queries)
