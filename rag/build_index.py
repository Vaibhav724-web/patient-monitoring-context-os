import faiss
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer

# Read knowledge base
with open("rag/knowledge_base.txt", "r", encoding="utf-8") as f:
    text = f.read()

# Split knowledge into sections
documents = [
    section.strip()
    for section in text.split("\n\n")
    if section.strip()
]

print(f"Loaded {len(documents)} knowledge sections")

# Convert text into TF-IDF vectors
vectorizer = TfidfVectorizer()
vectors = vectorizer.fit_transform(documents)

# FAISS needs float32 dense vectors
vectors = vectors.toarray().astype("float32")

# Create FAISS index
index = faiss.IndexFlatL2(vectors.shape[1])

# Add vectors
index.add(vectors)

# Save FAISS index
faiss.write_index(index, "rag/faiss.index")

# Save vectorizer and documents
with open("rag/metadata.pkl", "wb") as f:
    pickle.dump(
        {
            "vectorizer": vectorizer,
            "documents": documents
        },
        f
    )

print("FAISS index created successfully")
print("Documents indexed:", index.ntotal)
