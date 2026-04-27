from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from moviebox_api.v1 import Search, Session, SubjectType
from moviebox_api.v1.core import MovieDetails, DownloadableMovieFilesDetail

app = FastAPI(title="MovieBox REST API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/search")
async def search(q: str, page: int = 1):
    session = Session()
    s = Search(session, query=q, subject_type=SubjectType.MOVIES, page=page)
    results = await s.get_content()
    return results

@app.get("/sources")
async def sources(page_url: str):
    session = Session()
    md = MovieDetails(page_url, session=session)
    details = await md.get_content_model()
    dl = DownloadableMovieFilesDetail(session, details)
    files = await dl.get_content_model()
    return {
        "downloads": [{"url": f.url, "quality": str(f.quality), "size": str(f.size)} for f in (files.downloads or [])],
        "captions": [{"url": c.url, "language": c.language} for c in (files.captions or [])]
    }

@app.get("/health")
async def health():
    return {"status": "ok"}
