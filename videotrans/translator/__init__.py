# -*- coding: utf-8 -*-
from pathlib import Path
from typing import Union, List

from videotrans.configure import config
# 数字代表显示顺序
from videotrans.util import tools

GOOGLE_INDEX = 0
MICROSOFT_INDEX = 1
MyMemoryAPI_INDEX = 2
BAIDU_INDEX = 3
DEEPL_INDEX = 4
DEEPLX_INDEX = 5
OTT_INDEX = 6
TENCENT_INDEX = 7
CHATGPT_INDEX = 8
LOCALLLM_INDEX = 9
ZIJIE_INDEX = 10
AZUREGPT_INDEX = 11
GEMINI_INDEX = 12
TRANSAPI_INDEX = 13
QWENMT_INDEX = 14
CLAUDE_INDEX = 15
LIBRE_INDEX = 16
AI302_INDEX = 17
ALI_INDEX = 18
ZHIPUAI_INDEX = 19
SILICONFLOW_INDEX = 20
DEEPSEEK_INDEX = 21
OPENROUTER_INDEX = 22
# 翻译通道名字列表，显示在界面
TRANSLASTE_NAME_LIST = [
    "Google(免费)" if config.defaulelang == 'zh' else 'Google',
    "微软(免费)" if config.defaulelang == 'zh' else 'Microsoft',
    "MyMemory API(免费)" if config.defaulelang == 'zh' else 'MyMemory API',
    "百度翻译" if config.defaulelang == 'zh' else 'Baidu',
    "DeepL",
    "DeepLx",
    "OTT(本地)" if config.defaulelang == 'zh' else 'OTT',
    "腾讯翻译" if config.defaulelang == 'zh' else 'Tencent',
    "OpenAI ChatGPT" if config.defaulelang == 'zh' else 'OpenAI ChatGPT',
    "兼容AI/本地模型" if config.defaulelang == 'zh' else 'Local LLM',
    "字节火山AI" if config.defaulelang == 'zh' else 'VolcEngine LLM',
    "AzureGPT AI",
    "Gemini AI",
    "自定义翻译API" if config.defaulelang == 'zh' else 'Customized API',
    "阿里百炼" if config.defaulelang == 'zh' else 'Ali-Bailian',
    "Claude AI",
    "LibreTranslate(本地)" if config.defaulelang == 'zh' else 'LibreTranslate',
    "302.AI",
    "阿里机器翻译" if config.defaulelang == 'zh' else 'Alibaba Machine Translation',
    "智谱AI" if config.defaulelang == 'zh' else 'Zhipu AI',
    "硅基流动" if config.defaulelang == 'zh' else 'SiliconFlow',
    "DeepSeek",
    "OpenRouter"
]
# subtitles language code https://zh.wikipedia.org/wiki/ISO_639-2%E4%BB%A3%E7%A0%81%E5%88%97%E8%A1%A8
#  https://www.loc.gov/standards/iso639-2/php/code_list.php
# 腾讯翻译 https://cloud.tencent.com/document/api/551/15619
# google翻译 https://translate.google.com/
# 百度翻译 https://fanyi.baidu.com/
# deepl  https://deepl.com/
# microsoft https://www.bing.com/translator?mkt=zh-CN
# 阿里 https://help.aliyun.com/zh/machine-translation/developer-reference/machine-translation-language-code-list?spm=a2c4g.11186623.help-menu-30396.d_4_4.4bda2b009oye8y
LANGNAME_DICT = {
    "zh-cn": "Simplified Chinese" if config.defaulelang != 'zh' else '简体中文',
    "zh-tw": "Traditional Chinese" if config.defaulelang != 'zh' else '繁体中文',
    "en": "English" if config.defaulelang != 'zh' else '英语',
    "fr": "French" if config.defaulelang != 'zh' else '法语',
    "de": "German" if config.defaulelang != 'zh' else '德语',
    "ja": "Japanese" if config.defaulelang != 'zh' else '日语',
    "ko": "Korean" if config.defaulelang != 'zh' else '韩语',
    "ru": "Russian" if config.defaulelang != 'zh' else '俄罗斯语',
    "es": "Spanish" if config.defaulelang != 'zh' else '西班牙语',
    "th": "Thai" if config.defaulelang != 'zh' else '泰国语',
    "it": "Italian" if config.defaulelang != 'zh' else '意大利语',
    "pt": "Portuguese" if config.defaulelang != 'zh' else '葡萄牙语',
    "vi": "Vietnamese" if config.defaulelang != 'zh' else '越南语',
    "ar": "Arabic" if config.defaulelang != 'zh' else '阿拉伯语',
    "tr": "Turkish" if config.defaulelang != 'zh' else '土耳其语',
    "hi": "Hindi" if config.defaulelang != 'zh' else '印度语',
    "hu": "Hungarian" if config.defaulelang != 'zh' else '匈牙利语',
    "uk": "Ukrainian" if config.defaulelang != 'zh' else '乌克兰语',
    "id": "Indonesian" if config.defaulelang != 'zh' else '印度尼西亚语',
    "ms": "Malay" if config.defaulelang != 'zh' else '马来西亚语',
    "kk": "Kazakh" if config.defaulelang != 'zh' else '哈萨克语',
    "cs": "Czech" if config.defaulelang != 'zh' else '捷克语',
    "pl": "Polish" if config.defaulelang != 'zh' else '波兰语',
    "nl": "Dutch" if config.defaulelang != 'zh' else '荷兰语',
    "sv": "Swedish" if config.defaulelang != 'zh' else '瑞典语',
    "he": "Hebrew" if config.defaulelang != 'zh' else '希伯来语',
    "bn": "Bengali" if config.defaulelang != 'zh' else '孟加拉语',
    "fa": "Persian" if config.defaulelang != 'zh' else '波斯语',
    "fil": "Filipino" if config.defaulelang != 'zh' else '菲律宾语',
    "ur": "Urdu" if config.defaulelang != 'zh' else '乌尔都语',
    "yue": "Cantonese" if config.defaulelang != 'zh' else '粤语',
    "ug": "ug" if config.defaulelang != 'zh' else 'ug',
}

