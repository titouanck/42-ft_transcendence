# FUNCTIONS ****************************************************************** #

def needed_length(input_tuple):
	longest_item = ""
	max_length = 0
	for item in input_tuple:
		if len(str(item)) > max_length:
			longest_item = item
			max_length = len(str(item))
	return max_length

# CRUD *********************************************************************** #

CREATE = 1
READ = 2
UPDATE = 4
DELETE = 8

# PLAYER_RANKS *************************************************************** #

UNRANKED = 'UNRANKED'
BRONZE = 'BRONZE'
SILVER = 'SILVER'
GOLD = 'GOLD'
PLATINIUM = 'PLATINIUM'
DIAMOND = 'DIAMOND'
ELITE = 'ELITE'
CHAMPION = 'CHAMPION'
UNREAL = 'UNREAL'

PLAYER_RANKS_DEFAULT = UNRANKED
PLAYER_RANKS = (
	(UNRANKED, UNRANKED),
	(BRONZE, BRONZE),
	(SILVER, SILVER),
	(GOLD, GOLD),
	(PLATINIUM, PLATINIUM),
	(DIAMOND, DIAMOND),
	(ELITE, ELITE),
	(CHAMPION, CHAMPION),
	(UNREAL, UNREAL)
)

# PLAYER_STATUS ************************************************************** #

OFFLINE = 'Offline'
ONLINE = 'Online'
PLAYING = 'Playing'

PLAYER_STATUS_DEFAULT = OFFLINE
PLAYER_STATUS = (
	(OFFLINE, OFFLINE),
	(ONLINE, ONLINE),
	(PLAYING, PLAYING)
)

# MATCH_STATUS *************************************************************** #

PENDING = 'Pending'
SCHEDULED = 'Scheduled'
IN_PROGRESS = 'In progress'
COMPLETED = 'Completed'
ABANDONED = 'Abandoned'

MATCH_STATUS_DEFAULT = PENDING
MATCH_STATUS = (
	(PENDING, PENDING),
	(SCHEDULED, SCHEDULED),
	(IN_PROGRESS, IN_PROGRESS),
	(COMPLETED, COMPLETED),
	(ABANDONED, ABANDONED),
)

# MATCH_TYPE ***************************************************************** #

RANKED = 'Ranked'
CASUAL = 'Casual'
TOURNAMENT = 'Tournament'

MATCH_TYPE_DEFAULT = RANKED
MATCH_TYPE = (
	(RANKED, RANKED),
	(CASUAL, CASUAL),
	(TOURNAMENT, TOURNAMENT),
)
