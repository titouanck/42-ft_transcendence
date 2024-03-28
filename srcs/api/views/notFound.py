from app.functions import jsonError

def notFound(request, remainder):
    return jsonError(request, 404, f"Endpoint {remainder}/ does not exist")
