"""Handler for selecting and running editor features"""

from typing import Any, Union

from . import (
    helper,
    user_input_handler,
    config_manager,
)
from .edits import basic, cats, gamototo, levels, other, save_management


def fix_elsewhere_old(save_stats: dict[str, Any]) -> dict[str, Any]:
    """Fix the elsewhere error using 2 save files"""

    main_token = save_stats["token"]
    main_iq = save_stats["inquiry_code"]
    input(
        "Select a save file that is currently loaded in-game that doesn't have the elsehere error and is not banned\nPress enter to continue:"
    )
    new_path = helper.select_file(
        "Select a clean save file",
        helper.get_save_file_filetype(),
        helper.get_save_path(),
    )
    if not new_path:
        print("Please select a save file")
        return save_stats

    data = helper.load_save_file(new_path)
    new_stats = data["save_stats"]
    new_token = new_stats["token"]
    new_iq = new_stats["inquiry_code"]
    save_stats["token"] = new_token
    save_stats["inquiry_code"] = new_iq

    helper.colored_text(f"Replaced inquiry code: &{main_iq}& with &{new_iq}&")
    helper.colored_text(f"Replaced token: &{main_token}& with &{new_token}&")
    return save_stats


FEATURES: dict[str, Any] = {
    "세이브 관리": {
        "세이브 저장": save_management.save.save_save,
        "세이브 저장후 기종변경 코드 받기": save_management.server_upload.save_and_upload,
        "파일에 저장하기": save_management.save.save,
        "Save changes and push save data to the game with adb (don't re-open game)": save_management.save.save_and_push,
        "Save changes and push save data to the game with adb (re-open game)": save_management.save.save_and_push_rerun,
        "세이브 데이터를 JSON으로 컴파일": save_management.other.export,
        "Clear save data with adb (used to generate a new account without re-installing the game)": save_management.other.clear_data,
        "Upload tracked bannable items (This is done automatically when saving or exiting)": save_management.server_upload.upload_metadata,
        "새로운 세이브 데이터 로딩": save_management.load.select,
        "세이브 데이터 국가 변경": save_management.convert.convert_save,
        # "Manage Presets": preset_handler.preset_manager,
    },
    "아이템": {
        "통조림": basic.basic_items.edit_cat_food,
        "XP": basic.basic_items.edit_xp,
        "티켓": {
            "냥코 티켓": basic.basic_items.edit_normal_tickets,
            "레어 티켓": basic.basic_items.edit_rare_tickets,
            "플래티넘 티켓": basic.basic_items.edit_platinum_tickets,
            "플래티넘 조각": basic.basic_items.edit_platinum_shards,
            "레전드 티켓": basic.basic_items.edit_legend_tickets,
        },
        "NP": basic.basic_items.edit_np,
        "리더쉽": basic.basic_items.edit_leadership,
        "배틀 아이템": basic.basic_items.edit_battle_items,
        "캣츠아이": basic.catseyes.edit_catseyes,
        "개다래 / 수석": basic.catfruit.edit_catfruit,
        "본능 구슬": basic.talent_orbs_new.edit_talent_orbs,
        "고양이 드링크": basic.basic_items.edit_catamins,
        "항목 구성표(금지할 수 없는 항목을 얻을 수 있음)": other.scheme_item.edit_scheme_data,
    },
    "가마토토 / 오토토": {
        "오토토 조수": basic.basic_items.edit_engineers,
        "성 재료": basic.ototo_base_mats.edit_base_mats,
        "고양이 드링크": basic.basic_items.edit_catamins,
        "가마토토 XP / 레벨": gamototo.gamatoto_xp.edit_gamatoto_xp,
        "오토토 대포": gamototo.ototo_cat_cannon.edit_cat_cannon,
        "가마토토 대원": gamototo.helpers.edit_helpers,
        "가마토토가 게임을 튕기는 버그 수정": gamototo.fix_gamatoto.fix_gamatoto,
    },
    "캐릭터 / 특능": {
        "캐릭터 획득 / 제거": {
            "캐릭터 획득": cats.get_remove_cats.get_cat,
            "캐릭터 제거": cats.get_remove_cats.remove_cats,
        },
        "캐릭터 업그레이드": cats.upgrade_cats.upgrade_cats,
        "캐릭터 3단 진화": {
            "3단 진화 획득": cats.evolve_cats.get_evolve,
            "3단 진화 제거": cats.evolve_cats.remove_evolve,
            "강제 3단 진화 (3단 진화가 없는 고양이의 경우 빈 고양이로 채워짐)": cats.evolve_cats.get_evolve_forced,
        },
        "본능": {
            "선택한 각 고양이의 본능을 개별적으로 설정": cats.talents.edit_talents_individual,
            "선택된 모든 고양이 본능 만렙 / 제거": cats.talents.max_all_talents,
        },
        "캐릭터 도감": {
            "캐릭터 도감 획득 (통조림 X)": cats.clear_cat_guide.collect_cat_guide,
            "캐릭터 도감 미확인 상태": cats.clear_cat_guide.remove_cat_guide,
        },
        '스테이지 드롭 보상 받기 (보수 상태 획득)': cats.chara_drop.get_character_drops,
        "특능 편집": cats.upgrade_blue.upgrade_blue,
    },
    "스테이지 / 보물": {
        "스테이지 클리어 / 언클리어": {
            "선택한 모든 챕터의 모든 챕터에서 각 스테이지 클리어": levels.main_story.clear_all,
            "선택한 각 챕터의 모든 챕터에서 각 스테이지 클리어": levels.main_story.clear_each,
        },
        "보물": {
            "보물 그룹으로 설정": levels.treasures.treasure_groups,
            "모든 보물을 따로따로 설정": levels.treasures.specific_stages,
            "각 장별로 한번에 설정": levels.treasures.specific_stages_all_chapters,
        },
        "좀비스테이지": levels.outbreaks.edit_outbreaks,
        "이벤트 스테이지": levels.event_stages.event_stages,
        "구레전드 스테이지": levels.event_stages.stories_of_legend,
        "신레전드 스테이지": levels.uncanny.edit_uncanny,
        "마계편 클리어": levels.aku.edit_aku,
        "마계의 문 열기": levels.unlock_aku_realm.unlock_aku_realm,
        #"Gauntlets": levels.gauntlet.edit_gauntlet,
        #"Collab Gauntlets": levels.gauntlet.edit_collab_gauntlet,
        "탑": levels.towers.edit_tower,
        "초수 스테이지": levels.behemoth_culling.edit_behemoth_culling,
        "미래편 시간 점수": levels.itf_timed_scores.timed_scores,
        "챌린지 배틀 점수": basic.basic_items.edit_challenge_battle,
        "튜토리얼 클리어": levels.clear_tutorial.clear_tutorial,
        "냥코 도장 점수": basic.basic_items.edit_dojo_score,
        "발굴 스테이지 추가": levels.enigma_stages.edit_enigma_stages,
        "필리버스터 스테이지 언클리어": levels.allow_filibuster_clearing.allow_filibuster_clearing,
        "레전드 퀘스트": levels.legend_quest.edit_legend_quest,
    },
    "문의코드 / 토큰 / 계정": {
        "문의코드": basic.basic_items.edit_inquiry_code,
        "토큰": basic.basic_items.edit_token,
        "언밴 / 오류 해결": other.fix_elsewhere.fix_elsewhere,
        #"Old Fix elsewhere error / Unban account (needs 2 save files)": fix_elsewhere_old,
        "새 문의코드와 토큰 생성": other.create_new_account.create_new_account,
    },
    "기타": {
        "레어 뽑기 시드": basic.basic_items.edit_rare_gacha_seed,
        "캐릭터 편성": basic.basic_items.edit_unlocked_slots,
        "리스타트팩 설정": basic.basic_items.edit_restart_pack,
        "냥코 메달 설정": other.meow_medals.medals,
        "플레이타임 설정": other.play_time.edit_play_time,
        "적 도감 설정": other.unlock_enemy_guide.enemy_guide,
        "미션 설정": other.missions.edit_missions,
        "일반 티켓 최대 거래 진행률(금지할 수 없는 희귀 티켓 허용)": other.trade_progress.set_trade_progress,
        "골드패스 설정": other.get_gold_pass.get_gold_pass,
        "모든 유저 랭크 보상 제거 / 획득 (아이템을 주지 않음)": other.claim_user_rank_rewards.edit_rewards,
        "냥코 사당 레벨 / XP": other.cat_shrine.edit_shrine_xp,
    },
    "오류해결": {
        "시간 오류 해결": other.fix_time_issues.fix_time_issues,
        "캐릭터 편성 오류 해결": other.unlock_equip_menu.unlock_equip,
        "튜토리얼 클리어": levels.clear_tutorial.clear_tutorial,
        "언밴 / 오류 해결": other.fix_elsewhere.fix_elsewhere,
        #"Old Fix elsewhere error / Unban account (needs 2 save files)": fix_elsewhere_old,
        "가마토토 / 오토토 오류 해결": gamototo.fix_gamatoto.fix_gamatoto,
    },
    "에디터 설정 (사용 X)": {
        "Edit LOCALIZATION": config_manager.edit_locale,
        "Edit DEFAULT_COUNTRY_CODE": config_manager.edit_default_gv,
        "Edit DEFAULT_SAVE_PATH": config_manager.edit_default_save_file_path,
        "Edit FIXED_SAVE_PATH": config_manager.edit_fixed_save_path,
        "Edit EDITOR settings": config_manager.edit_editor_settings,
        "Edit START_UP settings": config_manager.edit_start_up_settings,
        "Edit SAVE_CHANGES settings": config_manager.edit_save_changes_settings,
        "Edit SERVER settings": config_manager.edit_server_settings,
        "Edit config path": config_manager.edit_config_path,
    },
    "종료": helper.exit_check_changes,
}