# 如果存在新增
try:
    if Path(config.ROOT_DIR+f'/videotrans/newlang.txt').exists():
        _new_lang=Path(config.ROOT_DIR+f'/videotrans/newlang.txt').read_text().strip().split("\n")
        for nl in _new_lang:
            LANGNAME_DICT[nl]=nl
except Exception as e:
    config.logger.exception(f'读取自定义新增语言代码 newlang.txt 时出错 {e}',exc_info=True)

LANGNAME_DICT_REV={v:k for k,v in LANGNAME_DICT.items()}
LANG_CODE = {
    "zh-cn": [
        "zh-cn",  # google通道
        "chi",  # 字幕嵌入语言
        "zh",  # 百度通道
        "ZH-HANS",  # deepl deeplx通道
        "zh",  # 腾讯通道
        "zh",  # OTT通道
        "zh-Hans",  # 微软翻译
        "Simplified Chinese" if config.defaulelang != 'zh' else '简体中文',  # AI翻译
        "zh",  # 阿里
        "Chinese" # qwen-mt
    ],
    "ur": [
        "ur",  # google通道
        "urd",  # 字幕嵌入语言
        "ur",  # 百度通道
        "No",  # deepl deeplx通道
        "No",  # 腾讯通道
        "No",  # OTT通道
        "ur",  # 微软翻译
        "Urdu" if config.defaulelang != 'zh' else '乌尔都语',  # AI翻译
        "ur",  # 阿里
        "Urdu"
    ],
    "yue": [
        "yue",  # google通道
        "chi",  # 字幕嵌入语言
        "yue",  # 百度通道
        "No",  # deepl deeplx通道
        "No",  # 腾讯通道
        "No",  # OTT通道
        "yue",  # 微软翻译
        "Cantonese" if config.defaulelang != 'zh' else '粤语',  # AI翻译
        "yue",  # 阿里
        "Cantonese"
    ],

    "fil": [
        "tl",  # google通道
        "fil",  # 字幕嵌入语言
        "fil",  # 百度通道
        "No",  # deepl deeplx通道
        "No",  # 腾讯通道
        "No",  # OTT通道
        "fil",  # 微软翻译
        "Filipino" if config.defaulelang != 'zh' else '菲律宾语',  # AI翻译
        "fil",  # 阿里
        "Filipino"
    ],
    "fi": [
        "fi",  # google通道
        "fin",  # 字幕嵌入语言
        "fin",  # 百度通道
        "FI",  # deepl deeplx通道
        "No",  # 腾讯通道
        "No",  # OTT通道
        "fi",  # 微软翻译
        "Finnish" if config.defaulelang != 'zh' else '芬兰语',  # AI翻译
        "fi",  # 阿里
        "Finnish" # qwen-mt 暂不支持翻译菲律宾语
    ],

    "zh-tw": [
        "zh-tw",
        "chi",
        "cht",
        "ZH-HANT",
        "zh-TW",
        "zt",
        "zh-Hant",
        "Traditional Chinese" if config.defaulelang != 'zh' else '繁体中文',
        "zh-tw",
        "Traditional Chinese",
    ],
    "en": [
        "en",
        "eng",
        "en",
        "EN-US",
        "en",
        "en",
        "en",
        "English language" if config.defaulelang != 'zh' else '英语',
        "en",
        "English"
    ],
    "fr": [
        "fr",
        "fre",
        "fra",
        "FR",
        "fr",
        "fr",
        "fr",
        "French language" if config.defaulelang != 'zh' else '法语',
        "fr",
        "French"
    ],
    "de": [
        "de",
        "ger",
        "de",
        "DE",
        "de",
        "de",
        "de",
        "German language" if config.defaulelang != 'zh' else '德语',
        "de",
        "German"
    ],
    "ja": [
        "ja",
        "jpn",
        "jp",
        "JA",
        "ja",
        "ja",
        "ja",
        "Japanese language" if config.defaulelang != 'zh' else '日语',
        "ja",
        "Japanese"
    ],
    "ko": [
        "ko",
        "kor",
        "kor",
        "KO",
        "ko",
        "ko",
        "ko",
        "Korean language" if config.defaulelang != 'zh' else '韩语',
        "ko",
        "Korean"
    ],
    "ru": [
        "ru",
        "rus",
        "ru",
        "RU",
        "ru",
        "ru",
        "ru",
        "Russian language" if config.defaulelang != 'zh' else '俄罗斯语',
        "ru",
        "Russian"
    ],
    "es": [
        "es",
        "spa",
        "spa",
        "ES",
        "es",
        "es",
        "es",
        "Spanish language" if config.defaulelang != 'zh' else '西班牙语',
        "es",
        "Spanish"
    ],
    "th": [
        "th",
        "tha",
        "th",
        "No",
        "th",
        "th",
        "th",
        "Thai language" if config.defaulelang != 'zh' else '泰国语',
        "th",
        "Thai"
    ],
    "it": [
        "it",
        "ita",
        "it",
        "IT",
        "it",
        "it",
        "it",
        "Italian language" if config.defaulelang != 'zh' else '意大利语',
        "it",
        "Italian"
    ],
    "pt": [
        "pt",  # pt-PT
        "por",
        "pt",
        "PT-PT",
        "PT-PT",
        "pt",
        "pt",
        "Portuguese language" if config.defaulelang != 'zh' else '葡萄牙语',
        "pt",
        "Portuguese"
    ],
    "vi": [
        "vi",
        "vie",
        "vie",
        "vi",
        "vi",
        "vi",
        "vi",
        "Vietnamese language" if config.defaulelang != 'zh' else '越南语',
        "vi",
        "Vietnamese"
    ],
    "ar": [
        "ar",
        "are",
        "ara",
        "AR",
        "ar",
        "ar",
        "ar",
        "Arabic language" if config.defaulelang != 'zh' else '阿拉伯语',
        "ar",
        "Arabic"
    ],
    "tr": [
        "tr",
        "tur",
        "tr",
        "TR",
        "tr",
        "tr",
        "tr",
        "Turkish language" if config.defaulelang != 'zh' else '土耳其语',
        "tr",
        "Turkish"
    ],
    "hi": [
        "hi",
        "hin",
        "hi",
        "No",
        "hi",
        "hi",
        "hi",
        "Hindi language" if config.defaulelang != 'zh' else '印度语',
        "hi",
        "Hindi"
    ],
    "hu": [
        "hu",
        "hun",
        "hu",
        "HU",
        "No",
        "hu",
        "hu",
        "Hungarian language" if config.defaulelang != 'zh' else '匈牙利语',
        "hu",
        "Hungarian"
    ],
    "uk": [
        "uk",
        "ukr",
        "ukr",  # 百度
        "UK",  # deepl
        "No",  # 腾讯
        "uk",  # ott
        "uk",  # 微软
        "Ukrainian language" if config.defaulelang != 'zh' else '乌克兰语',
        "No",
        "Ukrainian"
    ],
    "id": [
        "id",
        "ind",
        "id",
        "ID",
        "id",
        "id",
        "id",
        "Indonesian language" if config.defaulelang != 'zh' else '印度尼西亚语',
        "id",
        "Indonesian"
    ],
    "ms": [
        "ms",
        "may",
        "may",
        "No",
        "ms",
        "ms",
        "ms",
        "Malay language" if config.defaulelang != 'zh' else '马来西亚语',
        "ms",
        "Malay"
    ],
    "kk": [
        "kk",
        "kaz",
        "No",
        "No",
        "No",
        "No",
        "kk",
        "Kazakh language" if config.defaulelang != 'zh' else '哈萨克语',
        "kk",
        "Kazakh"
    ],
    "cs": [
        "cs",
        "ces",
        "cs",
        "CS",
        "No",
        "cs",
        "cs",
        "Czech language" if config.defaulelang != 'zh' else '捷克语',
        "cs",
        "Czech"
    ],
    "pl": [
        "pl",
        "pol",
        "pl",
        "PL",
        "No",
        "pl",
        "pl",
        "Polish language" if config.defaulelang != 'zh' else '波兰语',
        "pl",
        "Polish"
    ],
    "nl": [
        "nl",  # google通道
        "dut",  # 字幕嵌入语言
        "nl",  # 百度通道
        "NL",  # deepl deeplx通道
        "No",  # 腾讯通道
        "nl",  # OTT通道
        "nl",  # 微软翻译
        "Dutch" if config.defaulelang != 'zh' else '荷兰语',  # AI翻译
        "nl",
        "Dutch"
    ],
    "sv": [
        "sv",  # google通道
        "swe",  # 字幕嵌入语言
        "swe",  # 百度通道
        "SV",  # deepl deeplx通道
        "No",  # 腾讯通道
        "sv",  # OTT通道
        "sv",  # 微软翻译
        "Swedish" if config.defaulelang != 'zh' else '瑞典语',  # AI翻译
        "sv",
        "Swedish"
    ],
    "he": [
        "he",  # google通道
        "heb",  # 字幕嵌入语言
        "heb",  # 百度通道
        "HE",  # deepl deeplx通道
        "No",  # 腾讯通道
        "No",  # OTT通道
        "he",  # 微软翻译
        "Hebrew" if config.defaulelang != 'zh' else '希伯来语',  # AI翻译
        "he",
        "Hebrew"
    ],
    "bn": [
        "bn",  # google通道
        "ben",  # 字幕嵌入语言
        "ben",  # 百度通道
        "No",  # deepl deeplx通道
        "No",  # 腾讯通道
        "No",  # OTT通道
        "bn",  # 微软翻译
        "Bengali" if config.defaulelang != 'zh' else '孟加拉语',  # AI翻译,
        "bn",
        "Bengali"
    ],
    "fa": [
        "fa",  # google通道
        "per",  # 字幕嵌入语言
        "per",  # 百度通道
        "No",  # deepl deeplx通道
        "No",  # 腾讯通道
        "No",  # OTT通道
        "fa",  # 微软翻译
        "Persian" if config.defaulelang != 'zh' else '波斯语',  # AI翻译
        "fa",  # 阿里
        "Western Persian"
    ],
    "ug": [
        "ug",  # google通道
        "ug",  # 字幕嵌入语言
        "ug",  # 百度通道
        "No",  # deepl deeplx通道
        "No",  # 腾讯通道
        "No",  # OTT通道
        "ug",  # 微软翻译
        "ug" if config.defaulelang != 'zh' else 'ug',  # AI翻译
        "ug",  # 阿里
        "ug"
    ],
    "auto": [
        "auto",
        "auto",
        "auto",
        "auto",
        "auto",
        "auto",
        "auto",
        "auto",
        "auto",
        "auto",
    ]
}


