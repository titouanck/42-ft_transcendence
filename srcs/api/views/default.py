from app.functions import jsonError

def defaultAPIView(request, remainder):
    return jsonError(request, 404, f"Endpoint {remainder}/ does not exist")
