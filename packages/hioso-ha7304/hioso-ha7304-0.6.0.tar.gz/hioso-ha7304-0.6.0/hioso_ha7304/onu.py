import attr
from typing import Optional, List, Literal

CtcStatus = Literal[
    "--", "MpcpDiscovery", "MpcpSla", "CtcInfo", "RequestCfg", "CtcNegDone"
]
OfflineReason = Literal[
    "Dying_gasp",
    "Other",
    "TIMEOUT",
    "ONU-init",
    "OLT-init",
    "RejectByBlackList",
    "RejectByWhiteList",
]

AuthStatus = Literal["Activate", "Deactivate"]

CTC_STATUS: List[CtcStatus] = [
    "--",
    "MpcpDiscovery",
    "MpcpSla",
    "CtcInfo",
    "RequestCfg",
    "CtcNegDone",
]
OFFLINE_REASON: List[OfflineReason] = [
    "Other",
    "TIMEOUT",
    "ONU-init",
    "OLT-init",
    "RejectByBlackList",
    "RejectByWhiteList",
]


@attr.dataclass(slots=True)
class Onu:
    id: str
    name: str
    mac_address: str
    status: str
    fw_version: str
    chip_id: str
    ports: int
    rtt: int
    ctc_status: CtcStatus
    ctc_ver: int
    activate: AuthStatus
    temperature: Optional[float]
    tx_power: Optional[float]
    rx_power: Optional[float]
    online_time: str
    offline_time: str
    offline_reason: OfflineReason
    online: int
    deregister_cnt: int
    distance: float = 0

    def __str__(self) -> str:
        return f"{self.id} - {self.name}"

    def __attrs_post_init__(self) -> None:
        distance = self.rtt * 1.6393 - 157
        if distance > 157:
            self.distance = distance - 157.0
        else:
            self.distance = 0

    @classmethod
    def from_all_onu_data(cls, data: str) -> "Onu":
        d = data.split("','")
        off_reason_ = int((d[18]))
        off_reason: OfflineReason
        if off_reason_ == 1:
            off_reason = "Dying_gasp"
        elif off_reason_ < 6:
            off_reason = OFFLINE_REASON[off_reason_]
        else:
            off_reason = OFFLINE_REASON[0]
        return cls(
            id=d[0].lstrip("'"),
            name=d[1],
            mac_address=d[2],
            status=d[3],
            fw_version=d[4],
            chip_id=d[5],
            ports=int(d[6]),
            rtt=int(d[10]),
            ctc_status=CTC_STATUS[int(d[7])],
            ctc_ver=int(d[8]),
            activate="Deactivate" if int(d[9]) == 2 else "Activate",
            temperature=None if d[11] == "--" else float(d[11]),
            tx_power=None if d[14] == "--" else float(d[14]),
            rx_power=None if d[15] == "--" else float(d[15]),
            online_time=d[16],
            offline_time=d[17],
            offline_reason=off_reason,
            online=int(d[19]),
            deregister_cnt=int(d[20]),
        )
