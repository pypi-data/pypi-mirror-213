"""Module that runs when the module is run directly"""
import os
import sys
import traceback

from . import (
    adb_handler,
    config_manager,
    feature_handler,
    game_data_getter,
    helper,
    parse_save,
    patcher,
    serialise_save,
    server_handler,
    user_info,
    updater,
    user_input_handler,
    root_handler,
    locale_handler,
)
from .edits.levels import clear_tutorial


def print_start_up():
    """Print start up message"""

    locale_manager = locale_handler.LocalManager.from_config()

    helper.colored_text(
        f"{locale_manager.search_key('welcome_message')}\n"
        + locale_manager.search_key("config_file_message")
        % config_manager.get_config_path()
        + "\n"
        + locale_manager.search_key("scam_warning_message"),
        base=helper.CYAN,
        new=helper.WHITE,
    )
    local_version = updater.get_local_version()

    print()
    if "b" in local_version:
        helper.colored_text(
            locale_manager.search_key("beta_message"),
            base=helper.RED,
            new=helper.WHITE,
        )
    print()
    helper.colored_text(
        f"{locale_manager.search_key('thanks_title')}\n"
        + f"{locale_manager.search_key('lethal_thanks')}\n"
        + f"{locale_manager.search_key('beeven_cse_thanks')}\n"
        + f"{locale_manager.search_key('support_thanks')}\n"
        + locale_manager.search_key("discord_thanks"),
        base=helper.GREEN,
        new=helper.WHITE,
    )


def check_update() -> None:
    """Check if there is an update available and if so, ask the user if they want to update"""
    version_info = updater.get_version_info()
    locale_manager = locale_handler.LocalManager.from_config()
    if version_info is None:
        helper.colored_text(
            locale_manager.search_key("update_check_failed"), base=helper.RED
        )
        return
    stable_ver, pre_release_ver = version_info

    local_version = updater.get_local_version()

    helper.colored_text(
        f"{locale_manager.search_key('local_version') % local_version}",
        base=helper.CYAN,
        new=helper.WHITE,
        end="",
    )
    if pre_release_ver > stable_ver:
        helper.colored_text(
            f" &|& {locale_manager.search_key('latest_pre_release_version') % pre_release_ver}",
            base=helper.CYAN,
            new=helper.WHITE,
            end="",
        )
    print()


def main():
    """Main function"""

    if config_manager.get_config_value_category(
        "SERVER", "WIPE_TRACKED_ITEMS_ON_START"
    ):
        user_info.UserInfo.clear_all_items()
    game_data_getter.check_remove_handler()

    check_updates = config_manager.get_config_value_category(
        "START_UP", "CHECK_FOR_UPDATES"
    )
    show_start = not config_manager.get_config_value_category(
        "START_UP", "HIDE_START_TEXT"
    )

    if show_start or check_updates:
        print()
        helper.print_line_seperator(helper.CYAN, length=200)
    if show_start:
        print_start_up()
    if show_start or check_updates:
        helper.print_line_seperator(helper.CYAN, length=200)
    normal_start_up()


def normal_start_up(default_op: bool = True) -> None:
    """Display and handle options for downloading save data, pulling save data, selecting save data"""

    default_start_option = config_manager.get_config_value_category(
        "START_UP", "DEFAULT_START_OPTION"
    )
    locale_manager = locale_handler.LocalManager.from_config()
    if default_start_option != -1 and default_op:
        index = default_start_option - 1
    else:
        print()
        if not default_op:
            helper.print_line_seperator(helper.WHITE)
        options = [
            locale_manager.search_key("download_save"),
            locale_manager.search_key("select_save_file"),
            locale_manager.search_key("adb_pull_save"),
            locale_manager.search_key("load_save_data_json"),
        ]
        if helper.is_android():
            options[2] = locale_manager.search_key("android_direct_pull")
        index = (
            user_input_handler.select_single(
                options, title=locale_manager.search_key("select_save_option_title")
            )
            - 1
        )
    path = None
    if index == 0:
        helper.colored_text(locale_manager.search_key("data_transfer_message_enter"))
        path = server_handler.download_handler()
    elif index == 1:
        helper.colored_text(locale_manager.search_key("select_save_file_message"))
        path = helper.select_file(
            locale_manager.search_key("select_save_file_message"),
            helper.get_save_file_filetype(),
            initial_file=helper.get_save_path_home(),
        )
    elif index == 2:
        if not helper.is_android():
            helper.colored_text(locale_manager.search_key("adb_pull_message_enter"))
            game_versions = adb_handler.find_game_versions()
            if not game_versions:
                game_version = helper.ask_cc()
            else:
                index = (
                    user_input_handler.select_single(
                        game_versions,
                        locale_manager.search_key("select_l"),
                        locale_manager.search_key("pull_game_version_select"),
                        True,
                    )
                    - 1
                )
                game_version = game_versions[index]
            path = adb_handler.adb_pull_save_data(game_version)
        else:
            game_versions = root_handler.get_installed_battlecats_versions()
            if game_versions is not None:
                index = (
                    user_input_handler.select_single(
                        game_versions,
                        locale_manager.search_key("select_l"),
                        locale_manager.search_key("pull_game_version_select"),
                        True,
                    )
                    - 1
                )
                game_version = game_versions[index]
                path = root_handler.pull_save_data(game_version)
    elif index == 3:
        helper.colored_text(locale_manager.search_key("json_save_data_json_message"))
        js_path = helper.select_file(
            locale_manager.search_key("json_save_data_json_message"),
            [("Json", "*.json")],
            initial_file=helper.get_save_path_home() + ".json",
        )
        if js_path:
            path = helper.load_json_handler(js_path)
    else:
        helper.colored_text(locale_manager.search_key("error_option"), base=helper.RED)
        return normal_start_up(False)
    if not path:
        return normal_start_up(False)
    start(path)
    return None


