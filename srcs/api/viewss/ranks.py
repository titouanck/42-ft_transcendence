from django.http import JsonResponse
from app.functions import jsonError

def ranks(request):
	if request.method != 'GET':
		return jsonError(request, 405, "Method Not Allowed")
	ranks = [
		{
			'UNRANKED' : {
				'min_elo' : 0,
				'max_elo' : None,
			},
		},
		{
			'BRONZE' : {
				'min_elo' : None,
				'max_elo' : None,
			},
		},
		{
			'SILVER' : {
				'min_elo' : None,
				'max_elo' : None,
			},
		},
		{
			'GOLD' : {
				'min_elo' : None,
				'max_elo' : None,
			},
		},
		{
			'PLATINIUM' : {
				'min_elo' : None,
				'max_elo' : None,
			},
		},
		{
			'DIAMOND' : {
				'min_elo' : None,
				'max_elo' : None,
			},
		},
		{
			'ELITE' : {
				'min_elo' : None,
				'max_elo' : None,
			},
		},
		{
			'CHAMPION' : {
				'min_elo' : None,
				'max_elo' : None,
			},
		},
		{
			'UNREAL' : {
				'min_elo' : None,
				'max_elo' : None,
			},
		}
	]
	return JsonResponse(ranks, safe=False, json_dumps_params={'indent': 2})