# 根据界面显示的语言名称，比如“简体中文、English” 获取语言代码，比如 zh-cn en 等, 如果是cli，则直接是语言代码
def get_code(show_text=None):
    if not show_text or show_text in ['-','No']:
        return None

    if show_text in LANG_CODE:
        return show_text
    return LANGNAME_DICT_REV.get(show_text,show_text)


# 根据显示的语言和翻译通道，获取该翻译通道要求的源语言代码和目标语言代码
# translate_type 翻译通道索引
# show_source 显示的原语言名称或 - 或  语言代码 
# show_target 显示的目标语言名称 或 - 或语言代码
# 如果是AI渠道则返回语言的自然语言名称
# 新增的语言代码直接返回
# - No 是兼容早期不规范写法
def get_source_target_code(*, show_source=None, show_target=None, translate_type=None):
    source_list = None
    target_list = None

    if show_source and show_source not in ['-','No']:
        if show_source in LANG_CODE:
            source_list = LANG_CODE[show_source] 
        elif LANGNAME_DICT_REV.get(show_source):
            source_list=LANG_CODE.get(LANGNAME_DICT_REV.get(show_source))
            
    if show_target and show_target not in ['-','No']:
        if show_target in LANG_CODE:
            target_list = LANG_CODE[show_target] 
        elif LANGNAME_DICT_REV.get(show_target):
            target_list=LANG_CODE.get(LANGNAME_DICT_REV.get(show_target))

    # 均未找到，可能是新增语言代码
    if not source_list and not target_list:
        return show_source,show_target

    if translate_type in [GOOGLE_INDEX,QWENMT_INDEX, MyMemoryAPI_INDEX, TRANSAPI_INDEX]:
        return source_list[0] if source_list else show_source, target_list[0] if target_list else show_target

    if translate_type == BAIDU_INDEX:
        return source_list[2] if source_list else show_source, target_list[2] if target_list else show_target

    if translate_type in [DEEPLX_INDEX, DEEPL_INDEX]:
        return source_list[3] if source_list else show_source, target_list[3] if target_list else show_target

    if translate_type == TENCENT_INDEX:
        return source_list[4] if source_list else show_source, target_list[4] if target_list else show_target

    if translate_type in [CHATGPT_INDEX, AZUREGPT_INDEX, GEMINI_INDEX,
                            LOCALLLM_INDEX, ZIJIE_INDEX, AI302_INDEX, CLAUDE_INDEX, ZHIPUAI_INDEX, SILICONFLOW_INDEX,  DEEPSEEK_INDEX, OPENROUTER_INDEX]:
        return source_list[7] if source_list else show_source, target_list[7] if target_list else show_target
    if translate_type in [OTT_INDEX, LIBRE_INDEX]:
        return source_list[5] if source_list else show_source, target_list[5] if target_list else show_target
    if translate_type == MICROSOFT_INDEX:
        return source_list[6] if source_list else show_source, target_list[6] if target_list else show_target
    if translate_type == ALI_INDEX:
        return source_list[8] if source_list else show_source, target_list[8] if target_list else show_target
    return show_source,show_target


