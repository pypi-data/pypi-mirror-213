from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="ScanIssueInc")


@attr.s(auto_attribs=True)
class ScanIssueInc:
    """
    Attributes:
        issues_found (int):
    """

    issues_found: int
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        issues_found = self.issues_found

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "issues_found": issues_found,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        issues_found = d.pop("issues_found")

        scan_issue_inc = cls(
            issues_found=issues_found,
        )

        scan_issue_inc.additional_properties = d
        return scan_issue_inc

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
