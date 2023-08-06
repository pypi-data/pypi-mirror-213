from __future__ import annotations

from typing import Any


class CaseBuilder:
    def __init__(self, client):
        self._client = client
        self._case_id = ""
        self._query: list[dict] = []
        self._context: list[dict] = []
        self._response: list[dict] = []
        self._metadata: dict = {}

    def set_case_id(self, case_id: str):
        self._case_id = case_id
        return self

    def add_query(self, name: str, value: Any, type: str | dict):
        self._query.append({"name": name, "value": value, "type": type})
        return self

    def add_context(self, name: str, value: Any, type: str | dict):
        self._context.append({"name": name, "value": value, "type": type})
        return self

    def add_response(
        self,
        name: str,
        value: Any,
        type: str | dict,
        evaluation: list[dict] | None = None,
    ):
        self._response.append(
            {"name": name, "value": value, "type": type, "evaluation": evaluation or []}
        )
        return self

    def add_evaluation(self, question: str, name: str, **kwargs):
        self._response[-1]["evaluation"].append(
            {"question": question, "name": name, **kwargs}
        )
        return self

    def set_metadata(self, **kwargs):
        self._metadata = kwargs
        return self

    def send(self):
        self._client.send(
            {
                "case_id": self._case_id,
                "query": self._query,
                "context": self._context,
                "response": self._response,
                "metadata": self._metadata,
            }
        )