# 判断当前翻译通道和目标语言是否允许翻译
# 比如deepl不允许翻译到某些目标语言，某些通道是否填写api key 等
# translate_type翻译通道
# show_target 翻译后显示的目标语言名称
# only_key=True 仅检测 key 和api，不判断目标语言
def is_allow_translate(*, translate_type=None, show_target=None, only_key=False,  return_str=False):
    if translate_type in [GOOGLE_INDEX, MyMemoryAPI_INDEX, MICROSOFT_INDEX]:
        return True

    if translate_type == CHATGPT_INDEX and not config.params['chatgpt_key']:
        if return_str:
            return "Please configure the api and key information of the OpenAI ChatGPT channel first."
        from videotrans.winform import chatgpt
        chatgpt.openwin()
        return False
    if translate_type == ZHIPUAI_INDEX and not config.params['zhipu_key']:
        if return_str:
            return "请在菜单-智谱AI中填写智谱AI的api key"
        from videotrans.winform import zhipuai
        zhipuai.openwin()
        return False
    if translate_type == DEEPSEEK_INDEX and not config.params['deepseek_key']:
        if return_str:
            return "请在菜单-DeepSeek中填写api key"
        from videotrans.winform import deepseek
        deepseek.openwin()
        return False
    if translate_type == OPENROUTER_INDEX and not config.params['openrouter_key']:
        if return_str:
            return "请在菜单-OpenRouter中填写api key"
        from videotrans.winform import openrouter
        openrouter.openwin()
        return False

    if translate_type == SILICONFLOW_INDEX and not config.params['guiji_key']:
        if return_str:
            return "请在菜单-硅基流动中填写硅基流动的api key"
        from videotrans.winform import zhipuai
        zhipuai.openwin()
        return False
    if translate_type == AI302_INDEX and not config.params['ai302_key']:
        if return_str:
            return "Please configure the api and key information of the 302.AI channel first."
        from videotrans.winform import ai302
        ai302.openwin()
        return False
    if translate_type == CLAUDE_INDEX and not config.params['claude_key']:
        if return_str:
            return "Please configure the api and key information of the Claude API channel first."
        from videotrans.winform import claude
        claude.openwin()
        return False
    if translate_type == TRANSAPI_INDEX and not config.params['trans_api_url']:
        if return_str:
            return "Please configure the api and key information of the Trans_API channel first."
        from videotrans.winform import transapi
        transapi.openwin()
        return False

    if translate_type == LOCALLLM_INDEX and not config.params['localllm_api']:
        if return_str:
            return "Please configure the api and key information of the LocalLLM channel first."
        from videotrans.winform import localllm
        localllm.openwin()
        return False
    if translate_type == ZIJIE_INDEX and (
            not config.params['zijiehuoshan_model'].strip() or not config.params['zijiehuoshan_key'].strip()):
        if return_str:
            return "Please configure the api and key information of the ZiJie channel first."
        from videotrans.winform import zijiehuoshan
        zijiehuoshan.openwin()
        return False

    if translate_type == GEMINI_INDEX and not config.params['gemini_key']:
        if return_str:
            return "Please configure the api and key information of the Gemini channel first."
        from videotrans.winform import gemini
        gemini.openwin()
        return False
    if translate_type == QWENMT_INDEX and not config.params['qwenmt_key']:
        if return_str:
            return "Please configure the api and key information of the QwenMT channel first."
        from videotrans.winform import qwenmt
        qwenmt.openwin()
        return False
    if translate_type == AZUREGPT_INDEX and (
            not config.params['azure_key'] or not config.params['azure_api']):
        if return_str:
            return "Please configure the api and key information of the Azure GPT channel first."
        from videotrans.winform import azure
        azure.openwin()
        return False

    if translate_type == BAIDU_INDEX and (
            not config.params["baidu_appid"] or not config.params["baidu_miyue"]):
        if return_str:
            return "Please configure the api and key information of the Baidu channel first."
        from videotrans.winform import baidu
        baidu.openwin()
        return False
    if translate_type == TENCENT_INDEX and (
            not config.params["tencent_SecretId"] or not config.params["tencent_SecretKey"]):
        if return_str:
            return "Please configure the appid and key information of the Tencent channel first."
        from videotrans.winform import tencent
        tencent.openwin()
        return False
    if translate_type == ALI_INDEX and (
            not config.params["ali_id"] or not config.params["ali_key"]):
        if return_str:
            return "Please configure the appid and key information of the Alibaba translate channel first."
        from videotrans.winform import ali
        ali.openwin()
        return False
    if translate_type == DEEPL_INDEX and not config.params["deepl_authkey"]:
        if return_str:
            return "Please configure the api and key information of the DeepL channel first."
        from videotrans.winform import deepL
        deepL.openwin()
        return False
    if translate_type == DEEPLX_INDEX and not config.params["deeplx_address"]:
        if return_str:
            return "Please configure the api and key information of the DeepLx channel first."
        from videotrans.winform import deepLX
        deepLX.openwin()
        return False
    if translate_type == LIBRE_INDEX and not config.params["libre_address"]:
        if return_str:
            return "Please configure the api and key information of the LibreTranslate channel first."
        from videotrans.winform import libre
        libre.openwin()
        return False

    if translate_type == TRANSAPI_INDEX and not config.params["trans_api_url"]:
        if return_str:
            return "Please configure the api and key information of the TransAPI channel first."
        from videotrans.winform import transapi
        transapi.openwin()
        return False
    if translate_type == OTT_INDEX and not config.params["ott_address"]:
        if return_str:
            return "Please configure the api and key information of the OTT channel first."
        from videotrans.winform import ott
        ott.openwin()
        return False
    # 如果只需要判断是否填写了 api key 等信息，到此返回
    if only_key:
        return True
    # 再判断是否为No，即不支持
    index = 0
    if translate_type == BAIDU_INDEX:
        index = 2
    elif translate_type in [DEEPLX_INDEX, DEEPL_INDEX]:
        index = 3
    elif translate_type == TENCENT_INDEX:
        index = 4
    elif translate_type == MICROSOFT_INDEX:
        index = 6
    elif translate_type == ALI_INDEX:
        index = 8

    if show_target:
        target_list = LANG_CODE[show_target] if show_target in LANG_CODE else LANG_CODE.get(
            LANGNAME_DICT_REV.get(show_target))
        if target_list and target_list[index].lower() == 'no':
            if return_str:
                return config.transobj['deepl_nosupport'] + f':{show_target}'
            tools.show_error(config.transobj['deepl_nosupport'] + f':{show_target}')
            return False
    return True


