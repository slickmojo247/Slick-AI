from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from blueprint import app as color_tag_app
from directory_scanner import DirectoryScanner
import uvicorn

app = FastAPI(title="SLICK AI File Management System")

# Mount the color tagging subsystem
app.mount("/color-tags", color_tag_app)

# Mount reports directory for access
app.mount("/reports", StaticFiles(directory="reports"), name="reports")

@app.on_event("startup")
async def startup_event():
    """Initialize the system on startup"""
    print("Starting SLICK AI File Management System")
    # Initial scan can be triggered here if needed

if __name__ == "__main__":
    # Run the server
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000,
        reload=True,
        log_level="info"
    )