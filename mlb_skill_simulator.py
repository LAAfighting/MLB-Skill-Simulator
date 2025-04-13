import random
import enum
import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
from PIL import Image, ImageTk

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# 定義技能階級
class SkillTier(enum.Enum):
    BRONZE = "黃銅"
    SILVER = "炫銀"
    GOLD = "炫金"
    LEGEND = "傳說"

# 定義球員類型
class PlayerType(enum.Enum):
    BATTER = "打者"
    PITCHER = "投手"

# 定義投手位置
class PitcherPosition(enum.Enum):
    STARTER_1 = "先發1"
    STARTER_2 = "先發2"
    STARTER_3 = "先發3"
    STARTER_4 = "先發4"
    STARTER_5 = "先發5"
    BULLPEN_WIN_1 = "牛棚勝利組1"
    BULLPEN_WIN_2 = "牛棚勝利組2"
    BULLPEN_LOSE_3 = "牛棚敗處組3"
    BULLPEN_LOSE_4 = "牛棚敗處組4"
    BULLPEN_LOSE_5 = "牛棚敗處組5"
    LONG_RELIEF = "長中繼1"
    CLOSER = "終結者1"

# 定義打者棒次
class BatterPosition(enum.Enum):
    BATTING_1 = "1棒"
    BATTING_2 = "2棒"
    BATTING_3 = "3棒"
    BATTING_4 = "4棒"
    BATTING_5 = "5棒"
    BATTING_6 = "6棒"
    BATTING_7 = "7棒"
    BATTING_8 = "8棒"
    BATTING_9 = "9棒"
    SUB_1 = "候補1"
    SUB_2 = "候補2"
    SUB_3 = "候補3"
    SUB_4 = "候補4"
    SUB_5 = "候補5"

# 定義守備位置
class DefensivePosition(enum.Enum):
    C = "C"
    FIRST_BASE = "1B"
    SECOND_BASE = "2B"
    THIRD_BASE = "3B"
    SHORTSTOP = "SS"
    RIGHT_FIELD = "RF"
    CENTER_FIELD = "CF"
    LEFT_FIELD = "LF"
    DESIGNATED_HITTER = "DH"

# 技能類別
class Skill:
    def __init__(self, name, tier, level=1):
        self.name = name
        self.tier = tier
        self.level = level

    def __str__(self):
        return f"{self.name} Lv.{self.level}"

# 球員類別
class Player:
    def __init__(self, player_type, position, is_legend=False, is_black_diamond=True):
        self.player_type = player_type
        self.position = position
        self.is_legend = is_legend
        self.is_black_diamond = is_black_diamond
        self.skills = [None, None, None]
        self.defensive_position = None
        self.simulation_count = 0
        self.legend_count = 0
        self.level_sum_stats = {3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}
        self.level_sum_count = 0
        self.ticket_usage_stats = {
            "技能變更券": 0,
            "高級技能變更券": 0,
            "最高級技能變更券": 0,
            "傳說技能變更券": 0,
            "傳說技能選擇變更券": 0,
            "技能變更保護券": 0,
            "技能選擇變更券": 0
        }

    def set_skill(self, slot, skill):
        self.skills[slot] = skill

    def has_legend_skill(self):
        return any(skill and skill.tier == SkillTier.LEGEND for skill in self.skills)

    def is_legend_skill_in_slot(self, slot):
        return self.skills[slot] and self.skills[slot].tier == SkillTier.LEGEND

# 技能資料庫
BATTER_SKILLS = {
    SkillTier.BRONZE: ["代打專家", "鷹眼", "推打", "拉打", "左腕殺手", "右腕殺手", "守備將軍", "打點機器", "直球殺手", "集中力", "正面對決", "初球攻略"],
    SkillTier.SILVER: ["精密打擊", "揮大棒打者", "訓練上癮", "巨砲本能", "開路先鋒", "筋疲力盡", "忍術", "下盤鍛錬", "逆轉的力量", "勝負天性", "動物本能", "信賴", "克服弱點"],
    SkillTier.GOLD: ["雷射肩", "王牌殺手", "超級強打", "五拍子球員", "超能神話", "預知能力", "盜壘天王", "打擊機器", "自走砲", "萬眾矚目", "超級輔助", "強化優點", "廣角打者"],
    SkillTier.LEGEND: ["打者洞察力", "精準打擊", "壞球打者", "先鋒", "天生巨星", "機會製造者", "打者默契", "最強打者", "老手"]
}

PITCHER_SKILLS = {
    SkillTier.BRONZE: ["牽制王", "平靜", "佛祖保佑", "危機克服", "光速投球", "魔球大師", "左打殺手", "右打殺手", "鋼鐵人", "老謀深算", "強心臟", "冰凍"],
    SkillTier.SILVER: ["強力投手", "控球藝術家", "強打殺手", "國寶投手", "逆轉大師", "狙擊手", "野戰指揮", "投球機器", "布局", "乘勝追擊", "救火隊", "安全感", "調整節奏"],
    SkillTier.GOLD: ["決勝球", "巨人殺手", "自我解決", "大吃局數", "王牌", "最後大魔王", "無法觸碰", "門志", "技巧派投手", "壓倒性投手", "王牌終結者", "滾地球投手", "交錯之火", "投球協調者"],
    SkillTier.LEGEND: ["投手洞察力", "精準控球", "速球型投手", "先守後攻", "牛棚日", "合力投球", "投手默契", "工作馬", "完美先生"]
}

# 機率表
PROBABILITIES = {
    PlayerType.BATTER: {
        "base": [2.6316 / 100, 2.7027 / 100, 2.7778 / 100],
        "legend_first": [1.0, 2.6316 / 100, 2.7027 / 100],
        "legend_held": [2.7778 / 100, 2.8571 / 100],
        "no_legend_held": [2.8571 / 100, 2.9412 / 100]
    },
    PlayerType.PITCHER: {
        "base": [2.5641 / 100, 2.6316 / 100, 2.7027 / 100],
        "legend_first": [1.0, 2.5641 / 100, 2.6316 / 100],
        "legend_held": [2.7027 / 100, 2.7778 / 100],
        "no_legend_held": [2.7778 / 100, 2.8571 / 100]
    }
}

# 傳說技能出現機率
LEGEND_PROBABILITIES = {
    "傳說卡": {
        "高級技能變更券": 0.20,
        "最高級技能變更券": 0.25,
        "傳說技能變更券": 1.00,
        "傳說技能選擇變更券": 1.00,
    },
    "其他卡": {
        "高級技能變更券": 0.10,
        "最高級技能變更券": 0.15,
        "傳說技能變更券": 1.00,
        "傳說技能選擇變更券": 1.00,
    }
}

# 技能等級機率
LEVEL_PROB = {"等級1": 0.34, "等級2": 0.33, "等級3": 0.33}

# 技能等級總和機率（普通情況）
LEVEL_SUM_PROB_DEFAULT = {
    3: 0.34 * 0.34 * 0.34,
    4: 3 * (0.34 * 0.34 * 0.33),
    5: 3 * (0.34 * 0.33 * 0.33) + 3 * (0.34 * 0.33 * 0.34),
    6: 3 * (0.34 * 0.33 * 0.33) + 3 * (0.33 * 0.33 * 0.33),
    7: 3 * (0.33 * 0.33 * 0.33) + 3 * (0.33 * 0.33 * 0.34),
    8: 3 * (0.33 * 0.33 * 0.34),
    9: 0.33 * 0.33 * 0.33
}

