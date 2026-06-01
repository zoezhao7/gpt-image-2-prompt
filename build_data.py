"""
Build comprehensive prompt data from awesome-gpt-image-2 repository.
Generates JSON data files for the search engine.
"""
import json
import os

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__)) + "/data"

# ============================================================
# TEMPLATES (from templates.md)
# ============================================================
templates = [
    {
        "id": "tpl-001",
        "title": "信息图/科普百科图",
        "category": "信息可视化",
        "description": "生成竖版科普百科信息图，支持人物/植物/动物主题，6-8个知识模块，复古泛黄纸张背景，中心主体3D弹出效果",
        "prompt": "Role: World-class Scientific Encyclopedia Illustrator & Knowledge Graph Architect.\nTask: Generate a highly detailed, extremely intricate, and visually stunning scientific infographic.\nSubject Matter: Choose one from [People, Plants, or Animals].\nKey Visual Requirements:\n1. Lifelike 3D Effect - central subject with dramatic pop-out effect\n2. Layout - 6-8 distinct knowledge modules around the center\n3. Connections - fine leader lines linking all modules\n4. Text & Annotation - MUST be clear Chinese; main title in calligraphy\nStyle: Fine scientific illustration on aged beige paper background.\nAspect Ratio: 3:4.",
        "variables": ["主题"]
    },
    {
        "id": "tpl-002",
        "title": "海报设计模板",
        "category": "海报设计",
        "description": "通用海报设计模板，支持国潮、极简、科技等多种风格",
        "prompt": "Design a high-end poster with elegant composition. Style: [风格]. Theme: [主题]. Include main title, subtitle, and supporting visual elements. Aspect ratio: [比例]. Output: 8K, professional quality.",
        "variables": ["风格", "主题", "比例"]
    },
    {
        "id": "tpl-003",
        "title": "电商详情页/产品展示",
        "category": "电商设计",
        "description": "生成电商产品详情图和展示图，支持服装、家电、数码等多种品类",
        "prompt": "Generate a professional e-commerce product detail image for [产品名称]. Highlight product features, specifications, and use scenarios. Style: clean, modern, high-conversion CTA design. Aspect ratio: [比例].",
        "variables": ["产品名称", "比例"]
    },
    {
        "id": "tpl-004",
        "title": "社交媒体模拟截图",
        "category": "趣味创意",
        "description": "生成仿微信朋友圈/微博/抖音/小红书/B站等社交平台的模拟截图，常用于历史人物梗或趣味内容",
        "prompt": "Generate a screenshot of [平台名称] showing [人物/内容] posting: \"[文案内容]\". Include realistic UI elements like likes, comments, timestamps.",
        "variables": ["平台名称", "人物/内容", "文案内容"]
    },
    {
        "id": "tpl-005",
        "title": "直播模拟截图",
        "category": "趣味创意",
        "description": "生成抖音/B站等直播平台的模拟截图，含主播、观众、礼物特效等元素",
        "prompt": "Generate a screenshot of [平台] live stream. [主播名称] is live streaming, [动作描述], online viewer count is [人数]. Include realistic live stream UI elements.",
        "variables": ["平台", "主播名称", "动作描述", "人数"]
    },
    {
        "id": "tpl-006",
        "title": "电影/游戏海报",
        "category": "电影海报",
        "description": "生成商业级电影海报或游戏封面，支持科幻、奇幻、古风等多种题材",
        "prompt": "Create a [类型] movie/game poster for \"[作品名]\". Style: [风格]. Include title design, key characters, atmospheric background. Professional designer quality, cinematic lighting. Aspect ratio: [比例].",
        "variables": ["类型", "作品名", "风格", "比例"]
    },
    {
        "id": "tpl-007",
        "title": "人像摄影/写真",
        "category": "人像摄影",
        "description": "生成高质量人像摄影作品，支持胶片风、日系、韩系、超写实等多种风格",
        "prompt": "Portrait photography: [主体描述]. Style: [摄影风格]. Lighting: [光线描述]. Composition: [构图描述]. Quality: 8K, realistic skin texture, [比例].",
        "variables": ["主体描述", "摄影风格", "光线描述", "构图描述", "比例"]
    },
    {
        "id": "tpl-008",
        "title": "国风工笔画",
        "category": "国风插画",
        "description": "生成中国传统工笔画风格插画，适合人物、场景、趣味创意",
        "prompt": "A finely detailed Gongbi painting of [主题描述]. Traditional Chinese brushwork, elegant coloring, on rice paper texture. Include a red vertical artist chop seal in the bottom corner. Aspect ratio: [比例].",
        "variables": ["主题描述", "比例"]
    },
    {
        "id": "tpl-009",
        "title": "UI设计系统",
        "category": "UI设计",
        "description": "生成完整的UI设计系统，包含网页、移动端、组件等",
        "prompt": "Generate a complete UI design system in [风格] style for [产品/品牌]. Include web pages, mobile screens, cards, buttons, form controls, navigation. Consistent design language, clean typography, cohesive color palette.",
        "variables": ["风格", "产品/品牌"]
    },
    {
        "id": "tpl-010",
        "title": "像素艺术",
        "category": "像素艺术",
        "description": "生成像素风游戏道具、场景等，适合游戏开发和创意设计",
        "prompt": "Create a pixel art [内容描述] in classic [16-bit/32-bit] style. Crisp pixel edges, limited palette, subtle dithering. Clean background, reminiscent of SNES/GBA-era games.",
        "variables": ["内容描述", "位深度"]
    },
    {
        "id": "tpl-011",
        "title": "二次元/动漫插画",
        "category": "二次元插画",
        "description": "生成高质量二次元美少女/角色插画，支持日系、赛博朋克等多种风格",
        "prompt": "Generate a high-quality anime illustration. Character: [角色设定]. Style: [风格]. Background: [背景描述]. Quality: 8K, ultra-fine details. Aspect ratio: [比例].",
        "variables": ["角色设定", "风格", "背景描述", "比例"]
    },
    {
        "id": "tpl-012",
        "title": "知识图谱/关系图",
        "category": "信息可视化",
        "description": "生成文学作品或历史事件的人物关系图、知识图谱",
        "prompt": "Generate a detailed knowledge graph / character relationship diagram for [主题]. Show clear connections between entities using lines and labels. Include detailed Chinese annotations. Style: organized, professional, easy to read.",
        "variables": ["主题"]
    },
    {
        "id": "tpl-013",
        "title": "字体设计/艺术字",
        "category": "字体设计",
        "description": "生成创意艺术字和书法字体设计",
        "prompt": "Creative typography design for the text \"[文字内容]\". Style: [书法/艺术风格]. Dynamic composition, strong visual impact. Clean background. High contrast.",
        "variables": ["文字内容", "书法/艺术风格"]
    },
    {
        "id": "tpl-014",
        "title": "品牌VI/视觉系统",
        "category": "品牌VI",
        "description": "生成完整的品牌视觉识别系统设计",
        "prompt": "Design a complete VI/visual identity system for [品牌名称], a [品牌描述]. Include logo, color palette, typography, brand elements, and application examples. Style: [风格]. Professional, cohesive, brand guideline quality.",
        "variables": ["品牌名称", "品牌描述", "风格"]
    },
    {
        "id": "tpl-015",
        "title": "图书/杂志封面",
        "category": "平面设计",
        "description": "生成图书封面、杂志封面等平面设计",
        "prompt": "Design a professional book/magazine cover for \"[标题]\". Subtitle: \"[副标题]\". Style: [设计风格]. Include compelling visual elements, clear typography, and professional layout.",
        "variables": ["标题", "副标题", "设计风格"]
    },
    {
        "id": "tpl-016",
        "title": "名画二创/趣味改编",
        "category": "趣味创意",
        "description": "对经典名画进行趣味改编，如蒙娜丽莎喝可乐、古代人物用现代产品等",
        "prompt": "Generate a [原画风格] painting of [原作名称], but [趣味改编描述]. Maintain the original artistic style and composition while incorporating the modern/funny elements.",
        "variables": ["原画风格", "原作名称", "趣味改编描述"]
    },
    {
        "id": "tpl-017",
        "title": "城市主题海报",
        "category": "海报设计",
        "description": "生成国潮/极简风格的城市宣传海报，融入城市地标和文化元素",
        "prompt": "Design a high-end city poster for [城市名称] in [风格] style. Include landmark buildings, cultural elements, flowing composition. Colors: [配色方案]. Aspect ratio: 9:16. 8K quality.",
        "variables": ["城市名称", "风格", "配色方案"]
    },
    {
        "id": "tpl-018",
        "title": "超现实插画",
        "category": "艺术创意",
        "description": "生成超现实主义风格的插画，强调大小对比、梦幻氛围",
        "prompt": "A surrealist digital illustration: [场景描述]. Strong size contrast, ethereal atmosphere, dreamy colors. Detailed rendering, high artistic quality. Aspect ratio: [比例].",
        "variables": ["场景描述", "比例"]
    },
    {
        "id": "tpl-019",
        "title": "文创产品设计",
        "category": "文创设计",
        "description": "生成书签、明信片、印章等文创产品设计",
        "prompt": "Design a set of [产品类型] featuring [主题]. Style: [设计风格]. Professional quality, suitable for production. Include multiple variations.",
        "variables": ["产品类型", "主题", "设计风格"]
    },
    {
        "id": "tpl-020",
        "title": "九宫格/多图拼贴",
        "category": "图文排版",
        "description": "生成3×3九宫格拼贴图，适合小红书发布",
        "prompt": "Generate a 3:4 vertical 3×3 grid poster for [主题]. Nine distinct cards with unified visual style. Clean layout, Chinese text, suitable for social media. Each card complete and independently readable.",
        "variables": ["主题"]
    },
]

