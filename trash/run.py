import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",  # Allows external access
        port=8000,
        reload=True  # Enable auto-reload during development
    )
