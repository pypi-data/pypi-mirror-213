from typing import Any

from ... import item, csv_handler, game_data_getter, helper


def get_base_mats_names(is_jp: bool) -> list[str]:
    """Get the base material names"""

    file_data = game_data_getter.get_file_latest("resLocal", "GatyaitemName.csv", is_jp)
    if file_data is None:
        helper.error_text("기본 재료 이름을 가져오지 못했습니다.")
        return []
    item_names = csv_handler.parse_csv(
        file_data.decode("utf-8"),
        delimeter=helper.get_text_splitter(is_jp),
    )
    file_data = game_data_getter.get_file_latest("DataLocal", "Gatyaitembuy.csv", is_jp)
    if file_data is None:
        helper.error_text("재료 아이템 구매 데이터를 가져오지 못했습니다.")
        return []
    all_items = helper.parse_int_list_list(
        csv_handler.parse_csv(
            file_data.decode("utf-8"),
        )
    )[1:]
    base_mat_indexes: dict[int, str] = {}
    for item_id, item in enumerate(all_items):
        if item[6] == 7:
            index = int(item[7])
            base_mat_indexes[index] = item_names[item_id][0]

    base_mats_names: list[str] = []
    for index in sorted(base_mat_indexes):
        base_mats_names.append(base_mat_indexes[index])

    return base_mats_names


def edit_base_mats(save_stats: dict[str, Any]) -> dict[str, Any]:
    """Handler for editing base materials"""

    base_mats = item.IntItemGroup.from_lists(
        names=get_base_mats_names(helper.check_data_is_jp(save_stats)),
        values=save_stats["base_materials"],
        maxes=9999,
        group_name="오토토 재료",
    )
    base_mats.edit()
    save_stats["base_materials"] = base_mats.get_values()
    return save_stats
