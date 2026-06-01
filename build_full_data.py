"""
Build complete prompt data - with detailed Part 1 cases from latest fetch.
"""
import json
import os

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

# ============================================================
# GALLERY PART 1 - Detailed (from latest fetch, cases 1-73)
# ============================================================
gallery_part1_detailed = [
    {"id": "1", "title": "信息图可视化设计：城市生命系统图谱", "category": "信息可视化",
     "description": "9:16等距剖面图，智慧城市从天空到基岩的全维度展示",
     "prompt": "Vertical 9:16 isometric cutaway infographic \"城市生命系统图谱 / Urban Metabolism Atlas\". Smart city from sky to bedrock: skyscrapers, streets, subway, utility tunnels, water/sewage/gas/heating pipes, fiber, data center, flood tanks, aquifers, geothermal wells, bedrock. Color-coded flows. 12 numbered panels bilingual CN/EN. Style: engineering white paper + scientific atlas, 8K."},
    {"id": "2", "title": "社媒界面截图：X推文推荐", "category": "趣味创意",
     "description": "深色模式X截图，@OpenAI认证账号推荐AI Builder",
     "prompt": "画一张 X 的内容截图，深色模式，@OpenAI 蓝勾认证账号发推。正文推荐AI Builder Ailln AI。底部添加宣传海报。互动数据：评论8.9K、转发42K、点赞298K、收藏34K、浏览32.4M。3:4比例。"},
    {"id": "3", "title": "足球主题电影海报", "category": "电影海报",
     "description": "欧冠之夜史诗氛围，国际米兰后卫激情庆祝",
     "prompt": "生成一张「足球主题电影海报」风格的高清写真海报：国际米兰后卫巴斯托尼站在圣西罗球场中央激情庆祝，双手高举并披着波黑国旗。蓝黑色烟雾、聚光灯、飘扬旗帜。电影感光影，高对比度，超清细节，8K。"},
    {"id": "4", "title": "老干妈风味：特朗普抖音直播卖老干妈", "category": "趣味创意",
     "description": "特朗普在SpaceX科技感直播间卖老干妈",
     "prompt": "特朗普在抖音直播间卖老干妈，手里举着「老干妈风味」新品，背景是SpaceX科技感，左下角弹幕飘着「特斯拉车主：求上链接」。"},
    {"id": "5", "title": "主题海报版式设计：史诗叙事海报", "category": "海报设计",
     "description": "人物侧脸剪影+世界观填充式叙事合成，双重曝光+电影海报融合",
     "prompt": "根据主题自动生成收藏版史诗叙事海报：巨大优雅的人物侧脸剪影作为外轮廓，剪影内部自动生长出完整世界观。双重曝光式联想，电影海报与梦幻水彩插画融合风格。签名\"WHY\"低调清晰。版式克制高级。"},
    {"id": "6", "title": "插画艺术：日系唯美奇幻少女", "category": "二次元插画",
     "description": "天空之镜水面反射，粉紫星空，蓝色流星，9:16 4K",
     "prompt": "日系唯美奇幻风格插画。可爱少女站立在镜面般平滑水面中心。高饱和粉紫与深蓝交织天空，蓝色巨型流星划破天际。下方水面完美反射。比例9:16，分辨率4K。"},
    {"id": "7", "title": "应用界面样机：Galgame风格角色截图", "category": "UI设计",
     "description": "竖版手机截图风格，真人coser+二次元角色，galgame对话框",
     "prompt": "生成竖版手机截图，9:16。真人coser扮演二次元角色，写实风格五官略带动漫感。底部叠加半透明galgame风格对话框，左侧Q版头像，右侧角色名和治愈台词。底部操作栏仿galgame UI。"},
    {"id": "8", "title": "科普百科图：模块化科普信息图", "category": "信息可视化",
     "description": "兼具图鉴感、百科感、信息结构感的模块化科普图",
     "prompt": "根据主题生成高质量竖版科普百科图。包含主题主视觉、局部特征放大、圆角模块化信息分区、标题层级、百科内容、可视化评分。浅色干净背景，柔和配色，精致小图标，整洁排版。突出知识整理+模块信息+图鉴式展示。"},
    {"id": "9", "title": "主题海报：2026中国城市系列·北京", "category": "海报设计",
     "description": "国潮风城市海报，红绸S型构图，融合北京地标",
     "prompt": "2026中国城市系列宣传海报，主题北京。国潮风，竖版9:16。红色丝绸S型主构图。融合天坛、长城、鸟巢、什刹海等北京地标。SPRING 2026 + 竖排Beijing + 小印章\"北京\"。"},
    {"id": "10", "title": "主题海报：八十年代宣传画风格", "category": "海报设计",
     "description": "庆祝GPT-Image-2全量开放，Sam Altman等人戴红领巾",
     "prompt": "生成八十年代宣传画，标语\"热烈庆祝GPT-Image-2全量开放\"，人物包含Sam Altman、Dario Amodei、Elon Musk，Dario Amodei带上红领巾。"},
    {"id": "11", "title": "手绘城市美食地图·台州", "category": "信息可视化",
     "description": "鸟瞰手绘水彩风格，12个台州美食地点，1:1比例",
     "prompt": "手绘风格城市美食地图，台州为主题。鸟瞰视角水彩手绘，标注椒江、路桥、黄岩等区域。12个美食地点精致手绘小插画：蛋清羊尾、食饼筒、青蟹、海鲜面、糟羹等。藤蔓杨梅枝装饰边框。标题\"台州·山海食光地图\"。比例1:1。"},
    {"id": "13", "title": "信息图：中国高中数学试卷仿真", "category": "仿真生成",
     "description": "真实照片风格，黑白印刷数学试卷，手机随意拍摄效果",
     "prompt": "A realistic photo of a Chinese high school math exam paper, printed in black and white on slightly gray paper, titled \"数学试卷\". Photographed casually with smartphone, slightly tilted, uneven lighting, soft shadows, minor blur. Realistic paper texture."},
    {"id": "14", "title": "信息图：番茄炒蛋国民料理食谱", "category": "信息可视化",
     "description": "9:16竖版食谱信息图，Z字形动线，手工纸纹理",
     "prompt": "视觉设计：9:16竖版，米色手工纸背景，番茄红+橄榄油金黄+嫩草绿配色。Z字形动线排版。5步骤：挑选备菜→蛋液魔法→烈火蓬松蛋→番茄出浓汁→最后合奏。底部成品插图。署名[摄影师的厨房日记·2025]。"},
    {"id": "15", "title": "主题海报：趁年轻激爽才够味", "category": "海报设计",
     "description": "19岁少女夜宵摊喝啤酒吃小龙虾，芥末黄艺术字",
     "prompt": "生成海报图片，19岁中国少女，黑色直长发，很开心在夜宵摊上喝啤酒吃小龙虾。芥末黄色艺术字写着：趁年轻，激爽才够味！"},
    {"id": "16", "title": "主题海报：足球队史诗感双重曝光海报", "category": "海报设计",
     "description": "高完成度史诗感艺术海报，双重曝光构图，米白背景",
     "prompt": "生成高完成度史诗感艺术海报，双重曝光构图，米白色背景。球队大剪影占据主体，内部融合球队元素。压抑、决绝、宿命感极强，元素不冗杂，留白，印刷颗粒质感。竖版。"},
    {"id": "17", "title": "界面交互：VR头显爆炸图", "category": "UI设计",
     "description": "3D爆炸视图，展示VR头显9层内部组件",
     "prompt": "Exploded view product diagram of VR headset. 9 distinct layers: outer shell, camera sensors, motherboard, pancake lenses, internal frame, battery packs, straps, facial interface. Clean high-tech 3D render, studio lighting, glowing accents. Japanese annotations."},
    {"id": "18", "title": "信息图：成都吃货暴走地图", "category": "信息可视化",
     "description": "水彩+墨水手绘风格，12个美食地点，熊猫吉祥物",
     "prompt": "Illustrated map infographic. City: Chengdu. Title: \"吃货暴走地图\". Watercolor and ink hand-drawn on vintage parchment. 6 landmarks + 12 food spots + map legend. Centerpiece: giant panda eating bamboo. Cartoon red chili pepper mascot."},
    {"id": "19", "title": "信息图：桃太郎解说幻灯片", "category": "信息可视化",
     "description": "融合irasutoya温柔感和霞关幻灯片信息密度的解说图",
     "prompt": "Create an explanatory slide (ponchi-e diagram) for Momotaro that fuses the gentle atmosphere of Irasutoya with the overwhelming information density of Kasumigaseki slides."},
    {"id": "21", "title": "直播界面：马斯克直播间", "category": "趣味创意",
     "description": "Elon Musk抖音直播UI，Tesla产品卡，弹幕互动",
     "prompt": "Live stream UI mockup. Host: Elon Musk smiling, black t-shirt. SpaceX and Tesla logos in background. 55.6万本场点赞, 全站第1名. Chat messages, product card for Tesla Cybertruck ¥1,618,000. Realistic live stream interface."},
    {"id": "22", "title": "插画艺术：动漫武术格斗场景", "category": "二次元插画",
     "description": "两位女格斗家在传统道场的动漫风格战斗场景",
     "prompt": "Anime-style illustration of martial arts battle between two young female fighters in a traditional wooden dojo. Dynamic low-angle perspective, splintering floorboards, dramatic lighting. Sign text \"武術会\". Red+white vs green+purple color themes."},
    {"id": "23", "title": "信息图：人类演化时间线3D信息图", "category": "信息可视化",
     "description": "25级石阶展示人类演化，写实3D渲染，羊皮纸背景",
     "prompt": "Evolutionary timeline infographic. Transform flat vector into highly realistic 3D. Stone steps with 25 numbered organisms. Vintage textured parchment background. Title: \"人类演化\". 8 levels from single-cell life to Homo sapiens era."},
    {"id": "24", "title": "原神雷神coser漫展自拍", "category": "二次元插画",
     "description": "Genshin Impact Raiden Shogun cosplay at Shanghai Comic Con",
     "prompt": "Genshin Impact Raiden Shogun cosplay selfies at the Shanghai Comic Con"},
    {"id": "25", "title": "Minecraft皮肤设计", "category": "游戏设计",
     "description": "基于参考图创建Minecraft皮肤",
     "prompt": "create a minecraft skin inspired by my look"},
    {"id": "26", "title": "写实摄影：复古35mm胶片人像", "category": "人像摄影",
     "description": "老式CCD相机闪光灯，颗粒感，昏暗室内，随意自拍感",
     "prompt": "A vintage 35mm film photograph of a young Asian woman with long dark wavy hair. White ribbed tank top, loose beige knit cardigan. Harsh direct camera flash, candid amateur snapshot. Dimly lit messy room. Heavy film grain, muted colors, nostalgic texture."},
    {"id": "27", "title": "角色设定：拍立得照片合集", "category": "角色设计",
     "description": "10张拍立得照片平铺，粉发蓝内色女仆装角色",
     "prompt": "Collection of 10 instant photos laid flat on white fabric. Character: long pink hair with blue inner color, black and white maid uniform, reddish-pink eyes. Various poses and props: heart cushion, peace sign, rose, cake. Signatures and doodles on borders."},
    {"id": "28", "title": "写实摄影：2×2职业肖像网格", "category": "人像摄影",
     "description": "同一人物4种职业造型：商务/休闲/工人/医生",
     "prompt": "2x2 portrait grid. Same young East Asian male in 4 professions: corporate suit, casual tee, construction worker with hard hat, medical professional in lab coat. Photorealistic, professional lighting, consistent facial identity."},
    {"id": "29", "title": "电影感：传统哥特风格转变", "category": "人像摄影",
     "description": "将人物转变为trad goth风格，保留姿势和服装结构",
     "prompt": "Transform subject to trad goth aesthetic. Black hair with choppy bangs, heavy dark makeup, black lipstick. Add septum ring and nostril stud. Modify necklaces to inverted cross and pentagram. Preserve exact pose, clothing structure, background."},
    {"id": "30", "title": "写实摄影：涂鸦素描风格AI Builder", "category": "创意插画",
     "description": "涂鸦草图风格，快速勾勒，自由变形，即兴手绘感",
     "prompt": "Express a powerful AI builder in graffiti sketch style. Quick outlines, free deformation, improvised hand-drawing. Casual exaggerated lines. Rough dry-brush color blocks. White space background. Signature 'BlanPlan'."},
    {"id": "31", "title": "人像写实：低角度校服少女", "category": "人像摄影",
     "description": "动漫风格写实人像，灰白金长发，日式校服，蓝天背景",
     "prompt": "Photorealistic anime-style portrait of young woman crouching, looking down at camera from low angle. Long ash-blonde hair blowing in wind. Japanese school uniform. Background: clear blue sky with scattered clouds, blurred chain-link fence. Natural daylight."},
    {"id": "32", "title": "插画艺术：3×3角色表情网格", "category": "角色设计",
     "description": "皮克斯3D动画风格，9种表情，破纸探出构图",
     "prompt": "3x3 character expression grid. 3D animation Pixar style. Young woman with voluminous dark wavy hair, round wire-rimmed glasses. Peeking through torn hole in white paper. 9 different expressions and outfits. Wink, smirk, thinking, smile, etc."},
    {"id": "33", "title": "电商设计：可爱云朵3D角色", "category": "电商设计",
     "description": "软胶质感kawaii云朵角色，纯白背景，柔和渐变",
     "prompt": "3D render of cute kawaii cloud character on pure white background. Soft matte squishy clay texture. Large glossy black eyes, curved smile, round pink blush. Pastel gradient of pink/blue/purple on edges. Soft studio lighting, minimalist icon style."},
    {"id": "34", "title": "插画艺术：西游记角色圆形头像网格", "category": "国风插画",
     "description": "2D卡通矢量风格，12个西游记角色圆形头像",
     "prompt": "Character avatar grid. Theme: Journey to the West mythology. Clean 2D cartoon vector, thick outlines, flat colors. 12 characters in circular portraits: Sun Wukong, Tang Sanzang, Zhu Bajie, Sha Wujing, White Dragon Horse, Jade Emperor, Guanyin, etc."},
    {"id": "35", "title": "人像写实：日式和服枫叶回眸", "category": "人像摄影",
     "description": "浅米色枫叶纹和服，金带，秋季庭院背景",
     "prompt": "Photorealistic portrait of young Japanese woman looking back over shoulder with gentle smile. Light beige kimono with orange maple leaf patterns, gold obi. Dark hair in elegant updo. Background: autumn garden with vibrant red maple leaves, soft bokeh."},
    {"id": "36", "title": "品牌徽标：篮球场OpenAI logo自拍", "category": "品牌VI",
     "description": "写实自拍，篮球场场景，篮球上有OpenAI标志",
     "prompt": "Photorealistic selfie of young man on indoor basketball court. Black athletic t-shirt with white swoosh. Green basketball featuring large white OpenAI logo. Hardwood floor background. Casual social media aesthetic."},
    {"id": "37", "title": "LINE贴纸：24款动物贴纸", "category": "角色设计",
     "description": "手绘风格，瞄准日本Z世代，24款LINE贴纸",
     "prompt": "Create 24 LINE stickers of animals in a quirky hand-drawn style. Target Japanese Gen Z with a trendy style."},
    {"id": "41", "title": "插画艺术：VTuber角色设定表", "category": "角色设计",
     "description": "紫色优雅大小姐VTuber完整设定，含档案/性格/日程/链接",
     "prompt": "VTuber profile sheet. Theme: purple and white, elegant, lace, ribbon motifs. Character: Shisaki Lily, elegant ojousama archetype. Long black hair with purple highlights. White blazer, purple pleated skirt. Full profile layout with stats, personality, schedule, social links."},
    {"id": "42", "title": "写实摄影：涂鸦风格草图（变体）", "category": "创意插画",
     "description": "涂鸦速写风格，干笔触，留白设计，BlanPlan签名",
     "prompt": "Express a powerful AI builder in graffiti sketch style. Quick outlines, free deformation. Dry-brush feel, uneven smears, brush marks. White space main background. Signature 'BlanPlan'."},
    {"id": "43", "title": "插画艺术：权力的游戏角色头像网格", "category": "角色设计",
     "description": "2D扁平插画，9个GoT角色侧面头像",
     "prompt": "Character portrait grid. Theme: Game of Thrones characters. 2D flat illustration, clean line art, profile view. 9 portraits: Jon Snow, Daenerys, Tyrion, Cersei, Ned Stark, Arya, Jaime, Sansa, Theon. White rounded-rectangle frames."},
    {"id": "44", "title": "古风历史：明朝皇帝头像", "category": "国风插画",
     "description": "明朝各皇帝头像，下方标注谥号和名字",
     "prompt": "Generate avatars of various emperors from the Ming Dynasty based on the style of the uploaded image, with their posthumous names and personal names listed below the avatars."},
    {"id": "45", "title": "人像写实：黑白湿发男性特写", "category": "人像摄影",
     "description": "高对比度黑白肖像，湿发，水珠细节，电影明暗法",
     "prompt": "Striking black and white close-up portrait of handsome young Asian man with messy wet hair. Face glistening with water droplets. Intense melancholic gaze. Dramatic high-contrast lighting. Cinematic chiaroscuro. Pitch-black background."},
    {"id": "46", "title": "建筑空间：coser后台准备照", "category": "人像摄影",
     "description": "红发coser穿幻想战士服装在杂乱化妆间调整装备",
     "prompt": "Realistic photograph of young East Asian woman in cluttered backstage dressing room. Vibrant short red hair bob with bangs. Elaborate fantasy warrior costume: glossy red and gold tiered mini skirt, white corset. Adjusting arm guard. Fantasy sword nearby."},
    {"id": "47", "title": "建筑空间：2×2日式数字广告横幅", "category": "广告设计",
     "description": "四格日本数字广告：旅行/护肤/美食/在线教育",
     "prompt": "2x2 grid of Japanese digital advertisement banners. 4 quadrants: Travel (Okinawa beach), Skincare (dewy skin close-up), Gourmet Food (sizzling steak), Online Education (student at desk). Each with Japanese text and pricing."},
    {"id": "48", "title": "直播界面：刘亦菲抖音直播", "category": "趣味创意",
     "description": "9:16抖音直播截图，刘亦菲持牌欢迎畅聊",
     "prompt": "9:16 image, Douyin livestream screenshot. Liu Yifei broadcasting, holding sign: 'Streaming tonight, welcome to join Yifei's chat!'"},
    {"id": "50", "title": "建筑空间：暗黑哥特式大厅", "category": "概念设计",
     "description": "16:9电影感宽镜头，哥特式大厅，悬挂白瓷面具",
     "prompt": "Cinematic wide shot of grand dark gothic hall. Single figure in long white robe kneeling before golden altar. Massive dark stone pillars with glowing blue cracks. Dozens of white porcelain theatrical masks hanging from ceiling on strings. Format 16:9."},
    {"id": "51", "title": "信息图：一周穿搭指南", "category": "信息可视化",
     "description": "7天穿搭lookbook信息图，优雅亚洲女性，四季图标",
     "prompt": "7-day fashion lookbook infographic. 7 columns for Monday-Sunday. Young elegant Asian woman. Each day: main portrait, 4 detail thumbnails, outfit specs, color swatches, star ratings, season icons. Beige/pink/cream/champagne/blue/purple outfits."},
    {"id": "52", "title": "写实摄影：白板武士涂鸦", "category": "创意插画",
     "description": "真实白板照片，绿色马克笔武士素描，VAGABOND风格",
     "prompt": "Realistic photograph of whiteboard with detailed green dry-erase marker drawing of samurai with messy topknot. Manga sketch style. Handwritten text 'VAGABOND' and 'MUSASHI'. Glossy surface with realistic light reflections."},
    {"id": "53", "title": "室内空间：90年代街机维修场景", "category": "仿真生成",
     "description": "Y2K怀旧风格，年轻人跪着修理街机，闪光灯拍摄",
     "prompt": "Vintage late 90s amateur flash photograph of young man repairing arcade machine. Baggy blue jeans, chunky sneakers, baseball cap. Cabinet labeled 'Dancing Stage KONAMI'. Exposed internal electronics. Dimly lit arcade. Nostalgic Y2K aesthetic."},
    {"id": "54", "title": "角色设定：4格讽刺产品广告", "category": "趣味创意",
     "description": "2×2讽刺产品广告：坐石/不想刷牙的牙刷/云存钱罐/骂人石头",
     "prompt": "4-panel satirical product advertisement grid. Products: 座る石 (sitting stone), 磨きたくない人の歯ブラシ (toothbrush for those who don't want to brush), 雲の貯金箱 (cloud piggy bank), 叱ってくれる石 (scolding stone). Japanese text, professional ad layout."},
    {"id": "55", "title": "信息图：辣椒炒肉制作流程图", "category": "信息可视化",
     "description": "写实风格菜品制作流程图，适合小红书图文比例",
     "prompt": "Help me create a detailed production flowchart for the dish Fried Pork with Chili, in a realistic style, suitable for Xiaohongshu image-text proportions."},
    {"id": "56", "title": "写实摄影：哥特风少女骑投币独角兽", "category": "人像摄影",
     "description": "哥特风少女面无表情骑儿童投币摇摇车，日常街拍感",
     "prompt": "Candid realistic photograph of young goth woman with pale skin, long straight black hair, heavy black eyeliner, black lipstick. Deadpan expression, sitting on children's coin-operated unicorn ride. Black lace outfit, platform boots. Outside store, overcast daylight."},
    {"id": "57", "title": "界面交互：朱元璋登基推特/X界面", "category": "趣味创意",
     "description": "深色模式推特/X截图，朱元璋发布登基推文",
     "prompt": "Mobile social media app UI mockup, Twitter/X dark mode. Author: Emperor Zhu Yuanzhang, verified badge. Tweet: 'I have ascended to the Dragon Throne! Ming Dynasty, Hongwu era begins!' 3 media images, engagement stats. 1:36 PM · Jan 23, 1368."},
    {"id": "58", "title": "主题海报：东方奇幻城市海报（通用模板）", "category": "海报设计",
     "description": "9:16对角线+S型构图，金色能量线，城市地标，白发女性",
     "prompt": "Flat illustration, high-end oriental fantasy city poster, 9:16. Diagonal + S-shaped flow. Deep black grading to dark red. Golden flowing energy line. City landmarks emerge in golden flow. White-haired female figure with flowers at bottom. Songti font title. 8K."},
    {"id": "59", "title": "主题海报：日本弹珠厅恶搞电影海报", "category": "趣味创意",
     "description": "3D CGI动画风格电影海报，多位夸张人物角色",
     "prompt": "Cinematic promotional poster. 3D CGI animation style, caricature characters. Large shirtless man, elderly kimono woman, small mustached man in green sweater. Japanese text overlays. Chaotic energetic atmosphere."},
    {"id": "60", "title": "漫画分镜：5格拼贴画", "category": "创意插画",
     "description": "5格拼贴：时钟/扑克牌女人/红酒杯/棋盘/骰子",
     "prompt": "5-panel collage. Clock at 7:42 (flat vector), woman holding poker hand (oil painting), wine glass of dark red liquid (photorealistic), chessboard (high-angle photo), two dice showing 5 and 2 (pop art halftone)."},

    # More cases from the fetch - compact format for efficiency
    {"id": "61", "title": "主题海报：SNS学院2×2广告横幅", "category": "广告设计",
     "description": "4个SNS学院招生广告横幅，霓虹/明亮/暗黑/友好风格",
     "prompt": "2x2 grid of banner ads for SNS School. 4 styles: dark neon (purple/blue), bright pop (cyan), dark analytical (neon purple/green), bright friendly (purple/white). Each with different subjects and calls-to-action. Japanese text."},
    {"id": "62", "title": "插画艺术：妈妈向SNS学院广告横幅", "category": "广告设计",
     "description": "柔软亲和风格的SNS学院广告，面向妈妈群体",
     "prompt": "2x2 grid of banner ads for SNS School targeting moms. Soft approachable design, soft green/white/beige tones. Photography + watercolor illustration. Each panel: mother with laptop/child, features, green CTA buttons. Japanese text."},
    {"id": "63", "title": "主题海报：社交媒体内容创作学院广告", "category": "广告设计",
     "description": "2×2推广横幅，粉蓝渐变/深蓝几何/米白美学/粉红pop",
     "prompt": "2x2 grid of promotional banner ads for Social Media Content Creation School. 4 color themes: pastel pink-blue, deep blue-cyan geometric, soft beige-white, vibrant pink-magenta pop. Young models with cameras and smartphones."},
    {"id": "64", "title": "信息图：情绪管理8个方法", "category": "信息可视化",
     "description": "可爱扁平矢量风格，Morandi配色，3×3网格，8个情绪调节方法",
     "prompt": "Infographic poster, cute flat vector, pastel Morandi colors. Title: '情绪不好了？8个让你瞬间变好的方法'. Character: young woman with shoulder-length brown hair. 8 methods: 深呼吸/户外散步/写情绪日记/抱抱自己/听音乐/找人倾诉/看天空/冥想."},
    {"id": "65", "title": "信息图：儒释道根本区别", "category": "信息可视化",
     "description": "古典东方神话手稿风格，竖蛋形分层结构，鼠尾草绿+浅金配色",
     "prompt": "World-building infographic: Fundamental Differences between Confucianism, Buddhism, and Taoism. Ancient Oriental mythological manuscript style. Vertical egg-shaped layered structure. 3 layers: Buddhism (man vs self), Taoism (man vs nature), Confucianism (man vs man). 3:4 vertical."},
    {"id": "66", "title": "信息图：时装设计因果链", "category": "信息可视化",
     "description": "女装从纤维到成衣的完整因果链，10个模块",
     "prompt": "Fashion design process infographic: 'THE CAUSAL CHAIN OF A WOMEN'S GARMENT'. Exploded-view of trench coat dress. 13-step central chain. 10 modules: Raw Material, Inspiration, Design Sketch, Patternmaking, Cutting, Fitting, Team, Final Garment, etc."},
    {"id": "67", "title": "信息图：糖尿病因果链", "category": "信息可视化",
     "description": "医学信息图，透明人体展示循环系统和器官",
     "prompt": "Medical infographic: '糖尿病诞生的因果链 / THE CAUSAL CHAIN OF DIABETES'. Highly detailed anatomical illustrations. Transparent human body. 14 sections from glucose entry to organ damage. Bilingual CN/EN. Clinical white background."},
    {"id": "68", "title": "信息图：痛风因果链", "category": "信息可视化",
     "description": "3D医学插图，从嘌呤来源到痛风发作的完整链条",
     "prompt": "Comprehensive medical infographic: '痛风诞生的因果链 / THE CAUSAL CHAIN OF GOUT'. 3D medical illustration. Transparent body showing liver/kidneys/vascular system. 12 sections: Purine Sources → Uric Acid → Hyperuricemia → Crystallization → Immune Response → Flare."},
    {"id": "70", "title": "信息图：一张照片诞生的因果链", "category": "信息可视化",
     "description": "佳能EOS R5成像系统全流程，从光子到文件的13步",
     "prompt": "Technical infographic: '一张照片诞生的因果链 / THE CAUSAL CHAIN OF A PHOTOGRAPH'. Exploded isometric view of Canon EOS R5. 13 steps from Reality to Memory. 8 modules. Bilingual. Clean technical style."},
    {"id": "71", "title": "关系图谱：佳能EOS R5成像系统剖面", "category": "信息可视化",
     "description": "3D爆炸视图+8个编号剖面，详细相机成像知识",
     "prompt": "Technical infographic: 'CANON EOS R5 IMAGING ATLAS'. 3D exploded view of camera components. 8 numbered sections: Optical Entry, Aperture/Shutter, Focus, Sensor, IBIS, Analog Readout, DIGIC X Processing, File Output. Blueprint-style."},
    {"id": "72", "title": "信息图：石榴植物生长图谱", "category": "信息可视化",
     "description": "复古植物插图+现代信息图，从种子到果实的完整生命周期",
     "prompt": "Scientific botanical infographic: '植物生命路径剖面 / BOTANICAL GROWTH ATLAS'. Subject: Pomegranate. 8 sections: Seed Architecture, Germination, Root System, Stem/Leaf, Photosynthesis, Bud/Blooming, Pollination/Fruiting, Fruit Maturation. Vintage + modern style."},
    {"id": "73", "title": "信息图：上海城市系统剖面", "category": "信息可视化",
     "description": "暗色背景+发光蓝金紫色，3D等距剖面，城市系统全景",
     "prompt": "Complex urban systems atlas: '上海城市系统剖面 / SHANGHAI URBAN ATLAS'. Dark background with glowing blue, gold, and purple accents. 3D isometric cutaway. Comprehensive city infrastructure visualization."},
]