# 获取用于进行语音识别的预设语言，比如语音是英文发音、中文发音
# 根据 原语言进行判断,基本等同于google，但只保留_之前的部分
def get_audio_code(*, show_source=None):
    source_list = LANG_CODE[show_source] if show_source in LANG_CODE else LANG_CODE.get(LANGNAME_DICT_REV.get(show_source))
    return source_list[0] if source_list else "en"


# 获取嵌入软字幕的3位字母语言代码，根据目标语言确定
def get_subtitle_code(*, show_target=None):
    if show_target in LANG_CODE:
        return LANG_CODE[show_target][1]
    if show_target in LANGNAME_DICT_REV:
        return LANG_CODE[LANGNAME_DICT_REV[show_target]][1]
    return 'eng'

def _check_google():
    import requests
    try:
        requests.head(f"https://translate.google.com")
    except Exception as e:
        config.logger.exception(f'检测google翻译失败{e}', exc_info=True)
        return False
    
    return True
    


# 翻译,先根据翻译通道和目标语言，取出目标语言代码
def run(*, translate_type=None,
        text_list=None,
        inst=None,
        is_test=False,
        source_code=None,
        target_code=None,
        uuid=None) -> Union[List, str, None]:
    translate_type = int(translate_type)
    # ai渠道下，target_language是语言名称
    # 其他渠道下是语言代码
    # source_code是原语言代码
    target_language_name = target_code
    if translate_type in [GEMINI_INDEX, AZUREGPT_INDEX, CHATGPT_INDEX, AI302_INDEX, LOCALLLM_INDEX, ZIJIE_INDEX,  CLAUDE_INDEX, ZHIPUAI_INDEX, SILICONFLOW_INDEX,  DEEPSEEK_INDEX, OPENROUTER_INDEX]:
        # 对AI渠道，返回目标语言的自然语言表达
        _, target_language_name = get_source_target_code(show_target=target_code, translate_type=translate_type)
    kwargs = {
        "text_list": text_list,
        "target_language_name": target_language_name,
        "inst": inst,
        "source_code": source_code if source_code and source_code not in ['-', 'No'] else None,
        "target_code": target_code,
        "uuid": uuid,
        "is_test": is_test,
        "translate_type":translate_type
    }
    
    # 未设置代理并且检测google失败，则使用微软翻译
    if translate_type == GOOGLE_INDEX:
        if config.proxy or _check_google() is True:
            from videotrans.translator._google import Google
            return Google(**kwargs).run()
        config.logger.info('==未设置代理并且检测google失败，使用微软翻译')
        from videotrans.translator._microsoft import Microsoft
        return Microsoft(**kwargs).run()
        
    if translate_type == MyMemoryAPI_INDEX:
        from videotrans.translator._mymemory import MyMemory
        config.settings['trans_thread'] = min(10, int(config.settings.get('trans_thread', 5)))
        return MyMemory(**kwargs).run()
    if translate_type == QWENMT_INDEX:
        from videotrans.translator._qwenmt import QwenMT
        return QwenMT(**kwargs).run()

    if translate_type == MICROSOFT_INDEX:
        from videotrans.translator._microsoft import Microsoft
        return Microsoft(**kwargs).run()

    if translate_type == TENCENT_INDEX:
        from videotrans.translator._tencent import Tencent
        return Tencent(**kwargs).run()

    if translate_type == BAIDU_INDEX:
        from videotrans.translator._baidu import Baidu
        return Baidu(**kwargs).run()

    if translate_type == OTT_INDEX:
        from videotrans.translator._ott import OTT
        return OTT(**kwargs).run()

    if translate_type == TRANSAPI_INDEX:
        from videotrans.translator._transapi import TransAPI
        return TransAPI(**kwargs).run()

    if translate_type == DEEPL_INDEX:
        from videotrans.translator._deepl import DeepL
        return DeepL(**kwargs).run()

    if translate_type == DEEPLX_INDEX:
        from videotrans.translator._deeplx import DeepLX
        return DeepLX(**kwargs).run()

    if translate_type == AI302_INDEX:
        from videotrans.translator._ai302 import AI302
        return AI302(**kwargs).run()

    if translate_type == LOCALLLM_INDEX:
        from videotrans.translator._localllm import LocalLLM
        return LocalLLM(**kwargs).run()

    if translate_type == ZIJIE_INDEX:
        from videotrans.translator._huoshan import HuoShan
        return HuoShan(**kwargs).run()

    if translate_type == CHATGPT_INDEX:
        from videotrans.translator._chatgpt import ChatGPT
        return ChatGPT(**kwargs).run()
    if translate_type == ZHIPUAI_INDEX:
        from videotrans.translator._zhipuai import ZhipuAI
        return ZhipuAI(**kwargs).run()
    if translate_type == OPENROUTER_INDEX:
        from videotrans.translator._openrouter import OpenRouter
        return OpenRouter(**kwargs).run()
    if translate_type == DEEPSEEK_INDEX:
        from videotrans.translator._deepseek import DeepSeek
        return DeepSeek(**kwargs).run()

    if translate_type == SILICONFLOW_INDEX:
        from videotrans.translator._siliconflow import SILICONFLOW
        return SILICONFLOW(**kwargs).run()

    if translate_type == AZUREGPT_INDEX:
        from videotrans.translator._azure import AzureGPT
        return AzureGPT(**kwargs).run()

    if translate_type == GEMINI_INDEX:
        from videotrans.translator._gemini import Gemini
        return Gemini(**kwargs).run()
    if translate_type == CLAUDE_INDEX:
        from videotrans.translator._claude import Claude
        return Claude(**kwargs).run()
    if translate_type == LIBRE_INDEX:
        from videotrans.translator._libre import Libre
        return Libre(**kwargs).run()
    if translate_type == ALI_INDEX:
        from videotrans.translator._ali import Ali
        return Ali(**kwargs).run()

    raise RuntimeError('未选中任何翻译渠道')
