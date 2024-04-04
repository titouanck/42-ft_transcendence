from django.http import JsonResponse
from app.models import Match, Player
from app.functions import jsonError
from api.functions import getQueryParams
from django.db.models import Q

def matchs(request):
	if request.method != 'GET':
		return jsonError(request, 405, "Method Not Allowed")

	queryParams = getQueryParams(request.GET)
	matchs = _filter(Match.objects.all(), queryParams)

	objects = []
	for match in matchs:
		objects.append(match.publicData(request))
	return JsonResponse(objects, safe=False, json_dumps_params={'indent': 2})

def _filter(matchs, queryParams):
	if 'uid' in queryParams:
		q_objects = Q()
		for param in queryParams['uid']:
			q_objects |= Q(uid__iexact=param)	
		matchs = matchs.filter(q_objects)
	if 'uid_startswith' in queryParams:
		q_objects = Q()
		for param in queryParams['uid_startswith']:
			q_objects |= Q(uid__startswith=param)	
		matchs = matchs.filter(q_objects)
	if 'uid_endswith' in queryParams:
		q_objects = Q()
		for param in queryParams['uid_endswith']:
			q_objects |= Q(uid__endswith=param)	
		matchs = matchs.filter(q_objects)
	if 'uid_contains' in queryParams:
		q_objects = Q()
		for param in queryParams['uid_contains']:
			q_objects |= Q(uid__contains=param)	
		matchs = matchs.filter(q_objects)

	if 'match_status' in queryParams:
		q_objects = Q()
		for param in queryParams['match_status']:
			q_objects |= Q(match_status__iexact=param)	
		matchs = matchs.filter(q_objects)

	if 'scheduled_at' in queryParams:
		q_objects = Q()
		for param in queryParams['scheduled_at']:
			q_objects |= Q(scheduled_at=param)	
		matchs = matchs.filter(q_objects)

	if 'player_uid' in queryParams:
		q_objects = Q()
		for param in queryParams['player_uid']:
			q_objects |= (Q(left_player__uid=param, left_player__isnull=False) | Q(right_player__uid=param, right_player__isnull=False))
		matchs = matchs.filter(q_objects)
	if 'left_player_uid' in queryParams:
		q_objects = Q()
		for param in queryParams['left_player_uid']:
			q_objects |= (Q(left_player__uid=param, left_player__isnull=False))
		matchs = matchs.filter(q_objects)
	if 'right_player_uid' in queryParams:
		q_objects = Q()
		for param in queryParams['right_player_uid']:
			q_objects |= (Q(right_player__uid=param, right_player__isnull=False))
		matchs = matchs.filter(q_objects)

	if 'player_username' in queryParams:
		q_objects = Q()
		for param in queryParams['player_username']:
			q_objects |= (Q(left_player__username=param, left_player__isnull=False) | Q(right_player__username=param, right_player__isnull=False))
		matchs = matchs.filter(q_objects)
	if 'left_player_username' in queryParams:
		q_objects = Q()
		for param in queryParams['left_player_username']:
			q_objects |= (Q(left_player__username=param, left_player__isnull=False))
		matchs = matchs.filter(q_objects)
	if 'right_player_username' in queryParams:
		q_objects = Q()
		for param in queryParams['right_player_username']:
			q_objects |= (Q(right_player__username=param, right_player__isnull=False))
		matchs = matchs.filter(q_objects)
	
	if 'left_player_score' in queryParams:
		q_objects = Q()
		for param in queryParams['left_player_score']:
			q_objects |= (Q(left_player_score=param))
		matchs = matchs.filter(q_objects)
	if 'right_player_score' in queryParams:
		q_objects = Q()
		for param in queryParams['right_player_score']:
			q_objects |= (Q(right_player_score=param))
		matchs = matchs.filter(q_objects)

	if 'left_player_elo_initial' in queryParams:
		q_objects = Q()
		for param in queryParams['left_player_elo_initial']:
			q_objects |= (Q(left_player_elo_initial=param))
		matchs = matchs.filter(q_objects)
	if 'right_player_elo_initial' in queryParams:
		q_objects = Q()
		for param in queryParams['right_player_elo_initial']:
			q_objects |= (Q(right_player_elo_initial=param))
		matchs = matchs.filter(q_objects)

	if 'left_player_elo_final' in queryParams:
		q_objects = Q()
		for param in queryParams['left_player_elo_final']:
			q_objects |= (Q(left_player_elo_final=param))
		matchs = matchs.filter(q_objects)
	if 'right_player_elo_final' in queryParams:
		q_objects = Q()
		for param in queryParams['right_player_elo_final']:
			q_objects |= (Q(right_player_elo_final=param))
		matchs = matchs.filter(q_objects)

	return matchs