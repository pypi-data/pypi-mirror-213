import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.status_b4f_enum import StatusB4FEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.program import Program
    from ..models.task import Task


T = TypeVar("T", bound="ScanDetailedDetailed")


@attr.s(auto_attribs=True)
class ScanDetailedDetailed:
    """
    Attributes:
        id (int):
        program (Program): Adds nested create feature
        task_ongoing_or_failed (List['Task']):
        task_not_finished_count (int):
        task_success_count (int):
        task_all_count (int):
        name (str):
        status (StatusB4FEnum): * `0` - Just Added - Will be Scheduled Soon
            * `1` - Scheduled/Started Enum Phase
            * `2` - Preparing data for HTTPX
            * `3` - Ready for HTTPX
            * `4` - HTTPX Started/Ongoing
            * `5` - Preparing data for Nuclei
            * `6` - Ready for Nuclei
            * `7` - Nuclei Started
            * `8` - Scan Finished
        issues_found (Union[Unset, None, int]):
        comment (Union[Unset, None, str]):
        created_at (Optional[datetime.datetime]):
        updated_at (Optional[datetime.datetime]):
        reason (Union[Unset, None, str]):
        s_type (Union[Unset, None, str]):
        n_type (Union[Unset, None, str]):
    """

    id: int
    program: "Program"
    task_ongoing_or_failed: List["Task"]
    task_not_finished_count: int
    task_success_count: int
    task_all_count: int
    name: str
    status: StatusB4FEnum
    created_at: Optional[datetime.datetime]
    updated_at: Optional[datetime.datetime]
    issues_found: Union[Unset, None, int] = UNSET
    comment: Union[Unset, None, str] = UNSET
    reason: Union[Unset, None, str] = UNSET
    s_type: Union[Unset, None, str] = UNSET
    n_type: Union[Unset, None, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        program = self.program.to_dict()

        task_ongoing_or_failed = []
        for task_ongoing_or_failed_item_data in self.task_ongoing_or_failed:
            task_ongoing_or_failed_item = task_ongoing_or_failed_item_data.to_dict()

            task_ongoing_or_failed.append(task_ongoing_or_failed_item)

        task_not_finished_count = self.task_not_finished_count
        task_success_count = self.task_success_count
        task_all_count = self.task_all_count
        name = self.name
        status = self.status.value

        issues_found = self.issues_found
        comment = self.comment
        created_at = self.created_at.isoformat() if self.created_at else None

        updated_at = self.updated_at.isoformat() if self.updated_at else None

        reason = self.reason
        s_type = self.s_type
        n_type = self.n_type

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "program": program,
                "task_ongoing_or_failed": task_ongoing_or_failed,
                "task_not_finished_count": task_not_finished_count,
                "task_success_count": task_success_count,
                "task_all_count": task_all_count,
                "name": name,
                "status": status,
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )
        if issues_found is not UNSET:
            field_dict["issues_found"] = issues_found
        if comment is not UNSET:
            field_dict["comment"] = comment
        if reason is not UNSET:
            field_dict["reason"] = reason
        if s_type is not UNSET:
            field_dict["s_type"] = s_type
        if n_type is not UNSET:
            field_dict["n_type"] = n_type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.program import Program
        from ..models.task import Task

        d = src_dict.copy()
        id = d.pop("id")

        program = Program.from_dict(d.pop("program"))

        task_ongoing_or_failed = []
        _task_ongoing_or_failed = d.pop("task_ongoing_or_failed")
        for task_ongoing_or_failed_item_data in _task_ongoing_or_failed:
            task_ongoing_or_failed_item = Task.from_dict(task_ongoing_or_failed_item_data)

            task_ongoing_or_failed.append(task_ongoing_or_failed_item)

        task_not_finished_count = d.pop("task_not_finished_count")

        task_success_count = d.pop("task_success_count")

        task_all_count = d.pop("task_all_count")

        name = d.pop("name")

        status = StatusB4FEnum(d.pop("status"))

        issues_found = d.pop("issues_found", UNSET)

        comment = d.pop("comment", UNSET)

        _created_at = d.pop("created_at")
        created_at: Optional[datetime.datetime]
        if _created_at is None:
            created_at = None
        else:
            created_at = isoparse(_created_at)

        _updated_at = d.pop("updated_at")
        updated_at: Optional[datetime.datetime]
        if _updated_at is None:
            updated_at = None
        else:
            updated_at = isoparse(_updated_at)

        reason = d.pop("reason", UNSET)

        s_type = d.pop("s_type", UNSET)

        n_type = d.pop("n_type", UNSET)

        scan_detailed_detailed = cls(
            id=id,
            program=program,
            task_ongoing_or_failed=task_ongoing_or_failed,
            task_not_finished_count=task_not_finished_count,
            task_success_count=task_success_count,
            task_all_count=task_all_count,
            name=name,
            status=status,
            issues_found=issues_found,
            comment=comment,
            created_at=created_at,
            updated_at=updated_at,
            reason=reason,
            s_type=s_type,
            n_type=n_type,
        )

        scan_detailed_detailed.additional_properties = d
        return scan_detailed_detailed

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
