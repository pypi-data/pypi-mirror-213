"""Handler for editing tower stages"""
from typing import Any

from . import event_stages
from ... import user_input_handler

def edit_tower(save_stats: dict[str, Any]) -> dict[str, Any]:
    """Handler for editing tower stages"""

    stage_data = save_stats["tower"]["progress"]
    stage_data = {
        "Value": stage_data,
        "Lengths": {"stars": stage_data["stars"], "stages": stage_data["stages"]},
    }

    ids = []
    ids = user_input_handler.get_range(
        user_input_handler.colored_input(
            "타워 ID를 입력합니다(&이벤트 출시 순서 전투 고양이&를 찾아 &이벤트& 및 &장갑?&을 지나 스크롤하여 &타워& ID를 찾습니다)(&all&을 입력하여 범위(예: &1&-&49&, 또는 공백으로 구분된 ID(예: &5 4 7&)): "
        ),
        stage_data["Value"]["total"],
    )
    save_stats["tower"]["progress"] = event_stages.stage_handler(
        stage_data, ids, 0, False
    )["Value"]
    save_stats["tower"]["progress"]["total"] = stage_data["Value"]["total"]
    save_stats["tower"]["progress"]["stars"] = stage_data["Lengths"]["stars"]
    save_stats["tower"]["progress"]["stages"] = stage_data["Lengths"]["stages"]

    return save_stats
