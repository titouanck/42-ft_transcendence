from django.db.models import Case, IntegerField, Value, When
from django.db.models import Case, CharField, Value, When
from django.db.models.functions import Coalesce
from django.db.models.functions import Length
from django.db.models import Q
from django.http import JsonResponse
from app.models import Player
from api.functions import getQueryParams
from app.functions import jsonError

def users(request):
	if request.method != 'GET':
		return jsonError(request, 405, "Method Not Allowed")

	queryParams = getQueryParams(request.GET)
	players = _filter(Player.objects.all(), queryParams)

	objects = []
	for player in players:
		objects.append(player.publicData(request))
	return JsonResponse(objects, safe=False, json_dumps_params={'indent': 2})

def _filter(players, queryParams):
	if 'uid' in queryParams:
		q_objects = Q()
		for param in queryParams['uid']:
			q_objects |= Q(uid__iexact=param)	
		players = players.filter(q_objects)
	if 'uid_startswith' in queryParams:
		q_objects = Q()
		for param in queryParams['uid_startswith']:
			q_objects |= Q(uid__startswith=param)	
		players = players.filter(q_objects)
	if 'uid_endswith' in queryParams:
		q_objects = Q()
		for param in queryParams['uid_endswith']:
			q_objects |= Q(uid__endswith=param)	
		players = players.filter(q_objects)
	if 'uid_contains' in queryParams:
		q_objects = Q()
		for param in queryParams['uid_contains']:
			q_objects |= Q(uid__contains=param)	
		players = players.filter(q_objects)

	if 'username' in queryParams:
		q_objects = Q()
		for param in queryParams['username']:
			q_objects |= Q(username__iexact=param)	
		players = players.filter(q_objects)
	if 'username_startswith' in queryParams:
		q_objects = Q()
		for param in queryParams['username_startswith']:
			q_objects |= Q(username__startswith=param)	
		players = players.filter(q_objects)
	if 'username_endswith' in queryParams:
		q_objects = Q()
		for param in queryParams['username_endswith']:
			q_objects |= Q(username__endswith=param)	
		players = players.filter(q_objects)
	if 'username_contains' in queryParams:
		q_objects = Q()
		for param in queryParams['username_contains']:
			q_objects |= Q(username__contains=param)	
		players = players.filter(q_objects)

	if 'status' in queryParams:
		q_objects = Q()
		for param in queryParams['status']:
			q_objects |= Q(status__iexact=param)	
		players = players.filter(q_objects)

	rankOrder = {
		'UNRANKED': 0,
		'BRONZE': 1,
		'SILVER': 2,
		'GOLD': 3,
		'PLATINIUM': 4,
		'DIAMOND': 5,
		'ELITE': 6,
		'CHAMPION': 7,
		'UNREAL': 8,
	}
	if 'rank' in queryParams:
		q_objects = Q()
		for param in queryParams['rank']:
			q_objects |= Q(rank__iexact=param)	
		players = players.filter(q_objects)
	if 'rank_min' in queryParams:
		q_objects = Q()
		for param in queryParams['rank_min']:
			param = param.upper()
			if param in rankOrder:
				rankNumber = rankOrder[param]
				while rankNumber <= rankOrder['UNREAL']:
					rank = next(key for key, value in rankOrder.items() if value == rankNumber)
					q_objects |= Q(rank__iexact=rank)	
					rankNumber += 1
		players = players.filter(q_objects)
	if 'rank_max' in queryParams:
		q_objects = Q()
		for param in queryParams['rank_max']:
			param = param.upper()
			if param in rankOrder:
				rankNumber = rankOrder[param]
				while rankNumber >= rankOrder['UNRANKED']:
					rank = next(key for key, value in rankOrder.items() if value == rankNumber)
					q_objects |= Q(rank__iexact=rank)	
					rankNumber -= 1
		players = players.filter(q_objects)

	if 'elo' in queryParams:
		q_objects = Q()
		for param in queryParams['elo']:
			q_objects |= Q(elo=param)	
		players = players.filter(q_objects)
	if 'elo_min' in queryParams:
		q_objects = Q()
		for param in queryParams['elo_min']:
			q_objects |= Q(elo__gte=param)	
		players = players.filter(q_objects)
	if 'elo_max' in queryParams:
		q_objects = Q()
		for param in queryParams['elo_max']:
			q_objects |= Q(elo__lte=param)	
		players = players.filter(q_objects)

	if 'victories' in queryParams:
		q_objects = Q()
		for param in queryParams['victories']:
			q_objects |= Q(victories=param)	
		players = players.filter(q_objects)
	if 'victories_min' in queryParams:
		q_objects = Q()
		for param in queryParams['victories_min']:
			q_objects |= Q(victories__gte=param)	
		players = players.filter(q_objects)
	if 'victories_max' in queryParams:
		q_objects = Q()
		for param in queryParams['victories_max']:
			q_objects |= Q(victories__lte=param)	
		players = players.filter(q_objects)

	if 'defeats' in queryParams:
		q_objects = Q()
		for param in queryParams['defeats']:
			q_objects |= Q(defeats=param)	
		players = players.filter(q_objects)
	if 'defeats_min' in queryParams:
		q_objects = Q()
		for param in queryParams['defeats_min']:
			q_objects |= Q(defeats__gte=param)	
		players = players.filter(q_objects)
	if 'defeats_max' in queryParams:
		q_objects = Q()
		for param in queryParams['defeats_max']:
			q_objects |= Q(defeats__lte=param)	
		players = players.filter(q_objects)

	if 'order_by' in queryParams:
		q_objects = Q()
		orderOptions = ['uid', 'username', 'elo', 'status', 'victories', 'defeats']
		for param in queryParams['order_by']:
			if param in orderOptions:
				players = players.order_by(param)
			elif param[0] == '-' and param[1:] in orderOptions:
				players = players.order_by(f'-{param[1:]}')
			elif param == 'username_length':
				players = players.annotate(username_length=Length('username')).order_by('username_length')
			elif param == '-username_length':
				players = players.annotate(username_length=Length('username')).order_by('-username_length')
			elif param == 'rank':
				players = players.annotate(rank_order=Case(
					*[When(rank=rank, then=Value(rankOrder[rank])) for rank in rankOrder],
					default=Value(0),
					output_field=IntegerField(),
				)
				).order_by('rank_order')
			elif param == '-rank':
				players = players.annotate(rank_order=Case(
					*[When(rank=rank, then=Value(rankOrder[rank])) for rank in rankOrder],
					default=Value(0),
					output_field=IntegerField(),
				)
				).order_by('-rank_order')

	return players