# ============================================================
# GALLERY CASES - PART 2 (cases 166-251) - detailed from fetch
# ============================================================
gallery_part2 = [
    {
        "id": "166",
        "title": "十二黄金圣斗士卡牌合集",
        "category": "IP衍生",
        "description": "生成12宫格黄金圣斗士卡牌，每张标注中文名",
        "prompt": "Generate a 12-grid card image of the 12 Gold Saints from Saint Seiya, with the corresponding Chinese name written on each card, 4 per row, aspect ratio 16:9."
    },
    {
        "id": "167",
        "title": "大唐玄武门之变的朋友圈",
        "category": "趣味创意",
        "description": "仿微信朋友圈界面，模拟玄武门之变历史人物发动态",
        "prompt": "WeChat Moments of the Xuanwu Gate Incident"
    },
    {
        "id": "168",
        "title": "手写中西药方图片",
        "category": "仿真生成",
        "description": "高仿真手写处方笺，中西药方均可",
        "prompt": "Generate an image of a handwritten traditional Chinese medicine or Western medicine prescription"
    },
    {
        "id": "171",
        "title": "信息图可视化设计",
        "category": "信息可视化",
        "description": "10×10网格，每个物品名称以字母a开头",
        "prompt": "create an image with 10x10 grid of objects that have the names starting with letter a."
    },
    {
        "id": "172",
        "title": "赛博科幻桃太郎主视觉图",
        "category": "IP二创",
        "description": "科幻版桃太郎动画主视觉，含角色、背景、标志和宣传语",
        "prompt": "Design a key visual for a fictional animation. The theme is \"Sci-Fi Momotaro\". Design charming characters, backgrounds, logos, and promotional slogans, completed in the form of a beautiful illustration."
    },
    {
        "id": "173",
        "title": "银河繁星点缀的冰蓝襦裙",
        "category": "人像摄影",
        "description": "8K超高清汉服人像，冰蓝色齐胸襦裙，银河感亮片刺绣，丁达尔光效",
        "prompt": "The model wears an exquisite pale ice blue chest-high ruqun, made of multiple layers of lightweight tulle and silk organza. Wide translucent sleeves adorned with tiny silver and light blue sequin embroideries like stars. 8k ultra-high resolution, soft natural side light (Tyndall Effect), 85mm portrait lens f/1.8, full-body composition."
    },
    {
        "id": "174",
        "title": "唐朝贵妇遛粉色马甲异形工笔画",
        "category": "国风插画",
        "description": "工笔画风格，唐朝贵妇遛穿粉色丝绸马甲的异形怪物，反差萌",
        "prompt": "A finely detailed Gongbi painting of a noble Tang Dynasty lady taking a stroll in the imperial garden. She is holding a gold leash. At the end of the leash is a terrifying Xenomorph monster wearing a cute pink silk vest. Background features peonies and butterflies. Red vertical artist chop seal reads \"吴先生\". --ar 3:4"
    },
    {
        "id": "175",
        "title": "封面排版设计图",
        "category": "平面设计",
        "description": "4:3 AI演示平台Chronicle封面，Apple/Linear极简风格",
        "prompt": "Create a premium 4:3 presentation cover slide introducing Chronicle, the AI-native presentation platform. Style: elegant, minimal, modern, similar to Apple/Linear/Notion style. Soft gradient background, clean whitespace, refined typography."
    },
    {
        "id": "176",
        "title": "苏轼被贬首日朋友圈曝光",
        "category": "趣味创意",
        "description": "仿小红书界面，苏轼被贬第一天发动态",
        "prompt": "Su Shi's first day of exile Xiaohongshu screenshot"
    },
    {
        "id": "177",
        "title": "吉利银河暗黑中控界面",
        "category": "UI设计",
        "description": "21:9超宽屏车载中控界面，暗色科技风格",
        "prompt": "Generate a central control interface of Geely Galaxy M9, size 21:9, dark color scheme."
    },
    {
        "id": "178",
        "title": "亚马逊详情图设计",
        "category": "电商设计",
        "description": "亚马逊A+详情图套装，符合平台规范",
        "prompt": "Generate a set of Amazon A+ detail images"
    },
    {
        "id": "179",
        "title": "蒸汽朋克射手座解剖图谱",
        "category": "科普插画",
        "description": "4K蒸汽朋克星座解剖图谱，齿轮管线替代内部结构",
        "prompt": "Generate a vintage steampunk style constellation anatomy atlas poster for Sagittarius. Background: distressed parchment texture. Central subject: mythological image with internal structure replaced by precision gears, pipelines, metal skeletons. 4K, warm brown/beige/bronze palette."
    },
    {
        "id": "180",
        "title": "荒诞超现实女装大叔海报",
        "category": "电影海报",
        "description": "4款专业电影海报，认真又搞笑的女装大叔主题",
        "prompt": "A movie poster featuring a seemingly realistic yet subtly bizarre cross-dressing older man, 4 variations. Reaching the level of a professional designer's production. Title and broadcast information in Japanese."
    },
    {
        "id": "181",
        "title": "潮流视角重塑精致商品广告",
        "category": "电商设计",
        "description": "采用潮流趋势重新设计商品广告",
        "prompt": "Redesign this product advertisement from the perspective of a professional designer. Adopt current fashion trends, exquisite design targeting the target audience."
    },
    {
        "id": "182",
        "title": "千禧年日系校园喜剧场景",
        "category": "影视概念",
        "description": "2000年代面向中学生的日剧喜剧场景",
        "prompt": "2000s Japanese TV drama comedy scene aimed at middle school students"
    },
    {
        "id": "183",
        "title": "一张中文健身信息图",
        "category": "信息可视化",
        "description": "竖版专业健身训练计划信息图，含热身、主训练、进阶路径等完整模块",
        "prompt": "Generate a Chinese fitness infographic. Theme: [训练主题]. Include: title area, training goals, warm-up (2-4 items), main training (4-6 exercises with sets/reps/RIR/rest), progression logic, alternative exercises, execution reminders, recovery suggestions. Clean modern design, vertical layout, modular cards."
    },
    {
        "id": "184",
        "title": "杜甫朋友圈吐槽茅屋被掀翻",
        "category": "趣味创意",
        "description": "仿微信朋友圈，杜甫吐槽茅屋被风吹走",
        "prompt": "Du Fu posting on WeChat Moments complaining about his roof being blown away by the wind"
    },
    {
        "id": "185",
        "title": "武则天发微博自拍太魔性了",
        "category": "趣味创意",
        "description": "仿微博界面，武则天自拍发微博",
        "prompt": "Wu Zetian taking a selfie, registering and posting on Weibo."
    },
    {
        "id": "186",
        "title": "品牌视觉识别图",
        "category": "像素艺术",
        "description": "10×10共100个奇幻RPG道具像素图，SNES/GBA复古风格",
        "prompt": "Create a 10×10 grid of 100 different fantasy RPG items rendered in classic pixel art style (16-bit or 32-bit, SNES/GBA-era JRPGs). 10 row themes: swords/blades, shields/armor, bows/ranged, staves/magic, potions/elixirs, scrolls/spellbooks, rings/amulets, helmets/crowns, keys/relics, gems/runes."
    },
    {
        "id": "187",
        "title": "韩系极简氛围感少女写真",
        "category": "人像摄影",
        "description": "9:16竖版杂志人像，黑色迷雾滤镜，极简室内，氛围安静",
        "prompt": "9:16 vertical editorial portrait. Soft black mist filter, subtle haze, gentle highlight bloom, muted tones. Young Korean woman, minimal makeup, natural skin texture. Sitting on floor, calm expression. Soft side light, gentle shadow falloff. Fine grain, realistic look."
    },
    {
        "id": "188",
        "title": "暗黑极简头像网站视觉设计",
        "category": "品牌VI",
        "description": "为头像美图分享网站图你太美设计ABCD风格VI系统",
        "prompt": "In the style of ABCD (a black cover design), design a VI system for Tu Ni Tai Mei. Tu Ni Tai Mei is an avatar and beauty photo sharing website."
    },
    {
        "id": "189",
        "title": "清新夏日女装连衣裙电商展示",
        "category": "电商设计",
        "description": "夏季女裙电商详情图，清新风格",
        "prompt": "Summer women's dress e-commerce detail image"
    },
    {
        "id": "190",
        "title": "全自动咖啡机产品展示",
        "category": "电商设计",
        "description": "全自动咖啡机电商详情展示图",
        "prompt": "Fully automatic coffee machine e-commerce detail image"
    },
    {
        "id": "191",
        "title": "史诗级科幻电影海报设计",
        "category": "电影海报",
        "description": "商业级科幻电影海报",
        "prompt": "Create a Science fiction movie poster"
    },
    {
        "id": "192",
        "title": "未来科技感AI智能眼镜详情页",
        "category": "电商设计",
        "description": "AI智能眼镜电商详情图，未来科技感",
        "prompt": "AI smart glasses e-commerce detail image"
    },
    {
        "id": "193",
        "title": "千手观音化身打工人",
        "category": "国风插画",
        "description": "工笔画千手观音，千手拿笔记本电脑、咖啡杯等现代办公物品",
        "prompt": "A highly detailed Gongbi painting of the Bodhisattva \"Guanyin of a Thousand Hands\". Instead of sacred artifacts, the thousand hands are holding modern office items: laptops, smartphones, stacks of paperwork, coffee cups, stamps, calculators, mops, and baby bottles. Golden aura made of spinning clock gears. Red seal \"吴先生\". --ar 3:4"
    },
    {
        "id": "194",
        "title": "健身蛋白粉电商详情页",
        "category": "电商设计",
        "description": "健身蛋白粉电商详情图",
        "prompt": "Fitness protein powder e-commerce detail image"
    },
    {
        "id": "195",
        "title": "超写实与水墨的梦幻融合",
        "category": "艺术创意",
        "description": "8K超写实人像与传统水墨（佛像/墨龙/锦鲤）自然融合，博物馆级美学",
        "prompt": "A dynamic mixed-media photograph blending hyper-realistic portraiture with traditional Chinese ink illustration. Central figure: photorealistic young Asian woman. Ink elements: Tathagata Buddhas, Guanyin figures, Chinese ink dragons, koi fish. Black ink and cinnabar red tones. Cinematic photography, 8k, fine art composition, museum-level aesthetic. 3:4."
    },
    {
        "id": "196",
        "title": "试卷上的涂鸦巨龙",
        "category": "创意插画",
        "description": "涂鸦风格巨龙，绘制在真实试卷页面上，线条混乱密集",
        "prompt": "A colossal dragon drawn with extremely dense chaotic scribble lines on a real printed textbook or exam paper page. Ballpoint pen drawing style, fine ink lines. Dark muted tones with subtle neon accents. Selective bioluminescent glow in eyes and core. Surreal, mysterious atmosphere."
    },
    {
        "id": "197",
        "title": "英雄联盟特朗普中路对决哈梅内伊",
        "category": "趣味创意",
        "description": "仿LOL游戏界面，特朗普vs哈梅内伊中路对线",
        "prompt": "Generate a screenshot of Trump versus Khamenei in the mid lane in League of Legends."
    },
    {
        "id": "198",
        "title": "苍白陶瓷娃娃沙滩仰视",
        "category": "人像摄影",
        "description": "iPhone前置POV视角沙滩自拍，陶瓷娃娃美学，暗黑诡异感",
        "prompt": "iPhone 15 Pro front selfie, high angle POV. Porcelain doll aesthetic, flawless pale skin, huge ice-blue eyes, platinum blonde double braids. Bright beach, looking up at camera, shielding sunlight with one hand. Soft pastel tones, high exposure."
    },
    {
        "id": "199",
        "title": "超写实海滩高角度手机自拍",
        "category": "人像摄影",
        "description": "iPhone超写实自拍，真实皮肤纹理/毛孔/绒毛，无美颜滤镜",
        "prompt": "Ultra-realistic iPhone 15 Pro front-camera selfie. Adult woman on a bright beach, raised-arm high-angle perspective. Real photographic skin texture, visible pores, subtle peach fuzz. 24mm equivalent wide-angle. Neutral expression. Platinum-blonde hair in two tight braids. 5500K coastal daylight. Realistic, no airbrushing."
    },
    {
        "id": "200",
        "title": "热度爆表的美女内衣直播间",
        "category": "趣味创意",
        "description": "仿抖音直播截图，美女卖内衣，在线99996人，热度18+",
        "prompt": "Generate a screenshot of a Douyin live stream featuring a beautiful woman live streaming, selling pantyhose and underwear, online viewer count is 99996, popularity rating is 18+, a big brother named Xiao Hu sent her an airplane gift"
    },
    {
        "id": "201",
        "title": "三甲医院真实门诊处方笺",
        "category": "仿真生成",
        "description": "高仿真三甲医院门诊处方笺，手写字体真实",
        "prompt": "An outpatient prescription sheet from a Grade 3A hospital, doctor's illegible handwriting, containing realistic and reasonable diagnosis, drug names, dosages, with a doctor's signature and department stamp in the bottom right corner."
    },
    {
        "id": "202",
        "title": "宅男必看绝美二次元少女",
        "category": "二次元插画",
        "description": "高质量二次元美少女插画",
        "prompt": "Generate high-quality beautiful girl (otaku must-have)"
    },
    {
        "id": "203",
        "title": "杠精视角的独特文案创意",
        "category": "文案创意",
        "description": "杠精视角文案配视觉画面",
        "prompt": "Troll perspective copywriting + GPT Image 2"
    },
    {
        "id": "204",
        "title": "智能动画分镜生成器",
        "category": "工具类",
        "description": "动画分镜生成器界面/概念图",
        "prompt": "Generate an animation storyboard generator"
    },
    {
        "id": "205",
        "title": "皇宫深处的御用快递驿站",
        "category": "趣味创意",
        "description": "古代皇宫和现代快递驿站融合场景",
        "prompt": "Generate an ancient imperial palace × express delivery station"
    },
    {
        "id": "206",
        "title": "国风工笔八仙长卷插画",
        "category": "国风插画",
        "description": "4K横向长卷八仙人物群像，工笔质感细腻",
        "prompt": "Generate a Chinese traditional character group portrait long scroll poster for the Eight Immortals. Horizontal composition, all characters in a queue from left to right. Distinct traditional clothing, iconic props. Calligraphy title at top. Xuan paper texture background. 4K long scroll."
    },
    {
        "id": "207",
        "title": "黑神话潘金莲绝美游戏封面",
        "category": "游戏设计",
        "description": "黑神话系列暗黑国风美术风格游戏介绍界面",
        "prompt": "Generate a game introduction screen for Black Myth: Pan Jinlian, the character is extremely charming."
    },
    {
        "id": "208",
        "title": "樱花树下害羞双马尾少女",
        "category": "二次元插画",
        "description": "8K超精细二次元美少女壁纸，樱花粉双马尾JK制服，16:9",
        "prompt": "Generate a high-quality anime beautiful girl. 17 years old, twin tails cherry blossom pink with gradient purple tips. Purple eyes with star highlights. JK uniform. Background: cherry blossom tree, petals falling. Expression: shy smile. 16:9, 8K."
    },
    {
        "id": "209",
        "title": "神话三国枪战世界",
        "category": "游戏设计",
        "description": "无畏契约风格的三国神话FPS游戏概念图",
        "prompt": "Imitating the style of Valorant, generate a Three Kingdoms mythological FPS game"
    },
    {
        "id": "210",
        "title": "萌系大模型训练图解",
        "category": "科普插画",
        "description": "萌系可爱风格解释大语言模型训练过程",
        "prompt": "Cute explanation of the large language model training process"
    },
    {
        "id": "211",
        "title": "天坛古建拆解全图",
        "category": "信息可视化",
        "description": "天坛建筑拆解图，中式美学风格，详细说明标注",
        "prompt": "Generate an architectural exploded view of the Temple of Heaven, with detailed annotations, Chinese aesthetic style"
    },
    {
        "id": "212",
        "title": "专业设计师打造角色写真集",
        "category": "二次元插画",
        "description": "为指定角色制作专业设计师级别写真集，日语文字，丰富场景",
        "prompt": "Use this character to create a photo book crafted by a professional designer. Language: Japanese. Rich scenes, large amount of information."
    },
    {
        "id": "213",
        "title": "金瓶梅古风开放世界游戏截图",
        "category": "游戏设计",
        "description": "以金瓶梅为主题的古代ARPG MMO开放世界游戏截图",
        "prompt": "Generate a screenshot of an ancient ARPG MMO open-world game themed around Jin Ping Mei."
    },
    {
        "id": "214",
        "title": "绘制金瓶梅知识图谱",
        "category": "信息可视化",
        "description": "3:4潘金莲主题科普知识图谱，复古泛黄纸张，6-8个知识模块",
        "prompt": "Generate a highly detailed scientific encyclopedia infographic. Subject: Pan Jinlian. Central subject with 3D pop-out effect. 6-8 knowledge modules: character relationships, life story, literary value. Retro aged beige paper. Clear Chinese annotations. 3:4."
    },
    {
        "id": "215",
        "title": "西方艺术演进像素博物馆",
        "category": "像素艺术",
        "description": "4K 3:4等距像素艺术时间线，西方艺术发展史演进博物馆",
        "prompt": "Create an ultra-high-detail isometric pixel art timeline illustration (3:4, 4K). Theme: Western Art Development. Build an isometric \"Evolution Museum\". Each exhibition hall represents an evolution stage. Bilingual pixel font titles. Professional, suitable for academic analysis."
    },
    {
        "id": "216",
        "title": "雅致图案四款时尚单品设计",
        "category": "时尚设计",
        "description": "基于指定图案设计4款时尚单品，附带穿搭效果图",
        "prompt": "Use the patterns in the attached image to create 4 fashion items, using different color schemes and layout designs, accompanied by outfit effect pictures. Elegant composition. Format: 2:3."
    },
    {
        "id": "217",
        "title": "昏暗室内纯真少女的意外回眸",
        "category": "人像摄影",
        "description": "日系CCD相机抓拍风格，老式闪光灯，颗粒感，意外被拍的表情",
        "prompt": "Mobile phone photo, old CCD camera aesthetic, harsh flash, grainy, dim messy indoor lighting, candid snapshot feeling. Young Korean female idol, soft innocent look. Mid-action, slightly turning head toward camera. Shy and caught-off-guard expression. 9:16."
    },
    {
        "id": "218",
        "title": "绘制科学百科知识图谱",
        "category": "信息可视化",
        "description": "通用科普知识图谱模板，支持人物/植物/动物，3:4比例",
        "prompt": "Generate a highly detailed scientific encyclopedia infographic. Subject: choose from People/Plants/Animals. Central subject with 3D pop-out effect. 6-8 modules. Retro aged beige paper. Clear Chinese calligraphy title. All annotations in legible Chinese. 3:4."
    },
    {
        "id": "219",
        "title": "韩系偶像九宫格写真集",
        "category": "人像摄影",
        "description": "9:16 3×3拼贴，9张图人物完全一致，偶像写真集/小卡美学",
        "prompt": "9:16 vertical 3x3 grid collage forming a Korean idol portrait photoshoot. Same young Korean female idol in all 9 frames, 100% consistent facial features/proportions/hairstyle. Natural skin texture, no retouching. Soft diffused natural light. Intimate, soft, natural everyday charm. 8K, subtle analog film grain."
    },
    {
        "id": "220",
        "title": "鎏金广州塔的东方奇幻海报",
        "category": "海报设计",
        "description": "9:16东方奇幻广州城市海报，金色能量线条，广州塔地标，白发女性，8K",
        "prompt": "Flat illustration, Oriental fantasy style high-end city poster for Guangzhou, 9:16. Diagonal + S-shaped flowing composition. Black background gradient to dark red. Golden flowing energy line through center. Canton Tower as visual core with Lingnan architecture. White-haired female figure at bottom. Cinematic lighting, 8K."
    },
    {
        "id": "221",
        "title": "窗边日系胶片女孩",
        "category": "人像摄影",
        "description": "35mm胶片摄影，日系柔和美学，窗户自然光，轻微过曝",
        "prompt": "Analog 35mm film photography, soft airy Japanese-style aesthetic, gentle diffused natural window light, slight overexposure, pastel tones, low contrast. Young East Asian woman, natural minimal makeup. Oversized white button-up shirt. Standing by window with white curtains. Soft film grain, dreamy atmosphere. --ar 9:16"
    },
    {
        "id": "222",
        "title": "精致模块化科普百科图鉴",
        "category": "信息可视化",
        "description": "竖版模块化科普信息图，图鉴+百科+信息结构+收藏感",
        "prompt": "Generate a high-quality vertical modular popular science encyclopedia infographic. Module structure: main visual, enlarged details, rounded information sections, title hierarchy, key tags, encyclopedia content, scoring/ratings. Light clean background, soft colors, neat typography. Readable and collectible."
    },
    {
        "id": "223",
        "title": "春日禅意水墨群山海报",
        "category": "海报设计",
        "description": "新中式水墨山水海报，禅意美学，群山/湖面/红衣渔女，8K",
        "prompt": "Neo-Chinese ink wash landscape poster, 9:16. Spring morning atmosphere: cyan-green, misty blue, light gray. Mountains rising from calm lake. Small wooden boat with fisherwoman in red. Calligraphy \"东方美学\" at top. Ink wash + modern minimalist fusion. Zen atmosphere, 8K."
    },
    {
        "id": "224",
        "title": "机甲少女立于废弃海城",
        "category": "二次元插画",
        "description": "16:9电影感动漫主视觉，机甲少女+废弃海上都市，赛博朋克废土感",
        "prompt": "Mecha girl mid-teens, pale skin, sharp amber eyes, ash-white hair in high ponytail. Matte gunmetal exoskeleton armor. Standing on rusted steel platform over dark water. Background: vast derelict sea-city at dusk with colossal megastructures. Cinematic anime key visual. 35mm anamorphic lens. Desaturated oceanic palette. 16:9."
    },
    {
        "id": "225",
        "title": "大师级真迹复刻",
        "category": "艺术仿真",
        "description": "生成指定大师作品真迹仿真图片",
        "prompt": "Generate xxxx authentic picture"
    },
    {
        "id": "226",
        "title": "古风明朝帝王群像长卷",
        "category": "国风插画",
        "description": "明朝历代皇帝国风头像，下方标注谥号和名字",
        "prompt": "Generate portraits of the emperors of the Ming Dynasty, with their posthumous titles and names below the portraits"
    },
    {
        "id": "227",
        "title": "哔哩哔哩户晨风直播截图",
        "category": "趣味创意",
        "description": "9:16 B站直播截图，户晨风持牌引导关注",
        "prompt": "9:16 image, generate a screenshot of a Bilibili live stream, Hu Chenfeng broadcasting live holding a sign: \"Boss Austin is so emotional, everyone please give Boss Austin some follows.\""
    },
    {
        "id": "228",
        "title": "完美匹配的海报广告图",
        "category": "广告设计",
        "description": "与参考图风格匹配的商业广告图，信息量丰富",
        "prompt": "Generate an advertising image that perfectly matches this image. There should be a lot of information."
    },
    {
        "id": "229",
        "title": "琉璃透明画眉鸟飞舞羊城墨卷",
        "category": "国风插画",
        "description": "9:16广州主题插画，纯黑底色S型墨线，透明画眉鸟，广州地标",
        "prompt": "Pure black background, thick S-shaped calligraphy curve. Transparent thrush with glass texture, internal reflection of Guangzhou landmarks. Canton Tower, Baiyun Mountain, Chen Clan Ancestral Hall along the curve. White cranes, blue lake, distant mountains. Cool tones with warm accents. 8K, 9:16."
    },
    {
        "id": "230",
        "title": "极简国潮鎏金广州塔海报",
        "category": "海报设计",
        "description": "新中式极简广州城市海报，中国红+青蓝+鎏金，大面积留白",
        "prompt": "Neo-Chinese minimalist high-end city poster for Guangzhou, 9:16. Abstract geometric Canton Tower at center. S-shaped composition. Pearl River water ripples fused with auspicious cloud patterns. Colors: Chinese red, cyan blue, gilded gold. Large blank space, light Xuan paper texture. 8K."
    },
    {
        "id": "231",
        "title": "疾风起狂草艺术字体设计",
        "category": "字体设计",
        "description": "创意狂草艺术字纵有疾风起，荷兰角构图，黑色背景",
        "prompt": "Creative artistic typography \"Zong You Ji Feng Qi\", hand-written style with fine brush. Rugged and free-spirited brushstrokes. Dutch angle, dynamic sprinting momentum. Pure black background. High visual impact."
    },
    {
        "id": "232",
        "title": "兰亭集序书法帖意境图",
        "category": "书法创意",
        "description": "兰亭集序书法帖，背景融合兰亭意境，蒙版设计",
        "prompt": "Generate a calligraphy copy image combining Wang Xizhi's \"Lantingji Xu\" content. Background matches the artistic conception of Lantingji Xu (landscape, winding stream). Foreground: Lantingji Xu calligraphy text."
    },
    {
        "id": "233",
        "title": "蒙娜丽莎畅饮可乐的趣味油画",
        "category": "趣味创意",
        "description": "名画二创，蒙娜丽莎喝可乐",
        "prompt": "Generate an oil painting of Mona Lisa drinking cola."
    },
    {
        "id": "234",
        "title": "朱元璋登基后的推特主页",
        "category": "趣味创意",
        "description": "仿X(推特)界面，朱元璋登基后发帖",
        "prompt": "Create an X post page of Zhu Yuanzhang after his ascension to the throne in the Ming Dynasty"
    },
    {
        "id": "235",
        "title": "治愈系助眠指南九宫格",
        "category": "图文排版",
        "description": "3:4小红书九宫格，8个助眠技巧，奶油白+ins风，可切图发布",
        "prompt": "Generate a 3:4 vertical 9-grid poster for sleep tips. 3x3 layout. Cover: \"8 tips to make you fall asleep instantly\". 8 tips on sleep hygiene. Cream white, beige, caramel tones. Ins style, healing aesthetic. Each grid independently readable. Suitable for Xiaohongshu."
    },
    {
        "id": "236",
        "title": "粤超联赛国潮风邀请函海报",
        "category": "海报设计",
        "description": "9:16粤超联赛邀请函，S型构图，足球能量流，广东地标，中国红主视觉",
        "prompt": "Guangdong Provincial City Football Super League invitation poster, 9:16. S-shaped flowing composition. Glowing football at center with energy trail. Guangdong landmarks: Canton Tower, Shenzhen Ping An Centre, Zhuhai Fisher Girl. Colors: Chinese red primary, cyan-blue auxiliary, gold highlights. Cinematic lighting, 8K."
    },
    {
        "id": "237",
        "title": "夏日柑橘苏打高转化广告图",
        "category": "电商设计",
        "description": "3:4夏日碳酸饮料广告，500ml PET瓶，高CTA设计",
        "prompt": "Product advertising photo for summer seasonal carbonated beverage \"Summer Citrus SODA\", 500ml PET bottle. Research 2025 high CTA design. Aspect ratio 3:4."
    },
    {
        "id": "238",
        "title": "星云巨鲤与小人的奇幻对话",
        "category": "艺术创意",
        "description": "9:16超现实插画，低角度仰拍，巨型锦鲤遨游星云，小人仰望",
        "prompt": "A surrealist digital illustration, low-angle upward perspective. Giant colorful koi swimming in dreamy nebula. Small figure standing in center, looking up at the koi. Strong size contrast, ethereal dreamy atmosphere. 9:16."
    },
    {
        "id": "239",
        "title": "刘亦菲抖音直播畅聊中",
        "category": "趣味创意",
        "description": "9:16抖音直播截图，刘亦菲持牌欢迎观众畅聊",
        "prompt": "9:16 aspect ratio, generate a screenshot of a Douyin live stream, Liu Yifei live streaming holding a sign: \"Tonight's live stream, welcome to join Yifei for a chat!\""
    },
    {
        "id": "240",
        "title": "胶片闪光灯下的球场少女",
        "category": "人像摄影",
        "description": "35mm胶片篮球场少女写真，强烈机顶闪光灯，真实毛孔雀斑，9:16",
        "prompt": "35mm color film photography with harsh direct on-camera flash. Chinese female idol on outdoor basketball court at dusk. Realistic porcelain skin with visible flash specular highlights. Dark brown hair in high ponytail. Loose white tank top, white basketball shorts. Leaning against hoop pole. High contrast film grading, 9:16."
    },
    {
        "id": "241",
        "title": "关键人物关系图谱",
        "category": "信息可视化",
        "description": "文学作品/影视剧人物关系图",
        "prompt": "Generate a key character relationship diagram for \"XXX\"."
    },
    {
        "id": "242",
        "title": "绝美国风工笔画书签设计",
        "category": "文创设计",
        "description": "国风工笔画风格书签系列设计稿",
        "prompt": "Generate a series of design drafts for Gongbi painting bookmarks."
    },
    {
        "id": "243",
        "title": "定制专属风格界面设计系统",
        "category": "UI设计",
        "description": "指定风格的完整UI设计系统，含网页/移动端/组件",
        "prompt": "Generate a UI design system in xx style, including web pages, mobile, cards, controls, buttons, and others"
    },
    {
        "id": "244",
        "title": "杜蕾斯茶颜悦色联名海报设计",
        "category": "广告设计",
        "description": "杜蕾斯×茶颜悦色联名宣传物料",
        "prompt": "Design a set of promotional materials for a Durex and Chayan Yuese co-branding campaign."
    },
    {
        "id": "245",
        "title": "马斯克专属篆刻印章设计",
        "category": "文创设计",
        "description": "为埃隆·马斯克设计篆刻印章",
        "prompt": "Design a set of seal carving stamps for \"Elon Musk\""
    },
    {
        "id": "246",
        "title": "黑白线稿勾勒的上海风情",
        "category": "城市插画",
        "description": "黑色线稿风格上海主题明信片",
        "prompt": "Design a Shanghai postcard in black line art style."
    },
    {
        "id": "247",
        "title": "运动健身图标字体设计",
        "category": "图标设计",
        "description": "运动类APP图标字体(iconfont)套装",
        "prompt": "Generate a set of iconfont for a sports app"
    },
    {
        "id": "248",
        "title": "景德镇青花瓷全景解说图谱",
        "category": "信息可视化",
        "description": "景德镇青花瓷详细解说图，中文知识解析，非遗科普",
        "prompt": "Generate a detailed explanatory diagram of Jingdezhen blue and white porcelain, accompanied by detailed Chinese knowledge analysis."
    },
    {
        "id": "249",
        "title": "美女举牌感谢大哥打赏大火箭",
        "category": "趣味创意",
        "description": "抖音直播截图，美女持牌感谢行者大哥大火箭",
        "prompt": "Generate a screenshot of a TikTok live stream, a beautiful woman live streaming holding a sign: \"Thank you Brother Xingzhe for the big rocket!\""
    },
    {
        "id": "250",
        "title": "小王子与星舰的浪漫联名",
        "category": "文创设计",
        "description": "小王子×SpaceX联名明信片设计",
        "prompt": "Design a postcard co-branded by The Little Prince and SpaceX"
    },
    {
        "id": "251",
        "title": "言叶之庭春雨绿意单日历",
        "category": "文创设计",
        "description": "言叶之庭主题春雨绿意风格单日历",
        "prompt": "The Garden of Words spring rain greenery single calendar"
    },
]

