from typing import Any, Optional
from ... import user_input_handler, server_handler, helper, adb_handler
from ..levels import clear_tutorial


def select(save_stats: dict[str, Any]) -> dict[str, Any]:
    helper.check_changes(None)
    options = [
        "전송 및 확인 코드를 사용하여 게임에서 저장 데이터 다운로드",
        "파일에서 저장 파일 선택",
        "adb를 사용하여 루팅된 장치에서 저장을 가져옵니다.",
        "json에서 저장 데이터 불러오기",
    ]
    index = (
        user_input_handler.select_single(
            options, title="저장 데이터를 가져오는 옵션을 선택합니다."
        )
        - 1
    )
    save_path = handle_index(index)
    if not save_path:
        return save_stats
    helper.set_save_path(save_path)
    data = helper.load_save_file(save_path)
    save_stats = data["save_stats"]
    if save_path.endswith(".json"):
        input(
            "저장 데이터가 json 형식인 것 같습니다. json 데이터를 로드하려면 json 옵션을 가져오기 위해 사용하십시오.\n계속하려면 엔터 키를 누르십시오...:"
        )
    if not clear_tutorial.is_tutorial_cleared(save_stats):
        save_stats = clear_tutorial.clear_tutorial(save_stats)
    return save_stats


def handle_index(index: int) -> Optional[str]:
    path = None
    if index == 0:
        print("Enter details for data transfer:")
        path = server_handler.download_handler()
    elif index == 1:
        print("Select save file:")
        path = helper.select_file(
            "Select a save file:",
            helper.get_save_file_filetype(),
            initial_file=helper.get_save_path_home(),
        )
    elif index == 2:
        print("Enter details for save pulling:")
        game_versions = adb_handler.find_game_versions()
        if not game_versions:
            game_version = helper.ask_cc()
        else:
            index = (
                user_input_handler.select_single(
                    game_versions, "Select", "Select a game version to pull from:", True
                )
                - 1
            )
            game_version = game_versions[index]
        path = adb_handler.adb_pull_save_data(game_version)
    elif index == 3:
        print("Select save data json file")
        js_path = helper.select_file(
            "Select save data json file",
            [("Json", "*.json")],
            initial_file=helper.get_save_path_home() + ".json",
        )
        if js_path:
            path = helper.load_json_handler(js_path)
    else:
        helper.colored_text("Please enter a recognised option", base=helper.RED)
        return None
    return path
