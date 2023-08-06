from typing import Dict, Sequence, Optional, Any, TYPE_CHECKING, Optional
from datetime import datetime
from .. import GameMode, MembershipType, Raid
from .. import HashError

__all__: Sequence[str] = (
	'Activity',
)

class Activity:
	__slots__: Sequence[str] = (
		'_response', 'is_completed', 'mode', 'kills',
		'deaths', 'assists', 'kd', 'duration', 'player_count',
		'when', 'member_type', 'hash', 'image'
	)
	is_completed: str
	hash: int # Only for raids since we're not going to store everysingle other activity.
	mode: GameMode
	kills: int
	deaths: int
	when: Optional[datetime]
	assists: int
	duration: Optional[str]
	player_count: int
	image: str
	member_type: MembershipType

	def __init__(self, *, data: Dict[str, Any]) -> None:
		self._response = data.get('Response', None)
		self._update(self._response)

	def _update(self, data: Dict[str, Any]):
		self._response = data.get('activities')
		for i in self._response:
			self.when = i['period']
			self.mode = i['activityDetails'].get('mode')
			if self.mode == GameMode.RAID:
				self.hash = Raid(raid=i['activityDetails'].get('referenceId'))
				self.mode = 'Raid'
			self.is_completed = i[
				'values'
				].get(
					'completed'
					).get(
						'basic'
						)['displayValue']
			self.kills = i[
				'values'
				].get(
					'kills'
					).get(
						'basic'
						)['displayValue']
			self.assists = i[
				'values'
				].get(
					'assists'
					).get(
						'basic'
						)['displayValue']
			self.player_count = i[
				'values'
				].get(
					'playerCount'
					).get(
						'basic'
						)['displayValue']
			self.deaths = i[
				'values'
				].get(
					'deaths'
					).get(
						'basic'
						)['displayValue']
			self.duration = i[
				'values'
				].get(
					'activityDurationSeconds'
					).get(
						'basic'
						)['displayValue']
			self.member_type = i[
				'activityDetails'
				].get('mode')
			self.kd = i[
				'values'
				].get(
					'killsDeathsRatio'
					).get(
						'basic'
						)['displayValue']

	@property
	def raw_hash(self) -> int:
		'''Returns an int of the actual activity hash'''
		for i in self._response:
			return i['activityDetails'].get('referenceId')