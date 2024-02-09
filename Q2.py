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

#             #0 AS ANSWER
# def boolean_query(inverted_index, query_tokens, operators):
#     result = set()

#     # Combine tokens with the operators
#     final_query = ""
#     for i in range(len(query_tokens)):
#         final_query += query_tokens[i]
#         if i < len(operators):
#             final_query += f" {operators[i]} "

#     operator_index = 0
#     current_operator = None

#     for token in query_tokens:
#         if current_operator is None:
#             result.update(set(inverted_index[token]))
#         else:
#             if current_operator == 'AND':
#                 print("ANd")
#                 result.intersection_update(set(inverted_index[token]))
#             elif current_operator == 'OR':
#                 print("OR")
#                 result.update(set(inverted_index[token]))
#             elif current_operator == 'AND NOT':
#                 print("ANDNOY")
#                 result.difference_update(set(inverted_index[token]))
#             elif current_operator == 'OR NOT':
#                 print("orNOT")
#                 result.update(set(inverted_index[token]))

#         if operator_index < len(operators):
#             current_operator = operators[operator_index]
#             operator_index += 1

#     return result, final_query

def boolean_query(inverted_index, query_tokens, operators):
    result = set()

    # Combine tokens with the operators
    final_query = ""
    for i in range(len(query_tokens)):
        final_query += query_tokens[i]
        if i < len(operators):
            final_query += f" {operators[i]} "

    operator_index = 0
    current_operator = None

    unique_documents = set()

    for token in query_tokens:
        if current_operator is None:
            result.update(set(inverted_index.get(token, [])))
        else:
            if current_operator == 'AND':
                result.intersection_update(set(inverted_index[token]))
            elif current_operator == 'OR':
                result.update(set(inverted_index[token]))
            elif current_operator == 'AND NOT':
                if token in inverted_index:
                    result.difference_update(set(inverted_index[token]))
                else:
                    all_documents = set(filename for filename in os.listdir(directory))
                    result.difference_update(all_documents)
            elif current_operator == 'OR NOT':
            # Handle NOT query for a token not present in the inverted index first
                if token in inverted_index:
                    result.symmetric_difference_update(set(inverted_index[token]))
                else:
                    not_result = set(filename for filename in os.listdir(directory))
                    result.update(not_result)
            # Use symmetric difference (XOR) for 'OR NOT' after performing NOT
                


        if operator_index < len(operators):
            current_operator = operators[operator_index]
            operator_index += 1

    for doc_tuple in result:
        if(len(doc_tuple)!=2):
            return result, final_query
        unique_documents.add(doc_tuple[0])

    return unique_documents, final_query


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











#     # # Function to perform boolean queries
# # def boolean_query(inverted_index, query_tokens, operators):
# #     result = set()

# #     # Combine tokens with the operators
# #     final_query = ""
# #     for i in range(len(query_tokens)):
# #         final_query += query_tokens[i]
# #         if i < len(operators):
# #             final_query += f" {operators[i]} "

# #     if 'AND' in operators:
# #         print("anssd")
# #         result = set(inverted_index[query_tokens[0]])
# #         for token in query_tokens[1:]:
# #             result.intersection_update(set(inverted_index[token]))

# #     elif 'OR' in operators:
# #         print("orr")
# #         result = set()
# #         for token in query_tokens:
# #             result.update(set(inverted_index[token]))

# #     elif 'AND NOT' in operators:
# #         print("and not")
# #         result = set(inverted_index[query_tokens[0]])
# #         for token in query_tokens[1:]:
# #             result.difference_update(set(inverted_index[token]))

# #     # elif 'OR NOT' in operators:
# #     #     all_documents = set().union(*(set(inverted_index[token]) for token in query_tokens))
# #     #     result = all_documents.difference(set(inverted_index[query_tokens[1]]))
# #     elif ' OR NOT' in operators:
# #         print("iwdhuksjgv")
# #         or_result = set()
# #         for token in query_tokens:
# #             if token == 'OR':
# #                 result.update(or_result)
# #                 or_result = set()
# #             elif token != 'NOT':
# #                 or_result.update(set(inverted_index[token]))

# #         result.difference_update(set(inverted_index[query_tokens[-1]]))
# #     return result, final_query



# def boolean_query(inverted_index, query_tokens, operators):
#     result = set()

#     # Combine tokens with the operators
#     final_query = ""
#     for i in range(len(query_tokens)):
#         final_query += query_tokens[i]
#         if i < len(operators):
#             final_query += f" {operators[i]} "

#     operator_index = 0
#     current_operator = None

#     for token in query_tokens:
#         if current_operator is None:
#             result.update(set(inverted_index[token]))
#         else:
#             if current_operator == 'AND':
#                 print("ANd")
#                 result.intersection_update(set(inverted_index[token]))
#             elif current_operator == 'OR':
#                 print("OR")
#                 result.update(set(inverted_index[token]))
#             elif current_operator == 'AND NOT':
#                 print("ANDNOY")
#                 result.difference_update(set(inverted_index[token]))
#             elif current_operator == 'OR NOT':
#                 print("orNOT")
#                 result.update(set(inverted_index[token]))

#         if operator_index < len(operators):
#             current_operator = operators[operator_index]
#             operator_index += 1

#     return result, final_query

# # 2 as the answer
# # # Function to perform boolean queries
# # def boolean_query(inverted_index, query_tokens, operators):
# #     result = set()

# #     # Combine tokens with the operators
# #     final_query = " ".join([f"{query_tokens[i]} {operators[i]}" if i < len(operators) else f"{query_tokens[i]}" for i in range(len(query_tokens))])

# #     # Process the entire boolean expression
# #     current_operator = None
# #     current_set = set(inverted_index[query_tokens[0]])

# #     for i in range(1, len(query_tokens)):
# #         token = query_tokens[i]
# #         if token in {'AND', 'OR', 'NOT'}:
# #             current_operator = token
# #         else:
# #             if current_operator == 'AND':
# #                 current_set.intersection_update(set(inverted_index[token]))
# #             elif current_operator == 'OR':
# #                 current_set.update(set(inverted_index[token]))
# #             elif current_operator == 'NOT':
# #                 current_set.difference_update(set(inverted_index[token]))

# #     result.update(current_set)

# #     return result, final_query