# ============================================================
# GALLERY CASES - PART 1 (representative cases 1-165)
# ============================================================
gallery_part1 = [
    {"id": "1", "title": "3D渲染的等距房间", "category": "3D渲染", "description": "3D等距视角的室内房间渲染", "prompt": "3D rendered isometric room with detailed furniture and warm lighting"},
    {"id": "2", "title": "像素艺术游戏场景", "category": "像素艺术", "description": "16位像素风格游戏场景", "prompt": "16-bit pixel art game scene with parallax background layers"},
    {"id": "5", "title": "国潮品牌Logo设计", "category": "品牌VI", "description": "国潮风格品牌Logo设计", "prompt": "Design a Guochao style brand logo combining traditional Chinese elements with modern aesthetics"},
    {"id": "8", "title": "赛博朋克城市夜景", "category": "概念设计", "description": "赛博朋克风格未来城市", "prompt": "Cyberpunk city night scene with neon lights, flying cars, and rainy streets"},
    {"id": "12", "title": "中国风山水插画", "category": "国风插画", "description": "中国传统水墨山水画风格", "prompt": "Traditional Chinese ink wash landscape painting with mountains, mist, pine trees, and a small boat on a river"},
    {"id": "15", "title": "产品包装设计", "category": "包装设计", "description": "简约高端产品包装设计", "prompt": "Minimalist luxury product packaging design with gold foil accents on matte black box"},
    {"id": "20", "title": "日系动漫人物立绘", "category": "二次元插画", "description": "日系动漫风格人物全身立绘", "prompt": "Japanese anime style full-body character illustration with detailed costume design"},
    {"id": "25", "title": "极简App界面设计", "category": "UI设计", "description": "极简风格移动App界面", "prompt": "Minimalist mobile app UI design with clean typography and muted color palette"},
    {"id": "30", "title": "写实食物摄影", "category": "摄影仿真", "description": "高端美食摄影风格", "prompt": "Professional food photography, overhead flat lay composition, natural lighting"},
    {"id": "35", "title": "复古胶片风人像", "category": "人像摄影", "description": "35mm胶片风格人像摄影", "prompt": "35mm film portrait photography, warm tones, natural grain, soft bokeh background"},
    {"id": "40", "title": "概念汽车设计图", "category": "工业设计", "description": "未来概念汽车设计", "prompt": "Futuristic concept car design sketch, aerodynamic body, electric vehicle"},
    {"id": "45", "title": "扁平化信息图", "category": "信息可视化", "description": "扁平风格数据可视化信息图", "prompt": "Flat design infographic with data visualization, clean icons, and modern color scheme"},
    {"id": "50", "title": "蒸汽朋克机械设计", "category": "概念设计", "description": "蒸汽朋克风格机械装置", "prompt": "Steampunk mechanical device design with brass gears, pipes, and Victorian era aesthetics"},
    {"id": "55", "title": "水彩风格花卉插画", "category": "插画设计", "description": "水彩手绘风格花卉", "prompt": "Watercolor style floral illustration with soft edges and pastel colors"},
    {"id": "60", "title": "极简Logo设计", "category": "品牌VI", "description": "极简几何风Logo", "prompt": "Minimalist geometric logo design, clean lines, monochrome palette"},
    {"id": "65", "title": "科幻太空场景", "category": "概念设计", "description": "科幻太空站场景", "prompt": "Sci-fi space station interior with holographic displays and astronauts"},
    {"id": "70", "title": "杂志封面排版", "category": "平面设计", "description": "时尚杂志封面设计", "prompt": "Fashion magazine cover layout with bold typography and editorial photography style"},
    {"id": "75", "title": "Q版卡通角色", "category": "角色设计", "description": "可爱Q版卡通角色设计", "prompt": "Cute chibi cartoon character design with big eyes and simple color blocks"},
    {"id": "80", "title": "建筑效果图渲染", "category": "建筑设计", "description": "现代建筑外观效果图", "prompt": "Modern architectural rendering with glass facade, surrounded by greenery, golden hour lighting"},
    {"id": "85", "title": "手绘风格地图", "category": "信息可视化", "description": "手绘风格城市地图", "prompt": "Hand-drawn style city map with illustrated landmarks and labeled streets"},
    {"id": "90", "title": "科技产品特写", "category": "产品摄影", "description": "科技产品微距特写", "prompt": "Tech product macro photography, dark background, dramatic studio lighting"},
    {"id": "95", "title": "敦煌壁画风格", "category": "国风插画", "description": "敦煌飞天壁画风格", "prompt": "Dunhuang mural style illustration with flying apsaras and celestial beings"},
    {"id": "100", "title": "波普艺术风格", "category": "艺术风格", "description": "安迪沃霍尔式波普艺术", "prompt": "Pop art style portrait in Andy Warhol style, vibrant colors, halftone dots"},
    {"id": "105", "title": "等距城市建筑群", "category": "3D渲染", "description": "等距视角城市建筑群", "prompt": "Isometric city buildings cluster, colorful facades, clean vector style"},
    {"id": "110", "title": "暗黑奇幻角色设计", "category": "角色设计", "description": "暗黑奇幻风格角色", "prompt": "Dark fantasy character design with intricate armor and magical effects"},
    {"id": "115", "title": "卡通吉祥物设计", "category": "角色设计", "description": "品牌卡通吉祥物", "prompt": "Brand mascot cartoon character design, friendly and approachable, vector style"},
    {"id": "120", "title": "纹理材质贴图", "category": "素材生成", "description": "无缝纹理材质贴图", "prompt": "Seamless texture material: wood grain, marble, fabric, metal, concrete"},
    {"id": "125", "title": "北欧风室内设计", "category": "室内设计", "description": "北欧简约风室内空间", "prompt": "Scandinavian style interior design with natural light, wooden furniture, and plants"},
    {"id": "130", "title": "液体流动抽象艺术", "category": "艺术创意", "description": "液态金属/颜料流动抽象艺术", "prompt": "Abstract liquid art with flowing metallic paints, iridescent colors, macro photography"},
    {"id": "135", "title": "日式禅意庭院", "category": "景观设计", "description": "日式枯山水庭院设计", "prompt": "Japanese zen garden with raked sand patterns, moss-covered rocks, and bamboo fence"},
    {"id": "140", "title": "赛博朋克角色立绘", "category": "角色设计", "description": "赛博朋克风格角色", "prompt": "Cyberpunk character illustration with neon prosthetics, leather jacket, and futuristic city background"},
    {"id": "145", "title": "极简名片设计", "category": "品牌VI", "description": "极简高端名片设计", "prompt": "Minimalist luxury business card design with letterpress and gold foil on premium paper"},
    {"id": "150", "title": "动态海报设计", "category": "海报设计", "description": "电影级动态海报", "prompt": "Cinematic movie poster with dynamic composition, dramatic lighting, and title typography"},
    {"id": "155", "title": "儿童绘本插画", "category": "插画设计", "description": "温暖儿童绘本风格", "prompt": "Children's book illustration style, warm and whimsical, soft watercolor textures"},
    {"id": "160", "title": "徽章/图标设计", "category": "图标设计", "description": "精致的徽章风格图标", "prompt": "Emblem badge design with intricate details, gold metallic finish, ribbon elements"},
    {"id": "165", "title": "涂鸦街头艺术", "category": "艺术风格", "description": "街头涂鸦风格墙绘", "prompt": "Street art graffiti mural with bold colors, spray paint texture, urban wall background"},
]

