from celery_app import celery_app
from transformers import pipeline

# Global variable to lazy-load and reuse the ML model in memory
classifier = None

@celery_app.task(bind=True)
def run_sentiment_analysis(self, text: str):
    global classifier
    
    # Load model on first task execution to save VRAM/RAM
    if classifier is None:
        classifier = pipeline(
            "sentiment-analysis", 
            model="distilbert-base-uncased-finetuned-sst-2-english"
        )
    
    results = classifier(text)
    return results[0]