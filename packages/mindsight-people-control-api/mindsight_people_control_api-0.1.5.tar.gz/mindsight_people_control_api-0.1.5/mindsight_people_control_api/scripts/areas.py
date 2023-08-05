"""This module provide methods to work with areas entity"""

from datetime import date, datetime

from mindsight_people_control_api.helpers.models import (
    ApiEndpoint,
    ApiPaginationResponse,
)
from mindsight_people_control_api.settings import (
    API_ENDPOINT_AREAS,
    DATE_FORMAT,
    DATETIME_FORMAT,
)


class Areas(ApiEndpoint):
    """This class abstract the areas endpoint methods
    Reference: https://controle.mindsight.com.br/stone/api/v1/docs/#tag/Areas
    """

    def __init__(self) -> None:
        super().__init__(API_ENDPOINT_AREAS)

    def get_list_areas(
        self,
        name: str = None,
        code: str = None,
        created__gt: datetime = None,
        created__lt: datetime = None,
        modified__gt: datetime = None,
        modified__lt: datetime = None,
        active: str = None,
        search: str = None,
    ) -> ApiPaginationResponse:
        """Get areas data
        Reference: https://controle.mindsight.com.br/stone/api/v1/docs/#operation/listAreas

        Args:
            name (str, Optional): area_name
            code (str, Optional): Code of area
            created__gt (datetime, Optional): Datetime to apply filter ">=" on created dates.
                Format "%Y-%m-%d %H:%M:%S"
            created__lt (datetime, Optional): Datetime to apply filter "<=" on created dates.
                Format "%Y-%m-%d %H:%M:%S"
            modified__gt (datetime, Optional): Datetime to apply filter ">=" on modified dates.
                Format "%Y-%m-%d %H:%M:%S"
            modified__lt (datetime, Optional): Datetime to apply filter "<=" on modified dates.
                Format "%Y-%m-%d %H:%M:%S"
            active (str, Optional): is_active: Flag to get areas by status
            search: search
            }
        """

        path = ""
        parameters = {
            "name": name,
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
            "active": active,
            "search": search,
            "page_size": self.page_size,
        }
        return ApiPaginationResponse(
            **self._base_requests.get(path=path, parameters=parameters),
            headers=self._base_requests.headers,
        )

    def get_retrieve_area(
        self,
        _id: int,
        name: str = None,
        code: str = None,
        created__gt: datetime = None,
        created__lt: datetime = None,
        modified__gt: datetime = None,
        modified__lt: datetime = None,
        active: str = None,
        search: str = None,
    ) -> dict:
        """Get retrieve area
        Reference:
            https://controle.mindsight.com.br/stone/api/v1/docs/#tag/Areas/operation/retrieveArea

        Args:
            _id (int, Mandatory): Id of area to retrieve
            name (str, Optional): Name of area
            code (str, Optional): Code of area
            created__gt (datetime, Optional): Datetime to apply filter ">=" on created dates.
                Format "%Y-%m-%d %H:%M:%S"
            created__lt (datetime, Optional): Datetime to apply filter "<=" on created dates.
                Format "%Y-%m-%d %H:%M:%S"
            modified__gt (datetime, Optional): Datetime to apply filter ">=" on modified dates.
                Format "%Y-%m-%d %H:%M:%S"
            modified__lt (datetime, Optional): Datetime to apply filter "<=" on modified dates.
                Format "%Y-%m-%d %H:%M:%S"
            active (str, Optional): is_active: Flag to get areas by status
            search (str, Optional): search
        """
        path = f"/{_id}"

        parameters = {
            "name": name,
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
            "active": active,
            "search": search,
        }
        return self._base_requests.get(
            path=path,
            parameters=parameters,
        )

    def post_create_area(
        self,
        code: str,
        name: str,
        start_date: date,
        parent_area: int = None,
    ):
        """Create new area
        Reference:
            https://controle.mindsight.com.br/stone/api/v1/docs/#tag/Areas/operation/createCompleteArea

        Args:
            code (str, Mandatory): Code of area
            name (str, Mandatory): Name of area
            start_date (date, Mandatory): Area start date
            parent_area (int, Optional): Parent area id
        """
        path = "/create_complete"
        data = {
            "code": code,
            "name": name,
            "start_date": start_date.strftime(DATE_FORMAT),
            "parent_area": parent_area,
        }

        return self._base_requests.post(path=path, data=data)

    def patch_edit_area(
        self,
        _id: int,
        code: str = None,
        name: str = None,
        start_date: date = None,
        end_date: date = None,
    ) -> dict:
        """Edit area and last area record
        Reference:
            https://controle.mindsight.com.br/stone/api/v1/docs/#tag/Areas/operation/editAreaAndRecordArea

        Args:
            _id (int, Mandatory): Area id
            code (str, Optional): Code of area
            name (str, Optional): Name of area
            start_date (date, Optional): Area start date
            end_date (date, Optional): Area end date
        """
        path = f"/{_id}/edit_area_and_record"
        data = {
            "code": code,
            "name": name,
            "start_date": start_date.strftime(DATE_FORMAT) if start_date else None,
            "end_date": end_date.strftime(DATE_FORMAT) if end_date else None,
        }
        return self._base_requests.patch(path=path, data=data)

    def patch_edit_parent_area(
        self,
        _id: int,
        parent_id: int,
        start_date: date,
        end_date: date = None,
    ) -> dict:
        """Edit parent area
        Reference:
            https://controle.mindsight.com.br/stone/api/v1/docs/#tag/Areas/operation/editParentArea

        Args:
            _id (int, Mandatory): Area id
            parent_id (int, Mandatory): id of parent area
            start_date (date, Mandatory): Parent area assignment start date
            end_date (date, Optional): Parent area assignment end date
        """
        path = f"/{_id}/edit_parent"
        data = {
            "parent_id": parent_id,
            "start_date": start_date.strftime(DATE_FORMAT) if start_date else None,
            "end_date": end_date.strftime(DATE_FORMAT) if start_date else None,
        }
        return self._base_requests.patch(path=path, data=data)