def start(path: str) -> None:
    """Parse, patch, start the editor and serialise the save data"""

    locale_manager = locale_handler.LocalManager.from_config()

    if path.endswith(".json"):
        user_input_handler.colored_input(
            f"{locale_manager.search_key('error_save_json')}\n&{locale_manager.search_key('press_enter')}",
            base=helper.RED,
            new=helper.WHITE,
        )
    data = helper.load_save_file(path)
    save_stats = data["save_stats"]
    save_data: bytes = data["save_data"]
    if not clear_tutorial.is_tutorial_cleared(save_stats):
        save_stats = clear_tutorial.clear_tutorial(save_stats)
        save_data = serialise_save.start_serialize(save_stats)
    while True:
        save_stats = parse_save.start_parse(save_data, save_stats["version"])
        save_data = patcher.patch_save_data(save_data, save_stats["version"])
        save_stats = feature_handler.menu(save_stats, path)
        save_data = serialise_save.start_serialize(save_stats)
        save_data = patcher.patch_save_data(save_data, save_stats["version"])
        if config_manager.get_config_value_category(
            "SAVE_CHANGES", "SAVE_CHANGES_ON_EDIT"
        ):
            helper.write_file_bytes(path, save_data)
            helper.colored_text(
                locale_manager.search_key("save_data_saved") % path,
                base=helper.GREEN,
                new=helper.WHITE,
            )
        temp_path = os.path.join(config_manager.get_app_data_folder(), "SAVE_DATA_temp")
        helper.write_file_bytes(temp_path, save_data)
        if config_manager.get_config_value_category(
            "SAVE_CHANGES", "ALWAYS_EXPORT_JSON"
        ):
            helper.export_json(save_stats, path + ".json")