# 技能等級總和機率（最高級技能變更券，總和至少為 5）
LEVEL_SUM_PROB_SUPER = {
    3: 0.0,
    4: 0.0,
    5: 0.266495,
    6: 0.304984,
    7: 0.258657,
    8: 0.127398,
    9: 0.042466
}

# 系統模擬次數上限
MAX_SIMULATION_LIMIT = 10000

def get_skill_level(is_legend_player):
    if is_legend_player:
        return 3
    level = random.choices(
        ["等級1", "等級2", "等級3"],
        weights=[LEVEL_PROB["等級1"], LEVEL_PROB["等級2"], LEVEL_PROB["等級3"]],
        k=1
    )[0]
    return int(level.split("等級")[-1])

def simulate_skill_change(player, ticket_type, protected_slot=None):
    skills_db = BATTER_SKILLS if player.player_type == PlayerType.BATTER else PITCHER_SKILLS
    probs = PROBABILITIES[player.player_type]
    all_skills = []
    for tier in [SkillTier.BRONZE, SkillTier.SILVER, SkillTier.GOLD]:
        all_skills.extend([(name, tier) for name in skills_db[tier]])

    card_type = "傳說卡" if player.is_legend else "其他卡"
    legend_prob = LEGEND_PROBABILITIES[card_type].get(ticket_type, 0.0)

    selected_skills = [None, None, None]
    remaining_skills = all_skills.copy()

    if ticket_type == "技能變更券":
        for slot in range(3):
            prob = probs["base"][slot]
            weights = [prob] * len(remaining_skills)
            skill_name, skill_tier = random.choices(remaining_skills, weights=weights, k=1)[0]
            level = 3 if player.is_legend else get_skill_level(player.is_legend)
            selected_skills[slot] = Skill(skill_name, skill_tier, level)
            remaining_skills.remove((skill_name, skill_tier))
        return selected_skills

    elif ticket_type in ["高級技能變更券", "最高級技能變更券", "傳說技能變更券"]:
        if random.random() < legend_prob:
            legend_skills = [(name, SkillTier.LEGEND) for name in skills_db[SkillTier.LEGEND]]
            skill_name, skill_tier = random.choice(legend_skills)
            level = 3 if player.is_legend else get_skill_level(player.is_legend)
            selected_skills[0] = Skill(skill_name, skill_tier, level)
        else:
            gold_skills = [(name, SkillTier.GOLD) for name in skills_db[SkillTier.GOLD]]
            skill_name, skill_tier = random.choice(gold_skills)
            level = 3 if player.is_legend else get_skill_level(player.is_legend)
            selected_skills[0] = Skill(skill_name, skill_tier, level)
            remaining_skills.remove((skill_name, skill_tier))

        for slot in range(1, 3):
            prob = probs["base"][slot]
            weights = [prob] * len(remaining_skills)
            skill_name, skill_tier = random.choices(remaining_skills, weights=weights, k=1)[0]
            level = 3 if player.is_legend else get_skill_level(player.is_legend)
            selected_skills[slot] = Skill(skill_name, skill_tier, level)
            remaining_skills.remove((skill_name, skill_tier))

        if ticket_type == "最高級技能變更券":
            while True:
                total_level = sum(skill.level for skill in selected_skills if skill)
                if total_level >= 5 or player.is_legend:
                    break
                selected_skills = simulate_skill_change(player, "高級技能變更券", protected_slot)

        return selected_skills

    elif ticket_type == "傳說技能選擇變更券":
        if not player.has_legend_skill():
            raise ValueError("必須至少有一個傳說技能才能使用此變更券")

        # 找到第一個傳說技能的槽位
        legend_slot = None
        for slot in range(3):
            if player.skills[slot] and player.skills[slot].tier == SkillTier.LEGEND:
                legend_slot = slot
                break

        if legend_slot is None:
            raise ValueError("未找到傳說技能，無法使用此變更券")

        # 保留原始技能
        selected_skills = player.skills.copy()

        # 只對第一個傳說技能的槽位進行變更，並保留原始等級
        legend_skills = [(name, SkillTier.LEGEND) for name in skills_db[SkillTier.LEGEND]]
        current_skill = selected_skills[legend_slot]
        original_level = current_skill.level  # 取得原始技能等級
        if current_skill:
            skill_tuple = (current_skill.name, current_skill.tier)
            if skill_tuple in legend_skills:
                legend_skills.remove(skill_tuple)
        skill_name, skill_tier = random.choice(legend_skills)
        # 使用原始等級，而不是重新生成
        selected_skills[legend_slot] = Skill(skill_name, skill_tier, original_level)
        return selected_skills

    elif ticket_type == "技能變更保護券":
        if protected_slot is None:
            raise ValueError("必須指定保護的技能槽")
        selected_skills = [None, None, None]
        remaining_skills = all_skills.copy()
        if player.skills[protected_slot]:
            selected_skills[protected_slot] = player.skills[protected_slot]
            if (player.skills[protected_slot].name, player.skills[protected_slot].tier) in remaining_skills:
                remaining_skills.remove((player.skills[protected_slot].name, player.skills[protected_slot].tier))
        for slot in range(3):
            if slot == protected_slot:
                continue
            prob = probs["base"][slot]
            weights = [prob] * len(remaining_skills)
            skill_name, skill_tier = random.choices(remaining_skills, weights=weights, k=1)[0]
            level = 3 if player.is_legend else (player.skills[slot].level if player.skills[slot] else get_skill_level(player.is_legend))
            selected_skills[slot] = Skill(skill_name, skill_tier, level)
            remaining_skills.remove((skill_name, skill_tier))
        return selected_skills

    elif ticket_type == "技能選擇變更券":
        selected_slot = protected_slot if protected_slot is not None else random.randint(0, 2)
        selected_skills = player.skills.copy()
        remaining_skills = all_skills.copy()
        if not selected_skills[selected_slot]:
            selected_skills[selected_slot] = Skill("臨時技能", SkillTier.BRONZE, 3 if player.is_legend else get_skill_level(player.is_legend))
        if (selected_skills[selected_slot].name, selected_skills[selected_slot].tier) in remaining_skills:
            remaining_skills.remove((selected_skills[selected_slot].name, selected_skills[selected_slot].tier))
        prob = probs["base"][0]
        weights = [prob] * len(remaining_skills)
        skill_name, skill_tier = random.choices(remaining_skills, weights=weights, k=1)[0]
        level = 3 if player.is_legend else selected_skills[selected_slot].level
        selected_skills[selected_slot] = Skill(skill_name, skill_tier, level)
        return selected_skills

    else:
        raise ValueError("未知的變更券類型")

