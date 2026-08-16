from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {
        "message": "Student Chatbot Backend is running!"
    }