# ============================================================
# GALLERY PART 2 (detailed, already have)
# ============================================================
# Load existing part 2 data
with open(f"{OUTPUT_DIR}/cases.json", "r", encoding="utf-8") as f:
    existing_cases = json.load(f)

gallery_part2 = [c for c in existing_cases if c['id'].isdigit() and int(c['id']) >= 166]

# Combine
all_cases = gallery_part1_detailed + gallery_part2

# Templates (keep existing)
with open(f"{OUTPUT_DIR}/templates.json", "r", encoding="utf-8") as f:
    templates = json.load(f)

# Deduplicate by ID
seen = set()
unique_cases = []
for c in all_cases:
    if c['id'] not in seen:
        seen.add(c['id'])
        unique_cases.append(c)

# Save
with open(f"{OUTPUT_DIR}/cases.json", "w", encoding="utf-8") as f:
    json.dump(unique_cases, f, ensure_ascii=False, indent=2)

# Build combined
all_data = {
    "templates": templates,
    "cases": unique_cases,
    "metadata": {
        "source": "awesome-gpt-image-2 by freestylefly",
        "repo": "https://github.com/freestylefly/awesome-gpt-image-2",
        "gallery_visual": "https://gpt-image2.canghe.ai/",
        "total_templates": len(templates),
        "total_cases": len(unique_cases),
        "categories": list(set(
            [t["category"] for t in templates] +
            [c["category"] for c in unique_cases]
        ))
    }
}

with open(f"{OUTPUT_DIR}/all-data.json", "w", encoding="utf-8") as f:
    json.dump(all_data, f, ensure_ascii=False, indent=2)

print(f"Total templates: {len(templates)}")
print(f"Total cases: {len(unique_cases)}")
print(f"  Part 1 detailed: {len(gallery_part1_detailed)}")
print(f"  Part 2 detailed: {len(gallery_part2)}")
print(f"Total categories: {len(all_data['metadata']['categories'])}")