def get_feature(
    selected_features: Any, search_string: str, results: dict[str, Any]
) -> dict[str, Any]:
    """Search for a feature if the feature name contains the search string"""

    for feature in selected_features:
        feature_data = selected_features[feature]
        if isinstance(feature_data, dict):
            feature_data = get_feature(feature_data, search_string, results)
        if search_string.lower().replace(" ", "") in feature.lower().replace(" ", ""):
            results[feature] = selected_features[feature]
    return results


def show_options(
    save_stats: dict[str, Any], features_to_use: dict[str, Any]
) -> dict[str, Any]:
    """Allow the user to either enter a feature number or a feature name, and get the features that match"""

    if (
        not config_manager.get_config_value_category("EDITOR", "SHOW_CATEGORIES")
        and FEATURES == features_to_use
    ):
        user_input = ""
    else:
        prompt = (
            "에딧할 것을 선택하세요."
        )
        if config_manager.get_config_value_category(
            "EDITOR", "SHOW_FEATURE_SELECT_EXPLANATION"
        ):
            prompt += "\n원하시는 메뉴의 번호를 입력해주세요"
        user_input = user_input_handler.colored_input(f"{prompt}:\n")
    user_int = helper.check_int(user_input)
    results = []
    if user_int is None:
        results = get_feature(features_to_use, user_input, {})
    else:
        if user_int < 1 or user_int > len(features_to_use) + 1:
            helper.colored_text("번호가 메뉴에 없습니다.", helper.RED)
            return show_options(save_stats, features_to_use)
        if FEATURES != features_to_use:
            if user_int - 2 < 0:
                return menu(save_stats)
            results = features_to_use[list(features_to_use)[user_int - 2]]
        else:
            results = features_to_use[list(features_to_use)[user_int - 1]]
    if not isinstance(results, dict):
        save_stats_return = results(save_stats)
        if save_stats_return is None:
            return save_stats
        return save_stats_return
    if len(results) == 0:
        helper.colored_text("해당 메뉴가 없습니다.", helper.RED)
        return menu(save_stats)
    if len(results) == 1 and isinstance(list(results.values())[0], dict):
        results = results[list(results)[0]]
    if len(results) == 1:
        save_stats_return = results[list(results)[0]](save_stats)
        if save_stats_return is None:
            return save_stats
        return save_stats_return

    helper.colored_list(["뒤로가기"] + list(results))
    return show_options(save_stats, results)


def menu(
    save_stats: dict[str, Any], path_save: Union[str, None] = None
) -> dict[str, Any]:
    """Show the menu and allow the user to select a feature to edit"""

    if path_save:
        helper.set_save_path(path_save)
    if config_manager.get_config_value_category("EDITOR", "SHOW_CATEGORIES"):
        helper.colored_list(list(FEATURES))
    save_stats = show_options(save_stats, FEATURES)

    return save_stats