# GUI 應用程式類別
class MLBSkillSimulatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MLB 9局職棒25 技能模擬器")
        self.player = None
        self.players = {}
        self.pitcher_image = None
        self.batter_image = None
        self.stats_labels = {}
        self.ticket_stats_labels = {}
        self.probability_labels = {}
        self.original_pitcher_image = None
        self.original_batter_image = None
        self.simulation_entry = None
        self.stop_button = None
        self.is_simulating = False
        self.base_font_size = 12
        self.base_button_width = 12
        self.base_image_size = (150, 200)
        self.base_padx = 8
        self.base_pady = 8
        self.pitcher_skill_labels = {}
        self.batter_skill_labels = {}
        self.pitcher_legend_labels = {}
        self.batter_legend_labels = {}
        self.batter_position_comboboxes = {}
        self.load_images()
        self.setup_gui()
        self.set_default_selection()

    def load_images(self):
        try:
            img = Image.open(resource_path("pitcher_black_diamond.png"))
            self.original_pitcher_image = img
            img = img.resize(self.base_image_size, Image.Resampling.LANCZOS)
            self.pitcher_image = ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"無法載入投手選擇圖片: {e}")
            self.pitcher_image = None

        try:
            img = Image.open(resource_path("batter_black_diamond.png"))
            self.original_batter_image = img
            img = img.resize(self.base_image_size, Image.Resampling.LANCZOS)
            self.batter_image = ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"無法載入打者選擇圖片: {e}")
            self.batter_image = None

    def set_default_selection(self):
        self.select_pitcher("先發1")
        self.ticket_var.set("最高級技能變更券")
        self.update_slot_selection()
        self.show_pitcher()

    def setup_gui(self):
        self.main_frame = tk.Frame(self.root, bg="black")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=self.base_padx, pady=self.base_pady)

        self.combined_frame = tk.Frame(self.main_frame, bg="black")
        self.combined_frame.pack(side=tk.LEFT, fill=tk.Y, padx=self.base_padx, pady=self.base_pady)

        self.combined_canvas = tk.Canvas(self.combined_frame, bg="black", height=700, width=220)
        self.combined_scrollbar = tk.Scrollbar(self.combined_frame, orient=tk.VERTICAL, command=self.combined_canvas.yview)
        self.combined_scrollable_frame = tk.Frame(self.combined_canvas, bg="black")

        self.combined_scrollable_frame.bind(
            "<Configure>",
            lambda e: self.combined_canvas.configure(scrollregion=self.combined_canvas.bbox("all"))
        )

        self.combined_canvas.create_window((0, 0), window=self.combined_scrollable_frame, anchor="nw")
        self.combined_canvas.configure(yscrollcommand=self.combined_scrollbar.set)

        self.combined_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.combined_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.stats_inner_frame = tk.Frame(self.combined_scrollable_frame, bg="black")
        self.stats_inner_frame.pack(fill=tk.X, pady=self.base_pady)

        self.stats_title = tk.Label(self.stats_inner_frame, text="統計結果:", fg="white", bg="black", font=("Arial", self.base_font_size, "bold"), anchor="w")
        self.stats_title.pack(anchor="w")

        self.simulation_count_frame = tk.Frame(self.stats_inner_frame, bg="black")
        self.simulation_count_frame.pack(fill=tk.X)
        self.simulation_count_label = tk.Label(self.simulation_count_frame, text="已模擬:", fg="white", bg="black", font=("Arial", self.base_font_size), anchor="w")
        self.simulation_count_label.pack(side=tk.LEFT, padx=self.base_padx)
        self.stats_labels["simulation_count"] = tk.Label(self.simulation_count_frame, text="0 次", fg="white", bg="black", font=("Arial", self.base_font_size), anchor="w")
        self.stats_labels["simulation_count"].pack(side=tk.LEFT)

        self.legend_count_frame = tk.Frame(self.stats_inner_frame, bg="black")
        self.legend_count_frame.pack(fill=tk.X)
        self.legend_count_label = tk.Label(self.legend_count_frame, text="傳說技能出現:", fg="white", bg="black", font=("Arial", self.base_font_size), anchor="w")
        self.legend_count_label.pack(side=tk.LEFT, padx=self.base_padx)
        self.stats_labels["legend_count"] = tk.Label(self.legend_count_frame, text="0 次 (0.00%)", fg="white", bg="black", font=("Arial", self.base_font_size), anchor="w")
        self.stats_labels["legend_count"].pack(side=tk.LEFT)

        self.level_sum_title = tk.Label(self.stats_inner_frame, text="技能等級總和統計:", fg="white", bg="black", font=("Arial", self.base_font_size, "bold"), anchor="w")
        self.level_sum_title.pack(anchor="w", pady=self.base_pady)
        for level_sum in range(3, 10):
            frame = tk.Frame(self.stats_inner_frame, bg="black")
            frame.pack(fill=tk.X)
            label = tk.Label(frame, text=f"總和{level_sum}:", fg="white", bg="black", font=("Arial", self.base_font_size), anchor="w")
            label.pack(side=tk.LEFT, padx=self.base_padx)
            self.stats_labels[f"level_sum_{level_sum}"] = tk.Label(frame, text="0 次 (0.00%)", fg="white", bg="black", font=("Arial", self.base_font_size), anchor="w")
            self.stats_labels[f"level_sum_{level_sum}"].pack(side=tk.LEFT)

        self.ticket_stats_title = tk.Label(self.stats_inner_frame, text="變更券使用統計:", fg="white", bg="black", font=("Arial", self.base_font_size, "bold"), anchor="w")
        self.ticket_stats_title.pack(anchor="w", pady=self.base_pady)
        for ticket_type in [
            "技能變更券", "高級技能變更券", "最高級技能變更券", "傳說技能變更券",
            "傳說技能選擇變更券", "技能變更保護券", "技能選擇變更券"
        ]:
            frame = tk.Frame(self.stats_inner_frame, bg="black")
            frame.pack(fill=tk.X)
            label = tk.Label(frame, text=f"{ticket_type}:", fg="white", bg="black", font=("Arial", self.base_font_size), anchor="w")
            label.pack(side=tk.LEFT, padx=self.base_padx)
            self.ticket_stats_labels[ticket_type] = tk.Label(frame, text="0 次", fg="white", bg="black", font=("Arial", self.base_font_size), anchor="w")
            self.ticket_stats_labels[ticket_type].pack(side=tk.LEFT)

        self.separator_label = tk.Label(self.combined_scrollable_frame, text="—" * 30, fg="white", bg="black", font=("Arial", self.base_font_size), anchor="w")
        self.separator_label.pack(anchor="w", pady=self.base_pady)

        self.prob_inner_frame = tk.Frame(self.combined_scrollable_frame, bg="black")
        self.prob_inner_frame.pack(fill=tk.X, pady=self.base_pady)

        self.legend_prob_title = tk.Label(self.prob_inner_frame, text="傳說技能機率:", fg="white", bg="black", font=("Arial", self.base_font_size, "bold"), anchor="w")
        self.legend_prob_title.pack(anchor="w")
        self.legend_prob_legend_frame = tk.Frame(self.prob_inner_frame, bg="black")
        self.legend_prob_legend_frame.pack(fill=tk.X)
        self.legend_prob_legend_label = tk.Label(self.legend_prob_legend_frame, text="傳說卡:", fg="white", bg="black", font=("Arial", self.base_font_size), anchor="w")
        self.legend_prob_legend_label.pack(side=tk.LEFT, padx=self.base_padx)
        self.probability_labels["legend_prob_legend_card"] = tk.Label(self.legend_prob_legend_frame, text="0.00%", fg="white", bg="black", font=("Arial", self.base_font_size), anchor="w")
        self.probability_labels["legend_prob_legend_card"].pack(side=tk.LEFT)
        self.legend_prob_other_frame = tk.Frame(self.prob_inner_frame, bg="black")
        self.legend_prob_other_frame.pack(fill=tk.X)
        self.legend_prob_other_label = tk.Label(self.legend_prob_other_frame, text="其他卡:", fg="white", bg="black", font=("Arial", self.base_font_size), anchor="w")
        self.legend_prob_other_label.pack(side=tk.LEFT, padx=self.base_padx)
        self.probability_labels["legend_prob_other_card"] = tk.Label(self.legend_prob_other_frame, text="0.00%", fg="white", bg="black", font=("Arial", self.base_font_size), anchor="w")
        self.probability_labels["legend_prob_other_card"].pack(side=tk.LEFT)

        self.level_sum_prob_title = tk.Label(self.prob_inner_frame, text="等級總和機率表:", fg="white", bg="black", font=("Arial", self.base_font_size, "bold"), anchor="w")
        self.level_sum_prob_title.pack(anchor="w", pady=self.base_pady)
        for level_sum in range(3, 10):
            frame = tk.Frame(self.prob_inner_frame, bg="black")
            frame.pack(fill=tk.X)
            label = tk.Label(frame, text=f"總和{level_sum}:", fg="white", bg="black", font=("Arial", self.base_font_size), anchor="w")
            label.pack(side=tk.LEFT, padx=self.base_padx)
            probability = LEVEL_SUM_PROB_DEFAULT[level_sum] * 100
            self.probability_labels[f"level_sum_{level_sum}"] = tk.Label(frame, text=f"{probability:.2f}%", fg="white", bg="black", font=("Arial", self.base_font_size), anchor="w")
            self.probability_labels[f"level_sum_{level_sum}"].pack(side=tk.LEFT)

        self.right_frame = tk.Frame(self.main_frame, bg="black")
        self.right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=self.base_padx, pady=self.base_pady)

        self.switch_frame = tk.Frame(self.right_frame, bg="black")
        self.switch_frame.pack(fill=tk.X, pady=self.base_pady)
        self.pitcher_switch_button = tk.Button(
            self.switch_frame,
            text="投手",
            command=self.show_pitcher,
            bg="#4CAF50",
            fg="white",
            width=self.base_button_width,
            font=("Arial", self.base_font_size)
        )
        self.pitcher_switch_button.pack(side=tk.LEFT, padx=self.base_padx)
        self.batter_switch_button = tk.Button(
            self.switch_frame,
            text="打者",
            command=self.show_batter,
            bg="#4CAF50",
            fg="white",
            width=self.base_button_width,
            font=("Arial", self.base_font_size)
        )
        self.batter_switch_button.pack(side=tk.LEFT, padx=self.base_padx)

        self.selection_frame = tk.Frame(self.right_frame, bg="black")
        self.selection_frame.pack(fill=tk.BOTH, expand=True, pady=self.base_pady)

        self.selection_canvas = tk.Canvas(self.selection_frame, bg="black")
        self.selection_scrollbar = tk.Scrollbar(self.selection_frame, orient=tk.VERTICAL, command=self.selection_canvas.yview)
        self.selection_scrollable_frame = tk.Frame(self.selection_canvas, bg="black")

        self.selection_scrollable_frame.bind(
            "<Configure>",
            lambda e: self.selection_canvas.configure(scrollregion=self.selection_canvas.bbox("all"))
        )

        self.selection_canvas.create_window((0, 0), window=self.selection_scrollable_frame, anchor="nw")
        self.selection_canvas.configure(yscrollcommand=self.selection_scrollbar.set)

        self.selection_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.selection_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 投手選擇
        self.pitcher_frame = tk.Frame(self.selection_scrollable_frame, bg="black")
        self.pitcher_frame.pack(fill=tk.X, padx=self.base_padx, pady=self.base_pady)
        self.pitcher_label = tk.Label(self.pitcher_frame, text="投手:", fg="white", bg="black", font=("Arial", self.base_font_size))
        self.pitcher_label.pack(anchor="nw")

        self.starter_frame = tk.Frame(self.pitcher_frame, bg="black")
        self.starter_frame.pack(fill=tk.X)
        self.starter_label = tk.Label(self.starter_frame, text="先發投手:", fg="white", bg="black", font=("Arial", self.base_font_size))
        self.starter_label.pack(anchor="nw")
        starter_positions = ["先發1", "先發2", "先發3", "先發4", "先發5"]
        self.starter_buttons_frame = tk.Frame(self.starter_frame, bg="black")
        self.starter_buttons_frame.pack()
        for i, pos in enumerate(starter_positions):
            button_frame = tk.Frame(self.starter_buttons_frame, bg="black")
            button_frame.grid(row=0, column=i, padx=self.base_padx, pady=self.base_pady)
            button = tk.Button(
                button_frame,
                image=self.pitcher_image,
                command=lambda p=pos: self.select_pitcher(p),
                bg="black",
                borderwidth=0,
                highlightthickness=0
            )
            button.pack()
            legend_label = tk.Label(
                button_frame,
                text="L",
                fg="white",
                bg="red",
                font=("Arial", 12, "bold"),
                width=2,
                height=1
            )
            legend_label.place(relx=0.0, rely=0.0, anchor="nw", x=5, y=5)
            legend_label.lower()
            self.pitcher_legend_labels[pos] = legend_label
            pos_label = tk.Label(
                button_frame,
                text=pos,
                fg="white",
                bg="black",
                font=("Arial", self.base_font_size - 2)
            )
            pos_label.pack()
            skill_labels = []
            for j in range(3):
                skill_label = tk.Label(
                    button_frame,
                    text="未設置",
                    fg="white",
                    bg="gray",
                    font=("Arial", self.base_font_size - 1),
                    width=14,
                    anchor="w"
                )
                skill_label.pack(fill=tk.X)
                skill_labels.append(skill_label)
            self.pitcher_skill_labels[pos] = skill_labels

        self.bullpen_frame = tk.Frame(self.pitcher_frame, bg="black")
        self.bullpen_frame.pack(fill=tk.X)
        self.bullpen_label = tk.Label(self.bullpen_frame, text="牛棚投手:", fg="white", bg="black", font=("Arial", self.base_font_size))
        self.bullpen_label.pack(anchor="nw")
        bullpen_positions = [
            "牛棚勝利組1", "牛棚勝利組2",
            "牛棚敗處組3", "牛棚敗處組4", "牛棚敗處組5",
            "長中繼1", "終結者1"
        ]
        self.bullpen_buttons_frame = tk.Frame(self.bullpen_frame, bg="black")
        self.bullpen_buttons_frame.pack()
        for i, pos in enumerate(bullpen_positions):
            button_frame = tk.Frame(self.bullpen_buttons_frame, bg="black")
            button_frame.grid(row=0, column=i, padx=self.base_padx, pady=self.base_pady)
            button = tk.Button(
                button_frame,
                image=self.pitcher_image,
                command=lambda p=pos: self.select_pitcher(p),
                bg="black",
                borderwidth=0,
                highlightthickness=0
            )
            button.pack()
            legend_label = tk.Label(
                button_frame,
                text="L",
                fg="white",
                bg="red",
                font=("Arial", 12, "bold"),
                width=2,
                height=1
            )
            legend_label.place(relx=0.0, rely=0.0, anchor="nw", x=5, y=5)
            legend_label.lower()
            self.pitcher_legend_labels[pos] = legend_label
            pos_label = tk.Label(
                button_frame,
                text=pos,
                fg="white",
                bg="black",
                font=("Arial", self.base_font_size - 2)
            )
            pos_label.pack()
            skill_labels = []
            for j in range(3):
                skill_label = tk.Label(
                    button_frame,
                    text="未設置",
                    fg="white",
                    bg="gray",
                    font=("Arial", self.base_font_size - 1),
                    width=14,
                    anchor="w"
                )
                skill_label.pack(fill=tk.X)
                skill_labels.append(skill_label)
            self.pitcher_skill_labels[pos] = skill_labels

        # 打者選擇
        self.batter_frame = tk.Frame(self.selection_scrollable_frame, bg="black")
        self.batter_frame.pack(fill=tk.X, padx=self.base_padx, pady=self.base_pady)
        self.batter_label = tk.Label(self.batter_frame, text="打者:", fg="white", bg="black", font=("Arial", self.base_font_size))
        self.batter_label.pack(anchor="nw")

        self.batting_frame = tk.Frame(self.batter_frame, bg="black")
        self.batting_frame.pack(fill=tk.X)
        self.batting_label = tk.Label(self.batting_frame, text="打序:", fg="white", bg="black", font=("Arial", self.base_font_size))
        self.batting_label.pack(anchor="nw")
        batting_positions = ["1棒", "2棒", "3棒", "4棒", "5棒", "6棒", "7棒", "8棒", "9棒"]
        self.batting_buttons_frame = tk.Frame(self.batting_frame, bg="black")
        self.batting_buttons_frame.pack()
        defensive_positions = [pos.value for pos in DefensivePosition]
        for i, pos in enumerate(batting_positions):
            button_frame = tk.Frame(self.batting_buttons_frame, bg="black")
            button_frame.grid(row=i//5, column=i%5, padx=self.base_padx, pady=self.base_pady)
            button = tk.Button(
                button_frame,
                image=self.batter_image,
                command=lambda p=pos: self.select_batter(p),
                bg="black",
                borderwidth=0,
                highlightthickness=0
            )
            button.pack()
            legend_label = tk.Label(
                button_frame,
                text="L",
                fg="white",
                bg="red",
                font=("Arial", 12, "bold"),
                width=2,
                height=1
            )
            legend_label.place(relx=0.0, rely=0.0, anchor="nw", x=5, y=5)
            legend_label.lower()
            self.batter_legend_labels[pos] = legend_label
            pos_label = tk.Label(
                button_frame,
                text=pos,
                fg="white",
                bg="black",
                font=("Arial", self.base_font_size - 2)
            )
            pos_label.pack()
            position_var = tk.StringVar()
            position_combobox = ttk.Combobox(
                button_frame,
                textvariable=position_var,
                values=defensive_positions,
                state="readonly",
                width=5,
                font=("Arial", self.base_font_size - 2)
            )
            position_combobox.pack()
            position_combobox.bind("<<ComboboxSelected>>", lambda event, p=pos: self.update_defensive_position(p))
            self.batter_position_comboboxes[pos] = (position_var, position_combobox)
            skill_labels = []
            for j in range(3):
                skill_label = tk.Label(
                    button_frame,
                    text="未設置",
                    fg="white",
                    bg="gray",
                    font=("Arial", self.base_font_size - 1),
                    width=14,
                    anchor="w"
                )
                skill_label.pack(fill=tk.X)
                skill_labels.append(skill_label)
            self.batter_skill_labels[pos] = skill_labels

        self.sub_frame = tk.Frame(self.batter_frame, bg="black")
        self.sub_frame.pack(fill=tk.X)
        self.sub_label = tk.Label(self.sub_frame, text="候補:", fg="white", bg="black", font=("Arial", self.base_font_size))
        self.sub_label.pack(anchor="nw")
        sub_positions = ["候補1", "候補2", "候補3", "候補4", "候補5"]
        self.sub_buttons_frame = tk.Frame(self.sub_frame, bg="black")
        self.sub_buttons_frame.pack()
        for i, pos in enumerate(sub_positions):
            button_frame = tk.Frame(self.sub_buttons_frame, bg="black")
            button_frame.grid(row=0, column=i, padx=self.base_padx, pady=self.base_pady)
            button = tk.Button(
                button_frame,
                image=self.batter_image,
                command=lambda p=pos: self.select_batter(p),
                bg="black",
                borderwidth=0,
                highlightthickness=0
            )
            button.pack()
            legend_label = tk.Label(
                button_frame,
                text="L",
                fg="white",
                bg="red",
                font=("Arial", 12, "bold"),
                width=2,
                height=1
            )
            legend_label.place(relx=0.0, rely=0.0, anchor="nw", x=5, y=5)
            legend_label.lower()
            self.batter_legend_labels[pos] = legend_label
            pos_label = tk.Label(
                button_frame,
                text=pos,
                fg="white",
                bg="black",
                font=("Arial", self.base_font_size - 2)
            )
            pos_label.pack()
            position_var = tk.StringVar()
            position_combobox = ttk.Combobox(
                button_frame,
                textvariable=position_var,
                values=defensive_positions,
                state="readonly",
                width=5,
                font=("Arial", self.base_font_size - 2)
            )
            position_combobox.pack()
            position_combobox.bind("<<ComboboxSelected>>", lambda event, p=pos: self.update_defensive_position(p))
            self.batter_position_comboboxes[pos] = (position_var, position_combobox)
            skill_labels = []
            for j in range(3):
                skill_label = tk.Label(
                    button_frame,
                    text="未設置",
                    fg="white",
                    bg="gray",
                    font=("Arial", self.base_font_size - 1),
                    width=14,
                    anchor="w"
                )
                skill_label.pack(fill=tk.X)
                skill_labels.append(skill_label)
            self.batter_skill_labels[pos] = skill_labels

        self.button_frame = tk.Frame(self.right_frame, bg="black")
        self.button_frame.pack(fill=tk.X, pady=self.base_pady)

        self.simulate_button = tk.Button(self.button_frame, text="使用", command=self.simulate, bg="#2196F3", fg="white", width=self.base_button_width, font=("Arial", self.base_font_size))
        self.simulate_button.pack(side=tk.LEFT, padx=self.base_padx)
        self.reset_all_button = tk.Button(self.button_frame, text="全部重置", command=self.reset_all, bg="#FF5722", fg="white", width=self.base_button_width, font=("Arial", self.base_font_size))
        self.reset_all_button.pack(side=tk.LEFT, padx=self.base_padx)
        self.reset_single_button = tk.Button(self.button_frame, text="單一重置", command=self.reset_single_player, bg="#FF9800", fg="white", width=self.base_button_width, font=("Arial", self.base_font_size))
        self.reset_single_button.pack(side=tk.LEFT, padx=self.base_padx)
        self.quit_button = tk.Button(self.button_frame, text="停止", command=self.root.quit, bg="#F44336", fg="white", width=self.base_button_width, font=("Arial", self.base_font_size))
        self.quit_button.pack(side=tk.LEFT, padx=self.base_padx)

        self.simulation_count_input_label = tk.Label(self.button_frame, text="模擬次數:", fg="white", bg="black", font=("Arial", self.base_font_size))
        self.simulation_count_input_label.pack(side=tk.LEFT, padx=self.base_padx)
        self.simulation_entry = tk.Entry(self.button_frame, width=10, font=("Arial", self.base_font_size))
        self.simulation_entry.pack(side=tk.LEFT, padx=self.base_padx)
        self.simulation_limit_label = tk.Label(self.button_frame, text=f"(上限 {MAX_SIMULATION_LIMIT} 次)", fg="white", bg="black", font=("Arial", self.base_font_size))
        self.simulation_limit_label.pack(side=tk.LEFT, padx=self.base_padx)
        self.simulate_multiple_button = tk.Button(self.button_frame, text="一鍵模擬多次", command=self.simulate_multiple, bg="#FFC107", fg="black", width=self.base_button_width, font=("Arial", self.base_font_size))
        self.simulate_multiple_button.pack(side=tk.LEFT, padx=self.base_padx)
        self.stop_button = tk.Button(self.button_frame, text="停止模擬", command=self.stop_simulation, bg="#F44336", fg="white", width=self.base_button_width, font=("Arial", self.base_font_size))
        self.stop_button.pack_forget()

        self.options_frame = tk.Frame(self.right_frame, bg="black")
        self.options_frame.pack(fill=tk.X, pady=self.base_pady)

        self.ticket_frame = tk.Frame(self.options_frame, bg="black")
        self.ticket_frame.pack(side=tk.LEFT, padx=self.base_padx)
        self.ticket_label = tk.Label(self.ticket_frame, text="變更券:", fg="white", bg="black", font=("Arial", self.base_font_size))
        self.ticket_label.pack(side=tk.LEFT)
        self.ticket_var = tk.StringVar()
        self.ticket_combobox = ttk.Combobox(self.ticket_frame, textvariable=self.ticket_var, state="readonly", font=("Arial", self.base_font_size), width=15)
        self.ticket_combobox["values"] = [
            "技能變更券", "高級技能變更券", "最高級技能變更券", "傳說技能變更券",
            "傳說技能選擇變更券", "技能變更保護券", "技能選擇變更券"
        ]
        self.ticket_combobox.pack(side=tk.LEFT)
        self.ticket_combobox.bind("<<ComboboxSelected>>", self.update_slot_selection)

        self.slot_frame = tk.Frame(self.options_frame, bg="black")
        self.slot_frame.pack(side=tk.LEFT, padx=self.base_padx)
        self.slot_label = tk.Label(self.slot_frame, text="", fg="white", bg="black", font=("Arial", self.base_font_size))
        self.slot_label.pack(side=tk.LEFT)
        self.slot_var = tk.IntVar(value=1)
        self.slot_radio1 = tk.Radiobutton(self.slot_frame, text="技能1", variable=self.slot_var, value=1, fg="white", bg="black", selectcolor="black", font=("Arial", self.base_font_size))
        self.slot_radio1.pack(side=tk.LEFT)
        self.slot_radio2 = tk.Radiobutton(self.slot_frame, text="技能2", variable=self.slot_var, value=2, fg="white", bg="black", selectcolor="black", font=("Arial", self.base_font_size))
        self.slot_radio2.pack(side=tk.LEFT)
        self.slot_radio3 = tk.Radiobutton(self.slot_frame, text="技能3", variable=self.slot_var, value=3, fg="white", bg="black", selectcolor="black", font=("Arial", self.base_font_size))
        self.slot_radio3.pack(side=tk.LEFT)
        self.slot_frame.pack_forget()

    def show_pitcher(self):
        self.pitcher_frame.pack(fill=tk.X, padx=self.base_padx, pady=self.base_pady)
        self.batter_frame.pack_forget()
        self.pitcher_switch_button.config(bg="#4CAF50")
        self.batter_switch_button.config(bg="#2196F3")

    def show_batter(self):
        self.batter_frame.pack(fill=tk.X, padx=self.base_padx, pady=self.base_pady)
        self.pitcher_frame.pack_forget()
        self.batter_switch_button.config(bg="#4CAF50")
        self.pitcher_switch_button.config(bg="#2196F3")

    def update_legend_label(self, position, is_legend):
        labels = self.pitcher_legend_labels.get(position) or self.batter_legend_labels.get(position)
        if labels:
            if is_legend:
                labels.lift()
            else:
                labels.lower()

    def check_position_conflict(self, position_str, selected_position):
        batting_positions = ["1棒", "2棒", "3棒", "4棒", "5棒", "6棒", "7棒", "8棒", "9棒"]
        if position_str not in batting_positions:
            return True
        if not selected_position:
            return True
        used_positions = set()
        for pos in batting_positions:
            if pos == position_str:
                continue
            player = self.players.get(pos)
            if player and player.defensive_position:
                used_positions.add(player.defensive_position)
        return selected_position not in used_positions

    def update_defensive_position(self, position_str):
        position_var, _ = self.batter_position_comboboxes[position_str]
        selected_position = position_var.get()
        if not selected_position:
            if self.players.get(position_str):
                self.players[position_str].defensive_position = None
            return
        if not self.check_position_conflict(position_str, selected_position):
            messagebox.showwarning("警告", f"守備位置 {selected_position} 已被其他 1-9 棒使用，請選擇其他位置！")
            position_var.set("")
            if self.players.get(position_str):
                self.players[position_str].defensive_position = None
            return
        defensive_position_map = {pos.value: pos for pos in DefensivePosition}
        if self.players.get(position_str):


            self.players[position_str].defensive_position = defensive_position_map.get(selected_position)

    def select_pitcher(self, position_str):
        position_map = {
            "先發1": PitcherPosition.STARTER_1,
            "先發2": PitcherPosition.STARTER_2,
            "先發3": PitcherPosition.STARTER_3,
            "先發4": PitcherPosition.STARTER_4,
            "先發5": PitcherPosition.STARTER_5,
            "牛棚勝利組1": PitcherPosition.BULLPEN_WIN_1,
            "牛棚勝利組2": PitcherPosition.BULLPEN_WIN_2,
            "牛棚敗處組3": PitcherPosition.BULLPEN_LOSE_3,
            "牛棚敗處組4": PitcherPosition.BULLPEN_LOSE_4,
            "牛棚敗處組5": PitcherPosition.BULLPEN_LOSE_5,
            "長中繼1": PitcherPosition.LONG_RELIEF,
            "終結者1": PitcherPosition.CLOSER
        }
        position = position_map[position_str]
        is_legend = messagebox.askyesno("傳說球員", f"是否將 {position_str} 設為傳說球員？")
        if position_str not in self.players:
            self.players[position_str] = Player(
                PlayerType.PITCHER,
                position,
                is_legend,
                is_black_diamond=True
            )
        else:
            self.players[position_str].is_legend = is_legend
        self.player = self.players[position_str]
        self.update_legend_label(position_str, is_legend)
        self.update_player_skill_label(position_str, self.player.skills)
        self.update_stats()
        self.simulate_button.config(state="normal")

    def select_batter(self, position_str):
        position_map = {
            "1棒": BatterPosition.BATTING_1,
            "2棒": BatterPosition.BATTING_2,
            "3棒": BatterPosition.BATTING_3,
            "4棒": BatterPosition.BATTING_4,
            "5棒": BatterPosition.BATTING_5,
            "6棒": BatterPosition.BATTING_6,
            "7棒": BatterPosition.BATTING_7,
            "8棒": BatterPosition.BATTING_8,
            "9棒": BatterPosition.BATTING_9,
            "候補1": BatterPosition.SUB_1,
            "候補2": BatterPosition.SUB_2,
            "候補3": BatterPosition.SUB_3,
            "候補4": BatterPosition.SUB_4,
            "候補5": BatterPosition.SUB_5
        }
        position = position_map[position_str]
        is_legend = messagebox.askyesno("傳說球員", f"是否將 {position_str} 設為傳說球員？")
        if position_str not in self.players:
            self.players[position_str] = Player(
                PlayerType.BATTER,
                position,
                is_legend,
                is_black_diamond=True
            )
        else:
            self.players[position_str].is_legend = is_legend
        self.player = self.players[position_str]
        self.update_legend_label(position_str, is_legend)
        self.update_player_skill_label(position_str, self.player.skills)
        self.update_stats()
        self.simulate_button.config(state="normal")
        position_var, _ = self.batter_position_comboboxes[position_str]
        if self.player.defensive_position:
            position_var.set(self.player.defensive_position.value)
        else:
            position_var.set("")

    def update_player_skill_label(self, position, skills):
        labels = self.pitcher_skill_labels.get(position) or self.batter_skill_labels.get(position)
        if labels:
            for i, skill in enumerate(skills):
                text = f"{skill if skill else '未設置'}"
                bg_color = self.get_skill_background(skill)
                labels[i].config(text=text, bg=bg_color)

    def update_slot_selection(self, event=None):
        ticket_type = self.ticket_var.get()
        if ticket_type in ["技能變更保護券", "技能選擇變更券"]:
            self.slot_frame.pack()
            if ticket_type == "技能變更保護券":
                self.slot_label.config(text="需要保護變更的技能:")
            elif ticket_type == "技能選擇變更券":
                self.slot_label.config(text="需要選擇變更的技能:")
        else:
            self.slot_frame.pack_forget()

        legend_prob_legend_card = LEGEND_PROBABILITIES["傳說卡"].get(ticket_type, 0.0) * 100
        legend_prob_other_card = LEGEND_PROBABILITIES["其他卡"].get(ticket_type, 0.0) * 100
        self.probability_labels["legend_prob_legend_card"].config(text=f"{legend_prob_legend_card:.2f}%")
        self.probability_labels["legend_prob_other_card"].config(text=f"{legend_prob_other_card:.2f}%")

        if ticket_type == "最高級技能變更券":
            level_sum_prob = LEVEL_SUM_PROB_SUPER
        else:
            level_sum_prob = LEVEL_SUM_PROB_DEFAULT
        for level_sum in range(3, 10):
            probability = level_sum_prob[level_sum] * 100
            self.probability_labels[f"level_sum_{level_sum}"].config(text=f"{probability:.2f}%")

    def get_skill_background(self, skill):
        if skill is None:
            return "gray"
        if skill.tier == SkillTier.LEGEND:
            return "#000000"
        elif skill.tier == SkillTier.GOLD:
            return "#FFD700"
        elif skill.tier == SkillTier.SILVER:
            return "#808080"
        elif skill.tier == SkillTier.BRONZE:
            return "#8B4513"
        return "gray"

    def update_stats(self):
        if not self.player:
            return
        self.stats_labels["simulation_count"].config(text=f"{self.player.simulation_count} 次")
        probability = (self.player.legend_count / self.player.simulation_count * 100) if self.player.simulation_count > 0 else 0
        self.stats_labels["legend_count"].config(text=f"{self.player.legend_count} 次 ({probability:.2f}%)")
        for level_sum in range(3, 10):
            count = self.player.level_sum_stats.get(level_sum, 0)
            probability = (count / self.player.level_sum_count * 100) if self.player.level_sum_count > 0 else 0
            self.stats_labels[f"level_sum_{level_sum}"].config(text=f"{count} 次 ({probability:.2f}%)")
        for ticket_type, count in self.player.ticket_usage_stats.items():
            self.ticket_stats_labels[ticket_type].config(text=f"{count} 次")

    def show_skill_comparison(self, before_skills, after_skills, ticket_type, position_str):
        comparison_window = tk.Toplevel(self.root)
        comparison_window.title("技能變更比較")
        comparison_window.geometry("400x500")
        comparison_window.resizable(False, False)
        comparison_window.configure(bg="black")

        self.skill_selected = False

        def on_closing():
            if not self.skill_selected:
                messagebox.showwarning("警告", "請選擇技能！")
                return
            comparison_window.destroy()

        comparison_window.protocol("WM_DELETE_WINDOW", on_closing)

        main_frame = tk.Frame(comparison_window, bg="black")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        before_frame = tk.Frame(main_frame, bg="black", width=200)
        before_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5)
        before_frame.pack_propagate(False)

        before_image_frame = tk.Frame(before_frame, bg="black")
        before_image_frame.pack(pady=5)
        player_image = self.pitcher_image if self.player.player_type == PlayerType.PITCHER else self.batter_image
        before_image_label = tk.Label(before_image_frame, image=player_image, bg="black")
        before_image_label.pack()
        before_legend_label = tk.Label(
            before_image_frame,
            text="L",
            fg="white",
            bg="red",
            font=("Arial", 12, "bold"),
            width=2,
            height=1
        )
        before_legend_label.place(relx=0.0, rely=0.0, anchor="nw", x=5, y=5)
        if self.player.is_legend:
            before_legend_label.lift()
        else:
            before_legend_label.lower()
        before_pos_label = tk.Label(
            before_image_frame,
            text=position_str,
            fg="white",
            bg="black",
            font=("Arial", self.base_font_size - 2)
        )
        before_pos_label.pack()

        tk.Label(before_frame, text="使用前:", fg="white", bg="black", font=("Arial", 12, "bold")).pack(anchor="w")
        for i, skill in enumerate(before_skills):
            skill_text = f"技能{i+1}: {skill if skill else '未設置'}"
            bg_color = self.get_skill_background(skill)
            tk.Label(before_frame, text=skill_text, fg="white", bg=bg_color, font=("Arial", 12), anchor="w").pack(fill=tk.X, pady=2)

        after_frame = tk.Frame(main_frame, bg="black", width=200)
        after_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5)
        after_frame.pack_propagate(False)

        after_image_frame = tk.Frame(after_frame, bg="black")
        after_image_frame.pack(pady=5)
        after_image_label = tk.Label(after_image_frame, image=player_image, bg="black")
        after_image_label.pack()
        after_legend_label = tk.Label(
            after_image_frame,
            text="L",
            fg="white",
            bg="red",
            font=("Arial", 12, "bold"),
            width=2,
            height=1
        )
        after_legend_label.place(relx=0.0, rely=0.0, anchor="nw", x=5, y=5)
        if self.player.is_legend:
            after_legend_label.lift()
        else:
            after_legend_label.lower()
        after_pos_label = tk.Label(
            after_image_frame,
            text=position_str,
            fg="white",
            bg="black",
            font=("Arial", self.base_font_size - 2)
        )
        after_pos_label.pack()

        tk.Label(after_frame, text="使用後:", fg="white", bg="black", font=("Arial", 12, "bold")).pack(anchor="w")
        for i, skill in enumerate(after_skills):
            skill_text = f"技能{i+1}: {skill if skill else '未設置'}"
            bg_color = self.get_skill_background(skill)
            tk.Label(after_frame, text=skill_text, fg="white", bg=bg_color, font=("Arial", 12), anchor="w").pack(fill=tk.X, pady=2)

        button_frame = tk.Frame(comparison_window, bg="black")
        button_frame.pack(fill=tk.X, pady=10)
        tk.Button(
            button_frame,
            text="使用前",
            command=lambda: self.apply_skills(before_skills, ticket_type, position_str, comparison_window),
            bg="#FF5722",
            fg="white",
            font=("Arial", 12)
        ).pack(side=tk.LEFT, padx=5)
        tk.Button(
            button_frame,
            text="使用後",
            command=lambda: self.apply_skills(after_skills, ticket_type, position_str, comparison_window),
            bg="#4CAF50",
            fg="white",
            font=("Arial", 12)
        ).pack(side=tk.LEFT, padx=5)

    def apply_skills(self, selected_skills, ticket_type, position_str, window):
        self.skill_selected = True
        for i, skill in enumerate(selected_skills):
            self.player.set_skill(i, skill)
        self.update_player_skill_label(position_str, self.player.skills)
        if ticket_type in ["高級技能變更券", "最高級技能變更券"]:
            self.update_stats()
        window.destroy()
        self.simulate_button.config(state="normal")

    def simulate(self):
        if not self.player:
            messagebox.showwarning("警告", "請先選擇投手或打者！")
            return

        ticket_type = self.ticket_var.get()
        if not ticket_type:
            messagebox.showwarning("警告", "請選擇變更券類型！")
            return

        if ticket_type == "傳說技能選擇變更券" and not self.player.has_legend_skill():
            messagebox.showwarning("警告", "此變更券僅能在擁有傳說技能時使用！")
            return

        if ticket_type in ["技能變更保護券", "技能選擇變更券"] and not any(self.player.skills):
            skills_db = BATTER_SKILLS if self.player.player_type == PlayerType.BATTER else PITCHER_SKILLS
            all_skills = []
            for tier in [SkillTier.BRONZE, SkillTier.SILVER, SkillTier.GOLD]:
                all_skills.extend([(name, tier) for name in skills_db[tier]])
            for slot in range(3):
                skill_name, skill_tier = random.choice(all_skills)
                level = 3 if self.player.is_legend else get_skill_level(self.player.is_legend)
                self.player.set_skill(slot, Skill(skill_name, skill_tier, level))
                all_skills.remove((skill_name, skill_tier))

        protected_slot = None
        if ticket_type in ["技能變更保護券", "技能選擇變更券"]:
            protected_slot = self.slot_var.get() - 1
            if protected_slot not in [0, 1, 2]:
                messagebox.showwarning("警告", "請選擇有效的技能（技能1-技能3）！")
                return

        self.simulate_button.config(state="disabled")

        try:
            before_skills = self.player.skills.copy()
            skills = simulate_skill_change(self.player, ticket_type, protected_slot)
            self.player.ticket_usage_stats[ticket_type] += 1
            if ticket_type in ["高級技能變更券", "最高級技能變更券"]:
                self.player.simulation_count += 1
                if skills[0] and skills[0].tier == SkillTier.LEGEND:
                    self.player.legend_count += 1
                level_sum = sum(skill.level for skill in skills if skill)
                if level_sum in self.player.level_sum_stats:
                    self.player.level_sum_stats[level_sum] += 1
                self.player.level_sum_count += 1

            position_str = self.player.position.value
            if ticket_type == "傳說技能選擇變更券":
                self.show_skill_comparison(before_skills, skills, ticket_type, position_str)
            else:
                for i, skill in enumerate(skills):
                    self.player.set_skill(i, skill)
                self.update_player_skill_label(position_str, self.player.skills)
                self.update_stats()
                self.simulate_button.config(state="normal")

        except ValueError as e:
            messagebox.showerror("錯誤", str(e))
            self.simulate_button.config(state="normal")
            return

    def simulate_multiple(self):
        if not self.player:
            messagebox.showwarning("警告", "請先選擇投手或打者！")
            return

        ticket_type = self.ticket_var.get()
        if not ticket_type:
            messagebox.showwarning("警告", "請選擇變更券類型！")
            return

        if ticket_type == "傳說技能選擇變更券" and not self.player.has_legend_skill():
            messagebox.showwarning("警告", "此變更券僅能在擁有傳說技能時使用！")
            return

        try:
            num_simulations = int(self.simulation_entry.get())
            if num_simulations <= 0:
                messagebox.showwarning("警告", "模擬次數必須大於 0！")
                return
            if num_simulations > MAX_SIMULATION_LIMIT:
                messagebox.showwarning("警告", f"模擬次數不得超過系統上限 {MAX_SIMULATION_LIMIT} 次！")
                return
        except ValueError:
            messagebox.showwarning("警告", "請輸入有效的模擬次數（整數）！")
            return

        self.is_simulating = True
        self.stop_button.pack(side=tk.LEFT, padx=self.base_padx)
        self.simulate_multiple_button.config(state="disabled")

        for i in range(num_simulations):
            if not self.is_simulating:
                break
            self.player.ticket_usage_stats[ticket_type] += 1
            self.simulate()
            self.root.update()

        self.is_simulating = False
        self.stop_button.pack_forget()
        self.simulate_multiple_button.config(state="normal")

    def stop_simulation(self):
        self.is_simulating = False

    def reset_all(self):
        for player in self.players.values():
            player.simulation_count = 0
            player.legend_count = 0
            player.level_sum_stats = {3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}
            player.level_sum_count = 0
            player.ticket_usage_stats = {ticket: 0 for ticket in player.ticket_usage_stats}
            for i in range(3):
                player.set_skill(i, None)
            player.defensive_position = None

        self.player = None
        for pos in self.pitcher_skill_labels:
            for label in self.pitcher_skill_labels[pos]:
                label.config(text="未設置", bg="gray")
            self.pitcher_legend_labels[pos].lower()
        for pos in self.batter_skill_labels:
            for label in self.batter_skill_labels[pos]:
                label.config(text="未設置", bg="gray")
            self.batter_legend_labels[pos].lower()
            position_var, _ = self.batter_position_comboboxes[pos]
            position_var.set("")
        self.update_stats()
        self.probability_labels["legend_prob_legend_card"].config(text="0.00%")
        self.probability_labels["legend_prob_other_card"].config(text="0.00%")
        self.simulate_button.config(state="disabled")

    def reset_single_player(self):
        if not self.player:
            messagebox.showwarning("警告", "請先選擇投手或打者！")
            return
        position_str = self.player.position.value
        self.player.simulation_count = 0
        self.player.legend_count = 0
        self.player.level_sum_stats = {3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}
        self.player.level_sum_count = 0
        self.player.ticket_usage_stats = {ticket: 0 for ticket in self.player.ticket_usage_stats}
        for i in range(3):
            self.player.set_skill(i, None)
        self.player.defensive_position = None
        labels = self.pitcher_skill_labels.get(position_str) or self.batter_skill_labels.get(position_str)
        if labels:
            for label in labels:
                label.config(text="未設置", bg="gray")
        self.update_legend_label(position_str, self.player.is_legend)
        if position_str in self.batter_position_comboboxes:
            position_var, _ = self.batter_position_comboboxes[position_str]
            position_var.set("")
        self.update_stats()

def main():
    root = tk.Tk()
    root.geometry("1480x800")
    app = MLBSkillSimulatorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()