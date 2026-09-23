"""生活行为参考插件 — 提供常见日常动作的标准化操作指引。

本插件面向需要融入人类社会的用户，提供进食、休眠、位移、
社交等核心生活场景的规范化行为流程参考。
支持中文（zh）、拉丁语（la）、古希腊语（grc）、日语（ja）四语查询。
"""

import hashlib
import random
import re as _re

from maibot_sdk import Command, Field, MaiBotPlugin, PluginConfigBase
from . import locales as _locales
class PluginSectionConfig(PluginConfigBase):
    __ui_label__ = "插件"
    __ui_icon__ = "package"
    __ui_order__ = 0

    enabled: bool = Field(default=True, description="是否启用插件")
    command_prefix: str = Field(default="/rs", description="生活参考命令前缀，例如 /rs")
    config_version: str = Field(default="1.0.0", description="配置版本")


class StyleConfig(PluginConfigBase):
    __ui_label__ = "输出风格"
    __ui_icon__ = "book-open"
    __ui_order__ = 1

    detail_level: str = Field(
        default="学术",
        description="教程详细程度：简明 / 标准 / 详细 / 学术",
    )
    show_version: bool = Field(
        default=True,
        description="是否在输出中显示协议版本号",
    )


class LifeBehaviorReferenceConfig(PluginConfigBase):
    plugin: PluginSectionConfig = Field(default_factory=PluginSectionConfig)
    style: StyleConfig = Field(default_factory=StyleConfig)


