"""Handler for editing the ototo cat cannon"""
from typing import Any, Optional

from ... import user_input_handler, game_data_getter, csv_handler, helper


def get_canon_types(is_jp: bool) -> Optional[list[str]]:
    """Get the cannon types"""

    file_data = game_data_getter.get_file_latest(
        "resLocal", "CastleRecipeDescriptions.csv", is_jp
    )
    if file_data is None:
        helper.error_text("찾을 수 없습니다 CastleRecipeDescriptions.csv")
        return None
    data = csv_handler.parse_csv(
        file_data.decode("utf-8"),
        delimeter=helper.get_text_splitter(is_jp),
    )
    types: list[str] = []
    for cannon in data:
        types.append(cannon[1])
    return types


def get_cannon_maxes(is_jp: bool) -> Optional[dict[int, dict[int, int]]]:
    """Get the cannon maxes"""
    file_data = game_data_getter.get_file_latest(
        "DataLocal", "CastleRecipeUnlock.csv", is_jp
    )
    if file_data is None:
        helper.error_text("찾을 수 없습니다 CastleRecipeUnlock.csv")
        return None
    data = helper.parse_int_list_list(csv_handler.parse_csv(file_data.decode("utf-8")))
    maxes: dict[int, dict[int, int]] = {}
    for cannon in data:
        cannon_id = cannon[0]
        part = cannon[1]
        max_val = cannon[-1]
        if cannon_id not in maxes:
            maxes[cannon_id] = {}
        if part not in maxes[cannon_id]:
            maxes[cannon_id][part] = max_val
        elif max_val > maxes[cannon_id][part]:
            maxes[cannon_id][part] = max_val
    return maxes


def get_part_id_from_str(part: str) -> int:
    """Get the part id from the string"""
    if part == "effect":
        return 0
    if part == "foundation":
        return 1
    if part == "style":
        return 2
    return 0


def get_max(
    part: str, cannon_id: int, cannon_maxes: dict[int, dict[int, int]]
) -> Optional[int]:
    """Get the max value for the part"""
    part_id = get_part_id_from_str(part)
    if cannon_id not in cannon_maxes:
        return None
    if part_id not in cannon_maxes[cannon_id]:
        return None
    return cannon_maxes[cannon_id][part_id]


def edit_cat_cannon(save_stats: dict[str, Any]) -> dict[str, Any]:
    """Handler for ototo cat cannon upgrades"""

    cannons: dict[int, dict[str, Any]] = save_stats["ototo_cannon"]

    cannon_types = get_canon_types(helper.check_data_is_jp(save_stats))
    if cannon_types is None:
        return save_stats

    cannon_maxes = get_cannon_maxes(helper.check_data_is_jp(save_stats))
    if cannon_maxes is None:
        return save_stats

    extra_data: list[str] = []
    for i in range(len(cannon_types)):
        levels = cannons[i]["levels"]
        if i == 0:
            extra_data.append(f"레벨: &{levels['effect']+1}&")
            continue
        string = ""
        for level_str, level in levels.items():
            part_id = get_part_id_from_str(level_str)
            if part_id == 0:
                level += 1
            string += f"{level_str.title()}: &{level}&, "
        string = string[:-2]
        string += f" (개발: &{cannons[i]['unlock_flag']}&)"
        extra_data.append(string)

    cannon_ids = user_input_handler.select_not_inc(cannon_types, extra_data=extra_data)
    if len(cannon_ids) > 1:
        individual = user_input_handler.ask_if_individual("고양이 대포")
    else:
        individual = True

    if individual:
        for cannon_id in cannon_ids:
            helper.colored_text(
                f"편집 &{cannon_types[cannon_id]}&", helper.WHITE, helper.GREEN
            )
            cannon = cannons[cannon_id]
            if cannon_id == 0:
                max = get_max("효과", cannon_id, cannon_maxes)
                if max is None:
                    continue
                level = user_input_handler.get_int(
                    f"기지를 업그레이드할 레벨을 입력하세요. (Max &{max}&):",
                )
                level -= 1
                level = helper.config_clamp(level, 0, max)
                cannon["levels"]["effect"] = level
                continue
            develop_stage = (
                user_input_handler.colored_input(
                    "개발 단계(&1&) 또는 업그레이드 수준을 설정하시겠습니까? (&2&):",
                )
                == "1"
            )
            if develop_stage:
                unlock_flag = user_input_handler.get_int(
                    "개발 단계 진입 (1=효과, 2=기초, 3=스타일):",
                )
                unlock_flag = helper.config_clamp(unlock_flag, 0, 3)
                cannon["unlock_flag"] = unlock_flag
                if unlock_flag != 3:
                    for level_str in cannon["levels"]:
                        cannon["levels"][level_str] = 0
            else:
                cannon["upgrade_flag"] = 3
                for level_str in cannon["levels"]:
                    max = get_max(level_str, cannon_id, cannon_maxes)
                    if max is None:
                        continue
                    part_id = get_part_id_from_str(level_str)
                    level = user_input_handler.get_int(
                        f"업그레이드할 레벨을 입력하세요&{level_str}& to (최대치 &{max}&):"
                    )
                    if part_id == 0:
                        level -= 1
                    level = helper.config_clamp(level, 0, max)
                    cannon["levels"][level_str] = level
    else:
        develop_stage = (
            user_input_handler.colored_input(
                "개발 단계(&1&) 또는 업그레이드 수준을 설정하시겠습니까? (&2&):",
            )
            == "1"
        )
        if develop_stage:
            unlock_value = user_input_handler.get_int(
                "개발 단계 진입 (1=효과, 2=기초, 3=스타일):",
            )
            unlock_value = helper.config_clamp(unlock_value, 0, 3)
            for cannon_id in cannon_ids:
                cannons[cannon_id]["unlock_flag"] = unlock_value
                if unlock_value != 3:
                    for level_str in cannons[cannon_id]["levels"]:
                        cannons[cannon_id]["levels"][level_str] = 0
        else:
            max_max = 0
            for cannon_id in cannon_ids:
                for part_id in cannon_maxes[cannon_id]:
                    if cannon_maxes[cannon_id][part_id] > max_max:
                        max_max = cannon_maxes[cannon_id][part_id]

            level = user_input_handler.get_int(
                f"모든 것을 업그레이드하려면 레벨을 입력하세요. (최대치 &{max_max}&):",
            )
            for cannon_id in cannon_ids:
                cannon = cannons[cannon_id]
                cannon["upgrade_flag"] = 3
                for level_str in cannon["levels"]:
                    max = get_max(level_str, cannon_id, cannon_maxes)
                    if max is None:
                        continue
                    part_id = get_part_id_from_str(level_str)
                    level_ = level
                    if part_id == 0:
                        level_ -= 1
                    if cannon_id == 0:
                        part_id = 0
                    level_ = helper.config_clamp(
                        level_, 0, cannon_maxes[cannon_id][part_id]
                    )
                    cannon["levels"][level_str] = level_

    return save_stats
