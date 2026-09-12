import faiss
import pickle
import numpy as np

# Load FAISS index
index = faiss.read_index("rag/faiss.index")

# Load vectorizer and documents
with open("rag/metadata.pkl", "rb") as f:
    data = pickle.load(f)

vectorizer = data["vectorizer"]
documents = data["documents"]


def search_knowledge(query, k=3):

    # Convert query to TF-IDF vector
    query_vector = vectorizer.transform([query])
    query_vector = query_vector.toarray().astype("float32")

    # Search FAISS
    distances, indices = index.search(query_vector, k)

    results = []

    for distance, idx in zip(distances[0], indices[0]):

        if idx < len(documents):
            results.append({
                "document": documents[idx],
                "distance": float(distance)
            })

    return results


if __name__ == "__main__":

    query = "Why is a patient with SpO2 91 percent considered at risk?"

    print("\nQuery:")
    print(query)

    print("\nRetrieved Knowledge:\n")

    results = search_knowledge(query)

    for i, result in enumerate(results, 1):

        print(f"--- Result {i} ---")
        print(result["document"])
        print(f"Distance: {result['distance']:.4f}")
        print()