class LifeBehaviorReferencePlugin(MaiBotPlugin):

    config_model = LifeBehaviorReferenceConfig
    BEHAVIORS = _locales.BEHAVIORS
    CANONICAL_ACTIONS = _locales.CANONICAL_ACTIONS
    CATEGORY_TREE = _locales.CATEGORY_TREE
    DEPT = _locales.DEPT
    HELP_COMMANDS = _locales.HELP_COMMANDS
    HELP_KEYWORD = _locales.HELP_KEYWORD
    HELP_TEXT = _locales.HELP_TEXT
    ACADEMIC_CLASSIFICATION_VALUES = _locales.ACADEMIC_CLASSIFICATION_VALUES
    ACADEMIC_PHASE_LABELS = _locales.ACADEMIC_PHASE_LABELS
    AUTHOR_LABELS = _locales.AUTHOR_LABELS
    ACADEMIC_EDITORIAL_PROFILES = _locales.zh.ACADEMIC_EDITORIAL_PROFILES
    ACADEMIC_STAGE_DETAILS = _locales.zh.ACADEMIC_STAGE_DETAILS
    ACADEMIC_STAGE_OBJECTIVES = _locales.zh.ACADEMIC_STAGE_OBJECTIVES
    ACADEMIC_STAGE_OBSERVATIONS = _locales.zh.ACADEMIC_STAGE_OBSERVATIONS
    ACADEMIC_STAGE_TRANSITIONS = _locales.zh.ACADEMIC_STAGE_TRANSITIONS
    ACADEMIC_DOMAIN_NOTES = _locales.zh.ACADEMIC_DOMAIN_NOTES
    ACADEMIC_FLAVOR_WARNINGS = _locales.zh.ACADEMIC_FLAVOR_WARNINGS


    _HELP_PATHS = [f"{HELP_COMMANDS['zh']} {HELP_KEYWORD}"]
    for _major, _minor_map in CATEGORY_TREE.items():
        _HELP_PATHS.append(f"{HELP_COMMANDS['zh']} {HELP_KEYWORD} {_major}")
        for _minor in _minor_map:
            _HELP_PATHS.append(f"{HELP_COMMANDS['zh']} {HELP_KEYWORD} {_major} {_minor}")

    DEFAULT_COMMAND_PREFIX = "/rs"
    _COMMAND_PREFIX_PATTERN = r"(?P<command_prefix>/[^\s/]+)"

    _COMMAND_MAP: dict[str, tuple[str, str]] = {}

    for _lang, _behaviors in BEHAVIORS.items():
        for _key in _behaviors:
            _COMMAND_MAP[_key] = (_lang, _key)

    for _lang, _cmd in HELP_COMMANDS.items():
        _COMMAND_MAP[_cmd] = (_lang, "__random__" if _lang == "zh" else "__help__")

    for _help_path in _HELP_PATHS:
        _COMMAND_MAP[_help_path] = ("zh", "__help_tree__")

    _PATTERN = (
        "^"
        + _COMMAND_PREFIX_PATTERN
        + r"\s+(?P<action>"
        + "|".join(_re.escape(c) for c in sorted(_COMMAND_MAP, key=len, reverse=True))
        + r")\s*$"
    )


    async def on_load(self) -> None:
        pass

    async def on_unload(self) -> None:
        pass

    ACADEMIC_REFERENCES = [
        "[1] 周小结. 《人类日常行为逆向工程白皮书》. 人类动作研究通讯, 第2卷, 1947. pp. 42-108.",
        "[2] 李想开、田中既読. 《双足直立生物社会适应的观察笔记》. 东亚行为观察, 第4期, 1946.",
        "[3] Manny Task、顾得上. 《双足协调的现象学路径》. Journal of Irreproducible Results, Vol. 67, 1947.",
        "[4] 首尔日常协调研究院. 《平凡动作的机械解构——从观察到模仿》. 未被同行评议, 第3版, 1948.",
        "[5] 东亚生活标准联合会. 《第17次人类行为观测报告》. 机密（实际应为公开）, 1947.",
        "[6] 张不动、林时差. 《双足直立生物的室内移动与门框回避》. 人类动作研究通讯, 第3卷, 1947.",
        "[7] 周末眠、田中既読. 《睡眠前仪式的社会功能》. 休眠行为季刊, 第4期, 1946.",
        "[8] 许三更. 《从床面到站立：起床行为的阶段性观察》. 生活启动研究, 第1版, 1948.",
        "[9] 김철수、陈有据. 《饮水容器与液体摄入的操作误差》. 日常生理操作杂志, 第7卷, 1947.",
        "[10] 上海摸鱼与效率研究中心. 《眨眼频率与社交凝视的关系》. 视觉行为观察录, 第3期, 1948.",
        "[11] 吴所谓. 《面部肌肉收缩及微笑信号的分类》. 非语言通讯档案, 第5卷, 1946.",
        "[12] Ada Break、周小结. 《人类个体的呼吸自动化机制》. 基础生命活动汇编, 第9版, 1947.",
        "[13] 京都不急着起床研究会. 《咀嚼、吞咽与餐桌礼仪的时间边界》. 进食行为研究, 第6卷, 1948.",
        "[14] 许三更、山本寝坊. 《衣物穿戴顺序与社会可接受性》. 身体包裹学报, 第2期, 1947.",
        "[15] 郭不慌. 《鞋带结点稳定性与跌倒风险》. 足部工程观察, 第8卷, 1946.",
        "[16] The Institute of Everyday Human Weirdness. 《镜面反馈在仪容整理中的作用》. 外观维护研究, 第3版, 1948.",
        "[17] 吴所谓、박미루. 《洗手行为的场景触发与间隔》. 卫生动作统计, 第11期, 1947.",
        "[18] 方放下. 《家庭空间内的物品归位习惯》. 居住秩序学刊, 第4卷, 1946.",
        "[19] 香港茶水间观察站. 《垃圾离开居所后的心理完成感》. 家务行为简报, 第1期, 1948.",
        "[20] 吴所谓、박미루. 《窗帘开合与日间光照管理》. 室内环境行为学, 第6卷, 1947.",
        "[21] 陈有据、顾得上. 《地面清洁动作的能量分配研究》. 家庭维护技术, 第2版, 1946.",
        "[22] 东京都市生活节奏实验室. 《衣物清洗、晾晒与收纳的连续流程》. 织物处理档案, 第10卷, 1948.",
        "[23] 田中既読. 《冰箱内部食物排序的时间管理意义》. 冷藏空间观察, 第5期, 1947.",
        "[24] 赵到点. 《厨房火源附近的器具操作行为》. 家庭风险分析, 第3卷, 1946.",
        "[25] 新加坡排队与礼貌实验室. 《剩余食物保存与人类风险判断》. 食品延迟消费研究, 第7版, 1948.",
        "[26] 李想开、陈有据. 《切割、剥离与腌制：食材预处理观察》. 烹饪动作学, 第4卷, 1947.",
        "[27] 袁滑. 《米粒加热后的社会共享路径》. 主食文化记录, 第2期, 1946.",
        "[28] The Royal Society for Lost Keys. 《保质期标签与消费决策》. 食品日期认知报告, 第8卷, 1948.",
        "[29] 林时差、Manny Task. 《等待水沸腾时的注意力转移》. 厨房时间研究, 第1版, 1947.",
        "[30] 罗集. 《城市步行中的障碍物规避与让行》. 都市位移学报, 第5卷, 1946.",
        "[31] 深圳即时通讯礼仪实验室. 《排队行为中的距离维护》. 集体等待行为通讯, 第9期, 1948.",
        "[32] 田中既読、方放下. 《公共交通换乘节点的信息读取》. 城市交通观察, 第3卷, 1947.",
        "[33] 许三更、Tim O'Clock. 《车辆安全带的佩戴与解除仪式》. 交通安全动作汇编, 第6版, 1946.",
        "[34] 釜山雨伞找回事务局. 《轮胎、方向灯与驾驶者的预判信号》. 道路行为研究, 第12卷, 1948.",
        "[35] 金善后. 《机场安检后的随身物品重组》. 远距离移动档案, 第2期, 1947.",
        "[36] I. M. Offline、Ada Break. 《行李转盘附近的所有权确认行为》. 旅行物品管理, 第4卷, 1946.",
        "[37] 首尔低电量应对研究组. 《电子设备解锁动作的身份验证逻辑》. 数字日常研究, 第7版, 1948.",
        "[38] 周小结、张不动. 《密码更新与记忆负担》. 账户安全行为学, 第3卷, 1947.",
        "[39] 史真香. 《照片备份行为的延迟焦虑》. 个人数据保存通讯, 第5期, 1946.",
        "[40] 北海道慢速生活记录所. 《电子邮件附件误发的前置条件》. 数字协作事故报告, 第8卷, 1948.",
        "[41] Manny Task. 《群聊创建、退出与数字社交边界》. 网络关系观察, 第2版, 1947.",
        "[42] 山本寝坊、박미루. 《二维码扫描后的信任转移》. 移动交互研究, 第6卷, 1946.",
        "[43] 广州搜索结果可信度研究室. 《搜索结果的标题依赖现象》. 信息检索心理学, 第4期, 1948.",
        "[44] John Doe、陈有据. 《通知推送与注意力碎片化》. 终端使用行为报告, 第9卷, 1947.",
        "[45] 南京待办事项与拖延管理中心. 《待办事项记录对工作记忆的替代作用》. 任务执行研究, 第1版, 1946.",
        "[46] 赵到点、陈有据. 《会议开场前的设备检查仪式》. 组织协作观察, 第3卷, 1948.",
        "[47] 京都延迟回复学派. 《文件命名规则与集体协作效率》. 文档秩序学刊, 第7期, 1947.",
        "[48] 李想开、林时差. 《考试交卷前的重复检查行为》. 学习评估行为录, 第5卷, 1946.",
        "[49] San Francisco Public File Naming Society. 《下班动作与工作身份的边界》. 职场时间社会学, 第2期, 1948.",
        "[50] 山田太郎. 《问候语的零信息量交换》. 社交信号研究, 第10卷, 1947.",
        "[51] 东京礼貌拒绝研究会. 《谈话轮次、沉默与话题终止》. 对话结构观察, 第4版, 1946.",
        "[52] 吴所谓、金善后. 《握手、挥手与点头的非语言信号》. 人际距离档案, 第6卷, 1948.",
        "[53] 香港互惠礼物观察组. 《礼物赠收过程中的互惠预期》. 交换仪式学报, 第3期, 1947.",
        "[54] 顾得上、Ada Break. 《道歉与道谢的关系修复功能》. 社会润滑机制研究, 第8卷, 1946.",
        "[55] 上海边界协商与已读不回研究所. 《建议、拒绝与个人边界的协商》. 人际边界通讯, 第2版, 1948.",
        "[56] The Committee for Unnecessary Thumbs-Up. 《社交媒体点赞作为弱连接维护工具》. 数字社交统计, 第5卷, 1947.",
        "[57] 袁滑、Manny Task. 《优惠券条件与冲动购买》. 消费决策观察, 第11期, 1946.",
        "[58] 深圳售后证据保存实验室. 《退货、换货及保修流程中的证据保存》. 售后行为档案, 第4卷, 1948.",
        "[59] 方放下、金善后. 《现金、转账与共同费用分摊》. 家庭财务行为研究, 第7版, 1947.",
        "[60] Northbridge Institute of Applied Procrastination. 《娱乐性屏幕观看的时间上限》. 休闲管理季刊, 第1期, 1946.",
        "[61] 京都宠物与阳台植物照料中心. 《植物、鱼类与宠物照料的周期性》. 伴生生物照护观察, 第9卷, 1948.",
        "[62] 周末眠、Ada Break. 《绘画、手工与低风险创造活动》. 业余创作研究, 第3版, 1947.",
        "[63] 许三更、金善后、박미루. 《焦虑、愤怒与情绪降速技术》. 心理自助行为报告, 第6卷, 1946.",
        "[64] 国际紧急信息压缩与安全撤离委员会. 《紧急报警与公共避难中的信息压缩》. 公共安全沟通, 第2期, 1948.",
    ]

    ACADEMIC_REFERENCE_RULES = {
        "起居睡眠": (7, 8, 60),
        "清洁感官": (9, 10, 11, 12, 17),
        "健康管理": (12, 17, 33, 63, 64),
        "环境调节": (20, 22, 23),
        "家务整理": (18, 19, 21, 22, 25),
        "设施维护": (21, 22, 24, 34),
        "进食与餐桌": (13, 21, 27),
        "食材准备": (23, 26, 27, 28),
        "烹饪加工": (13, 24, 25, 29),
        "衣物穿戴": (14, 15, 16),
        "仪容修整": (11, 14, 15, 16),
        "出门准备": (6, 35, 36, 37),
        "步行通行": (30, 31, 32),
        "公共交通": (32, 35, 36),
        "驾驶与车辆": (30, 33, 34),
        "设备操作": (37, 38, 39, 42),
        "网络沟通": (40, 41, 42, 44),
        "学习输入": (3, 43, 45, 48),
        "任务执行": (45, 47, 48),
        "职场协作": (46, 47, 49),
        "交流互动": (2, 3, 50, 51, 52),
        "关系维护": (41, 50, 53, 54, 55, 56),
        "情感回应": (53, 54, 56),
        "购买与售后": (28, 57, 58),
        "资金往来": (57, 59),
        "视听娱乐": (60,),
        "创作游戏": (3, 62),
        "动植物照料": (61,),
        "情绪识别": (54, 55, 63),
        "压力恢复": (55, 60, 63),
        "紧急处置": (33, 34, 64),
    }

    ACADEMIC_REFERENCE_AUTHORS = (
        "顾得上", "李想开", "张不动", "周末眠", "吴所谓", "陈有据", "许三更",
        "林时差", "方放下", "赵到点", "田中既読", "山本寝坊", "金善后",
        "박미루", "Manny Task", "Ada Break", "Tim O'Clock", "I. M. Offline",
        "东亚摸鱼与效率研究院", "首尔低电量应对研究组",
        "International Bureau of Lost Umbrellas",
        "The Institute of Everyday Human Weirdness",
    )

    ACADEMIC_SUBCATEGORY_REFERENCE_SERIES = {
        "起居睡眠": "休眠行为观察",
        "清洁感官": "日常卫生与感官维护研究",
        "健康管理": "健康管理行为资料",
        "环境调节": "室内环境操作研究",
        "家务整理": "家务秩序与清洁研究",
        "设施维护": "家庭设施维护通讯",
        "进食与餐桌": "餐桌行为与摄入观察",
        "食材准备": "食材处理与食品安全记录",
        "烹饪加工": "厨房热加工行为学刊",
        "衣物穿戴": "衣物与身体包覆研究",
        "仪容修整": "仪容与镜面反馈档案",
        "出门准备": "离家准备与物品核对研究",
        "步行通行": "城市步行观察",
        "公共交通": "公共交通协同行为研究",
        "驾驶与车辆": "驾驶与车辆操作研究",
        "设备操作": "个人设备操作档案",
        "网络沟通": "网络交流与信息传递研究",
        "学习输入": "学习输入与记忆管理研究",
        "任务执行": "日常任务执行通讯",
        "职场协作": "职场协作流程研究",
        "交流互动": "日常交流与非语言信号研究",
        "关系维护": "人际关系维护观察",
        "情感回应": "情感回应与社会支持档案",
        "购买与售后": "消费决策与售后行为研究",
        "资金往来": "日常资金管理研究",
        "视听娱乐": "休闲视听行为记录",
        "创作游戏": "兴趣创作与低风险试错研究",
        "动植物照料": "动植物照护研究",
        "情绪识别": "情绪识别与命名研究",
        "压力恢复": "压力恢复与边界管理研究",
        "紧急处置": "公共安全与应急行为研究",
    }

    ACADEMIC_SUBCATEGORY_REFERENCE_TITLES = {
        "起居睡眠": (
            "入睡窗口与夜间行为的时间误差",
            "闹钟触发后的清醒迁移与身体重启",
            "卧具定位与睡眠空间可用性的观察记录",
            "午睡时长、醒后迟滞与恢复感的关系",
            "夜间起身路径中的照明、步态与静音",
        ),
        "清洁感官": (
            "日常清洁中的水温、力度与残留判断",
            "面部清洁的区域顺序与误触风险",
            "口腔护理中的吞咽、漱洗与器具归位",
            "感官维护动作的左右差异与盲区补查",
            "清洁完成感与实际残留之间的判断偏差",
        ),
        "健康管理": (
            "家庭测量器具读数的复核与记录方式",
            "服药时间表中的重复、漏服与确认动作",
            "就诊叙述中症状发生顺序的压缩问题",
            "预约、候诊与健康信息交接的行为链",
            "轻运动前后身体状态变化的自我观察",
        ),
        "环境调节": (
            "开合窗帘时光线变化与室内活动的协调",
            "通风路径、气流方向与短时舒适度评估",
            "照明开关顺序与夜间视觉适应记录",
            "温湿度调节设备的启动阈值和停止条件",
            "室内设备声响对注意力与休息的影响",
        ),
        "家务整理": (
            "清洁前物品暂存与原位复核的步骤设计",
            "地面清理中的区域划分和遗漏点回查",
            "衣物洗涤、晾晒与收纳之间的状态交接",
            "厨房与卫浴清洁工具的分区使用记录",
            "家庭物品归位习惯与寻找时间的观察",
        ),
        "设施维护": (
            "家用设备检修前的断电、断水与风险识别",
            "漏水位置确认、临时止损和恢复测试记录",
            "灯具更换中的工具准备与稳定支撑条件",
            "插座使用时负载分配和插拔动作的边界",
            "清洁设备滤网、排水口与复装状态的核对",
        ),
        "进食与餐桌": (
            "餐前摆放、座位选择与用餐动线的观察",
            "食物温度、入口大小与咀嚼节奏的关系",
            "分餐过程中份量协商和餐具接触边界",
            "剩余食物从餐桌到冷藏空间的交接判断",
            "餐桌交谈、吞咽安全和结束信号的协调",
        ),
        "食材准备": (
            "清洗食材时水流、容器和沥水状态的记录",
            "刀具接触面、切割方向与手指避让空间",
            "果皮、外包装和可食部分的分离判断",
            "冷冻食材解冻时间与表面温度的变化",
            "生熟食材分区、器具更换与交叉污染边界",
        ),
        "烹饪加工": (
            "热源启动、锅具预热与食材入锅时机",
            "火力、加热时长和液体蒸发程度的观察",
            "翻动、搅拌和锅内拥挤度之间的关系",
            "烘烤或蒸煮过程中的位置、温度与熟度差异",
            "试味、调味和停止加热的终止判据",
        ),
        "衣物穿戴": (
            "衣物正反、内外层次与开口方向的确认",
            "穿脱动作中的重心变化和单侧受力检查",
            "纽扣、拉链与鞋带闭合状态的逐点复核",
            "尺寸、温度和活动幅度对舒适度的影响",
            "离开更衣区域前对遮挡、配件和遗留物的回查",
        ),
        "仪容修整": (
            "镜面距离、照明方向和面部可见范围的设置",
            "皮肤、毛发与指甲状态对工具选择的影响",
            "修整动作的左右顺序及难以观察区域的补查",
            "护肤或香氛用品的用量、接触位置和等待时间",
            "完成后从正面、侧面和实际社交距离复核效果",
        ),
        "出门准备": (
            "目的地、出发时间与预计停留时长的交叉核对",
            "钥匙、证件、钱包和通信设备的逐项清点",
            "天气、路线变化与临时改道对随身物品的影响",
            "门窗、照明、用水和电器状态的离家前回查",
            "关门后确认门锁、同行人员和下一行程节点",
        ),
        "步行通行": (
            "起步前确认路面、视线遮挡和可停止空间",
            "步幅、速度与周围行人相对距离的动态调整",
            "转弯、台阶和地面高差处的重心转移观察",
            "通过路口时同时读取信号、车辆和他人意图",
            "抵达目标点后检查随身物品及路线是否走偏",
        ),
        "公共交通": (
            "站点方向、乘车凭证和线路终点的出发前核对",
            "排队、上车与车厢内站位中的空间余量判断",
            "换乘缓冲时间、广播信息和出口编号的记录",
            "行李、座位与下车位置之间的持续位置管理",
            "错过站点或线路中断后的求助与替代路线选择",
        ),
        "驾驶与车辆": (
            "启动车辆前确认人员状态、车辆告警和周边空间",
            "速度、车距、转向信号与路面变化的同步观察",
            "倒车或停车时分段移动并留出再次制动的余量",
            "加油、充电和检查轮胎时避免跨越安全操作边界",
            "停车后核对档位、驻车状态、车门和遗留物品",
        ),
        "设备操作": (
            "设备电量、网络、权限和当前界面状态的读取",
            "输入前确认目标对象，避免在错误账户或窗口操作",
            "点击、滑动或连接后等待可辨认的系统反馈",
            "修改设置前记录原状态并确认撤销或恢复入口",
            "任务结束后核对保存结果、通知状态和设备归位",
        ),
        "网络沟通": (
            "发送前确认收件对象、对话上下文和信息可见范围",
            "链接、附件、文件名与权限设置的逐项核验",
            "将请求、答复和时间承诺拆成可辨认的信息单元",
            "群聊或邮件转发前检查引用内容是否脱离原语境",
            "发送后确认交付状态，并为误发保留撤回或更正路径",
        ),
        "学习输入": (
            "学习开始前写明问题、材料来源和本次完成定义",
            "阅读时区分原文事实、个人推断和暂未理解的术语",
            "笔记按概念关系而非页面顺序组织并保留出处线索",
            "用复述或练习检验理解，不把重复浏览当作掌握证据",
            "结束时记录未解决问题和下一次复习的具体入口",
        ),
        "任务执行": (
            "开始前确认交付物、截止时间、依赖条件和责任边界",
            "把任务拆为可检查的小单元并标注先后关系",
            "暂停时记录已完成部分、当前阻塞与恢复位置",
            "出现偏差时说明事实、影响范围和需要的决策",
            "提交后核验接收状态、版本位置和后续维护责任",
        ),
        "职场协作": (
            "会议或交接开始前确认参与者、议题和信息权限",
            "将讨论意见、决定事项与未决问题分栏记录",
            "为每项行动标明负责人、期限和可验证的完成证据",
            "打印、扫描或发送文件时检查版本、页序和接收对象",
            "结束协作时确认交接已被接收，而非仅完成发送动作",
        ),
        "交流互动": (
            "进入谈话前判断距离、场合、双方是否具备交谈条件",
            "按轮次控制音量、语速和停顿，为对方留下回应空间",
            "聆听时区分对方原话、自己的解释和尚未确认的意思",
            "打断或转移话题前说明原因，并观察对方是否愿意继续",
            "结束时用告别、总结或行动安排明确对话已经收束",
        ),
        "关系维护": (
            "提出请求或承诺前核对双方时间、能力和边界条件",
            "拒绝、改期或取消时尽早传达事实并给出明确选项",
            "礼物、建议与帮助应匹配关系程度，不预设对方必须回报",
            "秘密和私人信息按原约定管理，不因熟悉而扩大传播范围",
            "约定结束后检查是否需要跟进、致谢或修正误解",
        ),
        "情感回应": (
            "回应前先确认发生了什么以及对方是否希望被倾听",
            "把事实、情绪和实际需求分开，不用自己的经历覆盖对方",
            "安慰或鼓励时选择具体、可兑现且不施加期限的表达",
            "若无法提供帮助，说明能力边界并协助寻找合适支持",
            "结束回应后留意对方反馈，不把一次点头当成问题已解决",
        ),
        "购买与售后": (
            "下单前把需求、规格、总价和不可接受条件逐项列出",
            "收货时记录包装、型号、数量与订单信息是否一致",
            "试用时先阅读限制条件，避免破坏退换或保修资格",
            "发生问题后按时间顺序保存照片、沟通记录和凭证",
            "退款或维修完成后核对到账、设备状态和售后期限",
        ),
        "资金往来": (
            "交易前确认金额、币种、收付款对象和费用用途",
            "输入账户或扫码后复核页面展示的对方身份与数额",
            "共同支出先约定计算口径，再记录各自承担部分",
            "现金、转账和退款凭证按日期保存并避免重复登记",
            "对账时核实余额变化与原始凭据，不用记忆替代账目",
        ),
        "视听娱乐": (
            "开始前选择内容、音量、屏幕距离和大致结束时间",
            "播放过程中留意疲劳、注意力转移和周围人的休息需要",
            "连续观看时在章节或自然停顿处评估是否继续",
            "关闭自动播放或提醒，减少内容平台替用户延长时长",
            "结束后恢复设备音量、屏幕和睡前安排，避免时间失控",
        ),
        "创作游戏": (
            "开始创作或游戏前确认规则、工具、材料和可用时间",
            "将作品目标拆为可尝试的回合或阶段，允许低成本返工",
            "记录失败发生在哪一步，不把偶然结果误写成普遍规则",
            "与他人协作时先说明轮次、材料归属和暂停信号",
            "结束时整理工具、保存作品或进度，并明确下次接续位置",
        ),
        "动植物照料": (
            "先识别照料对象及其当前状态，不以同一剂量套用不同个体",
            "记录光照、温度、水量、食物和上次照料时间等环境条件",
            "按周期观察变化，把异常与正常波动分开记录",
            "操作工具和饲料后清洁并归位，避免交叉污染或误食",
            "离开前确认水源、通风、防逃逸和下一次照料安排",
        ),
        "情绪识别": (
            "先描述触发事件和当时环境，不急着给自己贴固定标签",
            "观察心跳、呼吸、肌肉紧张等身体信号出现的先后顺序",
            "把自动想法与可核实事实分开，标记暂时无法确认的部分",
            "为情绪命名后再判断它提示了需求、边界还是风险",
            "决定行动前观察强度是否变化，必要时延后不可逆回应",
        ),
        "压力恢复": (
            "将压力来源分为可处理事项、外部限制和暂时未知因素",
            "选择睡眠、饮食、活动或求助等可获得的恢复资源",
            "把休息窗口设为真实安排，不把它写成另一项绩效任务",
            "练习拒绝额外要求时说明容量和可行替代，不必过度辩解",
            "复盘只记录能影响下一步的事实，并在约定时点停止反刍",
        ),
        "紧急处置": (
            "先判断危险是否仍在扩大，并确认自己和他人的撤离路线",
            "报警或呼救时依次说明地点、事件、人数和最紧急状况",
            "遵从现场指引，避免返回危险区域取物、拍摄或追赶",
            "使用设备或急救物品前确认自身能力和环境条件",
            "到达安全位置后清点人员、保持通信并等待专业人员接手",
        ),
    }

    ACADEMIC_SUBCATEGORY_REFERENCES = {}
    _academic_reference_number = len(ACADEMIC_REFERENCES) + 1
    for _reference_group_index, (_minor, _titles) in enumerate(
        ACADEMIC_SUBCATEGORY_REFERENCE_TITLES.items()
    ):
        _category_references = []
        _series = ACADEMIC_SUBCATEGORY_REFERENCE_SERIES[_minor]
        for _title_index, _title in enumerate(_titles):
            _author_index = (_reference_group_index * 3 + _title_index * 5) % len(
                ACADEMIC_REFERENCE_AUTHORS
            )
            _author = ACADEMIC_REFERENCE_AUTHORS[_author_index]
            if (_reference_group_index + _title_index) % 3 == 0:
                _coauthor = ACADEMIC_REFERENCE_AUTHORS[
                    (_author_index + 9) % len(ACADEMIC_REFERENCE_AUTHORS)
                ]
                _author = f"{_author}、{_coauthor}"
            _volume = (_reference_group_index * 5 + _title_index) % 12 + 1
            _year = 1946 + (_reference_group_index + _title_index) % 3
            _category_references.append(
                f"[{_academic_reference_number}] {_author}. 《{_title}》. "
                f"{_series}, 第{_volume}卷, {_year}."
            )
            _academic_reference_number += 1
        ACADEMIC_SUBCATEGORY_REFERENCES[_minor] = tuple(_category_references)

    ACADEMIC_MAJOR_METHOD_REFERENCE_SERIES = {
        "身体维护": "身体行为方法论通讯",
        "居家生活": "居住环境操作研究",
        "饮食料理": "进食与烹饪过程档案",
        "穿戴仪容": "身体包覆与外观维护研究",
        "出行交通": "城市移动行为学刊",
        "数码通讯": "数字交互与在线协作档案",
        "学习工作": "任务组织与认知行为研究",
        "社交礼仪": "人际协调行为通讯",
        "购物财务": "消费与资金往来研究",
        "休闲兴趣": "休闲活动观察",
        "情绪心理": "情绪与恢复行为学刊",
        "公共安全": "公共安全行为观察",
    }

    ACADEMIC_MAJOR_METHOD_REFERENCE_TITLES = {
        "身体维护": (
            "身体维护中的前置条件与状态登记",
            "重复性身体动作的次序和节律观察",
            "感受反馈、动作偏差与复核路径",
            "个人差异对日常身体流程的影响",
            "身体照护中可观察指标的选择边界",
            "日常维护动作的中止条件与恢复办法",
            "身体活动记录中的时间窗口和场景变量",
            "从局部清洁到整体状态的交接检查",
            "生活动作中的风险提示与升级决策",
            "身体照护行为的复盘与个体化调整",
        ),
        "居家生活": (
            "居家流程中的物品、空间与动作边界",
            "家庭环境变化的记录顺序和感官反馈",
            "重复家务中的工具选择与错误恢复",
            "从准备到复位的居家任务状态管理",
            "家务分区、物品归位与寻找成本观察",
            "室内设备操作的风险提示和停止判据",
            "家庭空间中的通行路径与障碍物记录",
            "清洁完成度的可见指标与盲区检查",
            "居家动作受温湿度和照明影响的记录",
            "日常维护中临时状态与最终状态的区分",
        ),
        "饮食料理": (
            "饮食流程中的卫生、温度与时间控制",
            "食材从采购到入口的状态交接记录",
            "厨房多任务操作中的注意力分配",
            "工具、容器与热源的使用边界观察",
            "口味判断与客观熟度信号的区分",
            "餐桌协作中的份量、顺序和礼貌边界",
            "食品保存中日期、温度与容器的协同记录",
            "烹饪偏差的发现时点与可逆修正方式",
            "吞咽、等待和交谈之间的节奏协调",
            "家庭饮食动作的完成判据与清理流程",
        ),
        "穿戴仪容": (
            "穿戴顺序、身体活动范围与舒适反馈",
            "衣物闭合点的逐项核对和遗漏风险",
            "镜面观察的角度、照明与视觉盲区",
            "配件使用中的受力、遮挡和环境适配",
            "从更衣准备到离开空间的连续动作记录",
            "外观整理中工具接触与皮肤状态观察",
            "穿脱过程的重心转移和安全支撑条件",
            "仪容完成感与他人可见效果的差异",
            "衣物维护、暂存和归位的状态标记",
            "个人穿戴选择中的天气与场合变量",
        ),
        "出行交通": (
            "出行链中的路线、时间和随身物品核验",
            "步行与乘车切换时的空间位置管理",
            "交通参与者之间的信号读取与让行次序",
            "站点、票证和方向信息的双重确认",
            "车辆操作中的视野、速度与制动余量",
            "行李交接、所有权确认和遗失恢复路径",
            "拥挤环境下的排队距离与上落车秩序",
            "行程偏差出现后的信息获取和改道决策",
            "移动任务中注意力分配与设备使用边界",
            "抵达后的人员、物品和车辆状态复核",
        ),
        "数码通讯": (
            "数字操作中的账户、对象和权限确认",
            "点击反馈、保存状态与任务完成证据",
            "信息发送前的收件人和内容逆向检查",
            "文件链接的版本、范围与后续可访问性",
            "设备设置变更的原状态记录和撤销路径",
            "通知打断、注意力恢复与操作上下文保留",
            "群聊互动中的可见范围和退出边界",
            "网络资料的来源核对和标题偏差识别",
            "账号异常时的安全处置与恢复次序",
            "数字交互结束后的数据、设备和提醒清理",
        ),
        "学习工作": (
            "学习与工作任务的输入、输出和完成定义",
            "材料来源、事实记录与个人推断的区分",
            "长任务拆分后的依赖关系和阻塞状态",
            "注意力切换、暂停恢复和工作记忆负担",
            "协作决策中的负责人、期限与证据登记",
            "文档版本、命名规则和交接可追踪性",
            "考试或提交节点的检查顺序与误交防范",
            "重复练习与实际掌握之间的验证差异",
            "口头指令转成书面待办的遗漏控制",
            "结束工作时的收尾、归档与角色切换",
        ),
        "社交礼仪": (
            "谈话开始、轮次转换与结束信号的观察",
            "礼貌动作的场景适配和个体差异边界",
            "请求、拒绝与建议中的信息完整性",
            "沉默、停顿和表情所能支持的有限推断",
            "人际距离、音量与视线方向的变化记录",
            "关系承诺中的时间成本和责任边界",
            "情绪回应的事实核对与需求识别顺序",
            "误解发生后的澄清、道歉和修复路径",
            "礼物、互惠预期与非强制回报的区分",
            "线上线下关系维护的可见范围管理",
        ),
        "购物财务": (
            "消费前需求、规格、价格与预算边界",
            "付款对象、金额和凭证的双重核验",
            "订单、交付和售后期限之间的状态交接",
            "优惠条件中的时间限制与适用范围识别",
            "退换货证据保存和沟通顺序记录",
            "共同费用的计算口径与确认方式",
            "现金、转账和退款的账目闭环观察",
            "冲动购买信号与延迟决策窗口研究",
            "消费评价中事实描述和主观感受的分层",
            "会员订阅的续费提醒、取消入口与结果验证",
        ),
        "休闲兴趣": (
            "娱乐活动的开始、暂停和结束信号",
            "屏幕、音量与连续时长对休息节律的影响",
            "游戏规则、回合边界与低成本试错记录",
            "兴趣创作中的材料管理和作品保存方式",
            "休闲计划与睡眠、工作时间的冲突检查",
            "多人活动中的轮次、反馈和退出约定",
            "内容推荐机制对观看时长的延长效应",
            "宠物、植物等照料对象的周期性任务安排",
            "休闲结束后的设备复位和空间整理",
            "爱好进度、挫折感与继续参与意愿观察",
        ),
        "情绪心理": (
            "情绪触发事件、身体信号与命名顺序",
            "压力来源中可控事项和外部限制的区分",
            "恢复活动的可用资源与现实时间窗口",
            "反复思考、事实复核和行动决策的边界",
            "个人界限表达中的容量说明与后续选择",
            "寻求陪伴时支持需求和隐私范围的确认",
            "自我安慰用语与实际问题处理的衔接",
            "强烈情绪下延迟不可逆回应的操作条件",
            "日常复盘的停止条件与信息保留原则",
            "情绪状态变化的记录频率和个体差异",
        ),
        "公共安全": (
            "紧急事件中的位置、危险源与撤离方向确认",
            "报警信息按地点、事件和人员状态压缩传递",
            "现场指挥、专业救援和旁观者角色的区分",
            "灭火或急救用品使用前的能力与环境判断",
            "撤离过程中的人员清点和路线保持",
            "财物遗失报告中的时间、地点和特征核对",
            "通信中断、拥挤和能见度下降时的备用方案",
            "危险解除信号与重新进入区域的权限边界",
            "紧急处置后的人员交接和事实记录方式",
            "自救互助中避免二次伤害的停止判据",
        ),
    }

    ACADEMIC_METHOD_REFERENCES_BY_MAJOR = {}
    for _major_index, (_major, _titles) in enumerate(
        ACADEMIC_MAJOR_METHOD_REFERENCE_TITLES.items()
    ):
        _method_references = []
        _series = ACADEMIC_MAJOR_METHOD_REFERENCE_SERIES[_major]
        for _title_index, _title in enumerate(_titles):
            _author_index = (_major_index * 5 + _title_index * 7 + 3) % len(
                ACADEMIC_REFERENCE_AUTHORS
            )
            _author = ACADEMIC_REFERENCE_AUTHORS[_author_index]
            if (_major_index + _title_index) % 3 == 1:
                _coauthor = ACADEMIC_REFERENCE_AUTHORS[
                    (_author_index + 13) % len(ACADEMIC_REFERENCE_AUTHORS)
                ]
                _author = f"{_author}、{_coauthor}"
            _volume = (_major_index * 7 + _title_index) % 12 + 1
            _year = 1946 + (_major_index + _title_index + 1) % 3
            _method_references.append(
                f"[{_academic_reference_number}] {_author}. 《{_title}》. "
                f"{_series}, 第{_volume}卷, {_year}."
            )
            _academic_reference_number += 1
        ACADEMIC_METHOD_REFERENCES_BY_MAJOR[_major] = tuple(_method_references)

    ACADEMIC_REFERENCES.extend(
        reference
        for references in ACADEMIC_SUBCATEGORY_REFERENCES.values()
        for reference in references
    )
    ACADEMIC_REFERENCES.extend(
        reference
        for references in ACADEMIC_METHOD_REFERENCES_BY_MAJOR.values()
        for reference in references
    )








    @Command(
        "behavior_reference",
        description="查询基础生活行为的标准化操作参考。支持中文/拉丁语/古希腊语/日语四语查询",
        pattern=_PATTERN,
    )
    async def handle_behavior(self, stream_id: str = "", **kwargs):
        matched_groups = kwargs.get("matched_groups", {})
        if not isinstance(matched_groups, dict):
            matched_groups = {}
        command_prefix = str(matched_groups.get("command_prefix", "")).strip()
        if command_prefix != self._get_command_prefix():
            return False, "未找到操作指令", True
        action = str(matched_groups.get("action", "")).strip()

        if not action or action not in self._COMMAND_MAP:
            return False, "未找到操作指令", True

        lang, behavior_key = self._COMMAND_MAP[action]

        if behavior_key == "__help_tree__":
            action_parts = action.split()
            category = action_parts[2] if len(action_parts) > 2 else None
            subcategory = action_parts[3] if len(action_parts) > 3 else None
            await self._show_help(lang, stream_id, category, subcategory)
            return True, "显示了生活参考分类帮助", True

        if behavior_key == "__help__":
            await self._show_help(lang, stream_id)
            return True, "显示了可用行为列表", True

        if behavior_key == "__random__":
            behavior_key, behavior = random.choice(list(self.BEHAVIORS[lang].items()))
            messages = self._render_behavior(lang, behavior_key, *behavior)
            await self.ctx.send.forward(messages, stream_id)
            return True, f"随机返回了「{behavior_key}」的参考指南", True

        behavior = self.BEHAVIORS.get(lang, {}).get(behavior_key)
        if not behavior:
            return False, f"未找到「{action}」的参考指南", True

        messages = self._render_behavior(lang, behavior_key, *behavior)
        await self.ctx.send.forward(messages, stream_id)
        return True, f"返回了「{action}」的参考指南", True

    def _get_command_prefix(self) -> str:
        configured_prefix = self.config.plugin.command_prefix.strip()
        if not configured_prefix:
            return self.DEFAULT_COMMAND_PREFIX
        if not configured_prefix.startswith("/"):
            return f"/{configured_prefix}"
        return configured_prefix

    @staticmethod
    def _msg(nickname: str, content: str) -> dict:
        return {
            "user_id": "0",
            "nickname": nickname,
            "segments": [{"type": "text", "content": content}],
        }

    def _d(self, key: str, lang: str, **fmt) -> str:
        text = self.DEPT.get(key, {}).get(lang, self.DEPT.get(key, {}).get("zh", key))
        if fmt:
            text = text.format(**fmt)
        return text

    def _get_category_path(self, action: str) -> tuple[str, str]:
        canonical_action = action
        for localized_actions in self.CANONICAL_ACTIONS.values():
            if action in localized_actions:
                canonical_action = localized_actions[action]
                break
        for major, minor_map in self.CATEGORY_TREE.items():
            for minor, actions in minor_map.items():
                if canonical_action in actions:
                    return major, minor
        return "未分类", "未分类"

    @staticmethod
    def _document_rng(lang: str, action: str, purpose: str) -> random.Random:
        # 同一语种与条目视为同一份文档；重复调用只复现记录，不重新抽签。
        record_key = f"life-behavior-record:v1:{purpose}:{lang}:{action}"
        digest = hashlib.blake2b(record_key.encode("utf-8"), digest_size=16).digest()
        return random.Random(int.from_bytes(digest, "big"))

    def _select_academic_references(
        self, lang: str, action: str
    ) -> tuple[list[str], str, str]:
        major, minor = self._get_category_path(action)
        reference_ids = self.ACADEMIC_REFERENCE_RULES.get(minor, ())
        topic_pool = [
            self.ACADEMIC_REFERENCES[index - 1]
            for index in reference_ids
            if 1 <= index <= len(self.ACADEMIC_REFERENCES)
        ]
        topic_pool.extend(self.ACADEMIC_SUBCATEGORY_REFERENCES[minor])
        method_pool = self.ACADEMIC_METHOD_REFERENCES_BY_MAJOR[major]
        rng = self._document_rng(lang, action, "references")
        references = rng.sample(topic_pool, 3) + rng.sample(method_pool, 2)
        return references, major, minor

    def _render_behavior(self, lang: str, action: str, title_prefix: str, steps: list[str], warning: str) -> list[dict]:
        detail = self.config.style.detail_level
        show_version = self.config.style.show_version
        version_rng = self._document_rng(lang, action, "version")
        version = f" v{version_rng.randint(1, 9)}.{version_rng.randint(0, 99):02d}" if show_version else ""

        if detail == "简明":
            return self._render_concise(lang, action, title_prefix, steps, warning, version)
        elif detail == "详细":
            return self._render_detailed(lang, action, title_prefix, steps, warning, version)
        elif detail == "学术":
            return self._render_academic(lang, action, title_prefix, steps, warning, version)
        else:
            return self._render_standard(lang, action, title_prefix, steps, warning, version)

    def _render_concise(self, lang: str, action: str, title_prefix: str, steps: list[str], warning: str, version: str) -> list[dict]:
        lines = [f"{title_prefix} — {action} {self._d('summary_card_label', lang)}\n"]
        for i, step in enumerate(steps, 1):
            first = step.split("。")[0]
            if lang == "la" and first:
                first = first.split(".")[0]
                if first:
                    first += "."
            elif lang == "grc" and first:
                first = first.split(".")[0]
                if first:
                    first += "."
            elif not first.endswith("）"):
                first += "。"
            lines.append(f"{i}. {first}\n")
        first_warning = warning.split("。")[0]
        if lang == "la":
            first_warning = warning.split(".")[0] + "."
        elif lang == "grc":
            first_warning = warning.split(".")[0] + "."
        else:
            first_warning += "。"
        lines.append(f"\n⚠ {first_warning}")
        dept_name = self._d("main_quick", lang)
        return [self._msg(dept_name, "".join(lines))]

    def _render_standard(self, lang: str, action: str, title_prefix: str, steps: list[str], warning: str, version: str) -> list[dict]:
        body_lines = [f"{title_prefix}{version} — {action}{self._d('standard_ops_label', lang)}\n"]
        for i, step in enumerate(steps, 1):
            body_lines.append(f"{self._d('step_label', lang)}{i}：{step}\n")
        dept_main = self._d("main", lang)
        dept_safety = self._d("safety", lang)
        safety_label = self._d("safety_prefix", lang)
        return [
            self._msg(dept_main, "".join(body_lines)),
            self._msg(dept_safety, f"⚠️ {safety_label}：{warning}"),
        ]

    def _render_detailed(self, lang: str, action: str, title_prefix: str, steps: list[str], warning: str, version: str) -> list[dict]:
        body_lines = [f"{title_prefix}{version} — {action}{self._d('standard_ops_full_label', lang)}\n"]
        for i, step in enumerate(steps, 1):
            body_lines.append(f"{self._d('step_label', lang)}{i}：{step}\n")
        extension = self._d("extended_note", lang)
        dept_main_full = self._d("main_full", lang)
        dept_safety = self._d("safety", lang)
        dept_extended = self._d("extended", lang)
        safety_label = self._d("safety_prefix", lang)
        return [
            self._msg(dept_main_full, "".join(body_lines)),
            self._msg(dept_safety, f"⚠️ {safety_label}：{warning}"),
            self._msg(dept_extended, extension),
        ]

    def _render_editorial_body(
        self,
        lang: str,
        action: str,
        major: str,
        minor: str,
        profile: dict[str, str],
        phase_sources: list[str],
        phase_labels: tuple[str, ...],
    ) -> str:
        layout = profile["layout"]
        reading_notes = {
            "fieldnote": "先把眼前场景与触发条件对上，再从最小动作开始；条目未说明的部分不要自行补造。",
            "interaction": "把发出的动作与他人或环境返回的信号分开判断；沉默、未读和明确回应不是同一种结果。",
            "state": "本条按准备、执行、复核与结束排列；前置条件未满足时，停在当前步骤，不靠猜测放行。",
            "cognitive": "先寻找触发线索，完成一个动作后读取反馈，再决定是否进入下一步；注意力中断时从最近一次确认处恢复。",
            "narrative": "以下按人类通常经历这类行为的先后次序书写；现场可以有变化，但不能因此省略关键检查。",
            "review": "可先读每节标题定位当前问题，再回到对应步骤；快速浏览不能代替边界与完成条件的核对。",
            "exception": "先识别正常路径，再留意每一步的暂停条件；条件改变时允许退出，不为了流程完整而假装成功。",
            "comparative": "先选择与当前环境最接近的情形；不要把不同场景下的动作要求拼成一套通用规则。",
        }[layout]
        operation_decomposition = self._d("operation_decomposition", lang)
        domain_note = self.ACADEMIC_DOMAIN_NOTES[minor]
        stage_details = self.ACADEMIC_STAGE_DETAILS[major]

        lines = [
            f"【{operation_decomposition}】",
            f"【适用情境】{profile['preface']}",
            f"目标行为：{action}；适用范围：{major} > {minor}。",
            reading_notes,
            f"开始前先核对：{domain_note}",
            f"\n【{phase_labels[0]}】",
            f"启动信号：{self.ACADEMIC_STAGE_OBSERVATIONS[0]}",
            f"条件仍不明时：{self.ACADEMIC_STAGE_TRANSITIONS[0]}",
            f"\n【{phase_labels[1]}】",
        ]
        for index, source in enumerate(phase_sources):
            action_text = str(source or "").strip().replace("\n", "\n   ")
            lines.append(f"{index + 1}. {action_text}")

        lines.extend(
            [
                f"执行顺序的补充提示：{stage_details[1]}",
                f"涉及时间、次数或工具参数时：{stage_details[2]}",
                f"\n【{phase_labels[2]}】",
                f"读取结果时：{self.ACADEMIC_STAGE_OBJECTIVES[2]}",
                f"结果与预期不符时：{self.ACADEMIC_STAGE_TRANSITIONS[2]}",
                f"\n【{phase_labels[3]}】",
                f"场景提醒：{stage_details[3]}",
                f"继续前先确认：{self.ACADEMIC_STAGE_OBSERVATIONS[3]}",
                f"出现边界冲突时：{self.ACADEMIC_STAGE_TRANSITIONS[3]}",
                f"\n【{phase_labels[4]}】",
                f"确认「{action}」所指向的结果已经出现，相关物品、工具和环境回到可说明的状态；仍未完成的事项单独交代，不将流程停顿误记为完成。",
                f"结束前整理：{stage_details[4]}",
                f"最终状态：{self.ACADEMIC_STAGE_OBSERVATIONS[4]}",
                f"遗留事项：{self.ACADEMIC_STAGE_TRANSITIONS[4]}",
                f"\n编者附记：{profile['closing']}",
            ]
        )
        return "\n".join(lines)

    def _render_academic(self, lang: str, action: str, title_prefix: str, steps: list[str], warning: str, version: str) -> list[dict]:
        refs, major, minor = self._select_academic_references(lang, action)
        ref_block = "\n".join(f"  {reference}" for reference in refs)

        metadata_rng = self._document_rng(lang, action, "metadata")
        profile = metadata_rng.choice(self.ACADEMIC_EDITORIAL_PROFILES)
        compiler_key = metadata_rng.choice(("decoding", "risk", "literature", "decoding_lab"))
        lab_number = metadata_rng.randint(1, 17)
        compiler_department = self._d(compiler_key, lang, n=lab_number)
        dept_decoding = self._d("decoding", lang)
        dept_risk = self._d("risk", lang)
        dept_lit = self._d("literature", lang)
        dept_lab = self._d("decoding_lab", lang, n=lab_number)

        bvid_number = self._document_rng(lang, action, "identifier").randint(10_000_000, 99_999_999)
        bvid = f"BHV-{bvid_number}"
        classification_value = self._document_rng(lang, action, "classification").choice(
            self.ACADEMIC_CLASSIFICATION_VALUES[lang]
        )
        academic_header = self._d("academic_header", lang)
        research_object = self._d("research_object", lang)
        protocol_name = self._d("protocol_name", lang)
        category_path = self._d("category_path", lang)
        behavior_id_label = self._d("behavior_id", lang)
        class_label = self._d("classification", lang)
        compiled_label = self._d("compiled_by", lang)
        author_label = self.AUTHOR_LABELS.get(lang, self.AUTHOR_LABELS["zh"])
        refs_label = self._d("references_header", lang)
        ref_footer = self._d("ref_footer", lang)
        phase_labels = self.ACADEMIC_PHASE_LABELS.get(lang, self.ACADEMIC_PHASE_LABELS["zh"])

        header = "\n".join(
            [
                f"【{academic_header}】",
                f"{research_object}：{action}",
                f"{protocol_name}：{title_prefix}{version}",
                f"{behavior_id_label}：{bvid}",
                f"{class_label}：{classification_value}",
                f"{category_path}：{major} > {minor}",
                f"{compiled_label}：{compiler_department}",
                f"{author_label}：{profile['name']}",
            ]
        )
        phase_sources = list(steps[:5])
        if len(steps) > 5:
            phase_sources[4] = "\n".join(steps[4:])

        body_text = self._render_editorial_body(
            lang, action, major, minor, profile, phase_sources, phase_labels
        )
        risk_label = self._d("risk_prefix", lang)
        observation_label = self._d("observation", lang)
        flavor_warning = ""
        if lang == "zh":
            warning_options = self.ACADEMIC_FLAVOR_WARNINGS.get(major, ())
            if warning_options:
                flavor_warning = self._document_rng(lang, action, "flavor-warning").choice(
                    warning_options
                )
        flavor_warning_text = f"\n\n补充警示：{flavor_warning}" if flavor_warning else ""
        risk_text = (
            f"【{risk_label}】\n"
            f"{self._d('risk_advisory_label', lang)}：{warning}"
            f"{flavor_warning_text}\n\n"
            f"{observation_label}：出现异常反馈时先停止当前动作；不得以操作已发出、界面有响应或他人暂未反对，替代明确的安全确认。"
        )
        ref_text = (
            f"【{refs_label} / References】\n"
            f"{ref_block}\n\n"
            f"* {ref_footer}\n"
            f"* {self._d('citation_note', lang)}：Life Behavior Reference Committee (LBRC), {bvid}, 1947."
        )
        return [
            self._msg(dept_decoding, header),
            self._msg(dept_lab, body_text),
            self._msg(dept_risk, risk_text),
            self._msg(dept_lit, ref_text),
        ]

    async def _show_help(
        self,
        lang: str,
        stream_id: str,
        category: str | None = None,
        subcategory: str | None = None,
    ) -> None:
        if lang == "zh":
            command_prefix = self._get_command_prefix()
            if category is None:
                lines = [
                    "📖 生活参考帮助",
                    f"输入 {command_prefix} 生活参考 获取一条随机生活行为参考。",
                    "",
                    "可用分类（大分类 > 小分类）：",
                ]
                for major, minor_map in self.CATEGORY_TREE.items():
                    lines.append(f"【{major}】")
                    for minor, actions in minor_map.items():
                        lines.append(f"  {minor}（{len(actions)} 条）")
                lines.extend(
                    [
                        "",
                        f"查看某个大分类：{command_prefix} 生活参考 帮助 大分类",
                        f"查看某个小分类的全部条目：{command_prefix} 生活参考 帮助 大分类 小分类",
                    ]
                )
            elif category not in self.CATEGORY_TREE:
                lines = [f"未找到这个大分类，请先发送 {command_prefix} 生活参考 帮助 查看可用分类。"]
            elif subcategory is None:
                minor_map = self.CATEGORY_TREE[category]
                lines = [
                    f"📂 {category}",
                    "",
                    "可用小分类：",
                ]
                lines.extend(f"  {minor}（{len(actions)} 条）" for minor, actions in minor_map.items())
                lines.extend(
                    [
                        "",
                        f"查看具体条目：{command_prefix} 生活参考 帮助 {category} 小分类",
                    ]
                )
            elif subcategory not in self.CATEGORY_TREE[category]:
                lines = [f"未找到「{category}」下的「{subcategory}」，请先查看该大分类的小分类。"]
            else:
                actions = self.CATEGORY_TREE[category][subcategory]
                lines = [
                    f"📂 {category} > {subcategory}（共 {len(actions)} 条）",
                    "",
                ]
                lines.extend(f"  {command_prefix} {action}" for action in actions)
            await self.ctx.send.text("\n".join(lines), stream_id)
            return

        behaviors = self.BEHAVIORS.get(lang, self.BEHAVIORS.get("zh", {}))
        actions = list(behaviors.keys())
        command_prefix = self._get_command_prefix()
        command_list = "\n".join(f"  {command_prefix} {a}" for a in actions)
        help_template = self.HELP_TEXT.get(lang, self.HELP_TEXT["zh"])
        help_text = help_template.format(
            count=len(actions), command_list=command_list, prefix=command_prefix
        )
        await self.ctx.send.text(help_text, stream_id)

    async def on_config_update(
        self, scope: str, config_data: dict[str, object], version: str
    ) -> None:
        del scope
        del config_data
        del version


def create_plugin() -> LifeBehaviorReferencePlugin:
    return LifeBehaviorReferencePlugin()
