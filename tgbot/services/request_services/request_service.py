import datetime

from dateutil.relativedelta import relativedelta

from tgbot.services.utils import with_session


class RequestService:

    @classmethod
    @with_session
    async def aggregate_by_month(cls, dt_from: datetime, dt_upto: datetime, session):
        pipeline = [
            {"$match": {"dt": {"$gte": dt_from, "$lte": dt_upto}}},
            {"$group": {
                "_id": {"$dateToString": {"format": "%Y-%m-01T00:00:00", "date": "$dt"}},
                "total_value": {"$sum": "$value"}
            }},
            {"$sort": {"_id": 1}}
        ]
        result = await session.aggregate(pipeline).to_list(length=None)
        all_dates = [dt_from + relativedelta(months=i) for i in
                     range((dt_upto.year - dt_from.year) * 12 + dt_upto.month - dt_from.month + 1)]
        date_value_map = {doc['_id']: doc['total_value'] for doc in result}

        dataset = [date_value_map.get(dt.strftime("%Y-%m-%dT%H:%M:%S"), 0) for dt in all_dates]
        labels = [dt.strftime("%Y-%m-%dT%H:%M:%S") for dt in all_dates]
        return {"dataset": dataset, "labels": labels}

    @classmethod
    @with_session
    async def aggregate_by_day(cls, dt_from: datetime, dt_upto: datetime, session):
        pipeline = [
            {"$match": {"dt": {"$gte": dt_from, "$lte": dt_upto}}},
            {"$group": {
                "_id": {"$dateToString": {"format": "%Y-%m-%dT00:00:00", "date": "$dt"}},
                "total_value": {"$sum": "$value"}
            }},
            {"$sort": {"_id": 1}}
        ]

        result = await session.aggregate(pipeline).to_list(length=None)

        all_dates = [dt_from + datetime.timedelta(days=i) for i in range((dt_upto - dt_from).days + 1)]
        date_value_map = {doc['_id']: doc['total_value'] for doc in result}

        dataset = [date_value_map.get(dt.strftime("%Y-%m-%dT%H:%M:%S"), 0) for dt in all_dates]
        labels = [dt.strftime("%Y-%m-%dT%H:%M:%S") for dt in all_dates]

        return {"dataset": dataset, "labels": labels}

    @classmethod
    @with_session
    async def aggregate_by_hour(cls, dt_from: datetime, dt_upto: datetime, session):
        pipeline = [
            {"$match": {"dt": {"$gte": dt_from, "$lte": dt_upto}}},
            {"$group": {
                "_id": {"$dateToString": {"format": "%Y-%m-%dT%H:00:00", "date": "$dt"}},
                "total_value": {"$sum": "$value"}
            }},
            {"$sort": {"_id": 1}}
        ]

        result = await session.aggregate(pipeline).to_list(length=None)

        all_dates = [dt_from + datetime.timedelta(hours=i) for i in
                     range(int((dt_upto - dt_from).total_seconds() / 3600) + 1)]
        date_value_map = {doc['_id']: doc['total_value'] for doc in result}

        dataset = [date_value_map.get(dt.strftime("%Y-%m-%dT%H:00:00"), 0) for dt in all_dates]
        labels = [dt.strftime("%Y-%m-%dT%H:00:00") for dt in all_dates]

        return {"dataset": dataset, "labels": labels}
