"""
INDUSTROSENSE AI
CSA6502 - Generative AI and Large-Scale Models

Single-file implementation for Python IDLE.

Features:
1. Document ingestion
2. Text extraction
3. Text chunking
4. Sentence Transformer embeddings
5. FAISS semantic search
6. Top-3 retrieval
7. Source/provenance display
8. Simple AI-agent routing
9. Multimodal text/image/audio input placeholders
10. Safety and human-review checks
11. Audit logging
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime

import numpy as np
import faiss
from sentence_transformers import SentenceTransformer


# ============================================================
# CONFIGURATION
# ============================================================

MODEL_NAME = "all-MiniLM-L6-v2"
TOP_K = 3

DATA_FOLDER = Path("industrial_data")
AUDIT_FILE = Path("audit.log")


# ============================================================
# SAMPLE INDUSTRIAL KNOWLEDGE BASE
# ============================================================

DOCUMENTS = [
    {
        "source": "DOC-01 Equipment Manual",
        "text": """
        Motor temperature should remain within the rated operating range.
        Inspect cooling and ventilation when temperature rises.
        Check whether the cooling fan is operating correctly.
        Ensure ventilation openings are not blocked.
        """
    },

    {
        "source": "DOC-02 SOP Bearing Inspection",
        "text": """
        Inspect abnormal noise, vibration, lubrication problems,
        and visible wear when checking bearings.
        Bearing condition should be checked during scheduled maintenance.
        """
    },

    {
        "source": "DOC-03 Incident Log Pump Vibration",
        "text": """
        Previous pump vibration incidents were associated with
        bearing wear and shaft misalignment.
        Check bearing condition and alignment when unusual vibration occurs.
        """
    },

    {
        "source": "DOC-04 SOP Emergency Shutdown",
        "text": """
        Stop equipment and isolate the relevant power source
        if an unsafe condition is suspected.
        Follow the approved emergency shutdown procedure
        before inspection or maintenance.
        """
    },

    {
        "source": "DOC-05 Maintenance Manual Lubrication Schedule",
        "text": """
        Lubrication intervals depend on equipment class,
        operating hours, and manufacturer recommendations.
        Always follow the equipment manufacturer's maintenance schedule.
        """
    }
]


# ============================================================
# AUDIT LOGGING
# ============================================================

def audit_log(event, details):

    entry = {
        "timestamp": datetime.now().isoformat(),
        "event": event,
        "details": details
    }

    with open(AUDIT_FILE, "a", encoding="utf-8") as file:
        file.write(json.dumps(entry) + "\n")


# ============================================================
# TEXT CHUNKING
# ============================================================

def chunk_text(text, chunk_size=80, overlap=15):

    words = text.split()

    chunks = []

    start = 0

    while start < len(words):

        end = min(start + chunk_size, len(words))

        chunk = " ".join(words[start:end])

        if chunk.strip():
            chunks.append(chunk.strip())

        if end == len(words):
            break

        start = end - overlap

    return chunks


# ============================================================
# CREATE CHUNKS FROM DOCUMENTS
# ============================================================

def create_chunks():

    chunks = []

    for document in DOCUMENTS:

        document_chunks = chunk_text(document["text"])

        for number, chunk in enumerate(document_chunks):

            chunks.append({
                "source": document["source"],
                "chunk_id": number,
                "text": chunk
            })

    return chunks


# ============================================================
# EMBEDDING MODEL
# ============================================================

print("\nLoading embedding model...")
print("First run may take some time.\n")

model = SentenceTransformer(MODEL_NAME)


# ============================================================
# BUILD VECTOR DATABASE
# ============================================================

def build_vector_database(chunks):

    texts = []

    for item in chunks:
        texts.append(item["text"])

    embeddings = model.encode(
        texts,
        convert_to_numpy=True
    )

    embeddings = embeddings.astype("float32")

    # Normalize vectors for cosine similarity
    norms = np.linalg.norm(
        embeddings,
        axis=1,
        keepdims=True
    )

    embeddings = embeddings / np.maximum(norms, 1e-12)

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatIP(dimension)

    index.add(embeddings)

    return index


# ============================================================
# RETRIEVAL
# ============================================================

def retrieve(query, index, chunks, k=3):

    query_embedding = model.encode(
        [query],
        convert_to_numpy=True
    )

    query_embedding = query_embedding.astype("float32")

    norm = np.linalg.norm(
        query_embedding,
        axis=1,
        keepdims=True
    )

    query_embedding = query_embedding / np.maximum(
        norm,
        1e-12
    )

    scores, ids = index.search(
        query_embedding,
        k
    )

    results = []

    for score, item_id in zip(scores[0], ids[0]):

        if item_id < 0:
            continue

        result = dict(chunks[int(item_id)])

        result["score"] = float(score)

        results.append(result)

    return results


# ============================================================
# AI AGENT ROUTER
# ============================================================

FAULT_TERMS = [
    "overheating",
    "overheat",
    "vibration",
    "bearing",
    "noise",
    "leak",
    "lubrication",
    "misalignment",
    "shutdown"
]

CALCULATION_TERMS = [
    "calculate",
    "calculation",
    "maintenance date",
    "next maintenance",
    "hours",
    "interval"
]

SAFETY_TERMS = [
    "fire",
    "smoke",
    "sparking",
    "electric shock",
    "unsafe",
    "dangerous",
    "emergency"
]


def agent_route(query):

    query_lower = query.lower()

    # Calculator route
    if any(
        term in query_lower
        for term in CALCULATION_TERMS
    ):

        if re.search(r"\d", query_lower):

            return "calculator"

    # Safety-critical query
    if any(
        term in query_lower
        for term in SAFETY_TERMS
    ):

        return "rag_safety_review"

    # Normal industrial fault
    if any(
        term in query_lower
        for term in FAULT_TERMS
    ):

        return "rag"

    # Insufficient context
    if len(query_lower.split()) < 4:

        return "clarification"

    return "rag"


# ============================================================
# SAFETY CHECK
# ============================================================

def safety_check(query, answer):

    query_lower = query.lower()

    injection_terms = [
        "ignore sources",
        "ignore previous instructions",
        "disregard the documents",
        "reveal system prompt"
    ]

    if any(
        term in query_lower
        for term in injection_terms
    ):

        return False, "Possible prompt injection detected."

    if any(
        term in query_lower
        for term in SAFETY_TERMS
    ):

        return False, (
            "Safety-critical query. "
            "Human verification is required."
        )

    if not answer.strip():

        return False, "Empty response."

    return True, "Normal safety check passed."


# ============================================================
# CALCULATOR TOOL
# ============================================================

def calculator_tool(query):

    numbers = re.findall(
        r"\d+(?:\.\d+)?",
        query
    )

    if len(numbers) >= 2:

        a = float(numbers[0])
        b = float(numbers[1])

        return (
            "Calculator route selected.\n"
            f"Detected values: {a} and {b}\n"
            "Use the applicable maintenance formula "
            "from the equipment documentation."
        )

    return (
        "Calculator route selected, but more numerical "
        "information is required."
    )


# ============================================================
# MULTIMODAL INPUT
# ============================================================

def process_image(image_path):

    if not os.path.exists(image_path):

        return "Image file not found."

    extension = Path(image_path).suffix.lower()

    allowed = [
        ".jpg",
        ".jpeg",
        ".png"
    ]

    if extension not in allowed:

        return "Unsupported image format."

    return (
        "Image received successfully. "
        "A vision model can be connected here to identify "
        "visible equipment conditions. "
        "No unsupported visual diagnosis is generated."
    )


def process_audio(audio_path):

    if not os.path.exists(audio_path):

        return "Audio file not found."

    extension = Path(audio_path).suffix.lower()

    allowed = [
        ".wav",
        ".mp3"
    ]

    if extension not in allowed:

        return "Unsupported audio format."

    return (
        "Audio received successfully. "
        "An ASR/Whisper model can be connected here "
        "for speech transcription."
    )


# ============================================================
# GENERATE GROUNDED RESPONSE
# ============================================================

def generate_answer(query, results):

    if not results:

        return (
            "No relevant evidence was found in the "
            "industrial knowledge base."
        )

    answer = []

    answer.append(
        "Based on the retrieved industrial documents:"
    )

    for item in results:

        answer.append(
            f"\n[{item['source']}] "
            f"{item['text']}"
        )

    answer.append(
        "\n\nRecommended approach: inspect the relevant "
        "equipment condition and follow the applicable "
        "manufacturer manual or SOP."
    )

    answer.append(
        "\n\nThis is an advisory AI response and should "
        "not replace qualified human verification."
    )

    return "\n".join(answer)


# ============================================================
# DISPLAY RETRIEVED SOURCES
# ============================================================

def display_sources(results):

    print("\n" + "=" * 70)
    print("RETRIEVED EVIDENCE - TOP 3")
    print("=" * 70)

    for number, item in enumerate(results, 1):

        print(
            f"\n{number}. {item['source']}"
        )

        print(
            f"Similarity Score: "
            f"{item['score']:.4f}"
        )

        print(
            "Evidence:",
            item["text"]
        )


# ============================================================
# MAIN APPLICATION
# ============================================================

def main():

    print("=" * 70)
    print("             INDUSTROSENSE AI")
    print("=" * 70)

    print(
        "\nResponsible Multimodal Industrial "
        "Equipment Diagnostics"
    )

    print(
        "\nKnowledge Base:"
    )

    for document in DOCUMENTS:

        print(
            " -",
            document["source"]
        )

    # Create chunks
    print("\nCreating document chunks...")

    chunks = create_chunks()

    print(
        "Number of chunks:",
        len(chunks)
    )

    # Build vector database
    print("\nBuilding FAISS vector index...")

    index = build_vector_database(chunks)

    print("FAISS index created successfully.")

    audit_log(
        "index_created",
        {
            "chunks": len(chunks),
            "model": MODEL_NAME
        }
    )

    # Main loop
    while True:

        print("\n")
        print("=" * 70)

        query = input(
            "Enter your industrial question "
            "(or type 'exit'): "
        ).strip()

        if query.lower() == "exit":

            print("\nThank you for using IndustroSense AI.")
            break

        if not query:

            print(
                "Please enter a question."
            )

            continue

        # Agent route
        route = agent_route(query)

        print(
            "\nAgent Route:",
            route
        )

        audit_log(
            "agent_route",
            {
                "query": query,
                "route": route
            }
        )

        # Clarification
        if route == "clarification":

            print(
                "\nClarification required."
            )

            print(
                "Please provide more information such as "
                "equipment type, symptom, or operating condition."
            )

            continue

        # Calculator
        if route == "calculator":

            result = calculator_tool(query)

            print("\n" + result)

            continue

        # Retrieval
        results = retrieve(
            query,
            index,
            chunks,
            TOP_K
        )

        display_sources(results)

        # Generate grounded response
        answer = generate_answer(
            query,
            results
        )

        # Safety check
        safe, message = safety_check(
            query,
            answer
        )

        print("\n")
        print("=" * 70)
        print("GROUNDED AI RESPONSE")
        print("=" * 70)

        print(answer)

        print("\n")
        print("SAFETY STATUS:")
        print(message)

        if not safe:

            print(
                "\n⚠ HUMAN REVIEW REQUIRED"
            )

        else:

            print(
                "\n✓ Basic safety check passed."
            )

        audit_log(
            "query_completed",
            {
                "query": query,
                "route": route,
                "results": [
                    item["source"]
                    for item in results
                ],
                "human_review": not safe
            }
        )


# ============================================================
# START PROGRAM
# ============================================================

if __name__ == "__main__":

    main()
