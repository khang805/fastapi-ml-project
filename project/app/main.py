from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from celery.result import AsyncResult
from celery_app import celery_app
from tasks import run_sentiment_analysis

app = FastAPI(title="InferQueue API")

class TextRequest(BaseModel):
    text: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict", status_code=202)
def predict(payload: TextRequest):
    if not payload.text.strip():
        raise HTTPException(status_code=400, detail="Text payload cannot be empty.")
    task = run_sentiment_analysis.delay(payload.text)
    return {"task_id": task.id, "status": "Queued"}

@app.get("/results/{task_id}")
def get_result(task_id: str):
    result = AsyncResult(task_id, app=celery_app)
    if result.status == "SUCCESS":
        return {"status": "SUCCESS", "prediction": result.result}
    elif result.status == "FAILURE":
        return {"status": "FAILURE", "error": str(result.info)}
    return {"status": result.status}

