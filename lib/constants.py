from config.parser import JsonCache

art = JsonCache.read_json("art")
resources = JsonCache.read_json("resources")

class Constants:
    # emotes
    EMOTES_GUILD_ID = 1038051105642401812
    
    # color scheme
    COLOR_DEFAULT = int(0xFF8C00)
    COLOR_WARNING = int(0xFF7600)
    COLOR_ERROR = int(0xFF4500)
    
    # strings
    STRINGS = JsonCache.read_json("strings")
    
    # repository
    REPO_URL = "https://git.wlinator.org/Luminara/Lumi"
    INVITE_LINK = "https://discord.com/oauth2/authorize?client_id=1038050427272429588&permissions=8&scope=bot"
    
    # KRC
    KRC_GUILD_ID: int = 719227135151046699
    KRC_INTRO_CHANNEL_ID: int = 973619250507972618
    KRC_QUESTION_MAPPING: dict[str, str] = resources["guild_specific"]["question_mapping"]
    
    # logo
    LUMI_LOGO_TRANSPARENT = art["logo"]["transparent"]
    LUMI_LOGO_OPAQUE = art["logo"]["opaque"]
    
    # icons art
    BOOST_ICON = art["icons"]["boost"]
    CHECK_ICON = art["icons"]["check"]
    CROSS_ICON = art["icons"]["cross"]
    EXCLAIM_ICON = art["icons"]["exclaim"]
    HAMMER_ICON = art["icons"]["hammer"]
    MONEY_BAG_ICON = art["icons"]["money_bag"]
    MONEY_COINS_ICON = art["icons"]["money_coins"]
    QUESTION_ICON = art["icons"]["question"]
    STREAK_ICON = art["icons"]["streak"]
    WARNING_ICON = art["icons"]["warning"]
    
    # birthdays
    BIRTHDAY_MESSAGES = JsonCache.read_json("birthday")["birthday_messages"]
    BIRTHDAY_MONTHS = JsonCache.read_json("birthday")["months"]
    
    # economy
    
    

CONST = Constants()
