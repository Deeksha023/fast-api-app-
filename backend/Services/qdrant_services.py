import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from fastembed import TextEmbedding
from sqlalchemy.orm import Session
from models.job import Job

load_dotenv()

COLLECTION_NAME = "job_descriptions"
VECTOR_SIZE = 384  # BAAI/bge-small-en-v1.5 outputs 384-dim vectors

qdrant = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY"),
)
embeddings_model = TextEmbedding("BAAI/bge-small-en-v1.5")

def ensure_qdrant_collection():
    collections=[c.name for c in qdrant.get_collections().collections]
    if COLLECTION_NAME  in collections:
        info= qdrant.get_collection(collection_name=COLLECTION_NAME)
        existing_vector_size = info.config.params.vectors.size
        if existing_vector_size != VECTOR_SIZE:
            qdrant.delete_collection(collection_name=COLLECTION_NAME)
            collections.remove(COLLECTION_NAME)
    if COLLECTION_NAME not in collections:
        qdrant.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=VECTOR_SIZE, 
            distance=Distance.COSINE)
        )
def embed_text(text: str) -> list[float]:
    # fastembed expects a list of documents
    return next(embeddings_model.embed([text])).tolist()

def embed_all_jobs(db: Session) -> int:
    ensure_qdrant_collection()
    jobs = db.query(Job).all()
    if not jobs:
        return 0
    points = []
    for job in jobs:
        text = f"{job.title} {job.description or ' '}"
        vector = embed_text(text)
        points.append(
            PointStruct(
                id=job.id,
                vector=vector,
                payload={
                    "job_id": job.id,
                    "title": job.title,
                    "description": job.description,
                    "salary": job.salary,
                }
            )
        )
    qdrant.upsert(collection_name=COLLECTION_NAME, points=points)
    return len(points)

def search_jobs(query: str, top_k: int = 5) -> list[dict]:
    ensure_qdrant_collection()
    query_vector = embed_text(query)
    results = qdrant.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=top_k
    )
    return [
        {
            "job_id": hit.payload.get("job_id") if hasattr(hit.payload, "get") else hit.payload.get("job_id", None),
            "title": hit.payload.get("title") if hasattr(hit.payload, "get") else hit.payload.get("title", ""),
            "description": hit.payload.get("description") if hasattr(hit.payload, "get") else hit.payload.get("description", ""),
            "salary": hit.payload.get("salary") if hasattr(hit.payload, "get") else hit.payload.get("salary", None),
            "score": round(hit.score, 4) if hasattr(hit, "score") else 0.0
        }
        for hit in getattr(results, "points", [])
    ]

def match_jobs_for_profile(skills: str, experience: str, top_k: int = 5) -> list[dict]:
    ensure_qdrant_collection()
    profile_text = f"{skills} {experience}"
    profile_vector = embed_text(profile_text)
    results = qdrant.query_points(
        collection_name=COLLECTION_NAME,
        query=profile_vector,
        limit=top_k
    )
    return [
        {
            "job_id": hit.payload.get("job_id") if hasattr(hit.payload, "get") else hit.payload.get("job_id", None),
            "title": hit.payload.get("title") if hasattr(hit.payload, "get") else hit.payload.get("title", ""),
            "description": hit.payload.get("description") if hasattr(hit.payload, "get") else hit.payload.get("description", ""),
            "salary": hit.payload.get("salary") if hasattr(hit.payload, "get") else hit.payload.get("salary", None),
            "score": round(hit.score, 4) if hasattr(hit, "score") else 0.0
        }
        for hit in getattr(results, "points", [])
    ]
    