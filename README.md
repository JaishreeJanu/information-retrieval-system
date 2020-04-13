## An information retrieval system from large document collection

- This application lets us search text documents for given text query by leveraging benefits of building inverted index prior to information access.
- For each term, there is a list of doc IDs where that term occurs.
- This list is called **postings list**. We take all postings list of query terms (user query) and merge(**intersection for conjunctive query and union for disjunctive query**) them to find documents containing query terms.
- You can read the blog [here](https://medium.com/@janujaishree94/searchit-an-information-retrieval-system-33d2af956da4) to know more about inverted index and how to create one(step by step).

## Development setup
- Collect document and put them in the folder ```document_collection```.
- Run ```python3 InvertedIndex.py```
- See your inverted index created in dict.json file
- Give any text query and see the list of documents containing the query terms.



