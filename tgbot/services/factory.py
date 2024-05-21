from tgbot.services.request_services.request_service import RequestService


class DataAggregator:
    _map = {
        'month': RequestService.aggregate_by_month,
        'day': RequestService.aggregate_by_day,
        'hour': RequestService.aggregate_by_hour
    }

    @classmethod
    async def aggregate(cls, data):
        aggregation_func = cls._map[data.group_type]
        result = await aggregation_func(dt_from=data.dt_from, dt_upto=data.dt_upto)
        return result
