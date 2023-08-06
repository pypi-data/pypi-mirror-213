from __future__ import annotations

from typing import Union
from collections.abc import Sequence
from enum import Enum
from dataclasses import dataclass, replace

import shapely.geometry as geometry
import numpy as np

from dna import Point
from dna.event import TrackEvent
from dna.utils import utc2datetime


@dataclass(frozen=True)
class LineTrack:
    track_id: str
    line: geometry.LineString
    frame_index: int
    ts: float
    source: TrackEvent
    
    def is_point_track(self) -> bool:
        return self.line.coords[0] == self.line.coords[1]
    
    @property
    def begin_point(self) -> Tuple:
        return self.line.coords[0]
    
    @property
    def end_point(self) -> Tuple:
        return self.line.coords[1]
        
    @staticmethod
    def from_events(t0:TrackEvent, t1:TrackEvent):
        def to_line_string(pt0:Point, pt1:Point) -> geometry.LineString:
            return geometry.LineString([list(pt0.xy), list(pt1.xy)])

        p0 = t0.location.center()
        p1 = t1.location.center()
        return LineTrack(track_id=t1.track_id, line=to_line_string(p0, p1), frame_index=t1.frame_index, ts=t1.ts, source=t1)
    
    def __repr__(self) -> str:
        def to_line_end_points(ls:geometry.LineString) -> tuple[Point,Point]:
            return tuple(Point(xy) for xy in ls.coords[:2])
        
        if self.line:
            start, end = to_line_end_points(self.line)
            return f'{self.track_id}: line={start}-{end}, frame={self.frame_index}]'
        else:
            return f'{self.track_id}: frame={self.frame_index}]'


class ZoneRelation(Enum):
    Unassigned = 0
    Entered = 1
    Left = 2
    Inside = 3
    Through = 4
    Deleted = 5
    
    @staticmethod
    def parseRelationStr(rel_str:str) -> tuple[ZoneRelation, str]:
        def parseZoneId(expr:str) -> str:
            return expr[2:-1]
            
        if rel_str[0] == 'U':
            return ZoneRelation.Unassigned, None
        elif rel_str[0] == 'E':
            return ZoneRelation.Entered, parseZoneId(rel_str)
        elif rel_str[0] == 'L':
            return ZoneRelation.Left, parseZoneId(rel_str)
        elif rel_str[0] == 'I':
            return ZoneRelation.Inside, parseZoneId(rel_str)
        elif rel_str[0] == 'T':
            return ZoneRelation.Through, parseZoneId(rel_str)
        elif rel_str[0] == 'D':
            return ZoneRelation.Deleted, parseZoneId(rel_str)


@dataclass(frozen=True)
class ZoneEvent:
    track_id: str
    relation: ZoneRelation
    zone_id: str
    frame_index: int
    ts: float
    source: TrackEvent

    def is_unassigned(self) -> bool:
        return self.relation == ZoneRelation.Unassigned
    def is_entered(self) -> bool:
        return self.relation == ZoneRelation.Entered
    def is_left(self) -> bool:
        return self.relation == ZoneRelation.Left
    def is_inside(self) -> bool:
        return self.relation == ZoneRelation.Inside
    def is_through(self) -> bool:
        return self.relation == ZoneRelation.Through
    def is_deleted(self) -> bool:
        return self.relation == ZoneRelation.Deleted

    @staticmethod
    def UNASSIGNED(line:LineTrack) -> ZoneEvent:
        return ZoneEvent(track_id=line.track_id, relation=ZoneRelation.Unassigned, zone_id=None,
                         frame_index=line.frame_index, ts=line.ts, source=line.source)
    
    def relation_str(self) -> str:
        if self.relation == ZoneRelation.Unassigned:
            return f'U'
        elif self.relation == ZoneRelation.Entered:
            return f'E({self.zone_id})'
        elif self.relation == ZoneRelation.Left:
            return f'L({self.zone_id})'
        elif self.relation == ZoneRelation.Through:
            return f'T({self.zone_id})'
        elif self.relation == ZoneRelation.Inside:
            return f'I({self.zone_id})'
        elif self.relation == ZoneRelation.Deleted:
            return 'D'
        else:
            raise ValueError(f'invalid zone_relation: {self.relation}')
    
    def __repr__(self) -> str:
        name = f'Zone{self.relation.name}'
        zone_str = f', zone={self.zone_id}' if self.zone_id else ''
        
        return f'{name}[track={self.track_id}{zone_str}, frame={self.frame_index}]'


@dataclass(frozen=True)
class LocationChanged:
    track_id: str
    zone_ids: set[str]
    frame_index: int
    ts: float


