"""This module provide methods to work with areas records entity"""
from datetime import datetime

from mindsight_people_control_api.helpers.models import (
    ApiEndpoint,
    ApiPaginationResponse,
)
from mindsight_people_control_api.settings import (
    API_ENDPOINT_AREAS_RECORDS,
    DATETIME_FORMAT,
)


class AreaRecords(ApiEndpoint):
    """This class abstract the areas records endpoint methods
    Reference: https://controle.mindsight.com.br/stone/api/v1/docs/#tag/Registros-de-area
    """

    def __init__(self) -> None:
        super().__init__(API_ENDPOINT_AREAS_RECORDS)

    def get_list_area_records(
        self,
        area: str = None,
        code: str = None,
        created__gt: datetime = None,
        created__lt: datetime = None,
        modified__gt: datetime = None,
        modified__lt: datetime = None,
        search: str = None,
    ) -> ApiPaginationResponse:
        """Get areas data
        Reference:
            https://controle.mindsight.com.br/stone/api/v1/docs/#tag/Registros-de-area/operation/listAreaRecords

        Args:
            area (str, Optional): Area name
            code (str, Optional): Code of area
            created__gt (datetime, Optional): Datetime to apply filter ">=" on created dates.
                Format "%Y-%m-%d %H:%M:%S"
            created__lt (datetime, Optional): Datetime to apply filter "<=" on created dates.
                Format "%Y-%m-%d %H:%M:%S"
            modified__gt (datetime, Optional): Datetime to apply filter ">=" on modified dates.
                Format "%Y-%m-%d %H:%M:%S"
            modified__lt (datetime, Optional): Datetime to apply filter "<=" on modified dates.
                Format "%Y-%m-%d %H:%M:%S"
            search: search
        """

        path = ""
        parameters = {
            "area": area,
            "code": code,
            "created__gt": created__gt.strftime(DATETIME_FORMAT)
            if created__gt
            else None,
            "created__lt": created__lt.strftime(DATETIME_FORMAT)
            if created__lt
            else None,
            "modified__gt": modified__gt.strftime(DATETIME_FORMAT)
            if modified__gt
            else None,
            "modified__lt": modified__lt.strftime(DATETIME_FORMAT)
            if modified__lt
            else None,
            "search": search,
            "page_size": self.page_size,
        }
        return ApiPaginationResponse(
            **self._base_requests.get(path=path, parameters=parameters),
            headers=self._base_requests.headers,
        )

    def get_retrieve_area_record(
        self,
        _id: int,
        area: str = None,
        code: str = None,
        created__gt: datetime = None,
        created__lt: datetime = None,
        modified__gt: datetime = None,
        modified__lt: datetime = None,
        search: str = None,
    ) -> dict:
        """Get retrieve area
        Reference:
            https://controle.mindsight.com.br/stone/api/v1/docs/#tag/Registros-de-area/operation/retrieveAreaRecord

        Args:
            _id (int, Mandatory): A unique integer value identifying this record of area.
            area (str, Optional): Area name
            code (str, Optional): Code of area
            created__gt (datetime, Optional): Datetime to apply filter ">=" on created dates.
                Format "%Y-%m-%d %H:%M:%S"
            created__lt (datetime, Optional): Datetime to apply filter "<=" on created dates.
                Format "%Y-%m-%d %H:%M:%S"
            modified__gt (datetime, Optional): Datetime to apply filter ">=" on modified dates.
                Format "%Y-%m-%d %H:%M:%S"
            modified__lt (datetime, Optional): Datetime to apply filter "<=" on modified dates.
                Format "%Y-%m-%d %H:%M:%S"
            search (str, Optional): search
        """
        path = f"/{_id}"

        parameters = {
            "area": area,
            "code": code,
            "created__gt": created__gt.strftime(DATETIME_FORMAT)
            if created__gt
            else None,
            "created__lt": created__lt.strftime(DATETIME_FORMAT)
            if created__lt
            else None,
            "modified__gt": modified__gt.strftime(DATETIME_FORMAT)
            if modified__gt
            else None,
            "modified__lt": modified__lt.strftime(DATETIME_FORMAT)
            if modified__lt
            else None,
            "search": search,
        }
        return self._base_requests.get(
            path=path,
            parameters=parameters,
        )
