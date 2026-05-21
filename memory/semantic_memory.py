import chromadb
from sentence_transformers import SentenceTransformer


class SemanticMemory:

    def __init__(self):
        # this model runs locally on your machine
        # no API key needed, completely free
        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        # chromadb stores vectors locally
        self.client = chromadb.Client()
        self.collection = (
            self.client.get_or_create_collection(
                name="agent_memory"
            )
        )
        self.counter = 0

    def save(self, task, result, success):
        # turn the task text into a vector (list of numbers)
        # two similar sentences will have similar vectors
        embedding = self.model.encode(
            task
        ).tolist()

        self.counter += 1

        self.collection.add(
            documents=[task],
            embeddings=[embedding],
            metadatas=[{
                "result": str(result),
                "success": str(success)
            }],
            ids=[f"mem_{self.counter}"]
        )

    def get_similar(self, task, top_k=2):
        if self.counter == 0:
            return []

        # turn current task into a vector
        # then find stored vectors closest to it
        embedding = self.model.encode(
            task
        ).tolist()

        results = self.collection.query(
            query_embeddings=[embedding],
            n_results=min(top_k, self.counter)
        )

        output = []
        for i, doc in enumerate(
            results["documents"][0]
        ):
            meta = results["metadatas"][0][i]
            output.append({
                "task": doc,
                "result": meta["result"],
                "success": meta["success"]
            })

        return output

    def as_context(self, task):
        similar = self.get_similar(task)
        if not similar:
            return ""

        lines = ["Semantically similar past tasks:"]
        for item in similar:
            outcome = (
                "succeeded"
                if item["success"] == "True"
                else "failed"
            )
            lines.append(
                f"  - '{item['task'][:60]}'"
                f" → {outcome}"
                f" | result: {item['result'][:40]}"
            )
        return "\n".join(lines)