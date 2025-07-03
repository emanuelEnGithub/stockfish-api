from fastapi import FastAPI, Request
from analyzer import analyze_pgn

app = FastAPI()

@app.post("/analyze-pgn")
async def analyze_pgn_route(request: Request):
    # Aquí debería obtener el JSON correctamente
    data = await request.json()
    
    # Ahora 'data' será un diccionario y podemos usar .get() para acceder a "pgn"
    pgn = data.get("pgn")
    depth = int(data.get("depth", 15))

    if not pgn:
        return {"error": "Missing PGN"}

    try:
        result = analyze_pgn(pgn, depth)
        return result
    except Exception as e:
        return {"error": str(e)}
