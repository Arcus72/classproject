from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import firebase_admin
from firebase_admin import credentials, db
import uvicorn

cred = credentials.Certificate("src/shoplist-key.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://shoplist-b42d0-default-rtdb.firebaseio.com/'
})

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/data")
async def add_data(data: dict):
    messages = data.get("messages", [])
    if not isinstance(messages, list):
        raise HTTPException(status_code=400, detail="Messages should be a list")

    ref = db.reference("items")
    ref.set(messages)

    return JSONResponse(content={"response": "Zaktualizowano listę", "messages": messages}, status_code=201)

@app.get("/api/data")
async def get_data():
    ref = db.reference("items")
    items = ref.get() or []
    return {"messages": items}

@app.delete("/api/data")
async def delete_data():
    ref = db.reference("items")
    ref.delete()
    return JSONResponse(content={"message": "Deleted all items"})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)

