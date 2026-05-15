import datetime

from pydantic import RootModel

from app.schemas import TaskTuple, MeetTuple

DayContentList = list[MeetTuple | TaskTuple]


class DayScheduleSchema(RootModel[dict[datetime.date, DayContentList]]): ...


CalendarSchema = list[DayScheduleSchema]
