from fastapi import FastAPI, Request
from analyzer import analyze_pgn

# Aquí definimos la aplicación FastAPI
app = FastAPI()

# Ahora puedes usar el decorador correctamente
@app.post("/analyze-pgn")
async def analyze_pgn_route(request: Request):
    data = await request.json()  # Deserializamos el JSON
    pgn = data.get("pgn")
    depth = int(data.get("depth", 15))

    if not pgn:
        return {"error": "Missing PGN"}

    try:
        result = analyze_pgn(pgn, depth)
        return result
    except Exception as e:
        return {"error": str(e)}