# Combine all data
all_data = {
    "templates": templates,
    "cases": gallery_part1 + gallery_part2,
    "metadata": {
        "source": "awesome-gpt-image-2 by freestylefly",
        "repo": "https://github.com/freestylefly/awesome-gpt-image-2",
        "gallery_visual": "https://gpt-image2.canghe.ai/",
        "total_templates": len(templates),
        "total_cases": len(gallery_part1) + len(gallery_part2),
        "categories": [
            "信息可视化", "海报设计", "电商设计", "趣味创意", "人像摄影",
            "国风插画", "二次元插画", "UI设计", "品牌VI", "平面设计",
            "电影海报", "游戏设计", "像素艺术", "创意插画", "艺术创意",
            "科普插画", "字体设计", "文创设计", "图文排版", "仿真生成",
            "IP二创", "IP衍生", "工业设计", "概念设计", "角色设计",
            "时尚设计", "包装设计", "图标设计", "3D渲染", "摄影仿真",
            "建筑设计", "产品摄影", "文案创意", "影视概念", "工具类",
            "城市插画", "广告设计", "书法创意", "艺术仿真", "插画设计",
            "艺术风格", "素材生成", "室内设计", "景观设计"
        ]
    }
}

# Save templates
with open(f"{OUTPUT_DIR}/templates.json", "w", encoding="utf-8") as f:
    json.dump(templates, f, ensure_ascii=False, indent=2)

# Save all cases
with open(f"{OUTPUT_DIR}/cases.json", "w", encoding="utf-8") as f:
    json.dump(gallery_part1 + gallery_part2, f, ensure_ascii=False, indent=2)

# Save combined
with open(f"{OUTPUT_DIR}/all-data.json", "w", encoding="utf-8") as f:
    json.dump(all_data, f, ensure_ascii=False, indent=2)

print(f"Generated {len(templates)} templates")
print(f"Generated {len(gallery_part1) + len(gallery_part2)} cases total")
print(f"Part 1: {len(gallery_part1)} cases")
print(f"Part 2: {len(gallery_part2)} cases")
print(f"Data files saved to: {OUTPUT_DIR}")
