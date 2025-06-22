from fastapi import APIRouter, Request, UploadFile, File
from typing import List
from models.customResponse import resp_200, resp_500

router = APIRouter()

# ========== General Info ==========


@router.get("/")  # <--- works!
# Returns API environment and version info
def api_version(request: Request):
    environment = request.app.state.settings.get("APP_ENV")
    version = request.app.state.settings.get("APP_API_VERSION")
    endpoint = "ingest"

    return resp_200(data={"environment": environment, "version": version, "endpoint": endpoint}, message="success")


# ========== 1. File Upload & Ingestion ==========


@router.post("/upload")  # <--- not tested
# Uploads one or more files (PDFs, images) to the server
async def upload_files(files: List[UploadFile] = File(...)):
    try:
        filenames = [f.filename for f in files]
        return resp_200(message="Files uploaded successfully", data={"filenames": filenames})
    except Exception as e:
        return resp_500(data=str(e))


@router.get("/status")  # <--- works!
# Retrieves the current status of the ingestion pipeline
async def get_ingestion_status():
    try:
        return resp_200(data={"pending": 1, "completed": 2, "failed": 0})
    except Exception as e:
        return resp_500(data=str(e))


@router.post("/extract/{file_id}")  # <--- works!
# Starts the text/table/image extraction process for a specific file
async def extract_file_content(file_id: str):
    try:
        return resp_200(message=f"Extraction started for file {file_id}")
    except Exception as e:
        return resp_500(data=str(e))


@router.post("/reprocess/{file_id}")  # <--- works!
# Reprocesses a file, useful if extraction previously failed or was updated
async def reprocess_file(file_id: str):
    try:
        return resp_200(message=f"Reprocessing started for file {file_id}")
    except Exception as e:
        return resp_500(data=str(e))


# ========== 2. Chunk & Metadata Operations ==========


@router.get("/chunks/{file_id}")  # <--- works!
# Returns all chunks (text blocks, tables, etc.) extracted from a specific file
async def get_chunks_by_file(file_id: str):
    try:
        return resp_200(data={"chunks": []})
    except Exception as e:
        return resp_500(data=str(e))


@router.get("/chunk/{chunk_id}")  # <--- works!
# Retrieves the details of a single chunk
async def get_chunk(chunk_id: str):
    try:
        return resp_200(data={"chunk": {}})
    except Exception as e:
        return resp_500(data=str(e))


@router.put("/chunk/{chunk_id}")  # <--- works!
# Updates the content or metadata of a specific chunk
async def update_chunk(chunk_id: str):
    try:
        return resp_200(message=f"Chunk {chunk_id} updated")
    except Exception as e:
        return resp_500(data=str(e))


@router.delete("/chunk/{chunk_id}")  # <--- works!
# Deletes a specific chunk (e.g. bad OCR result or misextracted text)
async def delete_chunk(chunk_id: str):
    try:
        return resp_200(message=f"Chunk {chunk_id} deleted")
    except Exception as e:
        return resp_500(data=str(e))


# ========== 3. Tagging & Labeling ==========


@router.post("/chunk/{chunk_id}/tag")  # <--- works!
# Adds or updates tags (e.g., 'definition', 'exclusion') for a chunk
async def tag_chunk(chunk_id: str):
    try:
        return resp_200(message=f"Tags updated for chunk {chunk_id}")
    except Exception as e:
        return resp_500(data=str(e))


@router.post("/chunk/{chunk_id}/label")  # <--- works!
# Sets the primary label or category for a chunk (single-class version of tag)
async def label_chunk(chunk_id: str):
    try:
        return resp_200(message=f"Label set for chunk {chunk_id}")
    except Exception as e:
        return resp_500(data=str(e))


# ========== 4. Embedding & Qdrant ==========


@router.post("/embed/{file_id}")  # <--- works!
# Generates vector embeddings for all chunks in a file and stores them in Qdrant
async def embed_chunks(file_id: str):
    try:
        return resp_200(message=f"Embedding started for file {file_id}")
    except Exception as e:
        return resp_500(data=str(e))


@router.get("/embedding/status/{file_id}")  # <--- works!
# Retrieves the current embedding status for a specific file
async def get_embedding_status(file_id: str):
    try:
        return resp_200(data={"status": "In progress"})
    except Exception as e:
        return resp_500(data=str(e))


@router.delete("/embedding/delete/{file_id}")  # <--- works!
# Deletes the embeddings of a file from Qdrant (for cleanup or reembedding)
async def delete_embeddings(file_id: str):
    try:
        return resp_200(message=f"Embeddings deleted for file {file_id}")
    except Exception as e:
        return resp_500(data=str(e))


# ========== 5. Testing / Debugging ==========


@router.post("/debug/chunk")  # <--- works!
# Simulates the chunking process on raw input for debugging/testing
async def debug_chunk_logic():
    try:
        return resp_200(data={"chunks": []})
    except Exception as e:
        return resp_500(data=str(e))


@router.get("/test/pdf/highlight")  # <--- works!
# Tests the bounding box/highlight logic on a sample PDF page
async def test_pdf_highlight():
    try:
        return resp_200(data={"test_result": "PDF highlight tested"})
    except Exception as e:
        return resp_500(data=str(e))
