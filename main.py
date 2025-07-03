@app.post("/analyze-pgn")
async def analyze_pgn_route(request: Request):
    # Aquí no debe haber redirección
    data = await request.json()
    pgn = data.get("pgn")
    depth = int(data.get("depth", 15))

    if not pgn:
        return {"error": "Missing PGN"}

    try:
        result = analyze_pgn(pgn, depth)
        return result
    except Exception as e:
        return {"error": str(e)}
