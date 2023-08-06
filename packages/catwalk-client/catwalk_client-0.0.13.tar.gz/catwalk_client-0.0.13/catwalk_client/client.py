from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from json import loads

from catwalk_common import CommonCaseFormat
from pydantic import error_wrappers

from catwalk_client.tools import CaseBuilder, CaseExporter, CaseExporterV2, SORT_ORDER
from catwalk_client.common import CatwalkHTTPClient
from catwalk_client.common.constants import CATWALK_CLIENT_THREAD_NAME_PREFIX
from catwalk_client.common.logger import init_logger


log = init_logger(__name__)


class CatwalkClient:
    def __init__(
        self,
        submitter_name: str = None,
        submitter_version: str = None,
        catwalk_url: str = None,
        auth_token: str = None,
        insecure: bool = True,
        timeout: int = 30,
        timezone: str = "UTC",
        concurrent: bool = False,
        max_workers: int = 4,
    ):
        self.http_client = CatwalkHTTPClient(
            catwalk_url, auth_token, insecure, timeout, timezone
        )
        self.submitter_name = submitter_name
        self.submitter_version = submitter_version
        self._max_workers = max_workers
        self._concurrent = concurrent

        if self._concurrent:
            self._executor = ThreadPoolExecutor(
                max_workers=self._max_workers,
                thread_name_prefix=CATWALK_CLIENT_THREAD_NAME_PREFIX,
            )
        else:
            self._executor = None

    def __setattr__(self, __name, __value):
        if __name != "http_client" and __name in self.http_client.__dict__.keys():
            log.warn(
                f" [DEPRECATED] Usage of 'CatwalkClient.{__name}=<value>' is DEPRECATED. Please use 'set_{__name}' method!"
            )
            self.http_client.__dict__[__name] = __value

        self.__dict__[__name] = __value

    def set_auth_token(self, auth_token: str):
        self.http_client.auth_token = auth_token

    def set_catwalk_url(self, catwalk_url: str):
        self.http_client.url = catwalk_url

    def set_insecure(self, insecure: bool):
        self.http_client.insecure = insecure

    def new_case(self) -> CaseBuilder:
        return CaseBuilder(client=self)

    def send(self, case: dict):
        if self._concurrent and self._executor:
            self._executor.submit(self._send, case)
        else:
            self._send(case)

    def _send(self, case: dict):
        try:
            case: CommonCaseFormat = CommonCaseFormat(
                submitter={
                    "name": self.submitter_name,
                    "version": self.submitter_version,
                },
                **case,
            )

            response, success = self.http_client.post("/api/cases/collect", case.dict())

            if success:
                case_id = loads(response)["id"]
                log.info(f" Collected catwalk case: {case_id}")
            else:
                log.error(response)
        except error_wrappers.ValidationError as ex:
            log.error(f" ValidationError: \n{ex}")
        except Exception as ex:
            log.error(f" {type(ex).__name__}: \n{str(ex)}\n{ex.__traceback__}")

    def export_cases(
        self,
        from_datetime: datetime,
        to_datetime: datetime,
        submitter_name: str | None = None,
        submitter_version: str | None = None,
        max_retries: int = 5,
        limit: int | None = None,
    ):
        exporter = CaseExporter(
            http_client=self.http_client,
            from_datetime=from_datetime,
            to_datetime=to_datetime,
            submitter_name=submitter_name or self.submitter_name,
            submitter_version=submitter_version or self.submitter_version,
            max_retries=max_retries,
            limit=limit,
        )
        yield from exporter.export()

    def export_cases_v2(
        self,
        submitter_name: str | None = None,
        submitter_version: str | None = None,
        datetime_from: datetime | None = None,
        datetime_to: datetime = datetime.now(),
        sort_by: list[str] | str | None = None,
        sort_order: list[SORT_ORDER] | SORT_ORDER = "desc",
        limit: int = 100,
        offset: int = 0,
        max_retries: int = 5,
    ):
        """Export cases using the v2 export endpoint.

        Args:
            submitter_name (Optional[str], optional): Name of submitter to export. Defaults to None.
            submitter_version (Optional[str], optional): Version of submitter to export. Defaults to None.
            datetime_from (Optional[datetime], optional): Lower boundary of case creation date. Defaults to None.
            datetime_to (datetime, optional): Upper boundary of case creation date. Defaults to current time.
            sort_by (Union[list[str], str, None], optional): Field(s) by which exported cases will be ordered. Defaults to None.
            sort_order (Union[list[SORT_ORDER], SORT_ORDER], optional): Order(s) by which exported cases will be ordered. Defaults to "desc".
            limit (int, optional): Size limit of a single batch fetched from the API (not overall limit).
                                   Defaults to 100. Max is 1000, if the limit is higher than 1000 the API will return an error.
            offset (int, optional): Starting offset of fetched data. Defaults to 0.
            max_retries (int, optional): Maximum number of retries in case the request does not succeed. Defaults to 5.

        Yields:
            OpenCase: Cases returned by the API.
        """
        exporter = CaseExporterV2(
            http_client=self.http_client,
            submitter_name=submitter_name or self.submitter_name,
            submitter_version=submitter_version or self.submitter_version,
            datetime_from=datetime_from,
            datetime_to=datetime_to,
            sort_by=sort_by,
            sort_order=sort_order,
            limit=limit,
            offset=offset,
            max_retries=max_retries,
        )
        yield from exporter.export()
