
from fastapi import FastAPI, Request

app = FastAPI()

@app.post("/netbox-webhook")
async def receive_webhook(request: Request):
    raw = await request.body()
    print("\n====== WEBHOOK RECEIVED (RAW) ======")
    print(raw[:2000])  
    print("====================================\n")
    return {"status": "received"}
