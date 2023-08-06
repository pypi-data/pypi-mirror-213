"""Handler for upgrading the blue upgrades"""
from typing import Any

from ... import helper, user_input_handler
from . import upgrade_cats

TYPES = [
    "냥코 대포 공격력",
    "냥코 대포 사정거리",
    "냥코 대포 충전",
    "일 고양이의 의 호율",
    "일 고양이의 의 지갑",
    "성 체력",
    "연구력",
    "회계력",
    "공부력",
    "통솔력",
]


def upgrade_blue_ids(save_stats: dict[str, Any], ids: list[int]) -> dict[str, Any]:
    """Upgrade blue upgrades for a set of ids"""

    save_stats["blue_upgrades"] = upgrade_cats.upgrade_handler(
        data=save_stats["blue_upgrades"],
        ids=ids,
        item_name="업그레이드",
        save_stats=save_stats,
    )
    save_stats = upgrade_cats.set_user_popups(save_stats)
    print("특수 기술을 성공적으로 설정")
    return save_stats


def upgrade_blue(save_stats: dict[str, Any]) -> dict[str, Any]:
    """Handler for editing blue upgrades"""

    levels = save_stats["blue_upgrades"]
    levels_removed = {
        "Base": [levels["Base"][0]] + levels["Base"][2:],
        "Plus": [levels["Plus"][0]] + levels["Plus"][2:],
    }

    levels_removed_formated: list[str] = []
    for base, plus in zip(levels_removed["Base"], levels_removed["Plus"]):
        levels_removed_formated.append(f"{base + 1}+{plus}")

    print("무엇을 업그레이드하고 싶습니까?:\n⚠️1만이상숫자넣지마십시요")
    helper.colored_list(TYPES, extra_data=levels_removed_formated)

    total = len(TYPES) + 1
    ids = user_input_handler.colored_input(
        f"{total}. &한 번에&\n1부터 숫자를 입력하세요.{total} (공백으로 구분된 여러 값을 입력하여 한 번에 여러 값을 편집할 수 있습니다.):"
    ).split(" ")
    ids = user_input_handler.create_all_list_not_inc(ids, 11)
    ids = helper.parse_int_list(ids, -1)
    new_ids: list[int] = []
    for blue_id in ids:
        if blue_id > 0:
            blue_id += 1
        new_ids.append(blue_id)
    ids = new_ids
    save_stats = upgrade_blue_ids(save_stats, ids)
    return save_stats