if __name__ == "__main__":
    main_properties_string = """
# start up text
welcome_message=&냥코대전쟁 한글 에디터&에 오신 것을 환영합니다.
author_message=Made by &fieryhenry& and &SintagramABP&
github_message=GitHub: &https://github.com/fieryhenry/BCSFE-Python&
discord_message=Discord: &https://discord.gg/DvmMgvn5ZB& - Please report any bugs to &#bug-reports&, or any suggestions to &#suggestions&
donate_message=Donate: &https://ko-fi.com/fieryhenry&
config_file_message=설정 파일 위치: &%s&
# 1: config file path
scam_warning_message=이 프로그램에 대해 비용을 지불하라는 요청을 받는 것은 사기입니다. 이 프로그램은 무료이며 앞으로도 그럴 것입니다. 사기를 당하셨다면 디스코드로 신고해주세요.

# update info
beta_message=You are using a &beta& release, some things may be broken. Please report any bugs you find to &#bug-reports& on Discord and specify that you are using a beta version
update_check_failed=Failed to check for updates
local_version=Local version: &%s&
# 1: local version
latest_stable_version=Latest stable version: &%s&
# 1: latest stable version
latest_pre_release_version=Latest pre-release version: &%s&
# 1: latest pre-release version
update_available=An update is available! would you like to update?

# main options
download_save=기종변경 코드로 받아오기
select_save_file=파일에서 불러오기
adb_pull_save=Use adb to pull the save from a rooted android device
load_save_data_json=Load save data from json
android_direct_pull=Use root access to access the save from local storage
select_save_option_title=옵션을 선택하세요:

# thanks
thanks_title=Thanks To:
lethal_thanks=&Lethal's editor& for giving me inspiration to start the project and it helped me work out how to patch the save data and edit cf/xp: &https://www.reddit.com/r/BattleCatsCheats/comments/djehhn/editoren&
beeven_cse_thanks=&Beeven& and &csehydrogen's& code, which helped me figure out how to patch save data: &https://github.com/beeven/battlecats& and &https://github.com/csehydrogen/BattleCatsHacker&
support_thanks=Anyone who has supported my work for giving me motivation to keep working on this and similar projects: &https://ko-fi.com/fieryhenry&
discord_thanks=Everyone in the discord for giving me saves, reporting bugs, suggesting new features, and for being an amazing community: &https://discord.gg/DvmMgvn5ZB&

# save selection
data_transfer_message_enter=세부 정보를 입력하세요:
select_save_file_message=세이브 파일 선택:
adb_pull_message_enter=Enter details for adb save pulling:
pull_game_version_select=Select a game version to pull from:
json_save_data_json_message=Select a save json file to load:

# misc
press_enter=엔터를 눌러서 계속하기
save_data_saved=파일을 저장함: &%s&
# 1: save file path

# errors
error_save_json=저장 데이터가 json 형식인 것 같습니다. json 데이터를 로드하려면 json 옵션을 가져오는 데 사용하십시오..
generic_error=오류 발생: &%s&
# 1: error message

    """

    item_properties_string = """
ban_warning=!!경고!! %s를 에딧하는 것은 밴 위험이 높습니다! 
ban_warning_leave=계속하시려면 y, 취소하려면 n을 입력하세요. (&y&/&n&):
current_item_value=현재 %s의 값은 &%s&입니다.
# 1: item name
# 2: value
max_str=(최대치 &%s&)
# 1: max value
enter_value_text=원하시는 %s의 값을 입력하세요. %s:
# 1: item name
# 2: max value
success_set=성공적으로 %s의 값을 &%s&로 바꿨습니다.
# 1: item name
# 2: value
item_value_changed=&%s&의 값이 &%s&에서 &%s&로 변경되었습니다.
# 1: item name
# 2: old value
# 3: new value
    """

    user_input_properties_string = """
enter_item_name_explain=Enter %s %s:
# 1: broad item name (e.g stage)
# 2: explanation
enter_item_name_group_explain=Enter %s for %s &%s& %s:
# 1: broad item name (e.g stage)
# 2: group name
# 3: item name
# 4: explanation
all_text=all
edit_text=edit
enter_range_text=%s의 아이디들을 입력하세요. (&{{all_text}}& 를 입력하여 모두 선택, 범위 예시: &1&-&50&, 여러아이디를 공백으로 구분해 입력: &5 4 7&):
# 1: group name
select_list=%s할 것들을 선택하세요. (공백으로 구분하여 여러개 선택하여 %s하기):
# 1: action (e.g. select)
# 2: action (e.g. select)
select_option_to=%s하기 위한 옵션을 선택하세요:
# 1: action (e.g. edit)
ask_individual=%s을 각각 에딧하려면 (&1&)번, 한번에 설정하려면 (&2&)번을 입력해주세요:
# 1: item name
select_all=&모두 선택&
select=선택
select_l=선택

invalid_input=잘못된 입력.
invalid_all={{invalid_input}} 여기서는 &모두&를 쓸 수 없습니다.
invalid_range_format={{invalid_input}} &-& 로 구분된 유효한 숫자 범위를 입력하십시오.
invalid_range={{invalid_input}} 1에서 %s까지의 유효한 숫자를 입력하세요.
# 1: max number
invalid_int={{invalid_input}} 유효한 숫자를 입력하세요..
invalid_yes_no={{invalid_input}} &yes& 또는 &no&를 입력하세요.

error_option=인식할 수 있는 옵션을 입력하세요.
error_no_options=선택할 수 있는 옵션이 없습니다:
    """

    config_properties_string = """
current_val=현재 보유량: &%s&
# 1: current value

enter_default_gv=Enter the default game version. {{current_val}} Leave blank to not specify a default game version:
select_default_save_path=Select the default save file path
fixed_save_path=Fixed save path? (on=not based on current working directory)
select_locale=Select the locale to use. {{current_val}}
flag_set_config=Do you want to enable (&1&) or disable (&0&) %s. {{current_val}}:
# 1: flag name
enter_new_val_config=%s의 새로운 값을 입력하세요. {{current_val}}:
# 1: value name
select_config_path=Select the config file path
enabled=Enabled
disabled=Disabled

    """
    localesdir = os.path.join(os.path.join(helper.get_local_files_path(), "locales"), "en")
    with open(os.path.join(localesdir, "main.properties"), "w+", encoding="utf-8") as main_properties:
        main_properties.write(main_properties_string)
    with open(os.path.join(localesdir, "item.properties"), "w+", encoding="utf-8") as item_properties:
        item_properties.write(item_properties_string)
    with open(os.path.join(localesdir, "config.properties"), "w+", encoding="utf-8") as config_properties:
        config_properties.write(config_properties_string)
    with open(os.path.join(localesdir, "user_input.properties"), "w+", encoding="utf-8") as user_input_properties:
        user_input_properties.write(user_input_properties_string)

    try:
        main()
    except KeyboardInterrupt:
        sys.exit()
    except Exception as e:  # pylint: disable=broad-except
        try:
            locale_manager = locale_handler.LocalManager.from_config()
            error_txt = locale_manager.search_key("generic_error") % e
        except Exception:  # pylint: disable=broad-except
            error_txt = "An error has occurred: %s" % e
        helper.colored_text(
            error_txt,
            base=helper.RED,
            new=helper.WHITE,
        )
        traceback.print_exc()
        helper.exit_check_changes()