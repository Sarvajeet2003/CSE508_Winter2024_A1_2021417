# Information Retrieval Assignment

This repository contains the code for an Information Retrieval assignment. The assignment is divided into three parts:

1. Data Preprocessing
2. Unigram Inverted Index and Boolean Queries
3. Positional Index and Phrase Queries

## Q1: Data Preprocessing

### Files
- **preprocessing.py**: Performs the following preprocessing steps on text files in the dataset:
  - Lowercase the text
  - Tokenization
  - Remove stopwords
  - Remove punctuations
  - Remove blank space tokens
  - Save preprocessed files

### Usage
```bash
python preprocessing.py
```
# Q2: Unigram Inverted Index and Boolean Queries

## Files
- **Q2.py:** Implements a unigram inverted index and supports boolean queries.
  
## Functions
1. `preprocess_text(text)`: Perform text preprocessing.
2. `build_inverted_index(directory)`: Build the unigram inverted index.
3. `save_inverted_index(inverted_index, filename)`: Save the inverted index.
4. `load_inverted_index(filename)`: Load the inverted index.
5. `boolean_query(inverted_index, query_tokens, operators)`: Perform boolean queries.

## Usage
```bash
python Q2.py
```
# Q3: Positional Index and Phrase Queries

## Files
- **Q3.py:** Implements a positional index and supports phrase queries.

## Functions
1. `preprocess_text(text)` Perform text preprocessing.
2. `build_positional_index(directory)` Build the positional index.
3. `save_positional_index(positional_index, filename)` Save the positional index.
4. `load_positional_index(filename)` Load the positional index.
5. `phrase_query(positional_index, query)` Perform phrase queries.

## Usage
```bash
python Q3.py
```