@dataclass(frozen=True)
class ResidentChanged:
    zone_id: str
    residents: set[int]
    frame_index: int
    ts: float


from datetime import timedelta
@dataclass
class ZoneVisit:
    zone_id: str
    enter_frame_index: int
    enter_ts: int
    leave_frame_index: int
    leave_ts: int
    
    @staticmethod
    def open(ev:ZoneEvent) -> ZoneVisit:
        return ZoneVisit(zone_id=ev.zone_id, enter_frame_index=ev.frame_index, enter_ts=ev.ts,
                          leave_frame_index=-1, leave_ts=-1)
        
    def is_open(self) -> bool:
        return self.leave_ts <= 0
        
    def is_closed(self) -> bool:
        return self.leave_ts > 0
    
    def close_at_event(self, zev:ZoneEvent) -> None:
        self.leave_frame_index = zev.frame_index
        self.leave_ts = zev.ts
    
    def close(self, frame_index:int, ts:float) -> None:
        self.leave_frame_index = frame_index
        self.leave_ts = ts
        
    def duplicate(self) -> ZoneVisit:
        return replace(self)
    
    def duration(self) -> timedelta:
        return timedelta(milliseconds=self.leave_ts - self.enter_ts) if self.is_closed() else None
    
    def __repr__(self) -> str:
        dur = self.duration()
        stay_str = f'{dur.seconds:.1f}s' if dur is not None else '?'
        leave_idx_str = self.leave_frame_index if self.leave_frame_index > 0 else '?'
        return f'{self.zone_id}[{self.enter_frame_index}-{leave_idx_str}:{stay_str}]'


class ZoneSequence:
    __slots__ = ( 'track_id', 'visits', '_first_frame_index', '_first_ts', '_frame_index', '_ts' )

    def __init__(self, track_id:str, visits:list[ZoneVisit]) -> None:
        self.track_id = track_id
        self.visits = visits
        self._first_frame_index = visits[0].enter_frame_index if visits else -1
        self._first_ts = visits[0].enter_ts if visits else -1
        self._frame_index = -2
        self._ts = -2

    @property
    def first_frame_index(self) -> int:
        return self._first_frame_index

    @property
    def first_ts(self) -> int:
        return self._first_ts

    @property
    def frame_index(self) -> int:
        if self._frame_index < -1:
            if self.visits:
                visit = self.visits[-1]
                self._frame_index = visit.leave_frame_index if visit.leave_frame_index >= 0 else visit.enter_frame_index
            else:
                self._frame_index = -1
        return self._frame_index

    @property
    def ts(self) -> int:
        if self._ts < -1:
            if self.visits:
                visit = self.visits[-1]
                return visit.leave_ts if visit.leave_ts >= 0 else visit.enter_ts
            else:
                return -1
        return self._ts
    
    def __getitem__(self, index) -> Union[ZoneVisit, ZoneSequence]:
        if isinstance(index, int):
            return self.visits[index]
        else:
            return ZoneSequence(track_id=self.track_id, visits=self.visits[index])
    
    def __len__(self) -> int:
        return len(self.visits)
    
    def __delitem__(self, idx) -> None:
        del self.visits[idx]
        
    def __iter__(self):
        return (visit for visit in self.visits)
        # class ZoneIter:
        #     def __init__(self, visits:list[ZoneVisit]) -> None:
        #         self.visits = visits
        #         self.index = 0
                
        #     def __next__(self):
        #         if self.index < len(self.visits):
        #             visit = self.visits[self.index]
        #             self.index += 1
        #             return visit
        #         else:
        #             raise StopIteration
        # return ZoneIter(self.visits)
    
    def append(self, visit:ZoneVisit) -> None:
        if self._first_frame_index < 0:
            self._first_frame_index = visit.enter_frame_index
        if self._first_ts < 0:
            self._first_ts = visit.enter_ts

        self.visits.append(visit)
        
    def remove(self, idx:int) -> None:
        self.visits.remove(idx)
        
    def duplicate(self) -> ZoneSequence:
        dup_visits = [visit.duplicate() for visit in self.visits]
        return ZoneSequence(track_id=self.track_id, visits=dup_visits)
    
    def sequence_str(self) -> str:
        seq_str = ''.join([visit.zone_id for visit in self.visits])
        return f'[{seq_str}]' if len(self.visits) == 0 or self[-1].is_closed() else f'[{seq_str})'

    def __repr__(self) -> str:
        return f'{self.track_id}:{self.sequence_str()}, frame={self.frame_index}'
    
    
