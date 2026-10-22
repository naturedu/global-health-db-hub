# -*- coding: utf-8 -*-
"""生成医学与健康研究公共数据库汇总网站 (index.html)。
数据来源：用户提供的 PDF《医学与健康研究公共数据库汇总》(29 页)。
站点含：开放度分级图例、总览速查表、12 大类分类卡片、实战阶梯、
以及「研究匹配查询器」（输入科学问题 -> 锁定数据库 + 研究范式）。
"""
import json, os, re

# ---------------------------------------------------------------------------
# 分类（对应 PDF 第 2-12 章）
# ---------------------------------------------------------------------------
CATS = [
    ("aging",        "老龄化追踪调查（HRS 家族）"),
    ("social",       "中国社会科学类面板"),
    ("biobank",      "大型生物样本库"),
    ("china_cohort", "中国本土大型人群队列"),
    ("monitor",      "国家健康监测与横断面调查"),
    ("rwd",          "医保行政数据与电子病历（真实世界）"),
    ("oceania",      "澳大利亚与大洋洲数据源"),
    ("icu",          "重症与临床电子病历数据库"),
    ("trial",        "临床试验与经典队列数据二次利用"),
    ("omics",        "衰老资源、组学数据与通用仓储"),
    ("cn_platform",  "中国国家级科学数据平台与知识库"),
    ("healthecon",   "卫生经济与卫生服务管理数据源"),
]

ACCESS = {
    1: "★ 完全公开，直接下载",
    2: "★★ 注册后下载",
    3: "★★★ 培训/签署协议后下载",
    4: "★★★★ 正式申请并付费",
    5: "★★★★★ 必须本地合作（常含共同署名）",
}

# 速查表分组（PDF 第 1 章）
QR = {
    "survey":   "1.1 老龄追踪与社会调查",
    "biobank":  "1.2 生物样本库与大型队列",
    "monitor":  "1.3 监测 / 医保 / 电子病历 / 登记",
    "trial":    "1.4 试验二次利用 / 组学 / 仓储",
    "oceania":  "1.5 澳大利亚与大洋洲",
}

def e(name, en, cat, access, urls, region="", scale="", timeSpan="",
      host="", content="", intro="", usage="", notes="", tags=None,
      paradigm="", qr=None, lite=False):
    return dict(name=name, en=en, cat=cat, access=access, urls=urls,
                region=region, scale=scale, timeSpan=timeSpan, host=host,
                content=content, intro=intro, usage=usage, notes=notes,
                tags=tags or [], paradigm=paradigm, qr=qr, lite=lite)

D = []  # 数据库列表

# ============================ 第二章 老龄化追踪 ============================
D.append(e("HRS 健康与退休研究", "Health and Retirement Study", "aging", 2,
    [{"label":"官网","url":"https://hrs.isr.umich.edu"},{"label":"调和数据 Gateway","url":"https://g2aging.org"}],
    region="美国", scale="约 2 万", timeSpan="1992 至今",
    host="密歇根大学社会研究所；美国国立老龄研究所(NIA)与社保署资助",
    content="50 岁及以上，每 2 年一轮，队列更替设计持续补充年轻队列。健康、认知、就业退休、收入财富、代际支持、医疗支出与保险。",
    intro="老龄追踪研究的标杆。做国际比较不要自己逐库对变量，直接用 Gateway to Global Aging Data 的统一编码调和版（Harmonized HRS/CHARLS/ELSA/SHARE/MHAS/KLoSA/LASI），可省 2-3 周清洗。RAND HRS Longitudinal File 是清洗好的纵向文件，强烈建议优先用它而非原始文件；HCAP 为认知深度评估；2006 起隔轮采干血斑/唾液；遗传数据需经 dbGaP 另申。",
    usage="注册后即可下载公开文件，免费；受限数据（详细地理、社保/医保链接）需签协议并说明数据安全环境。",
    notes="变量命名每轮前缀不同，不用 RAND 版本会非常痛苦。",
    tags=["老龄","认知","痴呆","失能","养老","退休","收入","财富","代际","美国","队列","前瞻性","问卷","随访"],
    paradigm="跨国/纵向老龄比较：用 g2aging 调和数据集统一变量→选取暴露(如认知/功能)与结局→多层/纵向模型；遗传相关变量走 dbGaP。",
    qr="survey"))

D.append(e("CHARLS 中国健康与养老追踪调查", "China Health and Retirement Longitudinal Study", "aging", 2,
    [{"label":"官网","url":"http://charls.pku.edu.cn"},{"label":"数据平台","url":"https://opendata.pku.edu.cn"}],
    region="中国", scale="约 1.7 万", timeSpan="2011 至今",
    host="北京大学国家发展研究院、中国社会科学调查中心",
    content="45 岁及以上，覆盖 150 县区/450 村居。人口学、健康功能、认知抑郁、医疗服务利用与支出、养老保险、收入消费、家庭结构。",
    intro="对中国肾脏与心血管方向极重要：2011 与 2015 两轮采静脉血，含血肌酐、胱抑素 C、尿素氮、尿酸、糖化血红蛋白、血脂、CRP，可算 eGFR（肌酐法/胱抑素C法/联合）且血压为实测值。中英文文档齐全。",
    usage="注册并填写用途后即可下载，免费。",
    notes="血样仅两轮，纵向 eGFR 斜率只有两个时间点，勿硬做轨迹模型；两轮检测批次/实验室有差异，跨轮比较建议校准；自报「医生告知患肾病」漏报率高，单靠自报定义 CKD 会严重低估。",
    tags=["老龄","中国","认知","抑郁","养老","医保","医疗支出","肾脏","eGFR","肌酐","血压","队列","前瞻性","问卷","体检","生化"],
    paradigm="中国中老年：用实测血压+静脉血生化构建暴露→肾病/心血管结局→Cox/轨迹模型；血样仅两轮，纵向分析注意时间点限制。",
    qr="survey"))

D.append(e("CLHLS 中国老年健康影响因素跟踪调查", "Chinese Longitudinal Healthy Longevity Survey", "aging", 2,
    [{"label":"数据平台","url":"https://opendata.pku.edu.cn"}],
    region="中国", scale="累计数万", timeSpan="1998 至今",
    host="北京大学健康老龄与发展研究中心（曾毅团队）",
    content="覆盖 23 省，约八轮。日常生活能力、认知、社会经济与照料、心理健康、临终照护回顾。",
    intro="不可替代之处是超高龄过采样：80 岁以上乃至百岁老人样本量全球稀缺，研究长寿、失能轨迹与临终照护必用。部分长寿地区采过血样（指标覆盖面与轮次以官网说明书为准）。",
    usage="注册申请后下载，免费。",
    notes="高龄组代理回答比例高，认知/自评健康类变量要单独处理；死亡随访是强项，但注意失访与死亡的竞争风险。",
    tags=["老龄","长寿","失能","百岁","临终照护","认知","中国","队列","前瞻性","问卷"],
    paradigm="长寿/失能轨迹：以超高龄过采样人群做生存与功能下降分析；注意代理回答偏倚与竞争风险。",
    qr="survey"))

D.append(e("CFPS 中国家庭追踪调查", "China Family Panel Studies", "social", 2,
    [{"label":"官网","url":"http://www.isss.pku.edu.cn/cfps/"},{"label":"数据平台","url":"https://opendata.pku.edu.cn"}],
    region="中国", scale="约 1.5 万户", timeSpan="2010 至今",
    host="北京大学中国社会科学调查中心",
    content="25 省市区，两年一轮。家庭/成人/少儿/社区四层问卷可匹配（最强之处）。",
    intro="健康相关含自评健康、慢病自报、医疗支出、医保类型、CES-D、部分轮次身高体重血压。典型用法：医保改革双重差分、家庭照料与老年健康、灾难性卫生支出。健康变量以自报为主，但社会经济/家庭结构/政策暴露是医学库没有的。",
    usage="注册后下载，免费。",
    notes="健康测量以自报为主，客观指标有限。",
    tags=["中国","家庭","社会","医疗支出","医保","灾难性卫生支出","抑郁","CES-D","队列","重复横断面","问卷"],
    paradigm="卫生政策评估：用四层匹配数据做 DID/断点回归评估医保或政策冲击对医疗利用与支出的影响。",
    qr="survey"))

D.append(e("CLASS 中国老年社会追踪调查", "China Longitudinal Aging Social Survey", "social", 2,
    [{"label":"CNSDA 入口","url":"http://www.cnsda.org"}],
    region="中国", scale="约 1.1 万", timeSpan="2014 至今",
    host="中国人民大学中国调查与数据中心",
    content="60 岁及以上，两年一轮。老年社会照料、养老服务需求、社区养老资源、代际支持。",
    intro="比 CHARLS 更聚焦老年社会照料与服务利用，变量粒度更细，是最贴合卫生管理方向、却最易被忽略的一个库。",
    usage="注册申请后下载，免费。",
    notes="健康指标以自报为主。",
    tags=["老龄","养老","社会服务","代际","中国","队列","重复横断面","问卷"],
    paradigm="老年服务体系研究：用服务利用/需求变量评估社区养老资源与照料供给差距。",
    qr="survey"))

D.append(e("CGSS 中国综合社会调查", "Chinese General Social Survey", "social", 2,
    [{"label":"CNSDA 入口","url":"http://www.cnsda.org"}],
    region="中国", scale="每轮上万", timeSpan="2003 至今",
    host="中国人民大学中国调查与数据中心",
    content="中国最早全国性综合社会调查。价值观、社会公平感、阶层认同等独一份。",
    intro="健康模块不深，但就医体验、医患信任、健康公平感知等变量很合适。",
    usage="注册申请后下载，免费。",
    notes="健康客观指标有限。",
    tags=["中国","社会","公平","医患信任","问卷","横断面"],
    paradigm="健康公平/就医体验：用社会态度变量分析健康公平感知与医患信任。",
    qr="survey"))

D.append(e("CHNS 中国健康与营养调查", "China Health and Nutrition Survey", "social", 2,
    [{"label":"官网","url":"https://www.cpc.unc.edu/projects/china"}],
    region="中国", scale="约 10 轮/12 省市", timeSpan="1989-2015",
    host="北卡大学人口中心与中国疾控中心营养与健康所",
    content="连续 3 天 24 小时膳食回顾 + 家庭食物称重盘存；多轮测血压、身高体重腰围；2009 一轮采空腹血样查多项生化。",
    intro="营养流行病学在中国几乎无替代。2015 后基本停更，做近年趋势不合适；做 1990-2015 膳食转型、城镇化与代谢病是绝配。",
    usage="注册申请后下载，免费。",
    notes="非概率抽样；2015 后停更。",
    tags=["中国","营养","膳食","代谢","肥胖","血压","生化","队列","重复横断面","问卷","体检"],
    paradigm="营养-代谢病：用 3 天膳食回顾+称重构建饮食暴露→代谢/心血管结局；注意非概率抽样与停更时间。",
    qr="survey"))

D.append(e("KLoSA 韩国老龄化追踪研究", "Korean Longitudinal Study of Ageing", "aging", 2,
    [{"label":"官网（待核）","url":"https://survey.keis.or.kr"}],
    region="韩国", scale="约 1 万", timeSpan="2006 至今",
    host="韩国雇佣情报院",
    content="45 岁及以上（济州岛除外），每 2 年一轮。偏就业、退休、收入保障。",
    intro="主办方为劳动就业口，健康变量以自报为主，生物样本非常有限。界面以韩文为主，英文文件另设下载区（入口待核）。",
    usage="注册申请，免费。",
    notes="拼写是 KLoSA 不是 KOLSA；健康客观指标少。",
    tags=["老龄","韩国","就业","退休","收入","问卷","队列","前瞻性"],
    paradigm="韩国社会经济与老龄化：做就业/退休对健康影响；慢病生物学用 KoGES、卫生服务用 NHIS。",
    qr="survey"))

D.append(e("MHAS 墨西哥健康与老龄化研究", "Mexican Health and Aging Study", "aging", 2,
    [{"label":"官网","url":"https://www.mhasweb.org"}],
    region="墨西哥", scale="约 1.5 万", timeSpan="2001 至今",
    host="德州大学医学部与墨西哥国家统计地理局",
    content="50 岁及以上；含大量美墨移民史变量、Mex-Cog 认知专项；部分轮次采干血斑与人体测量。",
    intro="拉美唯一大型全国代表性老龄面板，跨种族/跨发展阶段比较的关键一环；移民与健康研究的独门数据。英西双语文档。",
    usage="注册后即可下载，免费。",
    notes="",
    tags=["老龄","墨西哥","移民","认知","拉美","队列","前瞻性","问卷","体检"],
    paradigm="移民与健康/拉美老龄：用移民史变量+认知专项做跨发展阶段的比较研究。",
    qr="survey"))

D.append(e("ELSA 英格兰老龄化追踪调查", "English Longitudinal Study of Ageing", "aging", 2,
    [{"label":"官网","url":"https://www.elsa-project.ac.uk"}],
    region="英格兰", scale="数万", timeSpan="1998 至今",
    host="英国（与 HRS 高度对标）",
    content="含客观体检，与 HRS 设计对标。",
    intro="做欧洲/英美老龄比较的默认选择之一；可用 g2aging 调和数据集统一变量。",
    usage="注册后下载，免费。",
    notes="",
    tags=["老龄","英国","欧洲","认知","体检","队列","前瞻性","问卷"],
    paradigm="英美老龄比较：经 g2aging 调和变量与 HRS/SHARE 做跨国纵向比较。",
    qr="survey"))

D.append(e("SHARE 欧洲健康、老龄与退休调查", "Survey of Health, Ageing and Retirement in Europe", "aging", 2,
    [{"label":"官网","url":"https://share-eric.eu"}],
    region="欧洲 28 国", scale="数万至 7 万", timeSpan="2004 至今",
    host="欧洲多国联合",
    content="跨国样本量最大的老龄面板，做欧洲比较的默认选择。",
    intro="覆盖 28 国，变量经统一编码，适合跨国政策与健康不平等研究。",
    usage="注册后下载，免费。",
    notes="",
    tags=["老龄","欧洲","跨国","退休","健康不平等","队列","前瞻性","问卷"],
    paradigm="欧洲健康不平等：多国面板做跨国比较与政策评估。",
    qr="survey"))

D.append(e("LASI 印度纵向老龄化调查", "Longitudinal Aging Study in India", "aging", 2,
    [{"label":"官网","url":"https://www.lasi-india.org"}],
    region="印度", scale="7 万以上", timeSpan="2017 至今",
    host="印度（与 HRS 家族对标）",
    content="规模惊人的全国老龄面板。",
    intro="可经 g2aging 调和数据集与 HRS 家族统一变量做发展中国家老龄比较。",
    usage="注册后下载，免费。",
    notes="",
    tags=["老龄","印度","发展中国家","队列","前瞻性","问卷","体检"],
    paradigm="发展中大国老龄：大规模面板做健康转型与老龄化负担研究。",
    qr="survey"))

# ============================ 第四章 生物样本库 ============================
D.append(e("UK Biobank 英国生物样本库", "UK Biobank", "biobank", 4,
    [{"label":"官网","url":"https://www.ukbiobank.ac.uk"},{"label":"变量浏览 Showcase","url":"https://biobank.ndph.ox.ac.uk/showcase/"},{"label":"申请系统 AMS","url":"https://ams.ukbiobank.ac.uk"}],
    region="英国", scale="约 50 万", timeSpan="2006-2010 招募",
    host="英国（22 个评估中心）",
    content="基线问卷、体格测量、生化 30 余项（肌酐/胱抑素C/尿白蛋白肌酐比）、全基因组分型、WGS、蛋白组(Olink)、代谢组、多模态影像(脑心腹DXA)、加速度计、与 NHS 住院/癌登/死亡链接。",
    intro="需正式申请并付费。先在 Showcase 免账号浏览全部变量与分布；注册 AMS 提交约 2000 字研究计划+机构 PI 与合作者；审批后按字段范围付费；分析已迁至 DNAnexus 的 UKB-RAP 云平台，另有计算与存储费；结果需回传。",
    usage="正式申请+付费；周期 1-6 个月；云计算预算需提前算清。",
    notes="健康志愿者偏倚显著（应答率约 5%），绝对风险不可外推总人群，相对关联通常有效——讨论必写；组学项目易超支。",
    tags=["英国","一般人群","基因","多组学","影像","蛋白组","代谢组","队列","前瞻性","体检","生化","死亡登记","真实世界"],
    paradigm="大型前瞻队列：先用 Showcase 确定变量→AMS 提交计划→UKB-RAP 云上分析；注意志愿者偏倚与云成本。",
    qr="biobank"))

D.append(e("CKB 中国慢性病前瞻性研究", "China Kadoorie Biobank", "biobank", 4,
    [{"label":"官网","url":"https://www.ckbiobank.org"}],
    region="中国 10 地区", scale="约 51 万", timeSpan="2004-2008 基线",
    host="牛津大学临床试验服务部、中国医学科学院、北京大学",
    content="5 城市 5 农村，每约 5 年重复调查；与疾控监测/医保理赔/死因登记链接，随访完整度国内顶尖；基因分型约 10 万，另有测序/代谢/蛋白子集。",
    intro="分层开放：Open Access 层汇总数据与部分个体数据较快获取；深度数据需正式申请，常需与 CKB 团队合作署名。中国人群、样本量与 UKB 同量级且有医保理赔随访，做中国人高血压至心肾结局前瞻性证据最硬。",
    usage="分层开放；深度数据正式申请+合作署名，周期 1-6 个月。",
    notes="深度层门槛高，优先考虑 Open Access 与团队合",
    tags=["中国","一般人群","心血管","肾脏","高血压","队列","前瞻性","随访","医保","基因","真实世界"],
    paradigm="中国人群心肾结局：Open Access 先验证→深度数据走合作申请；利用医保/死因链接做结局确认。",
    qr="biobank"))

D.append(e("MCPS 墨西哥城前瞻性研究", "Mexico City Prospective Study", "biobank", 5,
    [{"label":"牛津 CTSU（入口待核）","url":"https://www.ctsu.ox.ac.uk"}],
    region="墨西哥", scale="约 15 万", timeSpan="长期随访",
    host="牛津大学临床试验服务部（与 CKB 同方法学谱系）",
    content="规模大、随访长、有基因组数据。",
    intro="做墨西哥人群生物标志物与死亡结局比 MHAS 更合适；申请入口待核，建议从牛津 CTSU 官网查。",
    usage="具体申请入口待核，建议从牛津 CTSU 官网查找。",
    notes="入口待核",
    tags=["墨西哥","一般人群","基因","队列","前瞻性","随访","死亡登记"],
    paradigm="拉美人群队列：生物标志物→死亡/慢病结局；入口从牛津 CTSU 查找。",
    qr="biobank"))

D.append(e("KoGES 韩国基因组流行病学研究", "Korean Genome Epidemiology Study", "biobank", 4,
    [{"label":"韩国国立保健研究院（入口待核）","url":"https://www.kdca.go.kr"}],
    region="韩国", scale="20 余万", timeSpan="2001 至今",
    host="韩国国立保健研究院",
    content="城市/农村/Ansan-Ansung 等多个子队列，有基因组与长期随访。",
    intro="做慢病生物学用 KoGES；做社会经济与老龄化用 KLoSA；做卫生服务与药物流行病学用 NHIS——三者定位不同，勿混用。",
    usage="申请入口与英文页待核，建议从韩国国立保健研究院官网进入。",
    notes="入口待核",
    tags=["韩国","一般人群","基因","队列","前瞻性","慢病","体检"],
    paradigm="韩国慢病遗传学：基因-环境交互；入口从韩国国立保健研究院进入。",
    qr="biobank"))

D.append(e("All of Us 美国全民健康研究", "All of Us Research Program", "biobank", 4,
    [{"label":"官网","url":"https://allofus.nih.gov"}],
    region="美国", scale="目标百万", timeSpan="进行中",
    host="美国 NIH",
    content="强调少数族裔代表性，含电子病历与可穿戴数据。",
    intro="代表性导向的生物样本库，适合健康公平与多族裔研究。",
    usage="正式申请并付费/审批。",
    notes="",
    tags=["美国","一般人群","基因","多组学","电子病历","可穿戴","真实世界","队列"],
    paradigm="多族裔健康公平：利用少数族裔代表性样本做精准医学与差异研究。",
    qr="biobank"))

D.append(e("FinnGen 芬兰基因组计划", "FinnGen", "biobank", 4,
    [{"label":"官网","url":"https://www.finngen.fi"}],
    region="芬兰", scale="50 万以上", timeSpan="进行中",
    host="芬兰（基因+全国登记链接）",
    content="基因加全国登记链接，GWAS 汇总统计公开。",
    intro="GWAS 汇总统计公开便于荟萃，个体级需申请。",
    usage="汇总统计公开；个体数据正式申请。",
    notes="",
    tags=["芬兰","基因","GWAS","登记","队列","真实世界"],
    paradigm="遗传流行病学：公开 GWAS 汇总统计做荟萃；个体数据走申请。",
    qr="biobank"))

D.append(e("BioBank Japan 日本生物样本库", "BioBank Japan", "biobank", 4,
    [{"label":"官网","url":"https://biobankjp.org"}],
    region="日本", scale="约 27 万", timeSpan="进行中",
    host="日本",
    content="东亚人群 GWAS 的重要来源。",
    intro="东亚人群遗传研究关键资源。",
    usage="正式申请。",
    notes="",
    tags=["日本","东亚","基因","GWAS","队列"],
    paradigm="东亚遗传：与东亚其他队列联合做 GWAS 与疾病关联。",
    qr="biobank"))

D.append(e("Million Veteran Program 百万退伍军人计划", "Million Veteran Program", "biobank", 4,
    [{"label":"官网","url":"https://www.research.va.gov/mvp"}],
    region="美国", scale="百万级", timeSpan="进行中",
    host="美国退伍军人事务部（男性为主）",
    content="退伍军人队列，含基因与电子病历。",
    intro="男性为主的大样本，适合男性健康与药物基因组。",
    usage="正式申请（需美方合作）。",
    notes="男性为主，性别外推差。",
    tags=["美国","男性","退伍军人","基因","电子病历","队列","真实世界"],
    paradigm="男性/退伍军人健康：基因-电子病历关联；注意男性偏倚。",
    qr="biobank"))

D.append(e("Estonian Biobank 爱沙尼亚生物样本库", "Estonian Biobank", "biobank", 4,
    [{"label":"官网","url":"https://genomics.ut.ee/en"}],
    region="爱沙尼亚", scale="约 20 万", timeSpan="进行中",
    host="爱沙尼亚（覆盖全国约 20% 成人）",
    content="全国代表性遗传队列。",
    intro="高覆盖率的全国样本，适合基因型-表型研究。",
    usage="正式申请。",
    notes="",
    tags=["爱沙尼亚","欧洲","基因","队列","真实世界"],
    paradigm="国家级遗传队列：高覆盖率样本做精准医学。",
    qr="biobank"))

# ============================ 第五章 中国本土队列 ============================
D.append(e("开滦队列", "Kailuan Study", "china_cohort", 5,
    [{"label":"团队论文方法学","url":"https://www.kailuanhospital.com"}],
    region="河北唐山", scale="101,510", timeSpan="2006 至今",
    host="开滦总医院及开滦集团 11 家医院（吴寿岭团队）",
    content="在职与离退休职工；每 2 年统一体检（血压/身高体重腰围/空腹血糖/血脂/肌酐/尿酸/hsCRP/肝肾/血尿常规/心电图），亚组含颈动脉超声、baPWV/ABI、脑核磁、认知、睡眠、眼底；结局经医保+死因+主动随访三重确认，终点委员会裁定。已在中国临床试验注册中心注册。",
    intro="方法学上极值钱：因每 2 年全套复测，可做累积暴露（血压/血糖/炎症负荷）、访视间变异性（SD/CV/独立于均值变异）、轨迹分析（潜类别增长模型）、时依协变量 Cox。与 24h 动态血压（短期变异）、累积负荷（暴露总量）是不同构念，讲清三层本身就是有分量的讨论。",
    usage="不公开下载。合作制，联系开滦总医院团队，常含共同署名；国内心血管会议是建立联系的渠道。",
    notes="男性约八成，性别外推差；单一企业/地域，社会经济同质；健康工人效应；早期轮次部分指标方法变更需校准。",
    tags=["中国","职业","职工","心血管","肾脏","CKD","血压","累积暴露","轨迹","队列","前瞻性","体检","生化","随访","合作"],
    paradigm="重复测量队列：累积暴露/访视间变异性/轨迹/LT-Cox；结局用医保+死因三重确认。男性职工偏倚需说明。",
    qr="biobank"))

D.append(e("同济东风队列", "Dongfeng-Tongji Cohort (DFTJ)", "china_cohort", 5,
    [{"label":"华中科大公卫学院","url":"https://en.tjmu.edu.cn"}],
    region="湖北十堰", scale="27,009→约 3.8 万", timeSpan="2008 至今",
    host="华中科技大学同济医学院公卫学院与东风汽车公司（邬堂春团队）",
    content="东风汽车退休职工；详尽职业暴露史（粉尘/噪声/金属/化学品）、生活方式、疾病用药；血压/人体测量/心电图，亚组颈动脉超声/肺功能；空腹血与 DNA 库，已有基因分型；与东风职工医保链接+死因登记。",
    intro="职业暴露+基因组+医保结局三合一，做基因-环境交互、职业暴露与心血管代谢结局国内几乎无对手。对同济系统内研究者门槛最低、契合度最高；人群为退休职工，年龄偏大、高血压患病率高，适合与院内电子病历队列对照。",
    usage="校内与机构间合作制，联系公卫学院相关团队。",
    notes="单一企业/城市、退休为主，年轻与非职业人群缺失。",
    tags=["中国","职业","暴露","基因","心血管","代谢","医保","队列","前瞻性","合作","环境"],
    paradigm="职业-基因交互：职业暴露史+基因分型+医保结局；适合院内跨机构合作。",
    qr="biobank"))

D.append(e("PBICR 中国居民心理与行为调查", "Psychology and Behavior Investigation of Chinese Residents", "china_cohort", 4,
    [{"label":"近期论文数据声明","url":"https://www.cnsda.org"}],
    region="中国 31 省", scale="单轮 2-3 万", timeSpan="2021 至今",
    host="国内多高校与研究机构联合（具体牵头待核）",
    content="全国性重复横断面，量表密度极高：PHQ-9、GAD-7、PSS、UCLA 孤独、PSQI、HPLP-II、FHS-SF、健康素养/eHEALS、EQ-5D、社会支持/资本/医患信任、就医行为。",
    intro="变量组合自由度极高，一个数据集可支撑几十个选题；对卫生管理、健康行为、健康心理方向极友好、出稿快。",
    usage="通过项目组申请，提交研究方案，通常采用合作署名（具体流程待核）。",
    notes="横断面为主、因果弱；全自报无客观体检生化，做慢病结局不行；同源方差/共同方法偏倚突出；配额抽样非概率，勿称全国代表性；产出同质化、撞题概率大。",
    tags=["中国","心理","抑郁","焦虑","睡眠","行为","健康素养","横断面","量表","合作","社会"],
    paradigm="健康心理/行为：高密度量表做关联+中介调节；强调横断面局限与同源方差，勿做因果。",
    qr="biobank"))

D.append(e("China-PAR 中国动脉粥样硬化性心血管病风险预测", "China Atherosclerotic Cardiovascular Disease Prediction", "china_cohort", 5,
    [{"label":"在线计算器","url":"https://www.cvdrisk.com.cn"}],
    region="中国多队列", scale="约 12.7 万", timeSpan="随访十余年",
    host="中国医学科学院阜外医院（顾东风团队）",
    content="整合 China-MUCA、InterASIA、CIMIC 等多队列；产出 China-PAR 10 年及终生 ASCVD 风险模型，已写入指南。",
    intro="原始数据不公开，但模型方程与在线计算器公开。做预测模型必须研究其建模策略（少而易获取变量）、报告规范（校准曲线/决策曲线/NRI/IDI）、转化路径（论文→指南）。",
    usage="原始数据不公开；模型与计算器公开。",
    notes="",
    tags=["中国","心血管","ASCVD","预测模型","风险","队列","合作"],
    paradigm="预测模型范式：少变量建模→校准/决策曲线/NRI/IDI→转化入指南；原始数据走合作。",
    qr="biobank"))

D.append(e("China PEACE / 百万人群项目", "China PEACE & Million Population Project", "china_cohort", 5,
    [{"label":"阜外医院","url":"https://www.fuwai.com"}],
    region="中国 31 省", scale="百万人群项目；住院病历抽样全国代表", timeSpan="进行中",
    host="中国医学科学院阜外医院（蒋立新团队）",
    content="百万人群：35-75 岁社区心血管高危筛查干预；回顾性：全国代表性住院病历两阶段随机抽样（急性心梗/心衰等）。",
    intro="中国极少数有严格抽样框架的全国性医疗质量评价研究，做医疗质量、区域差异、指南依从性的设计逻辑是国内标杆。",
    usage="合作制。",
    notes="",
    tags=["中国","心血管","医疗质量","卫生服务","抽样","合作"],
    paradigm="医疗质量评价：严格抽样框架的病历抽样→区域差异/指南依从性分析。",
    qr="biobank"))

D.append(e("CMEC 中国西南多民族队列", "China Multi-Ethnic Cohort", "china_cohort", 5,
    [{"label":"四川大学华西公卫","url":"https://wcsph.scu.edu.cn"}],
    region="云贵川渝藏", scale="近 10 万", timeSpan="2018 前后至今",
    host="四川大学华西公共卫生学院",
    content="覆盖藏、彝、苗、白、侗等民族，做民族健康差异与高原环境健康的唯一大型资源。",
    intro="民族健康差异与高原环境研究的独家大型队列。",
    usage="合作制。",
    notes="",
    tags=["中国","民族","高原","队列","合作","环境"],
    paradigm="民族/高原健康：多民族队列做健康差异与环境暴露。",
    qr="biobank"))

D.append(e("泰州队列", "Taizhou Cohort", "china_cohort", 5,
    [{"label":"复旦大学","url":"https://sph.fudan.edu.cn"}],
    region="江苏泰州", scale="十万量级（待核）", timeSpan="进行中",
    host="复旦大学",
    content="生物样本库完善，肿瘤与代谢方向。",
    intro="华东地区完善的生物样本队列。",
    usage="合作制。",
    notes="",
    tags=["中国","肿瘤","代谢","生物样本","队列","合作"],
    paradigm="肿瘤/代谢队列：完善样本库支撑生物标志物发现。",
    qr="biobank"))

D.append(e("上海女性/男性健康研究 SWHS/SMHS", "Shanghai Women's/Men's Health Studies", "china_cohort", 5,
    [{"label":"范德堡大学","url":"https://www.vanderbilt.edu"}],
    region="上海", scale="女 74,942 / 男 61,480", timeSpan="长期随访",
    host="上海市疾控与范德堡大学",
    content="膳食与肿瘤，随访极长；男女配对设计。",
    intro="东亚女性/男性大型队列，膳食-肿瘤经典。",
    usage="合作制。",
    notes="",
    tags=["中国","女性","男性","妇科","女性肿瘤","膳食","肿瘤","队列","合作"],
    paradigm="膳食-肿瘤：长随访配对队列做营养与肿瘤关联。",
    qr="biobank"))

D.append(e("CNSR 中国国家卒中登记", "China National Stroke Registry", "china_cohort", 5,
    [{"label":"国家神经系统疾病临床医学研究中心","url":"https://www.ncrcnd.org.cn"},
     {"label":"CNSR-III 项目站（数据共享）","url":"https://cs03.ncrcnd.org.cn"},
     {"label":"北京天坛医院","url":"https://www.bjtth.cn"}],
    region="中国", scale="CNSR-I 约 2.2 万｜CNSR-III 15,166 例（201 家中心）", timeSpan="CNSR-I 2007-2008；CNSR-III 2015-2019，随访 5 年",
    host="首都医科大学附属北京天坛医院 王拥军团队 / 国家神经系统疾病临床医学研究中心",
    content="连续入院的急性卒中患者登记：人口学、危险因素、院前延误、溶栓/取栓、影像（CT/MRI）、实验室、用药、院内结局与 3 个月/1 年/5 年随访（mRS、复发、死亡）；CNSR-III 另建血液样本与多组学（基因组、蛋白组、代谢组）子集。",
    intro="国内卒中方向体量与随访最完整的登记研究。CNSR-III 由王拥军教授牵头，全国 201 家分中心、15,166 例，随访 5 年，已完成 6000 TB 级组学数据采集，是全球数据量最大、覆盖面最广的脑血管病队列之一。做中国卒中医疗质量、溶栓/取栓疗效比较、复发风险预测、卒中分型与预后模型的首选数据源；配合国家卒中中心上报数据可做政策评估。",
    usage="合作制（★★★★★）：不开放公开下载。需与国家神经系统疾病临床医学研究中心团队建立合作，提交研究方案与变量清单，经学术委员会评审后，在指定安全环境内分析或由中心团队代跑；原始个体数据不出中心。CNSR-III 已于 2019 年公布数据共享规则，可按规则申请共享子集。周期通常 3-6 个月起，多数需共同署名。",
    notes="① 是「登记」不是「人群队列」，入院选择偏倚明显，不能算发病率；② 各分中心影像设备与判读标准不一，做影像组学须先做中心间一致性检验；③ 变量命名与随访轮次以中心提供的数据字典为准，勿照搬文献变量名；④ 涉人遗传资源，数据出境须走《人类遗传资源管理条例》审批。",
    tags=["中国","卒中","脑血管","神经","溶栓","取栓","复发","预后","影像","生物标志物","登记","随访","多组学","合作"],
    paradigm="卒中预后与医疗质量：以 CNSR-III 连续入院的急性缺血性卒中为对象，暴露取再灌注治疗（溶栓/取栓）或入院至溶栓时间(DNT)，结局取 3 个月 mRS>2 与 1 年复发，用多因素 logistic / Cox 并做中心随机效应与倾向性评分；敏感性分析排除失访与转院者。",
    qr="monitor"))

D.append(e("C-STRIDE 中国慢性肾脏病队列", "China Chronic Kidney Disease Cohort", "china_cohort", 5,
    [{"label":"北大一院","url":"https://www.pkufh.com"}],
    region="中国", scale="数千例 CKD 患者", timeSpan="前瞻性",
    host="北京大学第一医院",
    content="中国最重要的 CKD 进展前瞻队列。",
    intro="CKD 进展研究的国内核心队列。",
    usage="合作制。",
    notes="",
    tags=["中国","肾脏","CKD","进展","队列","合作"],
    paradigm="CKD 进展：eGFR 斜率/蛋白尿结局的前瞻随访。",
    qr="biobank"))

D.append(e("CK-NET 中国肾脏疾病网络", "China Kidney Disease Network", "china_cohort", 5,
    [{"label":"官网","url":"https://www.chinakidney.net"},
     {"label":"数据申请入口","url":"https://www.chinakidney.net/index.php/application.html"},
     {"label":"北京大学第一医院","url":"https://www.pkufh.com"}],
    region="中国", scale="全国医保与住院数据；70+ 家肾脏病中心协作网络", timeSpan="年度报告",
    host="北京大学第一医院肾内科 / 北京大学医学部肾脏疾病大数据研究中心",
    content="整合国家监管性数据库、医保给付数据与区域医疗平台，产出《中国肾脏疾病年度科学报告》；含 C-STRIDE、INDEED 等子队列。",
    intro="做中国肾脏病负担与医疗利用的权威数据网络。年度报告可直接作为论文的中国背景引用源；想拿个体级数据则需走官网申请页并与团队合作。",
    usage="官网有在线申请入口（填写研究名称、背景、目的、方法、主要变量、时间范围与申请人信息）→ 中心评审 → 签数据使用协议；参与单位可按数据共享权重获得返还数据。合作制为主。",
    notes="",
    tags=["中国","肾脏","医保","住院","卫生服务","合作"],
    paradigm="肾脏疾病负担：全国医保/住院数据做利用与质量分析，年度报告可引用。",
    qr="biobank"))

D.append(e("中国高血压调查 CHS", "China Hypertension Survey", "china_cohort", 5,
    [{"label":"阜外医院","url":"https://www.fuwai.com"}],
    region="中国", scale="大规模筛查", timeSpan="进行中",
    host="中国医学科学院阜外医院",
    content="中国高血压患病率、知晓率、治疗率、控制率的权威来源。",
    intro="高血压流行病学权威调查。",
    usage="合作/报告引用。",
    notes="",
    tags=["中国","高血压","流行病学","筛查","合作"],
    paradigm="高血压流行病学：患病率/知晓/治疗/控制率的描述与趋势。",
    qr="biobank"))

# ============================ 第六章 监测横断面 ============================
D.append(e("NHANES 美国国家健康与营养检查调查", "National Health and Nutrition Examination Survey", "monitor", 1,
    [{"label":"官网","url":"https://wwwn.cdc.gov/nchs/nhanes/"},{"label":"死亡链接文件","url":"https://www.cdc.gov/nchs/data-linkage/mortality-public.htm"}],
    region="美国", scale="每年约 5 千", timeSpan="1999 至今",
    host="美国 CDC 国家卫生统计中心",
    content="连续调查每 2 年一周期，复杂多阶段抽样提供权重；问卷+体检+实验室三位一体，与国家死亡索引链接的公开死亡随访免费。",
    intro="科研入门第一库：质控极严。肾脏方向可用标准化血肌酐、部分周期胱抑素 C、尿白蛋白肌酐比、多次标准化血压、降压药处方。横断面数据可经死亡链接变前瞻性队列。",
    usage="完全公开，零申请零费用直接下载；高度受限变量需赴 NCHS 研究数据中心现场使用。",
    notes="2017-2020 因疫情中断，官方发布合并文件必须用专门疫情前权重，不能沿用旧合并算法；真正的瓶颈是选题新颖性。",
    tags=["美国","一般人群","体检","生化","肌酐","eGFR","血压","营养","死亡登记","横断面","随访","公开"],
    paradigm="横断面→前瞻：用权重做复杂抽样估计；链接死亡文件把横断面转队列；注意周期权重。",
    qr="monitor"))

D.append(e("KNHANES 韩国国民健康营养调查", "Korea National Health and Nutrition Examination Survey", "monitor", 1,
    [{"label":"官网（待核）","url":"https://knhanes.kdca.go.kr"}],
    region="韩国", scale="全国样本", timeSpan="进行中",
    host="韩国 CDC",
    content="韩国版 NHANES，设计对标，公开下载，界面以韩文为主。",
    intro="韩国国家级体检+营养监测，适合跨国与 NHANES 对标。",
    usage="公开下载（韩文界面）。",
    notes="入口待核；韩文界面。",
    tags=["韩国","一般人群","体检","营养","生化","横断面","公开"],
    paradigm="韩国健康营养：对标 NHANES 做跨国比较与趋势。",
    qr="monitor"))

D.append(e("BRFSS 行为危险因素监测系统", "Behavioral Risk Factor Surveillance System", "monitor", 1,
    [{"label":"官网","url":"https://www.cdc.gov/brfss"}],
    region="美国", scale="每年数十万", timeSpan="1984 至今",
    host="美国 CDC",
    content="全球最大电话健康调查，具州级代表性。",
    intro="州级行为危险因素监测，适合健康行为与健康公平州际比较。",
    usage="完全公开下载。",
    notes="",
    tags=["美国","行为","健康公平","横断面","公开","问卷"],
    paradigm="健康行为州际比较：州代表样本做行为危险因素与政策评估。",
    qr="monitor"))

D.append(e("NHIS 美国国民健康访问调查", "National Health Interview Survey", "monitor", 1,
    [{"label":"官网","url":"https://www.cdc.gov/nchs/nhis/"}],
    region="美国", scale="大样本", timeSpan="进行中",
    host="美国 CDC",
    content="与 NHANES 互补，无体检但样本量大得多。",
    intro="大样本健康访谈，适合服务利用与保险研究。",
    usage="完全公开下载。",
    notes="",
    tags=["美国","服务利用","保险","横断面","公开","问卷"],
    paradigm="服务利用/保险：大样本访谈做医疗利用与覆盖分析。",
    qr="monitor"))

D.append(e("中国慢性病及危险因素监测", "China Chronic Disease and Risk Factor Surveillance", "monitor", 5,
    [{"label":"中国疾控慢病中心","url":"https://www.chinacdc.cn"}],
    region="中国", scale="代表性最好", timeSpan="进行中",
    host="中国疾控中心慢病中心",
    content="中国代表性最好的慢病监测数据。",
    intro="中国慢病患病率/危险因素的权威来源，但不公开。",
    usage="需合作。",
    notes="不公开。",
    tags=["中国","慢病","危险因素","监测","合作"],
    paradigm="中国慢病监测：代表性抽样做患病率与危险因素；需合作获取。",
    qr="monitor"))

# ============================ 第七章 真实世界 RWD ============================
D.append(e("香港医管局 CDARS", "Clinical Data Analysis and Reporting System", "rwd", 5,
    [{"label":"数据实验室（待核）","url":"https://www3.ha.org.hk/data/"},{"label":"公开汇总 data.gov.hk","url":"https://data.gov.hk"}],
    region="中国香港", scale="约 750 万", timeSpan="1990 年代至今",
    host="香港医院管理局（HA）",
    content="40 余公立医院+百余门诊；唯一匿名编码跨机构跨年随访；住院 ICD-9-CM、门诊 ICPC-2、处方配药、检验（肌酐序列）、影像手术、急诊住院、死亡链接；回溯 20 年以上。",
    intro="香港无「医保局」，公立医疗由税收筹资、医管局统一运营。典型设计：自身对照病例系列、新使用者设计、目标试验模拟、疫苗安全性主动监测。数据不可下载，在安全环境分析、结果审核后带出。",
    usage="经医管局数据实验室申请，需研究计划书+伦理批件+本地机构 PI，按项目收费；结果审核后带出。",
    notes="别混淆：医健通 eHRSS 是公私病历互通平台，与 CDARS 不是一回事；「香港理工大学数据库」无可靠对应，理大健康数据多走 HA 数据实验室或各院系自建队列。",
    tags=["香港","真实世界","电子病历","医保","处方","检验","死亡登记","队列","随访","合作","目标试验"],
    paradigm="真实世界(港): 新使用者设计/目标试验模拟/自身对照病例系列；安全环境分析、不可下载。",
    qr="monitor"))

D.append(e("韩国 NHIS 国民健康保险", "National Health Insurance Service", "rwd", 5,
    [{"label":"NHIS 数据共享","url":"https://nhiss.nhis.or.kr"}],
    region="韩国", scale="全国参保人", timeSpan="2002 至今",
    host="韩国国民健康保险公团",
    content="全民单一支付方，覆盖近全部人口；NHIS-NSC 全国代表性抽样队列（随访十余年）+ 健康检查数据库（法定定期体检含血压/空腹血糖/肌酐/尿蛋白等客观指标，与理赔一体化）。",
    intro="全世界少数「全民覆盖+客观体检+处方记录+长随访」四合一数据源。做降压药类别与肾脏结局的目标试验模拟证据等级极高。",
    usage="需韩国本地合作者+伦理审查+按项目付费，在指定分析中心操作，数据不可带出；基本必须合作。",
    notes="",
    tags=["韩国","真实世界","医保","理赔","体检","处方","队列","随访","合作","目标试验","肾脏"],
    paradigm="真实世界(韩): 四合一数据做目标试验模拟/新使用者设计；须本地合作、分析中心内操作。",
    qr="monitor"))

D.append(e("韩国 HIRA 健康保险审查评价院", "Health Insurance Review & Assessment", "rwd", 5,
    [{"label":"官网","url":"https://www.hira.or.kr"}],
    region="韩国", scale="全国理赔", timeSpan="进行中",
    host="韩国健康保险审查评价院",
    content="全国理赔审核数据，处方级别粒度。",
    intro="与 NHIS 互补，处方粒度更细，做药物流行病学。",
    usage="需本地合作+分析中心。",
    notes="",
    tags=["韩国","真实世界","医保","理赔","处方","合作","药物流行病学"],
    paradigm="药物流行病学(韩): 理赔处方级数据做用药模式与安全监测；须合作。",
    qr="monitor"))

D.append(e("CPRD 英国基层医疗数据库", "Clinical Practice Research Datalink", "rwd", 4,
    [{"label":"官网","url":"https://cprd.com"}],
    region="英国", scale="累计逾 6000 万患者", timeSpan="1987 至今",
    host="英国（GOLD 与 Aurum 两库）",
    content="基层医疗记录，可链接 HES 住院、ONS 死亡与癌症登记。",
    intro="药物流行病学的国际金标准。",
    usage="需研究方案审批并付费。",
    notes="",
    tags=["英国","真实世界","电子病历","基层","处方","药物流行病学","队列","随访","死亡登记"],
    paradigm="药物流行病学(英): 基层处方+住院/死亡链接做药物安全与疗效。",
    qr="monitor"))

D.append(e("OpenSAFELY 英国全民健康记录分析平台", "OpenSAFELY", "rwd", 4,
    [{"label":"官网","url":"https://www.opensafely.org"}],
    region="英国", scale="全英 NHS 记录", timeSpan="进行中",
    host="英国（代码在安全环境运行）",
    content="代码在安全环境内运行，全流程开源，透明度行业标杆。",
    intro="可信分析平台范式，适合快速大规模观察性研究。",
    usage="需审批，代码在安全环境运行。",
    notes="",
    tags=["英国","真实世界","电子病历","NHS","透明","合作"],
    paradigm="可信分析: 在 OpenSAFELY 安全环境提交分析代码，全流程开源可复现。",
    qr="monitor"))

D.append(e("QResearch 英国基层医疗数据库", "QResearch", "rwd", 4,
    [{"label":"官网","url":"https://www.qresearch.org"}],
    region="英国", scale="基层医疗大样本", timeSpan="进行中",
    host="牛津托管（QRISK 来源）",
    content="QRISK 等风险模型的数据来源。",
    intro="风险预测模型研究与验证的英国数据源。",
    usage="需审批/合作。",
    notes="",
    tags=["英国","真实世界","电子病历","基层","预测模型","合作"],
    paradigm="风险模型(英): 基层数据开发与验证风险预测模型。",
    qr="monitor"))

D.append(e("北欧登记体系", "Nordic Registries (Denmark/Sweden/Norway/Finland)", "rwd", 5,
    [{"label":"各国登记官网","url":"https://www.norden.org"}],
    region="丹麦/瑞典/挪威/芬兰", scale="全民", timeSpan="出生到死亡",
    host="北欧各国",
    content="唯一编号贯穿出生到死亡，随访完整度全球第一。",
    intro="做因果推断与药物安全的天然实验场；通常需本地 PI 与合作。",
    usage="需本地 PI，通常必须合作。",
    notes="",
    tags=["北欧","真实世界","登记","随访","队列","合作","药物流行病学"],
    paradigm="北欧登记: 唯一编号全周期随访做因果/药物安全；须本地 PI。",
    qr="monitor"))

D.append(e("台湾 NHIRD 全民健康保险研究数据库", "Taiwan National Health Insurance Research Database", "rwd", 5,
    [{"label":"资料科学中心","url":"https://dep.mohw.gov.tw/dos/"}],
    region="中国台湾", scale="全民健保", timeSpan="1995 至今",
    host="台湾卫生福利部资料科学中心",
    content="全民健保数据，现由资料科学中心管理，需现场分析。",
    intro="曾经极易发表，现在门槛提高很多。",
    usage="需现场分析，门槛提高。",
    notes="",
    tags=["台湾","真实世界","医保","理赔","合作","现场分析"],
    paradigm="台湾健保: 现场分析做真实世界研究；门槛已提高。",
    qr="monitor"))

D.append(e("日本 NDB / JMDC", "Japan NDB / JMDC", "rwd", 5,
    [{"label":"NDB 官网","url":"https://www.mhlw.go.jp"}],
    region="日本", scale="全国理赔/商保", timeSpan="进行中",
    host="日本（NDB 全国理赔；JMDC 含体检）",
    content="全国理赔数据，JMDC 含体检数据。",
    intro="需日方合作。",
    usage="需日方合作。",
    notes="",
    tags=["日本","真实世界","医保","理赔","体检","合作"],
    paradigm="日本真实世界: 理赔/商保数据做药物与卫生服务研究；须合作。",
    qr="monitor"))

D.append(e("TriNetX 全球联邦式研究网络", "TriNetX", "rwd", 4,
    [{"label":"官网","url":"https://trinetx.com"}],
    region="全球联邦式", scale="数百家医疗机构", timeSpan="进行中",
    host="商业联邦网络",
    content="机构订阅制，几分钟出队列计数与倾向性评分匹配；看不到原始病历，数据质量取决于各院映射。",
    intro="适合快速筛选研究问题与可行性评估。",
    usage="机构订阅制。",
    notes="看不到原始病历，数据质量依赖映射。",
    tags=["全球","真实世界","联邦","队列","订阅","可行性"],
    paradigm="可行性筛选: 联邦网络快速出队列计数与 PSM，用于研究问题可行性。",
    qr="monitor"))

D.append(e("MarketScan / Optum / IQVIA 美国商保数据", "Commercial Claims Data", "rwd", 4,
    [{"label":"IBM MarketScan","url":"https://www.ibm.com/products/marketscan"},{"label":"Optum","url":"https://www.optum.com"}],
    region="美国", scale="千万至亿级", timeSpan="进行中",
    host="商业授权（药企/咨询常用）",
    content="商业保险理赔数据，昂贵。",
    intro="真实世界证据（RWE）与药物流行病学的商业数据源。",
    usage="商业授权，昂贵。",
    notes="",
    tags=["美国","真实世界","医保","理赔","商业","昂贵"],
    paradigm="商保 RWE: 理赔数据做药物利用与真实世界证据；商业授权。",
    qr="monitor"))

D.append(e("CMS Medicare/Medicaid (ResDAC)", "US CMS Medicare/Medicaid", "rwd", 4,
    [{"label":"ResDAC","url":"https://www.resdac.org"}],
    region="美国", scale="全国老年与低收入人群", timeSpan="进行中",
    host="美国 CMS（经 ResDAC 申请）",
    content="全国老年与低收入人群医保；与 SEER 链接即 SEER-Medicare。",
    intro="老年人群真实世界研究的权威来源。",
    usage="经 ResDAC 申请，付费。",
    notes="",
    tags=["美国","真实世界","医保","老年","肿瘤","合作"],
    paradigm="老年真实世界: Medicare 数据做老年医疗利用；链接 SEER 做肿瘤。",
    qr="monitor"))

# ============================ 第八章 重症/ICU ============================
D.append(e("MIMIC-IV 重症监护数据库", "Medical Information Mart for Intensive Care IV", "icu", 3,
    [{"label":"PhysioNet 数据集","url":"https://physionet.org/content/mimiciv/"},{"label":"平台","url":"https://physionet.org"}],
    region="美国单中心", scale="30 万+ 住院", timeSpan="2008 至今",
    host="Beth Israel Deaconess 医学中心 / MIT 实验计算生理学实验室",
    content="hosp（住院：实验室/处方/诊断/微生物）、icu（ICU：生命体征/给药/出入量/评分）、MIMIC-IV-ED（急诊）、MIMIC-IV-Note（去标识文本，NLP/大模型核心）、MIMIC-IV-ECG（波形心电）、MIMIC-CXR（胸片+报告）。",
    intro="免费。获取流程：①注册 PhysioNet 账号；②完成 CITI「Data or Specimens Only Research」培训取证书；③提交 credentialing 申请（上传证书+导师/主管推荐人），审核数天至数周（推荐人不回邮件是最常见失败原因）；④签 DUA 后下载。建议 BigQuery 或本地 PostgreSQL，纯 CSV 很痛苦。",
    usage="免费；培训+DUA，周期 2-6 周。",
    notes="单中心、美国、ICU 人群，外推有限；时间戳随机偏移，不能做真实历法季节分析；同一患者多次入院注意聚类；AKI 需自行按 KDIGO 从肌酐序列构建。",
    tags=["美国","ICU","重症","电子病历","重症","AKI","KDIGO","文本","影像","心电","NLP","队列","公开-协议"],
    paradigm="ICU 预测/预后：hosp+icu 模块构建暴露结局→ML/统计模型；AKI 按 KDIGO 自肌酐序列构建；注意单中心偏倚与时间偏移。",
    qr="monitor"))

D.append(e("eICU-CRD 重症数据库", "eICU Collaborative Research Database", "icu", 3,
    [{"label":"PhysioNet","url":"https://physionet.org/content/eicu-crd/"}],
    region="美国多中心", scale="200 余家医院", timeSpan="进行中",
    host="PhysioNet（多中心）",
    content="弥补 MIMIC 单中心缺陷，多中心 ICU 数据。",
    intro="MIMIC 训练 + eICU 外部验证是审稿接受度最高的搭配。",
    usage="免费；同 MIMIC 的 CITI+DUA 流程。",
    notes="",
    tags=["美国","ICU","重症","多中心","电子病历","外部验证","公开-协议"],
    paradigm="多中心外部验证: MIMIC 训练 → eICU 验证，提升泛化证据。",
    qr="monitor"))

D.append(e("AmsterdamUMCdb 重症数据库", "Amsterdam University Medical Centers DB", "icu", 3,
    [{"label":"项目主页","url":"https://amsterdammedicaldatascience.nl"},
     {"label":"代码与数据说明（GitHub）","url":"https://github.com/AmsterdamUMC/AmsterdamUMCdb"}],
    region="荷兰", scale="约 2.3 万次 ICU 入住 / 2 万例患者（2003-2016）", timeSpan="2003-2016",
    host="阿姆斯特丹大学医学中心（Amsterdam UMC）",
    content="欧洲首个大型开放 ICU 数据库：人口学、诊断（APACHE IV）、生命体征、实验室、用药、液体与通气、SOFA 与结局；时间分辨率 1 分钟级，另提供 12 小时重采样版本便于与 MIMIC 对齐。",
    intro="欧洲人群的 MIMIC 对照库。适合做「北美训练 → 欧洲验证」的跨大陆外部验证，检验模型在院前流程、治疗强度、病历记录习惯不同时的稳健性。变量结构参考 MIMIC-III/IV 设计，迁移成本低。",
    usage="签署数据使用协议（DUA）后免费获取：在项目主页按说明提交申请，声明用途与不尝试再识别，获批后通过指定链接下载；需完成数据保护与 GDPR 相关承诺。周期约 2-6 周，无数据费。",
    notes="① 单中心（两家院区），外推需谨慎；② 变量编码体系与 MIMIC 不完全一致，映射表要自己核对，别直接套 MIMIC 的 SQL；③ 荷兰语记录字段需查数据字典；④ 只允许在安全环境分析，不得再分发。",
    tags=["欧洲","荷兰","ICU","重症","电子病历","外部验证","时间序列","公开-协议"],
    paradigm="跨大陆外部验证：用 MIMIC-IV 训练 28 天死亡/急性肾损伤预测模型 → 在 AmsterdamUMCdb 上按同一变量定义与预处理流程验证，报告 AUC 衰减与校准曲线漂移，并做重新校准（recalibration）。",
    qr="monitor"))

D.append(e("HiRID 高分辨率重症数据库", "High Time Resolution ICU Dataset", "icu", 3,
    [{"label":"官网","url":"https://hirid.intensivecare.ai"}],
    region="瑞士", scale="高时间分辨率", timeSpan="进行中",
    host="瑞士",
    content="高时间分辨率（可达 2 分钟级）生理数据。",
    intro="适合生理信号处理与高分辨率预警模型。",
    usage="开放获取（流程类似）。",
    notes="",
    tags=["瑞士","ICU","重症","高分辨率","生理信号","公开-协议"],
    paradigm="高分辨率生理: 2 分钟级信号做早期预警与生理建模。",
    qr="monitor"))

D.append(e("SICdb 萨尔茨堡重症数据库", "Salzburg Intensive Care Database", "icu", 3,
    [{"label":"官网与文档","url":"https://www.sicdb.com"},
     {"label":"数据下载（PhysioNet）","url":"https://physionet.org/content/sicdb/1.0.8/"},
     {"label":"论文（Critical Care 2023）","url":"https://pmc.ncbi.nlm.nih.gov/articles/PMC10287776/"}],
    region="奥地利", scale="27,350+ 次 ICU 入住（2013-2021，4 个 ICU / 41 张床）", timeSpan="2013-2021",
    host="萨尔茨堡大学医院（University Hospital Salzburg）麻醉与重症医学科 / 帕拉塞尔苏斯医科大学",
    content="7 张数据表、数十亿条记录：cases（年龄/体重/性别分箱、诊断、ICD-10、评分、住院与 1 年死亡）、laboratory（实验室）、medication（用药）、data_float_h（每小时聚合的监护信号与呼吸机参数，另含每分钟原始流的序列化字段）、data_ref（名义变量）、data_range（有起止时间的事件，如中心静脉导管、引流）、unitlog。所有编码字段由 d_references 提供字典与单位。",
    intro="欧洲（奥地利）单中心、四院区 ICU 开放数据集，规模与粒度介于 MIMIC 与 HiRID 之间。特点是「小时级 + 分钟级」双层结构：常规建模用 data_float_h 足够，做高频信号或早期预警再解包每分钟流。同时提供手术前数据与 1 年死亡，适合做术后重症结局与长期死亡分析。",
    usage="免费但受控：需在 PhysioNet 完成 CITI「Data or Specimens Only Research」培训、签署数据使用协议并申请 credentialed 用户身份，获批后下载 CSV（gzip）。流程约 1-4 周，无数据费。官方另提供 Docker 环境（RooDataServer）便于把 CSV 导入数据库后查询。",
    notes="① 单中心四院区，病例以奥地利外科/麻醉人群为主，外推受限；② 年龄、体重、身高按 5 岁/5kg 分箱，别当连续变量做精细建模；③ 分钟级数据存在序列化字段里，需用官方解包脚本，直接读 CSV 会得到乱码；④ 版本迭代快（1.0.5 → 1.0.8），引用必须带版本号与 DOI。",
    tags=["欧洲","奥地利","ICU","重症","电子病历","高分辨率","信号","外部验证","公开-协议"],
    paradigm="术后重症结局：以 SICdb 中带前置手术的 ICU 入住为对象，暴露取术中/术后早期低血压时长或液体平衡，结局取院内死亡与 1 年死亡，用 Cox 或竞争风险模型并校正 APACHE/SOFA 与手术类型；按小时聚合数据做 landmark 分析避免 immortal time bias。",
    qr="monitor"))

D.append(e("INSPIRE 韩国围手术期数据库", "INTensive care Precision and REsearch", "icu", 3,
    [{"label":"官网","url":"https://inspire.re.kr"}],
    region="韩国", scale="围手术期为主", timeSpan="进行中",
    host="韩国",
    content="围手术期为主，亚洲人群。",
    intro="亚洲人群围手术期 ICU 研究资源。",
    usage="开放获取（流程类似）。",
    notes="",
    tags=["韩国","ICU","重症","围手术期","亚洲","公开-协议"],
    paradigm="围手术期 ICU: 亚洲人群围术期结局与预测。",
    qr="monitor"))

D.append(e("PIC 浙江大学附属儿童医院重症数据库", "Pediatric Intensive Care Database", "icu", 3,
    [{"label":"浙大儿院","url":"https://www.zjuch.com"}],
    region="中国", scale="儿科重症", timeSpan="进行中",
    host="浙江大学医学院附属儿童医院",
    content="儿科重症，中国唯一同类开放库。",
    intro="中国儿科 ICU 预测模型与外部验证的独家资源。",
    usage="开放获取（流程类似）。",
    notes="",
    tags=["中国","儿科","儿童","ICU","重症","电子病历","公开-协议"],
    paradigm="儿科 ICU: 中国唯一开放儿科重症库，做儿童重症预测。",
    qr="monitor"))

# ============================ 第九章 试验二次利用 ============================
D.append(e("BioLINCC 美国心肺血研究所数据仓库", "Biologic Specimen and Data Repository", "trial", 3,
    [{"label":"官网","url":"https://biolincc.nhlbi.nih.gov"}],
    region="美国", scale="SPRINT/ALLHAT/AASK/ARIC/MESA/CARDIA 等", timeSpan="经典试验与队列",
    host="美国国立心肺血液研究所 (NHLBI)",
    content="个体水平数据免费公开申请：SPRINT（强化降压 120 vs 140，含肾脏结局与 eGFR 序列）、ALLHAT（四类降压药头对头，4 万余人含 ESRD）、AASK（非裔高血压性肾硬化）、ACCORD（糖尿病强化控制）、ARIC（社区队列随访 30 余年）、MESA（多种族影像）、CARDIA（青年血压轨迹）、Framingham、CHS、Jackson Heart Study、LookAHEAD。",
    intro="本文件信息差最严重、性价比最高的一档：审批周期数周、零费用。注册账号→在线提交研究计划（篇幅不长）→伦理批件或豁免证明→签 DUA→数周获批下载。数据已去标识化并部分粗化；发表需注明来源并附免责声明。",
    usage="免费；注册+计划+伦理+DUA，周期 2-6 周。",
    notes="NHLBI 不为分析结论背书；数据部分粗化。",
    tags=["美国","RCT","二次利用","心血管","肾脏","高血压","降压","CKD","ESRD","队列","IPD","公开-协议"],
    paradigm="RCT 二次利用: 选 SPRINT/ALLHAT/AASK 等做降压/肾保护分析；提交计划+伦理+DUA，零费用数周获批。",
    qr="trial"))

D.append(e("NIDDK-CR 美国糖尿病消化肾病研究所中央数据仓库", "NIDDK Central Repository", "trial", 3,
    [{"label":"官网","url":"https://repository.niddk.nih.gov"}],
    region="美国", scale="CRIC/CKiD/DCCT-EDIC/LookAHEAD/DPP", timeSpan="长期随访",
    host="美国国立糖尿病消化肾病研究所 (NIDDK)",
    content="CRIC 慢性肾功能不全队列（CKD3-4 期，密集随访 eGFR 斜率/蛋白尿/ESRD/心血管/死亡，全球最重要 CKD 进展前瞻队列）；CKiD 儿童 CKD；DCCT/EDIC 1 型糖尿病里程碑；LookAHEAD、DPP。",
    intro="流程与 BioLINCC 类似，免费。CKD 进展预测模型要发国际期刊，在 CRIC 上做一次外部验证说服力远超再加一个中国中心。",
    usage="免费；流程同 BioLINCC。",
    notes="",
    tags=["美国","RCT","二次利用","肾脏","CKD","糖尿病","eGFR","IPD","公开-协议"],
    paradigm="CKD 进展: CRIC 做 eGFR 斜率/ESRD 分析；国际期刊外部验证首选。",
    qr="trial"))

D.append(e("NIA AgingResearchBiobank 美国老龄研究样本库", "NIA Aging Research Biobank", "trial", 3,
    [{"label":"官网","url":"https://agingresearchbiobank.nia.nih.gov"}],
    region="美国", scale="Health ABC/MrOS/SOF/InCHIANTI/LIFE 等", timeSpan="经典老年队列",
    host="美国国立老龄研究所 (NIA)",
    content="集中托管再分发已完成 NIA 资助研究的样本与数据：Health ABC、MrOS、SOF、InCHIANTI、LIFE、LookAHEAD、巴尔的摩老龄化纵向研究等。",
    intro="表型极精细（步速、肌少症、骨密度、炎症因子系列），单独找原团队极难，此处可统一申请。数据申请友好（计划+协议）；生物样本门槛高得多。注意与第十章中国 Aging Biobank 完全不同。",
    usage="免费；数据申请友好（计划+协议）；样本门槛高。",
    notes="勿与中国的 Aging Biobank (ABB) 混淆，名称相近但主办方/内容/流程完全不同。",
    tags=["美国","老龄","衰弱","肌少症","队列","二次利用","公开-协议"],
    paradigm="老年综合征: 精细表型队列（肌少/衰弱）统一申请；区分中美两个 Aging Biobank。",
    qr="trial"))

D.append(e("Vivli / YODA / CSDR 临床试验个体数据共享平台", "Clinical Trial Data Sharing Platforms", "trial", 3,
    [{"label":"Vivli","url":"https://vivli.org"},{"label":"YODA","url":"https://yoda.yale.edu"},{"label":"CSDR","url":"https://www.clinicalstudydatarequest.com"}],
    region="全球", scale="多方汇集 RCT 个体数据", timeSpan="进行中",
    host="Vivli（多方）/ YODA（耶鲁，强生等）/ CSDR（GSK 等）",
    content="个体患者数据 (IPD) 荟萃分析与二次研究的核心入口。",
    intro="做 IPD meta 分析的首选；YODA 由耶鲁托管强生等试验，CSDR 为 GSK 等（参与企业近年有变动）。",
    usage="免费/审批；提交研究计划与 DUA。",
    notes="CSDR 参与企业名单有变动（待核）。",
    tags=["全球","RCT","IPD","meta","二次利用","公开-协议"],
    paradigm="IPD meta: 跨试验个体数据合并做荟萃与异质性分析。",
    qr="trial"))

D.append(e("dbGaP 基因型与表型数据库", "Database of Genotypes and Phenotypes", "trial", 4,
    [{"label":"官网","url":"https://www.ncbi.nlm.nih.gov/gap"}],
    region="美国", scale="受控访问", timeSpan="进行中",
    host="美国 NIH",
    content="受控访问的人类基因型与表型数据（含 TCGA 受控层、多队列遗传数据）。",
    intro="受控访问：需 NIH eRA Commons 账户、在线申请、签署 Data Use Certification、机构签署官员(ISO)审批、DAC 评审、签 DUA 后开通 GDC 下载。",
    usage="受控访问；机构审批+DUA，周期数周至数月。",
    notes="仅限批准用途；禁止再识别；强制安全培训。",
    tags=["美国","基因","表型","受控","伦理","DUA","合作"],
    paradigm="受控遗传数据: eRA Commons+机构 ISO+DAC 评审+DUA；严禁再识别。",
    qr="trial"))

# ============================ 第十章 组学/仓储 ============================
D.append(e("Aging Biobank (ABB) 中国衰老生物样本库", "Aging Biobank", "omics", 5,
    [{"label":"官方入口（待核）","url":"https://cbb.cncb.ac.cn/abb/"}],
    region="中国", scale="待核", timeSpan="进行中",
    host="国家生物信息中心 / 国家基因组科学数据中心体系",
    content="面向衰老研究的生物样本与配套数据资源平台，服务衰老机制、标志物与老年疾病。同源含 AgingAtlas 等多组学资源。",
    intro="具体样本规模、队列构成、数据类型与申请流程编制时无法核实，请以官网说明与联系方式为准（标记为待核）。命名易与美国 NIA AgingResearchBiobank 冲突，致谢与数据可用性声明务必写全称与网址。",
    usage="申请流程待核，请以官网为准。",
    notes="与美国 NIA AgingResearchBiobank 完全不同，检索/写作务必区分。",
    tags=["中国","衰老","多组学","生物样本","合作","待核"],
    paradigm="中国衰老资源: 先 NGDC DatabaseCommons 检索该体系全部衰老资源，再定向进入具体平台。",
    qr="trial"))

D.append(e("GEO 基因表达综合数据库", "Gene Expression Omnibus", "omics", 1,
    [{"label":"官网","url":"https://www.ncbi.nlm.nih.gov/geo/"}],
    region="全球", scale="海量 GSE 系列", timeSpan="进行中",
    host="美国 NCBI",
    content="芯片/RNA-seq/单细胞/甲基化/ChIP-seq 等功能基因组数据，GSE(研究)/GSM(样本)/GPL(平台)，多数附临床表型。",
    intro="完全公开无需申请。用 GEO2R 快速探路，正式分析下原始矩阵自行处理；R 包 GEOquery 是标准入口。元数据质量参差，选数据集先看元数据完整度再看样本量；整合分析必须处理批次效应。",
    usage="完全公开，直接下载。",
    notes="characteristics 字段临床注释常残缺；跨数据集批次效应必须处理。",
    tags=["全球","基因","转录组","单细胞","甲基化","组学","公开","仓储"],
    paradigm="功能基因组: GEOquery 取数→差异分析→批次效应校正；先看元数据完整度。",
    qr="trial"))

D.append(e("Dryad 通用数据仓储", "Dryad", "omics", 1,
    [{"label":"官网","url":"https://datadryad.org"}],
    region="全球", scale="论文原始数据", timeSpan="进行中",
    host="通用仓储（CC0）",
    content="托管论文背后的原始数据，CC0 协议。",
    intro="很多期刊要求数据存缴，这里能找到已发表研究的个体水平数据，做二次分析与再验证很有用；下载免费，存缴由作者付费。学术惯例仍应引用原文。",
    usage="下载免费。",
    notes="应引用原始论文。",
    tags=["全球","通用","仓储","原始数据","公开","二次利用"],
    paradigm="数据再验证: 检索已发表研究原始数据做二次分析/方法学验证。",
    qr="trial"))

D.append(e("SRA 序列读取归档", "Sequence Read Archive", "omics", 1,
    [{"label":"官网","url":"https://www.ncbi.nlm.nih.gov/sra"}],
    region="全球", scale="高通量测序原始数据", timeSpan="进行中",
    host="美国 NCBI",
    content="高通量测序原始数据归档。",
    intro="测序原始数据的权威来源，常配合 GEO/GDC 使用。",
    usage="完全公开。",
    notes="",
    tags=["全球","基因","测序","转录组","公开","仓储"],
    paradigm="测序原始数据: 从 SRA 拉取 fastq 做重分析。",
    qr="trial"))

D.append(e("ArrayExpress / BioStudies", "EMBL-EBI", "omics", 1,
    [{"label":"EBI 官网","url":"https://www.ebi.ac.uk/arrayexpress/"}],
    region="欧洲", scale="功能基因组仓储", timeSpan="进行中",
    host="EMBL-EBI",
    content="欧洲版功能基因组仓储。",
    intro="与 GEO 互为补充。",
    usage="完全公开。",
    notes="",
    tags=["欧洲","基因","组学","公开","仓储"],
    paradigm="欧洲组学: 与 GEO 互补的功能基因组数据。",
    qr="trial"))

D.append(e("GDC / TCGA / cBioPortal 癌症多组学", "Genomic Data Commons", "omics", 1,
    [{"label":"GDC 门户","url":"https://portal.gdc.cancer.gov"},{"label":"cBioPortal","url":"https://www.cbioportal.org"}],
    region="全球", scale="泛癌种", timeSpan="进行中",
    host="美国 NCI / GDC；cBioPortal 可视化前端",
    content="癌症多组学（突变/表达/甲基化/临床），开放数据免审批；部分受控数据需 dbGaP 授权。",
    intro="GDC 下载+R 包 TCGAbiolinks 取数；cBioPortal 是探索期最快的可视化查询前端。",
    usage="开放数据直接下载；受控数据走 dbGaP。",
    notes="受控层需 dbGaP 授权。",
    tags=["全球","肿瘤","癌症","多组学","基因组","公开","受控","仓储"],
    paradigm="癌症多组学: TCGAbiolinks 取数→差异/突变分析；cBioPortal 探索；受控层走 dbGaP。",
    qr="trial"))

D.append(e("Zenodo / figshare / Mendeley Data", "General Repositories", "omics", 1,
    [{"label":"Zenodo","url":"https://zenodo.org"},{"label":"figshare","url":"https://figshare.com"},{"label":"Mendeley Data","url":"https://data.mendeley.com"}],
    region="全球", scale="通用代码与数据", timeSpan="进行中",
    host="通用仓储",
    content="代码与数据均可存缴/获取；Mendeley Data 为 Elsevier 系期刊常用。",
    intro="论文附带的代码、数据集与材料常在此存放。",
    usage="下载免费。",
    notes="",
    tags=["全球","通用","仓储","代码","公开"],
    paradigm="补充数据/代码: 检索论文附带的代码与数据集。",
    qr="trial"))

D.append(e("ICPSR / IPUMS 调查与微观数据仓储", "Survey & Microdata Repositories", "omics", 1,
    [{"label":"ICPSR","url":"https://www.icpsr.umich.edu"},{"label":"IPUMS","url":"https://www.ipums.org"}],
    region="全球", scale="社会/普查微观数据", timeSpan="进行中",
    host="密歇根大学 (ICPSR) / 明尼苏达 (IPUMS)",
    content="ICPSR 是社会科学数据总仓库，很多老龄调查在此二次分发；IPUMS 提供全球普查与调查微观数据的调和版本（含 IPUMS Health Surveys）。",
    intro="想找老龄/社会调查的原始微观数据，ICPSR 与 IPUMS 常是入口。",
    usage="多数公开/注册下载。",
    notes="",
    tags=["全球","社会","调查","微观数据","公开","仓储","调和"],
    paradigm="微观数据: 在 ICPSR/IPUMS 找调查原始微观数据做调和分析。",
    qr="trial"))

# ============================ 第十一章 中国国家级平台 ============================
D.append(e("国家自然科学基金基础研究知识库", "NSFC Open Repository", "cn_platform", 1,
    [{"label":"官网","url":"http://ir.nsfc.gov.cn"}],
    region="中国", scale="基金资助论文", timeSpan="进行中",
    host="国家自然科学基金委员会",
    content="论文全文知识库（非数据库），收录基金资助产出，作者按规定存缴。",
    intro="免费获取部分付费墙后中英文全文；反向检索某学者/某基金号产出全貌，写标书找同行或判断资助密度很好用。",
    usage="完全公开。",
    notes="是知识库不是数据集。",
    tags=["中国","论文","知识库","基金","公开","文献"],
    paradigm="文献/标书调研: 检索基金号产出与同行，定位研究方向。",
    qr="trial"))

D.append(e("NCMI 国家人口健康科学数据中心", "National Population Health Data Center", "cn_platform", 5,
    [{"label":"官网（域名待核）","url":"https://www.ncmi.cn"}],
    region="中国", scale="多领域科学数据", timeSpan="进行中",
    host="中国医学科学院医学信息研究所",
    content="国家科技资源共享服务平台，汇交基础/临床/公卫/中医药/药学等多领域科学数据。",
    intro="资源以汇交项目数据集为主，质量与开放差异大，有些只给元数据需联系提供方，能直接下载的个体级数据比预期少。建议先当数据资源目录检索，了解国内有哪些团队汇交过什么，再定向联系合作。",
    usage="先目录检索→定向联系合作；域名待核。",
    notes="直接可下载的个体级数据偏少，多需联系。",
    tags=["中国","国家级","科学数据","目录","合作","平台"],
    paradigm="中国数据目录: 当资源目录检索→定向联系汇交团队合作。",
    qr="trial"))

D.append(e("NGDC 国家基因组科学数据中心", "National Genomics Data Center", "cn_platform", 2,
    [{"label":"官网","url":"https://ngdc.cncb.ac.cn"}],
    region="中国", scale="GSA/OMIX 等", timeSpan="进行中",
    host="国家生物信息中心 (CNCB)",
    content="GSA 测序数据归档、OMIX 组学数据，可理解为中国版 GEO 与 SRA。",
    intro="建议先在 DatabaseCommons 检索该体系下全部衰老/组学相关资源，再定向进入具体平台。",
    usage="注册/开放下载。",
    notes="",
    tags=["中国","基因","组学","测序","国家级","公开","仓储"],
    paradigm="中国组学: GSA/OMIX 归档与检索；DatabaseCommons 发现资源。",
    qr="trial"))

D.append(e("ScienceDB 科学数据银行", "Science Data Bank", "cn_platform", 1,
    [{"label":"官网","url":"https://www.scidb.cn"}],
    region="中国", scale="通用数据仓储", timeSpan="进行中",
    host="中国科学院",
    content="通用数据仓储，中国版 Dryad。",
    intro="论文数据存缴与共享的中国平台。",
    usage="公开下载。",
    notes="",
    tags=["中国","通用","仓储","公开","平台"],
    paradigm="中国数据仓储: 论文配套数据存缴与获取。",
    qr="trial"))

D.append(e("NMDC 国家微生物科学数据中心", "National Microbiology Data Center", "cn_platform", 1,
    [{"label":"官网","url":"https://nmdc.cn"}],
    region="中国", scale="微生物/微生物组", timeSpan="进行中",
    host="中国科学院",
    content="微生物与微生物组学数据。",
    intro="微生物组研究的中国国家级资源。",
    usage="公开下载。",
    notes="",
    tags=["中国","微生物","组学","国家级","公开","平台"],
    paradigm="微生物组: 国家微生物数据中心检索与下载。",
    qr="trial"))

D.append(e("国家/卫生健康统计年鉴", "China Health Statistics Yearbook", "cn_platform", 1,
    [{"label":"国家统计局","url":"https://www.stats.gov.cn"},{"label":"国家卫健委","url":"https://www.nhc.gov.cn"}],
    region="中国", scale="宏观指标", timeSpan="年度",
    host="国家统计局 / 国家卫健委",
    content="宏观卫生资源与服务量指标，用于生态学分析与政策背景。",
    intro="中国宏观卫生资源的权威来源。",
    usage="官方发布，公开。",
    notes="",
    tags=["中国","宏观","卫生资源","年鉴","公开","政策"],
    paradigm="宏观背景: 年鉴指标做生态学分析与政策背景。",
    qr="trial"))

# ============================ 第十二章 卫生经济/服务 ============================
D.append(e("HCUP 美国医疗成本与利用项目", "Healthcare Cost and Utilization Project", "healthecon", 4,
    [{"label":"官网","url":"https://hcup-us.ahrq.gov"}],
    region="美国", scale="NIS 每年约 700 万出院", timeSpan="1988 至今",
    host="美国医疗保健研究与质量局 (AHRQ)",
    content="NIS 全国住院样本（加权代表约 3500 万次住院）、NRD 再入院库、KID 儿科住院、SID/SEDD/SASD 州级住院/急诊/日间手术；含诊断操作编码、住院日、总费用、付费方、转归、医院特征。",
    intro="卫生管理方向核心：住院费用、住院日、再入院率、医院/区域差异是卫生事业管理议题，NIS 是全球最成熟的数据源。完成在线数据使用协议培训后购买，每个库每年数百美元量级。",
    usage="培训后购买，每年数百美元量级。",
    notes="需购买。",
    tags=["美国","卫生经济","卫生服务","住院","再入院","费用","医院","购买"],
    paradigm="卫生服务研究: NIS/NRD 做住院费用/再入院/区域差异；培训后购买。",
    qr="trial"))

D.append(e("MEPS 美国医疗支出面板调查", "Medical Expenditure Panel Survey", "healthecon", 1,
    [{"label":"官网","url":"https://meps.ahrq.gov"}],
    region="美国", scale="家庭面板", timeSpan="1996 至今",
    host="美国 AHRQ",
    content="两年期面板，免费公开；家庭医疗服务使用、支出、支付来源、保险状态，并与机构/雇主问卷交叉验证。",
    intro="灾难性卫生支出、自付比例、保险对服务利用影响；卫生技术评估的成本参数来源或国际对照。",
    usage="完全公开下载。",
    notes="",
    tags=["美国","卫生经济","支出","保险","面板","公开","问卷"],
    paradigm="卫生经济: 面板数据做灾难性支出/自付比例/保险效应。",
    qr="trial"))

D.append(e("GBD / GHDx 全球疾病负担", "Global Burden of Disease", "healthecon", 1,
    [{"label":"GHDx","url":"https://ghdx.healthdata.org"}],
    region="全球", scale="国家/省/年龄/性别/年份", timeSpan="年度更新",
    host="IHME（华盛顿大学）",
    content="DALY、YLL、YLD，可按国家/省份/年龄/性别/年份查询。",
    intro="论文背景章节与政策论证的必备引用源。",
    usage="完全公开。",
    notes="",
    tags=["全球","疾病负担","DALY","宏观","公开","政策"],
    paradigm="疾病负担: GBD 指标做背景论证与跨国比较。",
    qr="trial"))

D.append(e("WHO 全球卫生观察站 / 卫生支出 / OECD / 世界银行", "Global Health Indicators", "healthecon", 1,
    [{"label":"WHO GHO","url":"https://www.who.int/data/gho"},{"label":"世界银行","url":"https://data.worldbank.org"},{"label":"CDC WONDER","url":"https://wonder.cdc.gov"}],
    region="全球", scale="宏观指标", timeSpan="年度",
    host="WHO / OECD / 世界银行 / CDC",
    content="WHO 官方指标库；各国卫生总费用构成（筹资比较）；OECD 发达国家卫生系统比较；世界银行宏观社会经济与卫生指标；CDC WONDER 美国死亡与出生在线查询。",
    intro="卫生系统比较与政策背景的权威宏观源（部分入口待核，请现查）。",
    usage="完全公开。",
    notes="OECD/WHO 卫生支出入口网站改版过，请现查。",
    tags=["全球","宏观","卫生系统","筹资","卫生支出","公开","政策"],
    paradigm="卫生系统比较: 宏观指标做跨国筹资与系统比较。",
    qr="trial"))

# ============================ 澳大利亚与大洋洲（联网核实） ============================
D.append(e("45 and Up Study 澳大利亚 45 岁以上人群队列", "The 45 and Up Study", "oceania", 4,
    [{"label":"官网","url":"https://45andup.org.au/"},
     {"label":"Sax Institute 申请页","url":"https://www.saxinstitute.org.au/solutions/45-and-up-study/use-the-45-and-up-study/cupl/"},
     {"label":"邮件咨询","url":"mailto:45andUp.Research@saxinstitute.org.au"}],
    region="澳大利亚（新南威尔士州）", scale="逾 25 万（招募逾 26.7 万）", timeSpan="2005 至今",
    host="Sax Institute（与 Cancer Council NSW、NSW Ministry of Health 合作）",
    content="45 岁及以上人群纵向调查，覆盖健康行为、生活经历、家庭与人口学、照护责任、心理困扰、生命质量与慢病；可链接 MBS（医保诊疗）、PBS（药品）、住院、癌症登记等行政与登记数据；含生物样本与地理空间数据。",
    intro="澳大利亚规模最大的健康与老龄化持续研究，由 Sax Institute 管理。参与者均同意其调查数据与常规行政健康数据链接。可开发子研究（sub-study）邀请受试者参加干预、采集体检与生物样本。数据经安全统一研究环境（SURE）访问，严格保密。",
    usage="研究者向 Sax Institute 提交申请：需科学合理可行的研究方案、伦理批件、数据保管方(custodian)批准，并承担 45 and Up 许可费与 SURE 使用费。任何 bona fide 研究者均可申请。",
    notes="队列基于 NSW 州，全国代表性有限；80 岁以上与农村偏远地区人群过采样；应答率约 19%。",
    tags=["澳大利亚","大洋洲","队列","前瞻性","老龄","慢病","真实世界","医保","MBS","PBS","链接","癌症登记","生物样本"],
    paradigm="澳洲老龄与慢病：以 45 and Up 调查+MBS/PBS/住院链接做慢病发生与结局；需 SURE 安全环境分析。",
    qr=None))

D.append(e("CUPL 慢性疾病伞式数据链接项目", "Chronic Conditions Umbrella Program Linkage", "oceania", 4,
    [{"label":"CUPL 官方页","url":"https://www.saxinstitute.org.au/solutions/45-and-up-study/use-the-45-and-up-study/cupl/"}],
    region="澳大利亚", scale="45 and Up + 10 个行政数据集", timeSpan="持续更新（年更或更频）",
    host="Sax Institute（经 PHSREC 与各数据保管方批准）",
    content="一次审批即可获取 45 and Up 调查 + 10 个数据集：MBS（含 DVA）、PBS（含 RPBS）、NSW 住院(APDC)、出生死亡婚姻登记(RBDM-Death)、死因单元记录(COD-URF)、急诊(EDDC)、癌症登记(NSW CCR)、精神健康数据(CHAMB)、传染病报告(NCIMS，含 COVID)。",
    intro="CUPL 让研究者用一次审批同时拿到调查数据与 10 类行政健康数据，相比逐个数据保管方申请可将等待时间缩短至多 80%——原本可能需要一年以上，经 CUPL 最短约 2-3 个月。数据经 SURE 安全环境提供。",
    usage="经 Sax Institute 申请，聚焦慢性疾病的研究方案；需伦理与数据保管方批准；数据在 SURE 内分析。",
    notes="仅适用于慢性疾病相关研究（含多病共存、慢病急性加重、长期传染病等）。",
    tags=["澳大利亚","慢病","多病共存","医保","MBS","PBS","住院","急诊","癌症登记","死亡登记","真实世界","链接"],
    paradigm="澳洲慢病真实世界：一次审批打通调查+10类行政数据，在 SURE 内做慢病发生率、多病共存与结局研究。",
    qr=None))

D.append(e("PLIDA 澳大利亚个人级整合数据资产（ABS DataLab）", "Person Level Integrated Data Asset", "oceania", 4,
    [{"label":"ABS 官网（检索 PLIDA / DataLab）","url":"https://www.abs.gov.au/"},
     {"label":"咨询邮箱","url":"mailto:mydataportal@abs.gov.au"}],
    region="澳大利亚", scale="全国人口级纵向资产", timeSpan="纵向（跨年份）",
    host="澳大利亚统计局 ABS（Accredited Data Service Provider）",
    content="以 Person Linkage Spine 链接的纵向数据资产，涵盖健康、教育、政府支付、收入与税收、就业、人口普查等。核心模块：残障、教育、家庭与住户、健康、收入与税收、移民、社会支持；含 MBS 模块。",
    intro="PLIDA（前身 MADIP）由 ABS 牵头，联合税务、教育、卫生、社会服务、Services Australia、内政部等机构共建。经审批的研究者可在 ABS DataLab 内使用去标识化微观数据（PLIDA Modular Product），按研究需要逐模块申请。",
    usage="澳大利亚政府机构或学术机构所属研究者可申请；通过 ABS DataLab 项目提案申请，需各数据保管方批准；在 DataLab 内用统计软件分析，数据不可带出。",
    notes="模块需单独申请与批准；仅限获批项目所需模块。",
    tags=["澳大利亚","全国","真实世界","医保","MBS","税收","教育","普查","DataLab","微观数据","纵向"],
    paradigm="澳洲政策评估：在 ABS DataLab 用 PLIDA 模块做健康-收入-教育-税收的跨部门政策评估与纵向分析。",
    qr=None))

D.append(e("MBS / PBS 澳大利亚医保诊疗与药品报销数据", "Medicare Benefits Schedule / Pharmaceutical Benefits Scheme", "oceania", 4,
    [{"label":"Services Australia","url":"https://www.servicesaustralia.gov.au/"}],
    region="澳大利亚", scale="全国参保人诊疗与药品报销记录", timeSpan="持续",
    host="Services Australia（经数据保管方批准后链接获取）",
    content="MBS 为医保诊疗服务项目记录，PBS 为药品报销（含 RPBS 退役军人药品）记录；处方与服务级别粒度，可链接住院、癌症登记、死亡登记等。",
    intro="澳洲全民医保（Medicare）的行政数据，是卫生服务利用与药物流行病学研究的核心。一般不直接向研究者开放下载，需通过 PLIDA（ABS DataLab）或 CUPL（Sax Institute SURE）等受控链接途径在安全环境内申请使用。",
    usage="须经数据保管方批准，通过 PLIDA / CUPL 等受控链接途径在安全环境内分析；需伦理审批与项目付费。",
    notes="不可直接下载；须走链接与审批路径。",
    tags=["澳大利亚","医保","MBS","PBS","处方","理赔","药物流行病学","真实世界","卫生服务","受控"],
    paradigm="澳洲药物流行病学：经 PLIDA/CUPL 链接 MBS/PBS，在安全环境做用药模式、依从性与结局的目标试验模拟。",
    qr=None))

D.append(e("AIHW 澳大利亚健康与福利研究院", "Australian Institute of Health and Welfare", "oceania", 2,
    [{"label":"官网","url":"https://www.aihw.gov.au/"}],
    region="澳大利亚", scale="全国健康与福利统计", timeSpan="持续",
    host="澳大利亚健康与福利研究院（AIHW）",
    content="全国卫生与福利统计：疾病负担、医院服务、癌症、心理健康、老龄化、原住民健康、卫生支出等公开报告与数据集。",
    intro="澳洲官方卫生统计权威机构，大量指标在线免费查看/下载，适合做背景论证、国际比较与生态学分析；更细的单元记录数据需另行申请。",
    usage="公开报告与数据集免费；细粒度数据需申请/合作。",
    notes="公开层面以汇总统计为主；个体级数据需另走审批。",
    tags=["澳大利亚","官方统计","疾病负担","卫生服务","老龄化","心理健康","公开","宏观"],
    paradigm="澳洲背景与比较：用 AIHW 官方统计做疾病负担、卫生服务与支出的背景论证与跨国比较。",
    qr=None))

D.append(e("HILDA 澳大利亚家庭收入与劳动力动态调查", "Household, Income and Labour Dynamics in Australia", "oceania", 2,
    [{"label":"墨尔本研究院","url":"https://melbourneinstitute.unimelb.edu.au/hilda"}],
    region="澳大利亚", scale="全国住户面板", timeSpan="2001 至今",
    host="墨尔本大学墨尔本研究院",
    content="全国代表性住户面板：收入、就业、家庭结构、健康与福祉、生活满意度等年度随访。",
    intro="澳洲版的社会经济面板，与 CFPS/HRS 属同类设计，可用于健康的社会决定因素、卫生服务公平与政策评估。",
    usage="注册并申请数据许可后下载（通常免费/学术用途）。",
    notes="健康变量以自报为主，客观体检指标有限。",
    tags=["澳大利亚","面板","家庭","收入","就业","健康","公平","问卷","队列"],
    paradigm="澳洲健康公平：住户面板做收入/就业与健康的关系及政策评估。",
    qr=None))

D.append(e("ALSWH 澳大利亚女性健康纵向研究", "Australian Longitudinal Study on Women's Health", "oceania", 4,
    [{"label":"官网","url":"https://alswh.org.au/"}],
    region="澳大利亚", scale="多出生队列女性", timeSpan="1996 至今",
    host="澳大利亚（联邦卫生署支持）",
    content="按出生年份划分的女性队列（青年、中年、老年），长期随访健康、生活方式、医疗服务利用、心理健康与生命质量。",
    intro="澳洲女性健康研究的核心长期队列，可链接行政健康数据（MBS/PBS/住院等）。",
    usage="需提交研究方案申请并获批；可申请链接行政数据。",
    notes="仅限女性人群。",
    tags=["澳大利亚","女性","队列","纵向","健康","生活行为","心理健康","链接"],
    paradigm="澳洲女性健康：多出生队列做生命历程健康、生殖与慢病轨迹研究。",
    qr=None))

D.append(e("Ten to Men 澳大利亚男性健康纵向研究", "Australian Longitudinal Study on Male Health", "oceania", 4,
    [{"label":"官网","url":"https://tentomen.org.au/"}],
    region="澳大利亚", scale="全国男性样本", timeSpan="2013 前后至今",
    host="澳大利亚（男性健康纵向研究）",
    content="10 岁及以上男性队列，涵盖健康行为、心理健康、伤害、医疗服务利用、社会决定因素。",
    intro="澳洲男性健康研究的对应资源，弥补男性健康证据缺口。",
    usage="需申请数据访问许可。",
    notes="仅限男性人群。",
    tags=["澳大利亚","男性","队列","纵向","健康","心理健康","伤害","行为"],
    paradigm="澳洲男性健康：男性队列做健康行为、伤害与心理健康研究。",
    qr=None))

# 补充条目：北方生活方式队列（用户指定，牵头 苗玉东教授）
D.append(e("北方生活方式队列", "Northern China Lifestyle Cohort", "china_cohort", 5,
    [{"label":"以团队官方发布为准（待核）","url":"https://www.cnsda.org"}],
    region="中国北方", scale="规模待核", timeSpan="待核",
    host="苗玉东教授团队（具体依托单位与联系方式待核）",
    content="以生活方式为核心暴露的人群队列（膳食、运动、吸烟饮酒、体重与代谢等），用于慢病与生活方式关联研究。",
    intro="由苗玉东教授牵头的生活方式队列。具体依托单位、基线年份、样本量、随访周期、变量清单与申请流程本文件未能核实，请以团队官方发布与近期论文的方法学部分为准（本条标记为待核）。",
    usage="预计为合作制（参照中国本土队列通行做法：联系团队、提交研究方案、通常涉及共同署名）；具体流程待核。",
    notes="本条由用户补充，细节待核实；引用前务必核对团队官方信息。",
    tags=["中国","生活方式","膳食","运动","慢病","队列","合作","待核","北方"],
    paradigm="生活方式-慢病：以膳食/运动/吸烟饮酒等生活方式暴露为核心，做慢病风险与交互分析；需联系团队获取。",
    qr=None))

# 补充条目：SEER 美国肿瘤登记（肿瘤方向最常用的公开登记数据）
D.append(e("SEER 美国肿瘤登记", "Surveillance, Epidemiology, and End Results Program", "rwd", 3,
    [{"label":"官网","url":"https://seer.cancer.gov"},
     {"label":"申请入口（SEER*Request）","url":"https://seerdataaccess.cancer.gov"},
     {"label":"SEER-Medicare 链接数据","url":"https://healthcaredelivery.cancer.gov/seermedicare/"},
     {"label":"SEER*Stat 软件","url":"https://seer.cancer.gov/seerstat/"}],
    region="美国（部分登记处，覆盖约 48% 人口）", scale="约 1300 万+ 肿瘤病例", timeSpan="1975 至今",
    host="美国国立癌症研究所（NCI）DCCPS",
    content="基于人群的肿瘤登记：发病（部位、组织学、AJCC 分期、初治方案）、生存随访（生存时间与状态、死因）、人口学与社会经济属性；可与 Medicare 理赔、人口普查属性链接（SEER-Medicare）得到治疗与费用信息。",
    intro="肿瘤方向最主流的公开登记数据：不需自建队列即可做发病率趋势、分期-生存、治疗模式与健康差异研究；SEER*Stat 提供现成的发病率/生存率计算，出图出表极快。局限是只记录初治、无复发与后续治疗，也没有实验室指标。",
    usage="在 SEER*Request 提交研究摘要与数据使用协议（RDA），由 PI（一般要求 faculty 级）发起、机构签署，免费；审核约 2-6 周。SEER-Medicare 另需 CMS 的数据使用协议。",
    notes="①只记录首次治疗，复发/后续治疗缺失，不能做疗效比较；②无实验室与影像原始数据；③分期版本跨年份不一致（AJCC 3/6/7/8 混用）需谨慎合并；④SEER-Medicare 仅覆盖 65 岁以上医保人群，存在选择偏倚；⑤小样本亚组（罕见瘤种×县级）易被抑制。",
    tags=["美国","肿瘤","癌症登记","登记","随访","真实世界","生存分析","公开-协议","慢病"],
    paradigm="肿瘤登记范式：定义瘤种/分期队列 → 计算年龄标化发病率与 APC 趋势 → Kaplan-Meier 与 Cox 做分期-治疗-生存 → 倾向评分或 SEER-Medicare 链接校正治疗选择 → 按种族/社会经济地位做差异分析。",
    qr="monitor"))

# 补充条目：中国肿瘤登记（国家癌症中心）
D.append(e("中国肿瘤登记（NCCR 国家癌症中心）", "National Central Cancer Registry of China", "rwd", 5,
    [{"label":"国家癌症中心","url":"https://www.chinacdc.cn"},
     {"label":"《中国肿瘤登记年报》检索","url":"https://www.cnki.net"},
     {"label":"PubMed 检索 China cancer registry","url":"https://pubmed.ncbi.nlm.nih.gov/?term=China+cancer+registry+incidence+mortality"}],
    region="中国（登记处覆盖全国约四成人口）", scale="覆盖人口数亿级（逐年扩大）", timeSpan="1959 起，2008 年后规范化",
    host="国家癌症中心 / 中国医学科学院肿瘤医院",
    content="登记处上报的肿瘤发病与死亡个案（部位、组织学、分期部分可得）、随访生存（部分登记处）、地区与年龄别率；《中国肿瘤登记年报》发布汇总发病与死亡负担。",
    intro="中国肿瘤负担研究的官方口径来源：做中国癌谱、城乡差异、筛查效果评估必引。汇总数据（年报）可公开获取，个体级登记数据不开放下载，需要与国家癌症中心/地方登记处合作。",
    usage="年报与汇总统计可通过出版物/官网获取；个体级数据需向国家癌症中心或地方肿瘤登记处提交研究方案，签署合作协议并通常涉及共同署名，周期数月。",
    notes="①数据质量地区差异大（登记处成熟度不一），需报告质控指标（MV%、DCO%）；②分期与治疗字段缺失较多；③个体数据不开放，声称“下载即用”是错的；④跨年比较注意 ICD-O 版本与人口标化标准（中国标化 vs 世界标化）。",
    tags=["中国","肿瘤","癌症登记","登记","死亡登记","监测","国家级","合作","慢病"],
    paradigm="中国癌谱范式：选取质控合格登记处 → 计算中国标化/世界标化发病与死亡率 → Joinpoint/APC 趋势 → 年龄-时期-队列分解 → 与 GBD 或年报口径交叉验证。",
    qr="monitor"))

# ================= 中国可获取的数据库（2026-10 联网核实补充） =================

# 中国队列共享平台：找中国队列的「总目录」
D.append(e("CCC 中国队列共享平台", "China Cohort Consortium", "china_cohort", 4,
    [{"label":"官网","url":"http://chinacohort.bjmu.edu.cn"},
     {"label":"平台数据说明（IJE 2020）","url":"https://academic.oup.com/ije/article/49/5/1436/5899247"}],
    region="中国（覆盖各省）", scale="60+ 个队列，累计 1000 万+ 人", timeSpan="2017 年 10 月至今",
    host="北京大学公共卫生学院牵头；北京大学健康医疗大数据国家研究院、中华流行病学杂志共建",
    content="把国内已有队列的元信息做成可检索目录，分三级：①队列基本信息（公开）②字典变量 / codebook（部分公开）③原始数据（留在原队列，不在平台）。可按变量跨队列检索，再向队列方发起合作申请；2021 年起用联盟区块链记录申请与授权。",
    intro="做中国人群研究时最容易被忽略的一步：先来这里看「国内到底有哪些队列、谁手上有你要的变量」。平台不直接给数据，但它把 60 多个队列的研究对象数、基线年份、随访轮次和部分变量字典摊开，能省掉几个月的人脉摸索。",
    usage="官网注册账号后免费检索队列基本信息与部分字典变量；提合作申请需向 chinacohort@163.com 或各工作组提交研究方案（背景与意义、目的、设计、方法），由科学顾问委员会与工作组初审，再与数据方谈共享协议。周期约 1-3 个月。",
    notes="①平台是「目录 + 撮合」，不提供个体数据下载；②字典变量只对部分队列开放；③各队列变量口径不一，跨队列分析必须先做 harmonization；④合作常要求队列方作为共同作者。",
    tags=["中国","队列","目录","平台","变量","合作","慢病","国家级"],
    paradigm="跨队列合作范式：在 CCC 用变量字典筛出 2-5 个口径一致的队列 → 提合作申请 → 各队列用同一分析脚本跑 → 随机效应 meta 合并 → 报告异质性与人群差异。",
    qr="survey"))

# 广州生物库队列 GBCS
D.append(e("GBCS 广州生物库队列", "Guangzhou Biobank Cohort Study", "china_cohort", 5,
    [{"label":"官网","url":"http://gzbiobank.org"},
     {"label":"PubMed 检索 GBCS","url":"https://pubmed.ncbi.nlm.nih.gov/?term=Guangzhou+Biobank+Cohort+Study"}],
    region="中国（广州）", scale="30,430 人（≥50 岁）", timeSpan="2003-2008 基线，长期随访",
    host="广州、香港大学、英国伯明翰大学多方合作；现由粤港澳大湾区公共卫生研究协作组（GPHRC）团队维护",
    content="访谈 + 体格检查 + 空腹血样：人口学、生活方式（吸烟饮酒膳食体力活动）、职业暴露、家族史、身高体重腰围血压、血糖血脂、肝肾功能、DNA；随访健康、疾病与死亡。已发表 170+ 篇 SCI。",
    intro="国内最早以中老年人为核心的生物库队列之一，特色是职业暴露与生活方式数据做得细，血样可支撑生化和遗传分析。适合做「环境/职业暴露 → 慢病 → 死亡」这条链。",
    usage="合作制：数据由 GBCS 数据访问委员会（Data Access Committee）审批，申请邮箱 gbcsdata@hku.hk；需提交研究方案、签数据使用协议，并通常要求与队列方合作署名。",
    notes="①仅广州 ≥50 岁人群，不能直接外推全国；②死亡与发病随访依赖登记链接，失访需说明；③职业暴露变量是优势也是限制（特定行业集中）；④个体数据不公开下载。",
    tags=["中国","广东","老龄","生物样本","队列","职业","暴露","慢病","合作"],
    paradigm="职业暴露-慢病范式：以职业/环境暴露为暴露组 → 校正生活方式与社会经济 → Cox 或竞争风险模型看发病与死亡 → 按暴露剂量分层做趋势检验。",
    qr="biobank"))

# 广州出生队列 BIGCS（含 GDBIG 基因组库）
D.append(e("BIGCS 广州出生队列", "Born in Guangzhou Cohort Study", "china_cohort", 5,
    [{"label":"官网","url":"https://bigcs.com.cn"},
     {"label":"数据获取政策","url":"https://bigcs.com.cn/en_menu_d1.html"},
     {"label":"GDBIG 基因组数据库","url":"http://gdbig.bigcs.com.cn"}],
    region="中国（广州）", scale="拟 5 万孕妇及其子代；GDBIG 含 4,053 人低深度 WGS", timeSpan="2012 年起",
    host="广州市妇女儿童医疗中心 / 广州医科大学",
    content="母婴配对设计：孕期暴露（营养、环境、心理）、出生结局（早产、低出生体重）、儿童生长发育与过敏；亲子生物样本库。GDBIG 子库提供父母-子三代低深度 WGS（约 6.6×）与孕期表型，可在线做等位基因频率查询、基因型填充、GWAS meta。",
    intro="中国最具影响力的出生队列之一，强在「两代人 + 生物样本 + 基因组」三件套齐全。做生命早期暴露与跨代遗传的，这是国内少数能把链条走完的资源。",
    usage="门槛写得很明确（官网 Data Access Policy）：申请人须有博士学历或副高以上、以第一/通讯作者发表 IF>10 论文 ≥2 篇、主持过国家级项目且经费 >100 万元；须与广州市妇女儿童医疗中心建立合作项目并经其伦理委员会批准，国际合作还需科技部人类遗传资源国际合作备案；签合作协议 + 保密协议 + 数据使用协议。",
    notes="①申请资质门槛是全国最高的一档，学生个人无法申请；②个体数据禁止再分发（含测序数据与派生变量）；③区县等精细地理信息不公开；④跨境使用受《人类遗传资源管理条例》约束。",
    tags=["中国","广东","出生队列","妇幼","儿童","基因","组学","生物样本","合作"],
    paradigm="生命早期暴露范式：孕期暴露 → 出生结局 → 儿童期结局的两代链式分析；遗传部分用 GDBIG 做 PRS/基因型-表型关联与基因-环境交互（G×E）。",
    qr="biobank"))

# 中国精神卫生调查 CMHS
D.append(e("CMHS 中国精神卫生调查", "China Mental Health Survey", "monitor", 5,
    [{"label":"承担单位（北大六院）","url":"https://www.pkuh6.cn"},
     {"label":"Lancet Psychiatry 主论文","url":"https://pubmed.ncbi.nlm.nih.gov/30792114/"},
     {"label":"PubMed 检索 CMHS","url":"https://pubmed.ncbi.nlm.nih.gov/?term=China+Mental+Health+Survey"}],
    region="中国 31 省 157 个县/区", scale="32,552 人（应答率 84.3%）", timeSpan="2013-2015 年现场调查",
    host="北京大学第六医院（黄悦勤团队）牵头，联合 43 家精神专科医院与高校",
    content="7 大类 36 种精神障碍的患病率、残疾率与致残率、疾病负担、卫生服务利用及影响因素；标准化诊断访谈工具（CIDI 等）+ 多级复杂概率抽样，样本来自国家 CDC 慢病监测点。",
    intro="中国唯一具有全国代表性的精神障碍流行病学调查，任何写「中国精神障碍患病率」的论文都绕不开它。除了患病率，它的服务利用数据（多少人没就诊、就诊了有没有被识别、治疗是否充分）对卫生政策研究更有价值。",
    usage="主要结果已通过论文与官方报告公开；个体级数据不提供下载，需与北京大学第六医院团队建立合作（提交研究方案、签数据使用协议）。周期数月起。",
    notes="①横断面，只能算患病率不能算发病率；②诊断依赖访谈员培训与质控，跨研究比较要注意工具版本；③无体检与生化指标，做生物机制研究不适用；④部分病种（如进食障碍）样本量小，亚组分析效能不足。",
    tags=["中国","心理","精神","心理健康","横断面","全国","量表","合作"],
    paradigm="精神障碍负担范式：加权患病率 → 服务利用级联（是否就诊 / 是否被识别 / 是否治疗 / 治疗是否充分）→ 与社会人口因素、保险覆盖的关联 → 未满足需求测算。",
    qr="survey"))

# 国家罕见病注册系统 NRDRS
D.append(e("NRDRS 国家罕见病注册系统", "National Rare Diseases Registry System of China", "rwd", 5,
    [{"label":"官网","url":"http://www.nrdrs.org.cn"},
     {"label":"系统介绍（罕见病研究）","url":"https://jrd.pumch.cn/article/doi/10.12376/j.issn.2097-0501.2022.02.001"}],
    region="中国 29 省 104 家协作单位", scale="176 种/类罕见病、194 个队列、7.1 万例（2023-10）", timeSpan="2016 年 12 月启动",
    host="北京协和医院（依托国家重点研发计划「罕见病临床队列研究」2016YFC0901500）",
    content="人口学 + 临床病史与表型 + 检测结果 + 生物样本 + 多组学；含罕见病知识库（第一批目录 121 种疾病释义、中文版 GeneReviews、OMIM/Orphanet 链接）；支持联网抓取、单机导入、手工录入三种上报方式。",
    intro="做罕见病如果只靠自己医院几十例，审稿人一定问代表性。NRDRS 是国内唯一覆盖 100+ 家中心的国家级罕见病登记网络，单病种能凑到可用于自然史研究的样本量。",
    usage="以协作单位上报为主；研究者间共享走「群组」形式，由科研合作协议约定共享范围；公众可查病例地域分布、已注册疾病与项目周报。需先与牵头/协作单位建立合作。",
    notes="①单病种样本量仍小，随访不均衡，统计效能有限；②诊断与表型录入依赖各中心水平，需做一致性核查；③数据以协作网络内共享为主，不对外下载；④引用时注明数据来自 NRDRS 及具体协作单位。",
    tags=["中国","罕见病","登记","队列","基因","多中心","国家级","合作"],
    paradigm="罕见病自然史范式：单病种队列 → 表型聚类（聚类分析 / 潜类别）→ 基因型-表型关联 → 生存或功能结局 → 与国外登记（Orphanet / RDCRN）对照。",
    qr="monitor"))

# 全国血液净化病例信息登记 CNRDS
D.append(e("CNRDS 全国血液净化病例信息登记", "Chinese National Renal Data System", "rwd", 5,
    [{"label":"官网","url":"http://www.cnrds.net"},
     {"label":"系统简介","url":"https://www.cnrds.net/static/systemintroduction.html"}],
    region="中国", scale="6,000+ 家透析中心", timeSpan="2010 年至今（纵向登记）",
    host="中华医学会肾脏病学分会牵头，国家卫生健康委支持；肾脏病医疗质量控制中心运行",
    content="血液透析与腹膜透析患者的结构化登记：人口学、原发病、透析方式与处方、并发症、实验室指标（血红蛋白、钙磷、PTH、白蛋白、Kt/V 等）、转归（死亡 / 肾移植 / 转院）。",
    intro="中国透析人群的「官方底账」：全国 6000 多家透析中心按统一口径上报，做 ESRD 负担、透析质量达标率、中心间变异研究，这是唯一有全国覆盖的源头数据。",
    usage="面向透析中心与省级质控中心账号（工作性上报）；科研使用需经国家肾脏病质控中心 / 省级质控中心协作申请并签数据使用协议，个体数据不公开下载。",
    notes="①为质控目的采集，变量偏管理口径，缺科研专用的暴露与混杂信息；②各中心上报质量差异大，需做数据质量核查；③不能用它算发病率（只有已透析人群）；④与 CK-NET 的年度报告口径需对齐。",
    tags=["中国","肾脏","ESRD","透析","登记","质控","真实世界","合作"],
    paradigm="透析人群范式：透析起始队列 → 质量指标达标率（贫血 / 矿物质代谢 / 透析充分性）→ 生存与住院风险（Cox / 竞争风险）→ 中心间变异（多水平模型）。",
    qr="monitor"))

# 中国临床试验注册中心 ChiCTR
D.append(e("ChiCTR 中国临床试验注册中心", "Chinese Clinical Trial Registry", "trial", 1,
    [{"label":"官网","url":"https://www.chictr.org.cn"},
     {"label":"检索已注册试验","url":"https://www.chictr.org.cn/searchproj.html"}],
    region="中国 / 全球（接受各国注册）", scale="5 万+ 注册试验", timeSpan="2005 年建立，持续更新",
    host="四川大学华西医院（吴泰相、李幼平团队）；WHO 国际临床试验注册平台（ICTRP）一级注册机构",
    content="试验注册信息：注册号、题目、研究类型、设计、样本量、干预措施、主要与次要结局、伦理批件、实施单位、注册状态、结果公开状态；全部可公开检索。",
    intro="做二次研究、查发表偏倚、找未发表试验，这里是中国的入口。它同时是 WHO ICTRP 一级注册机构，注册信息会汇入全球检索。注意：注册信息不是个体数据。",
    usage="完全免费公开检索，无需注册；反向使用（自己注册试验）也免费，但需伦理批件。",
    notes="①只有注册摘要级信息，没有个体数据；②结局报告常不完整；③部分试验注册后未发表，可用来做发表偏倚与结局改换（outcome switching）研究；④中文为主，英文检索需注意译名。",
    tags=["中国","临床试验","RCT","注册","公开","二次利用","文本"],
    paradigm="注册库范式：按病种/干预检索注册试验 → 与 PubMed / 万方发表情况比对 → 计算发表率与发表偏倚 → 比对注册结局与论文结局的一致性。",
    qr="trial"))

# 药物临床试验登记与信息公示平台（NMPA/CDE）
D.append(e("药物临床试验登记与信息公示平台（NMPA）", "China Drug Trials Registry and Information Publicity Platform", "trial", 1,
    [{"label":"官网","url":"https://www.chinadrugtrials.org.cn"},
     {"label":"国家药监局药品审评中心","url":"https://www.cde.org.cn"}],
    region="中国", scale="2 万+ 登记项目", timeSpan="2012 年起（按国家局通告要求登记）",
    host="国家药品监督管理局药品审评中心（CDE）",
    content="以药品注册为目的的临床试验登记信息：登记号（CTR）、申请人、药物名称与靶点、适应症、试验分期、设计、样本量、牵头与参加机构、状态；部分项目公示结果摘要。",
    intro="看中国药物研发在做什么、在哪做、做到几期，这是最权威的官方口径。和 ChiCTR 的区别：ChiCTR 覆盖研究者发起的试验，这里覆盖申报注册的试验，两者互补。",
    usage="公开查询，无需注册、无需申请。",
    notes="①只覆盖以注册为目的的试验；②结果信息有限（多为止市摘要）；③登记号是 CTR 开头，与 ChiCTR 的 ChiCTR 号不同，引用时别混；④适应症表述以企业申报为准，需自行归并。",
    tags=["中国","临床试验","药物","注册","公开","政策","真实世界"],
    paradigm="研发格局范式：按靶点/适应症统计登记数量与分期分布 → 年度趋势 → 与 ClinicalTrials.gov 全球数据对照 → 识别同质化（扎堆）适应症。",
    qr="trial"))

# 中国家庭金融调查 CHFS
D.append(e("CHFS 中国家庭金融调查", "China Household Finance Survey", "social", 2,
    [{"label":"官网","url":"https://chfs.swufe.edu.cn"},
     {"label":"数据申请平台","url":"http://chfser.swufe.edu.cn/datas/"}],
    region="中国 29 省 269 个区县", scale="2021 年 22,027 户；2025 年 23,277 户", timeSpan="2011 年起，两年一轮，已 8 轮",
    host="西南财经大学中国家庭金融调查与研究中心",
    content="个人基本信息与就业、金融资产与非金融资产（农业、工商业、住房、土地、耐用品）、家庭负债、收入与支出、社会保障与商业保险；可算财富分布、家庭杠杆率、医疗保险覆盖与医疗支出。",
    intro="做「因病致贫」「家庭医疗支出与保险」这类卫生经济题目，CHFS 的财务口径比一般健康调查细得多。缺点是健康变量少，做临床结局不行，但做支付能力、灾难性卫生支出的分母很好用。",
    usage="官网数据平台实名注册 → 填写研究计划与身份材料 → 审核通过后免费获取（在线使用，不得转让或转借账号）；部分年份需按公告窗口申请。",
    notes="①金融口径强、健康与临床变量弱；②区县代码原则上不公开，做地理分析受限；③跨轮变量有调整（2019 版曾对收入/消费/资产做重算），跨年比较要先核对；④与 CHARLS 样本不重叠，不能直接合并。",
    tags=["中国","家庭","收入","财富","保险","医疗支出","灾难性卫生支出","卫生经济","面板","问卷","公开"],
    paradigm="家庭经济-健康范式：医疗支出占家庭消费比 → 灾难性卫生支出（10%/25% 阈值）→ 保险覆盖与共付比例的关联 → 因病致贫/致富的转移矩阵分析。",
    qr="survey"))


# PBICR 补充更详实的检索入口
for d in D:
    if d["name"].startswith("PBICR"):
        d["intro"] = ("PBICR（Psychology and Behavior Investigation of Chinese Residents）中国居民心理与行为调查，"
            "全国性重复横断面调查，2021 年起开展，以第七次全国人口普查为基础的配额抽样结合多阶段分层，覆盖 31 个省级行政区。"
            "它真正的卖点是量表密度极高，是国内变量最丰富的心理行为类调查之一；一个数据集可支撑几十个不同选题，出稿速度快。")
        d["notes"] = ("横断面为主、因果推断能力弱；全自报，无客观体检与生化指标，做慢病结局完全不行；"
            "同源方差与共同方法偏倚突出；配额抽样属非概率抽样，勿直接声称全国代表性；产出同质化、撞题概率大。")
        d["urls"] = [{"label":"CNSDA 中国国家调查数据库（检索 PBICR）","url":"http://www.cnsda.org"},
                     {"label":"PubMed 检索 PBICR 相关研究","url":"https://pubmed.ncbi.nlm.nih.gov/?term=PBICR"}]

# 经典指标（主要/经典变量）——依据 PDF 明确记载整理，未记载者留空由页面提示查 codebook
IND = {
 "CCC 中国队列共享平台":"队列级元信息（研究对象数、基线年份、随访轮次、变量字典/问卷）；跨队列可检索的共性变量（人口学、生活方式、体检生化、慢病结局）；原始个体数据留在各队列、不在平台",
 "GBCS 广州生物库队列":"职业暴露（工种/粉尘/化学物/噪声）、生活方式（吸烟饮酒膳食体力活动）、家族史、身高体重腰围血压、空腹血糖血脂、肝肾功能、血常规、DNA；随访疾病与死亡",
 "BIGCS 广州出生队列":"孕期暴露（营养/环境/心理）、出生结局（早产、低出生体重）、儿童生长发育与过敏；亲子低深度 WGS（约 6.6×）/SNP、等位基因频率、基因型填充、GWAS meta",
 "CMHS 中国精神卫生调查":"心境障碍、焦虑障碍、酒精药物使用障碍、间歇爆发性障碍、进食障碍、精神分裂症谱系、老年期痴呆；残疾率与致残率、服务利用（就诊/识别/治疗/充分治疗）、治疗延迟",
 "NRDRS 国家罕见病注册系统":"病种与发病年龄、基因变异、临床表型与量表、治疗与用药、生物样本、随访结局；另含罕见病知识库（121 种目录释义、中文版 GeneReviews、OMIM/Orphanet 链接）",
 "CNRDS 全国血液净化病例信息登记":"透析起始时间、原发病、透析方式与频次、Kt/V、血红蛋白、钙磷、PTH、白蛋白、住院、死亡与肾移植转归",
 "ChiCTR 中国临床试验注册中心":"注册号、研究类型、样本量、干预措施、主要/次要结局、伦理批件、注册时间、结果公开状态",
 "药物临床试验登记与信息公示平台（NMPA）":"登记号(CTR)、药物名称与靶点、适应症、试验分期、设计、样本量、牵头与参加机构、状态",
 "CHFS 中国家庭金融调查":"家庭总收入/消费/资产/负债、金融资产结构、社会保障与商业保险、医疗支出、就业与自雇、住房与土地",
 "SEER 美国肿瘤登记":"原发部位与组织学（ICD-O-3）、AJCC 分期（T/N/M/总期）、诊断时年龄与性别、种族/族裔、初治方案（手术/放疗/化疗，仅首程）、生存时间与生存状态、死因、随访月数、登记处与县属性；SEER-Medicare 另含理赔、处方与费用",
 "中国肿瘤登记（NCCR 国家癌症中心）":"发病与死亡个案（部位、组织学、诊断日期、年龄性别）、部分登记处的分期与随访生存、地区别与年龄别发病率/死亡率、中国标化率与世界标化率；年报另含 5 年生存率抽查结果",
 "HRS 健康与退休研究":"健康与功能、认知、就业与退休、收入财富、家庭代际支持、医疗支出与保险；RAND HRS 纵向文件；生物标志物（干血斑/唾液，2006 起隔轮采集）",
 "CHARLS 中国健康与养老追踪调查":"血肌酐、胱抑素C、尿素氮、尿酸、糖化血红蛋白、血脂、CRP、实测血压（可算 eGFR）；认知与抑郁量表、医疗服务利用与支出、养老保险",
 "CLHLS 中国老年健康影响因素跟踪调查":"日常生活活动能力(ADL/IADL)、认知、心理健康、临终照护回顾问卷、死亡随访；超高龄与百岁老人过采样",
 "CFPS 中国家庭追踪调查":"自评健康、慢病自报、医疗支出、医保类型、CES-D 心理量表；部分轮次身高体重血压；家庭/成人/少儿/社区四层匹配",
 "CHNS 中国健康与营养调查":"连续 3 天 24 小时膳食回顾、家庭食物称重盘存、血压、身高体重腰围；2009 年空腹血多项生化",
 "UK Biobank 英国生物样本库":"血液尿液生化约 30 余项（肌酐、胱抑素C、尿微量白蛋白、尿肌酐→可算 eGFR 与 UACR）、全基因组分型、WGS、Olink 蛋白组、Nightingale 代谢组、多模态影像、加速度计；NHS 住院/癌登/死亡链接",
 "CKB 中国慢性病前瞻性研究":"基因分型约 10 万人，另含测序、代谢组、蛋白组子集；结局经疾病监测点、医保理赔、死因登记链接",
 "开滦队列":"标准化血压、身高体重腰围、空腹血糖、血脂四项、血肌酐、尿酸、超敏CRP、肝肾功能、血常规、尿常规、心电图；亚组含颈动脉超声、baPWV/ABI、脑核磁、认知",
 "同济东风队列":"职业暴露史（工种/粉尘/噪声/金属/化学品）、血压、人体测量、心电图、颈动脉超声、肺功能；空腹血与 DNA 及基因分型；医保与死因链接结局",
 "PBICR 中国居民心理与行为调查":"PHQ-9、GAD-7、PSS 感知压力、UCLA 孤独、PSQI 睡眠、HPLP-II 健康促进生活方式、FHS-SF 家庭健康、健康素养与 eHEALS、EQ-5D、社会支持/社会资本/医患信任、就医行为",
 "NHANES 美国国家健康与营养检查调查":"标准化血肌酐、部分周期胱抑素C、尿白蛋白肌酐比(UACR)、多次标准化血压测量、处方药文件中的降压药使用；国家死亡索引链接随访",
 "香港医管局 CDARS":"住院诊断 ICD-9-CM、基层门诊 ICPC-2、处方与配药记录、实验室检验值（含肌酐序列）、影像与手术操作、急诊与住院、死亡链接",
 "韩国 NHIS 国民健康保险":"法定定期国民健康体检（血压、空腹血糖、血肌酐、尿蛋白定性）+ 理赔与处方记录；NHIS-NSC 全国代表性抽样队列",
 "MIMIC-IV 重症监护数据库":"hosp 模块（实验室、处方、ICD-9/10 诊断、微生物学）、icu 模块（生命体征、给药事件、出入量、评分）、MIMIC-IV-ED、MIMIC-IV-Note 临床文本、MIMIC-IV-ECG 波形、MIMIC-CXR 影像",
 "BioLINCC 美国心肺血研究所数据仓库":"SPRINT/ALLHAT/AASK/ACCORD 等试验的血压、eGFR 序列、ESRD 与心血管结局；ARIC、MESA、CARDIA、Framingham、CHS、JHS 队列变量",
 "NIDDK-CR 美国糖尿病消化肾病研究所中央数据仓库":"CRIC：eGFR 斜率、蛋白尿、终末期肾病、心血管结局与死亡；CKiD 儿童 CKD；DCCT/EDIC 1 型糖尿病",
 "NIA AgingResearchBiobank 美国老龄研究样本库":"步速、肌少症、骨密度、炎症因子系列等精细老年表型",
 "GEO 基因表达综合数据库":"芯片、RNA-seq、单细胞、甲基化、ChIP-seq 表达矩阵与临床表型（GSE/GSM/GPL 三级结构）",
 "HCUP 美国医疗成本与利用项目":"诊断与操作编码、住院日、住院总费用、付费方、转归、医院特征（教学属性、床位规模、地区、所有制）；NRD 再入院数据库",
 "MEPS 美国医疗支出面板调查":"家庭医疗服务使用、支出、支付来源、保险状态（与机构/雇主问卷交叉验证）",
 "GBD / GHDx 全球疾病负担":"DALY、YLL、YLD，可按国家/省份/年龄/性别/年份查询",
 "China-PAR 中国动脉粥样硬化性心血管病风险预测":"China-PAR 10 年及终生 ASCVD 风险模型变量（年龄、血压、血脂、吸烟、糖尿病等易获取指标）",
 "C-STRIDE 中国慢性肾脏病队列":"eGFR、蛋白尿、CKD 进展终点（数千例 CKD 患者前瞻随访）",
 "中国高血压调查 CHS":"高血压患病率、知晓率、治疗率、控制率",
 "CK-NET 中国肾脏疾病网络":"全国医保与住院数据的肾脏疾病指标；年度报告可直接作为论文中国背景引用源",
 "CNSR 中国国家卒中登记":"卒中登记信息、III 期含生物标志物与影像",
 "CMEC 中国西南多民族队列":"民族（藏、彝、苗、白、侗等）、高原环境暴露、体检与生化指标",
 "上海女性/男性健康研究 SWHS/SMHS":"膳食问卷、体格测量、肿瘤随访（女性 40-70 岁 / 男性 40-74 岁配对设计）",
 "GDC / TCGA / cBioPortal 癌症多组学":"突变、基因表达、甲基化、拷贝数及配套临床信息",
 "泰州队列":"完善生物样本库（血液/DNA 等）、肿瘤与代谢方向指标（具体变量清单以团队/官网说明为准）",
 "ELSA 英格兰老龄化追踪调查":"与 HRS 高度对标的健康、认知、就业退休、收入财富变量，并含客观体检",
 "SHARE 欧洲健康、老龄与退休调查":"欧洲多国统一编码的健康、认知、退休与经济状况变量",
 "dbGaP 基因型与表型数据库":"受控访问的基因型与表型数据（需机构签署与 DAC 评审）",
}

# 代表性 / 里程碑文献（均建议以官网 Publications 页核对）
PAPERS = {
 "CCC 中国队列共享平台":["Wang L, et al. Data Resource Profile: China Cohort Consortium (CCC). Int J Epidemiol. 2020;49(5):1436（平台架构与三级数据共享规则）","建议同步访问 chinacohort.bjmu.edu.cn 查看最新队列列表"],
 "CMHS 中国精神卫生调查":["Huang Y, Wang Y, Wang H, et al. Prevalence of mental disorders in China: a cross-sectional epidemiological study. Lancet Psychiatry. 2019;6(3):211-224（主结果论文）","建议 PubMed 检索 “China Mental Health Survey” 核对后续服务利用与疾病负担论文"],
 "GBCS 广州生物库队列":["Jiang C, Thomas GN, Lam TH, et al. Cohort profile: The Guangzhou Biobank Cohort Study, a Guangzhou-Hong Kong-Birmingham collaboration. Int J Epidemiol. 2006;35(4):844-852","建议 PubMed 检索 “Guangzhou Biobank Cohort Study” 核对最新成果（已发表 170+ 篇）"],
 "BIGCS 广州出生队列":["Qiu X, Lu JH, He JR, et al. The Born in Guangzhou Cohort Study (BIGCS). Eur J Epidemiol. 2017;32(4):337-346","GDBIG 基因组平台论文（2025, Genomics Proteomics Bioinformatics, PMID 40372478）"],
 "SEER 美国肿瘤登记":["National Cancer Institute. SEER Cancer Statistics Review（历年版本，官网可下载）","Duggan MA, et al. The Surveillance, Epidemiology, and End Results (SEER) Program and Pathology: Toward Strengthening the Critical Relationship. Am J Surg Pathol. 2016（SEER 数据与病理字段说明）","建议 PubMed 检索 “SEER database” 核对目标瘤种的最新研究"],
 "中国肿瘤登记（NCCR 国家癌症中心）":["国家癌症中心.《中国肿瘤登记年报》（年度出版物，引用时注明年份与登记处覆盖人口）","Zheng RS, et al. Cancer incidence and mortality in China（年度统计论文，发表于 Journal of the National Cancer Center）"],
 "BioLINCC 美国心肺血研究所数据仓库":["SPRINT 强化降压试验（NEJM 2015，收缩压目标 120 vs 140，含完整肾脏结局与 eGFR 序列）","ALLHAT 四类降压药头对头试验（JAMA 2002，4 万余人，含终末期肾病结局）","AASK 非裔高血压性肾硬化试验（JAMA 2002）"],
 "UK Biobank 英国生物样本库":["Sudlow C, et al. UK Biobank: An Open Access Resource for Identifying the Causes of Disease. PLoS Med. 2015（队列描述）","建议同步查阅官网 Publications 页按年份检索最新成果"],
 "CHARLS 中国健康与养老追踪调查":["Zhao Y, et al. Cohort profile: the China Health and Retirement Longitudinal Study (CHARLS). Int J Epidemiol. 2014","建议以 CHARLS 官网与 PubMed 检索 “CHARLS” 核对最新论文"],
 "CKB 中国慢性病前瞻性研究":["Chen Z, et al. China Kadoorie Biobank of 0.5 million people: survey methods, baseline characteristics and long-term follow-up. Int J Epidemiol. 2011","CKB 官网 Publications 页有完整成果列表"],
 "MIMIC-IV 重症监护数据库":["Johnson A, et al. MIMIC-IV, a freely accessible electronic health record dataset. Sci Data. 2023","PhysioNet 官网提供完整的 MIMIC 相关文献列表"],
 "开滦队列":["开滦研究团队在心血管与肾病方向的系列论文（建议 PubMed 检索 “Kailuan Study” 核对）","团队论文方法学部分含队列注册号"],
 "NIDDK-CR 美国糖尿病消化肾病研究所中央数据仓库":["CRIC 研究（慢性肾功能不全队列）系列论文，为 CKD 进展预测模型的国际验证基准"],
 "NHANES 美国国家健康与营养检查调查":["CDC/NCHS 官方《NHANES 分析指南与权重说明》为必读方法学文件","PubMed 检索 “NHANES” 可查海量已发表研究"],
 "CLHLS 中国老年健康影响因素跟踪调查":["曾毅教授团队关于中国长寿、失能轨迹与临终照护的系列研究"],
 "GEO 基因表达综合数据库":["以各 GSE 数据集对应的原始发表论文为准（每条 GSE 记录均附 PubMed 链接）"],
}

for d in D:
    d["indicators"] = IND.get(d["name"], "")
    d["papers"] = PAPERS.get(d["name"], [])
    d["pubmed"] = "https://pubmed.ncbi.nlm.nih.gov/?term=" + \
        (d["en"].replace(" ", "+") if d["en"] else d["name"])

# 论文致谢 / 数据可用性声明模板（[XXXXX] 为批准/项目编号占位）
ACK_SPECIAL = {
 "SEER 美国肿瘤登记":(
   "This study used the SEER [22/18/17] registries database, released [Month Year], based on the "
   "[November Year] submission. The interpretation of these data is solely that of the authors and "
   "does not necessarily endorse the views of the SEER registries or the National Cancer Institute.",
   "本研究使用 SEER（[22/18/17] 个登记处）数据库（[年份] 发布版，基于 [年份] [月份] 提交数据）。"
   "本文对数据的解读仅代表作者本人观点，不代表 SEER 登记处或美国国立癌症研究所的立场。"),
 "中国肿瘤登记（NCCR 国家癌症中心）":(
   "The cancer registry data used in this study were provided by the National Central Cancer Registry "
   "of China (NCCR) / National Cancer Center, under data use agreement [XXXXX]. The authors thank the "
   "contributing population-based cancer registries.",
   "本研究使用的肿瘤登记数据由国家癌症中心（NCCR）提供，数据使用协议编号 [XXXXX]。"
   "感谢各以人群为基础的肿瘤登记处（各登记点）的数据上报与质控工作。"),
 "UK Biobank 英国生物样本库":(
   "This research has been conducted using the UK Biobank Resource under Application Number [XXXXX].",
   "本研究使用英国生物样本库（UK Biobank）资源开展，批准申请编号为 [XXXXX]。"),
 "MIMIC-IV 重症监护数据库":(
   "This research used the MIMIC-IV database (version [X.X]), maintained by the MIT Laboratory for "
   "Computational Physiology and hosted on PhysioNet, accessed under approved credentialed access "
   "(certification number [XXXXX]).",
   "本研究使用 MIMIC-IV 数据库（版本 [X.X]，由 MIT 实验计算生理学实验室维护、PhysioNet 托管），"
   "经凭证化访问批准后使用（证书编号 [XXXXX]）。"),
 "dbGaP 基因型与表型数据库":(
   "Data used in this study were obtained from the database of Genotypes and Phenotypes (dbGaP) "
   "under accession [phsXXXXXX], with approved project number [XXXXX].",
   "本研究数据来源于 dbGaP（基因型与表型数据库），数据集编号 [phsXXXXXX]，批准项目编号 [XXXXX]。"),
 "NHANES 美国国家健康与营养检查调查":(
   "Data from the National Health and Nutrition Examination Survey (NHANES), US Centers for Disease "
   "Control and Prevention / National Center for Health Statistics, were used in this study. "
   "NCHS does not endorse or assume responsibility for the analyses or interpretations presented here.",
   "本研究使用了美国疾控中心国家卫生统计中心（CDC/NCHS）的 NHANES 数据；NCHS 不对本研究的分析与解读背书或担责。"),
 "CHARLS 中国健康与养老追踪调查":(
   "This research uses data from the China Health and Retirement Longitudinal Study (CHARLS), "
   "conducted by Peking University, under data use approval [XXXXX].",
   "本研究使用了北京大学中国健康与养老追踪调查（CHARLS）数据，数据使用批准号 [XXXXX]。"),
 "CKB 中国慢性病前瞻性研究":(
   "This research used data from the China Kadoorie Biobank (CKB) under approved project / "
   "collaboration number [XXXXX].",
   "本研究使用了中国慢性病前瞻性研究（CKB）数据，批准项目/合作编号 [XXXXX]。"),
 "GEO 基因表达综合数据库":(
   "Publicly available datasets (GSE accession number [GSEXXXXX]) were obtained from the NCBI Gene "
   "Expression Omnibus (GEO).",
   "本研究数据来源于 NCBI GEO 公共数据集（GSE 编号 [GSEXXXXX]）。"),
}
for d in D:
    sp = ACK_SPECIAL.get(d["name"])
    if sp:
        d["ackEn"], d["ackCn"] = sp[0], sp[1]
    else:
        en = d["en"] or d["name"]
        d["ackEn"] = ("This research used data from %s. Data access was granted under approved "
                      "application / project number [XXXXX] (or through a collaboration agreement "
                      "with the data custodian)." % en)
        d["ackCn"] = ("本研究使用了 %s 的数据；数据获取经申请批准，批准/项目编号为 [XXXXX]"
                      "（或通过与数据持有方的合作协议获得）。" % d["name"])

# ============ 内容加厚：申请步骤统一升级 + 重点库补充介绍/指标 ============
GEN_USAGE = {
 1: "无需申请：在官网直接检索/下载（部分需注册免费账号）。使用时遵守数据许可（如 CC0 / CC-BY），论文中须引用数据来源；高度受限变量需另行申请。",
 2: "在官网注册免费账号并说明研究用途后即可下载。建议先下载官方 codebook / Data Dictionary 核对变量名与年份；部分受限变量或链接数据需另签协议。",
 3: "完成指定培训（如 CITI「Data or Specimens Only Research」）取得证书，签署数据使用协议（DUA/SDUA）后获取。审批通常数天至数周，免费；数据多在安全环境或授权账号内分析。",
 4: "提交研究计划/数据申请并签署协议，部分需付费、机构审批与数据保管方（custodian）批准，周期约 1-6 个月。按获批的变量字段范围提供数据；受控数据还需 DAC/伦理评审。",
 5: "不公开下载，走合作制：需联系数据持有团队、提交研究方案、签署合作协议，通常涉及共同署名；周期半年起。个体级数据须在合作框架与伦理批件下获取。",
}
GEN_IND = {
 "aging": "健康与功能、认知与心理、就业退休与收入、家庭与代际、医疗支出与保险（类别级概述，具体变量见官方 codebook）",
 "social": "自评健康、慢病自报、医疗支出与医保、社会态度与家庭结构（类别级概述，具体变量见 codebook）",
 "biobank": "基线问卷、体格测量、血液生化、基因组/多组学，以及与登记或医保链接的结局变量（详见官网 Showcase / codebook）",
 "china_cohort": "体检与生化、生活方式与职业暴露、基因/生物样本，及医保或死因链接的结局（详见团队论文方法学与数据说明）",
 "monitor": "问卷、体检、实验室指标与死亡链接（详见官方 codebook 与权重说明）",
 "rwd": "诊断与操作编码、处方/配药、检验值、就诊与住院、死亡登记（详见数据字典）",
 "oceania": "调查问卷、体检与生化、与 MBS/PBS/住院/癌症/死亡登记的链接变量（详见 Data Dictionary）",
 "icu": "生命体征、实验室检验、用药与操作、严重度评分、住院与转归（详见数据字典）",
 "trial": "试验/队列原始变量：暴露、结局、协变量与随访时间（详见各研究 codebook）",
 "omics": "原始数据、表达/变异矩阵与元数据、临床表型注释（详见数据集说明）",
 "cn_platform": "平台汇交的数据与指标、元数据描述（详见平台数据说明）",
 "healthecon": "费用、服务利用、支付方、结局与宏观指标（详见数据字典 / 官方统计口径）",
}
# 重点库：更详实的介绍 / 申请方式 / 指标
OVR = {
 "ELSA 英格兰老龄化追踪调查": dict(
   intro="英格兰 50 岁及以上人群的老龄化追踪研究，1998 年起多轮随访，设计上与美国 HRS 高度对标，因此可与 HRS/CHARLS/SHARE 做统一编码的跨国比较（推荐用 g2aging 调和数据集）。除问卷外含客观体检、护士访视与生物样本，是欧洲老龄研究中体检模块较完整的一个。",
   usage=None, indicators="健康与功能、认知、心理健康、就业与退休、收入与财富、社会参与；客观体检（血压、人体测量、体成分、肺功能等）与生物样本"),
 "SHARE 欧洲健康、老龄与退休调查": dict(
   intro="覆盖欧洲 28 国的跨国老龄面板（2004 年起），样本量与国别覆盖在欧洲最大，是欧洲跨国比较的默认数据源。变量经统一编码（含健康、认知、经济、社会网络），并可与部分国家的行政登记链接；跨国比较建议直接用 Harmonized SHARE。",
   indicators="健康与功能、认知、抑郁(CES-D/Euro-D)、就业退休、收入财富、社会网络与代际支持；部分国家含体检与生物样本"),
 "LASI 印度纵向老龄化调查": dict(
   intro="印度全国代表性老龄面板（2017-2019 基线，样本 7 万以上），是研究发展中大国老龄化、慢病与家庭照料的关键资源，可与 HRS 家族做统一编码比较。含认知、功能、健康行为与生物标志物子样本。",
   indicators="健康与功能、认知、慢病自报、健康行为、家庭与经济状况；部分子样本含血压、人体测量与生物标志物"),
 "CLASS 中国老年社会追踪调查": dict(
   intro="中国人民大学中国调查与数据中心主办的 60 岁及以上老年社会调查（2014 年基线，约 1.1 万人，两年一轮）。相比 CHARLS 更聚焦老年社会照料、养老服务需求、社区养老资源与代际支持，服务利用变量粒度更细，最贴合卫生管理与养老服务体系研究。",
   indicators="ADL/IADL、慢病自报、养老服务需求与利用、社区养老资源、代际支持、经济状况；客观体检指标有限"),
 "CGSS 中国综合社会调查": dict(
   intro="中国人民大学中国调查与数据中心主办的全国性综合社会调查（2003 年起），是中国最早的综合社会调查。健康模块不深，但价值观、社会公平感、阶层认同、医患信任等变量独一份，适合就医体验、健康公平感知与卫生政策社会基础研究。",
   indicators="自评健康、就医行为与医患信任、社会公平感、阶层认同、社会保障参与；以自报为主"),
 "All of Us 美国全民健康研究": dict(
   intro="美国 NIH 的全民健康研究计划，目标招募百万人，强调少数族裔与 underrepresented 人群代表性。数据类型包括电子病历、问卷、可穿戴设备、体检与生物样本（基因组、代谢组）。研究者通过 Researcher Workbench 云端环境在受控层级下分析，无需下载原始数据。",
   usage="注册研究者账号（需机构邮箱与身份核验）→ 完成研究用途声明与数据使用协议 → 在 Researcher Workbench 云端分析。分层数据（Public/Registered/Controlled）权限不同，Controlled 层需额外审批。免费。",
   indicators="电子病历（诊断/用药/检验）、问卷（健康、生活方式、社会决定因素）、可穿戴（活动/心率）、基因组与代谢组、体检"),
 "FinnGen 芬兰基因组计划": dict(
   intro="芬兰国家級基因组计划，约 50 万人，将基因型与全国健康登记（住院、处方、死亡等）链接，形成高质量的表型-基因关联资源。GWAS 汇总统计在官网公开，可直接下载用于荟萃分析；个体级数据需向 FinnGen/THL 申请。",
   usage="GWAS 汇总统计在官网公开下载；个体级数据需提交研究申请并经 FinnGen/THL 审批，部分需在芬兰安全环境分析。",
   indicators="基因型/全基因组、全国登记表型（诊断、处方、住院、死亡）、GWAS 汇总统计（含 AF、beta、SE、P）"),
 "BioBank Japan 日本生物样本库": dict(
   intro="日本大型生物样本库（约 27 万人，涵盖 12 类疾病），是东亚人群 GWAS 与疾病遗传学的重要来源，与欧美队列联合可做跨族裔比较。以 DNA 与临床信息为主。",
   usage="通过 BioBank Japan / 理化学研究所（RIKEN）提交研究申请，说明研究目的与所需数据，经审批后获取（多为合作或受控方式）。",
   indicators="DNA/基因型、疾病诊断（12 类疾病）、临床基本信息；GWAS 汇总统计"),
 "Million Veteran Program 百万退伍军人计划": dict(
   intro="美国退伍军人事务部（VA）的百万级队列，以男性为主，整合基因组、电子病历与问卷，是研究男性健康、药物基因组学与创伤后应激等的重要资源。数据在 VA 受控环境中分析。",
   usage="需通过 VA 研究审批（ORD）与数据使用协议，在 VA 安全环境内分析；一般需美方合作者。",
   indicators="基因组、电子病历（诊断/用药/检验）、问卷（暴露、心理健康、生活方式）"),
 "Estonian Biobank 爱沙尼亚生物样本库": dict(
   intro="爱沙尼亚全国性生物样本库，约 20 万人（覆盖全国约 20% 成年人口），基因型与全国电子健康记录链接，是国家级精准医学与药物基因组学的代表性资源。",
   usage="向爱沙尼亚塔尔图大学生物样本库提交研究申请，经伦理与数据审批后在受控环境分析；部分数据需合作。",
   indicators="基因型/全基因组、电子健康记录（诊断、处方、检验）、问卷与体检"),
 "KoGES 韩国基因组流行病学研究": dict(
   intro="韩国国立保健研究院主导的基因组流行病学研究，含城市、农村、Ansan-Ansung 等多个子队列，合计 20 余万人，有基因组与长期随访。做慢病遗传与基因-环境交互用 KoGES；做社会经济与老龄化用 KLoSA；做卫生服务与药物流行病学用 NHIS。",
   usage=None, indicators="基因型、体检与生化（血糖、血脂、血压、肝肾功能）、生活方式问卷、随访结局"),
 "CMEC 中国西南多民族队列": dict(
   intro="四川大学华西公共卫生学院牵头的大型多民族队列（云贵川渝藏，近 10 万人，2018 年前后起），覆盖藏、彝、苗、白、侗等民族，是研究民族健康差异与高原环境健康的唯一大型资源。",
   indicators="民族与人口学、生活方式、体检与生化、高原环境暴露；生物样本"),
 "泰州队列": dict(
   intro="复旦大学在江苏泰州建立的区域人群队列，生物样本库较完善，主要面向肿瘤与代谢方向研究。具体基线年份与样本量以团队公开论文为准（本页标注十万量级，待核）。",
   indicators="问卷与生活方式、体检与生化、生物样本；肿瘤与代谢相关指标（以团队数据说明为准）"),
 "上海女性/男性健康研究 SWHS/SMHS": dict(
   intro="上海市疾控与范德堡大学合作的上海女性健康研究（74,942 名 40-70 岁女性）与上海男性健康研究（61,480 名 40-74 岁男性），采用配对设计，随访极长，是膳食与肿瘤研究的经典东亚队列。",
   indicators="膳食问卷（食物频率）、生活方式、生殖与激素因素、体格测量；肿瘤发病与死亡随访"),
 "CNSR 中国国家卒中登记": dict(
   intro="北京天坛医院王拥军团队牵头中国国家卒中登记（CNSR），I 期约 2.2 万、III 期约 1.5 万例，III 期含生物标志物与影像，是卒中方向国内最强、可用于预后与医疗质量评价的登记数据。",
   indicators="卒中类型与严重度（NIHSS）、影像、生物标志物、治疗与转归（mRS）、院内结局"),
 "C-STRIDE 中国慢性肾脏病队列": dict(
   intro="北京大学第一医院牵头的中国慢性肾脏病（CKD）前瞻队列，纳入数千例 CKD 患者，密集随访 eGFR、蛋白尿与肾脏终点，是中国最重要的 CKD 进展研究资源。",
   indicators="eGFR 与 eGFR 斜率、蛋白尿（UACR/24h）、血压、CKD 进展与 ESRD、心血管事件与死亡"),
 "CK-NET 中国肾脏疾病网络": dict(
   intro="北京大学第一医院牵头、基于全国医保与住院数据的肾脏疾病网络，发布年度《中国肾脏疾病年度科学报告》，是论文中国背景、疾病负担与医疗利用的权威引用源。",
   indicators="CKD/ESRD 患病与治疗（透析、移植）、住院与费用、地区差异；年度报告指标"),
 "中国高血压调查 CHS": dict(
   intro="中国医学科学院阜外医院开展的大规模高血压流行病学调查，是中国高血压患病率、知晓率、治疗率、控制率的权威来源，常用于论文背景与政策论证。",
   indicators="血压测量、患病率、知晓率、治疗率、控制率；地区与人群分层"),
 "KNHANES 韩国国民健康营养调查": dict(
   intro="韩国疾病管理厅（KDCA）的全国健康与营养调查，设计对标美国 NHANES，自 1998 年起每年开展约万人规模，含问卷、体检与实验室检查，可公开下载（韩文界面为主），适合与 NHANES 做跨国比较。",
   indicators="血压、身高体重腰围、空腹血糖、血脂、肝肾功能、血常规；膳食与健康行为问卷"),
 "BRFSS 行为危险因素监测系统": dict(
   intro="美国 CDC 的年度电话健康调查，全球规模最大的行为危险因素监测，每年数十万人、具州级代表性，适合健康行为、慢病筛查与健康公平的州际比较。",
   indicators="吸烟/饮酒、体力活动、饮食、体重、慢病自报、健康筛查利用、自评健康"),
 "NHIS 美国国民健康访问调查": dict(
   intro="美国 CDC/NCHS 的全国健康访谈调查，样本量大、无体检，与 NHANES 互补，适合医疗服务利用、保险覆盖与健康可及性研究。",
   indicators="自报健康状况与慢病、医疗服务利用、保险类型与覆盖、就医障碍、健康行为"),
 "中国慢性病及危险因素监测": dict(
   intro="中国疾控中心慢病中心主办的全国慢性病与危险因素监测，是中国代表性最好的慢病监测数据，含吸烟、饮酒、膳食、体力活动、血压血糖等，但不公开下载，需合作获取。",
   usage=None, indicators="吸烟/饮酒/膳食/体力活动、血压、血糖、血脂、身高体重腰围、慢病患病自报"),
 "韩国 HIRA 健康保险审查评价院": dict(
   intro="韩国健康保险审查评价院（HIRA）掌握全国理赔审核数据，处方级粒度，与 NHIS 互补，适合药物流行病学、用药模式与医疗利用研究。需本地合作，在指定分析中心操作。",
   indicators="诊断编码、处方与配药（药品名/剂量/天数）、门诊与住院、医疗费用"),
 "CPRD 英国基层医疗数据库": dict(
   intro="英国临床实践研究数据链（CPRD），含 GOLD 与 Aurum 两个库，累计逾 6000 万患者，可链接 HES 住院、ONS 死亡与癌症登记，是药物流行病学的国际金标准。",
   indicators="基层就诊与诊断（Read code）、处方、检验值、转诊；链接住院(HES)、死亡(ONS)、癌症登记"),
 "OpenSAFELY 英国全民健康记录分析平台": dict(
   intro="OpenSAFELY 是英国 NHS 的可信分析平台，研究者的分析代码在安全环境中运行、全流程开源，透明度是行业标杆，适合大规模观察性研究与快速政策评估。",
   usage="提交分析代码与研究申请，经审批后在 OpenSAFELY 安全环境运行；代码与结果可复现、公开。",
   indicators="NHS 电子病历（诊断、处方、检验、就诊）、死亡登记；通过可复现代码提取"),
 "QResearch 英国基层医疗数据库": dict(
   intro="QResearch 是英国大型基层医疗数据库（牛津托管），是 QRISK 系列心血管风险模型的数据来源，适合风险预测模型的开发与外部验证。",
   indicators="基层诊断与处方、检验（血压、血脂、血糖、肌酐）、BMI、吸烟；结局与死亡链接"),
 "北欧登记体系": dict(
   intro="丹麦、瑞典、挪威、芬兰的全民登记体系，用唯一个人编号贯穿出生到死亡，随访完整度全球第一，是因果推断与药物安全的天然实验场。通常需本地 PI 与合作。",
   indicators="诊断（ICD）、处方、住院、死亡、出生与移民；可与生物样本库和队列链接"),
 "台湾 NHIRD 全民健康保险研究数据库": dict(
   intro="台湾全民健康保险研究数据库（NHIRD），覆盖全民、1995 年起，现由卫生福利部资料科学中心管理。曾在真实世界研究中产出极多，近年需现场分析、门槛提高。",
   indicators="诊断（ICD-9/10）、处方与用药、住院与门诊、手术操作、费用"),
 "日本 NDB / JMDC": dict(
   intro="日本 NDB 为全国医保理赔数据（覆盖广、粒度细），JMDC 为商业保险理赔数据并含体检信息。两者互补，适合药物流行病学与卫生服务研究，需日方合作。",
   indicators="诊断、处方、诊疗行为、住院；JMDC 另含体检（血压、血糖、血脂、BMI）"),
 "TriNetX 全球联邦式研究网络": dict(
   intro="TriNetX 是连接数百家医疗机构的联邦式研究网络，可在几分钟内产出队列计数与倾向性评分匹配结果，适合快速筛选研究问题与可行性评估。局限是看不到原始病历，数据质量取决于各机构映射。",
   usage="机构订阅制：由所属机构开通账号后，在平台内在线查询与做倾向性评分匹配；不提供原始病历下载。",
   indicators="诊断、用药、检验、手术、就诊；以标准化术语映射后的计数与分布为主"),
 "MarketScan / Optum / IQVIA 美国商保数据": dict(
   intro="美国商业保险理赔数据（MarketScan、Optum、IQVIA 等），规模千万至亿级，是真实世界证据（RWE）、药物利用与卫生经济评价的常用商业数据源，价格昂贵，药企与咨询公司常用。",
   usage="商业授权：按项目或年度订阅购买，签署数据使用协议后在指定环境分析，费用较高。",
   indicators="诊断与操作编码、处方与配药、住院与门诊、费用与支付方；部分含实验室结果"),
 "CMS Medicare/Medicaid (ResDAC)": dict(
   intro="美国 CMS 的 Medicare（老年/残障）与 Medicaid（低收入）全国医保数据，经 ResDAC 申请并付费获取；与 SEER 链接后即为 SEER-Medicare，是老年肿瘤与卫生服务研究的权威数据源。",
   usage="经 ResDAC 提交申请、签署数据使用协议并付费，审批数周；数据在受控环境使用。",
   indicators="诊断与操作（ICD）、处方(Part D)、住院与门诊、费用与支付、机构特征；链接 SEER 可得肿瘤分期与治疗"),
 "eICU-CRD 重症数据库": dict(
   intro="美国多中心重症监护数据库（200 余家医院），弥补 MIMIC 单中心缺陷。做多中心外部验证时，MIMIC-IV 训练 + eICU 外部验证是目前审稿接受度最高的搭配。",
   indicators="生命体征、实验室、用药与输液、APACHE IV 评分、诊断与转归；多中心异质性可用于外部验证"),
 "AmsterdamUMCdb 重症数据库": dict(
   intro="欧洲首个大型开放 ICU 数据库（荷兰阿姆斯特丹大学医学中心），可作欧洲人群的外部验证集，弥补 MIMIC/eICU 以美国人群为主的局限。",
   indicators="生命体征、实验室、用药、通气与评分；欧洲人群表型"),
 "HiRID 高分辨率重症数据库": dict(
   intro="瑞士伯尔尼的高时间分辨率 ICU 数据库（部分变量可达 2 分钟级），适合生理信号处理、早期预警模型与高分辨率时序分析。",
   indicators="高频生命体征与血流动力学、实验室、用药；2 分钟级时间序列"),
 "SICdb 萨尔茨堡重症数据库": dict(
   intro="奥地利萨尔茨堡较新的开放 ICU 数据集，可作为额外的欧洲外部验证集，补充 MIMIC/eICU/AmsterdamUMCdb 的人群与机构多样性。",
   indicators="生命体征、实验室、用药、评分与转归"),
 "INSPIRE 韩国围手术期数据库": dict(
   intro="韩国围手术期重症数据库，以亚洲人群为主，适合围手术期结局、术后并发症与预测模型研究，是亚洲 ICU 外部验证的补充资源。",
   indicators="围手术期生命体征、麻醉与用药、实验室、术后并发症与转归"),
 "PIC 浙江大学附属儿童医院重症数据库": dict(
   intro="浙江大学医学院附属儿童医院的儿科重症数据库，是中国唯一同类开放库，适合儿童重症预测模型、儿科 AKI/ARDS 等研究及外部验证。",
   indicators="儿童生命体征、实验室、用药与通气、评分、转归；儿科特异表型"),
 "Vivli / YODA / CSDR 临床试验个体数据共享平台": dict(
   intro="临床试验个体水平数据（IPD）共享平台：Vivli 汇集多方试验（做 IPD meta 分析首选）、YODA 由耶鲁托管强生等企业试验、CSDR 汇集 GSK 等药企数据（参与企业近年有变动）。适合个体数据荟萃、亚组与异质性分析。",
   indicators="试验个体数据：随机分组、暴露与剂量、主要/次要结局、协变量、随访时间"),
 "dryad": dict(),
 "SRA 序列读取归档": dict(
   intro="NCBI 的 Sequence Read Archive（SRA），归档高通量测序原始数据（fastq），常与 GEO/GDC 配合使用；可公开下载并重新比对分析。",
   indicators="测序原始 reads、样本元数据、平台与文库信息"),
 "ArrayExpress / BioStudies": dict(
   intro="EMBL-EBI 的功能基因组数据仓储（ArrayExpress 及后续 BioStudies），是欧洲版的功能基因组资源，与 NCBI GEO 互为补充。",
   indicators="表达矩阵、样本与平台注释、实验设计元数据"),
 "Zenodo / figshare / Mendeley Data": dict(
   intro="通用数据与代码仓储：Zenodo（CERN）、figshare、Mendeley Data（Elsevier 系期刊常用），论文附带的代码、数据集与补充材料常存放于此，可直接下载复用。",
   indicators="论文配套数据集、分析代码、补充材料与元数据"),
 "ICPSR / IPUMS 调查与微观数据仓储": dict(
   intro="ICPSR 是密歇根大学的社会科学数据总仓库，很多老龄与社会调查在此二次分发；IPUMS 提供全球普查与调查微观数据的调和版本（含 IPUMS Health Surveys），便于跨国与跨年比较。",
   indicators="调查微观数据（人口、健康、经济、家庭）、普查样本；IPUMS 提供统一编码的调和变量"),
 "国家自然科学基金基础研究知识库": dict(
   intro="国家自然科学基金资助论文的全文知识库（非数据集），作者按规定存缴。可用于免费获取部分付费墙后的中英文全文，也能反向检索某学者、某基金号的全部产出，写标书、判断方向资助密度很好用。",
   usage="公开访问：在官网按作者、机构、基金号或关键词检索，直接下载可获取的全文。",
   indicators="论文全文与元数据（作者、机构、基金号、期刊、年份）"),
 "NGDC 国家基因组科学数据中心": dict(
   intro="国家基因组科学数据中心（CNCB-NGDC），下设 GSA（测序数据归档，中国版 SRA）与 OMIX（组学数据），以及 Aging Atlas 等专题资源。建议先在 Database Commons 检索该体系下的资源，再定向进入具体平台。",
   indicators="测序原始数据、组学矩阵、样本与实验元数据；专题资源（如衰老多组学）"),
 "ScienceDB 科学数据银行": dict(
   intro="中国科学院主办的通用数据仓储（中国版 Dryad），支持论文数据存缴与共享，可公开检索与下载，适合获取已发表研究配套的数据与代码。",
   indicators="论文配套数据集、代码与元数据"),
 "NMDC 国家微生物科学数据中心": dict(
   intro="国家微生物科学数据中心，汇聚微生物与微生物组学数据，是微生物组、病原与感染研究的国家级资源。",
   indicators="微生物基因组、微生物组测序、样本元数据"),
 "国家/卫生健康统计年鉴": dict(
   intro="国家统计局与国家卫健委发布的年度统计年鉴，提供卫生资源、服务量、费用等宏观指标，常用于论文背景、生态学分析与政策论证。",
   usage="官方出版物/官网公开：直接查阅或下载年鉴表格；按年度与地区口径引用。",
   indicators="卫生机构与床位、卫生人员、诊疗人次、住院与费用、卫生总费用、期望寿命等宏观指标"),
 "MEPS 美国医疗支出面板调查": dict(
   intro="美国医疗支出面板调查（MEPS），两年期面板设计、免费公开，记录家庭医疗服务使用、支出、支付来源与保险状态，并与医疗机构与雇主问卷交叉验证。适合灾难性卫生支出、自付比例与保险效应研究。",
   indicators="医疗服务使用、总支出与自付、支付来源、保险状态、健康与功能、收入"),
 "GBD / GHDx 全球疾病负担": dict(
   intro="全球疾病负担研究（GBD，IHME），提供按国家、省份、年龄、性别、年份的 DALY、YLL、YLD 等指标，是论文背景与政策论证的必备引用源。",
   usage="完全公开：在 GHDx 网站按指标/地区/年份查询并下载结果表。",
   indicators="DALY、YLL、YLD、患病率、发病率、死亡率、危险因素归因负担"),
 "WHO 全球卫生观察站 / 卫生支出 / OECD / 世界银行": dict(
   intro="全球宏观卫生指标集合：WHO 全球卫生观察站（GHO）官方指标库、WHO 全球卫生支出数据库（各国卫生总费用构成）、OECD Health Statistics（发达国家卫生系统比较）、世界银行开放数据（宏观社会经济与卫生）、CDC WONDER（美国死亡与出生）。适合卫生系统与筹资的跨国比较。",
   usage="完全公开：在各自官网按指标查询/下载；注意各平台口径与年份差异。",
   indicators="卫生总费用与构成、期望寿命、死亡率、疾病负担、卫生资源、社会经济指标"),
 "45 and Up Study 澳大利亚 45 岁以上人群队列": dict(
   intro="澳大利亚规模最大的健康与老龄化持续研究（Sax Institute 管理），2005-2009 年在新南威尔士州招募逾 26.7 万名 45 岁及以上人群，应答率约 19%。参与者均同意将调查数据与 MBS（医保诊疗）、PBS（药品）、住院、癌症登记等行政数据链接；含生物样本与地理空间数据，并可开发子研究。数据经 SURE 安全环境访问。",
   indicators="问卷（健康行为、慢病、心理困扰、生命质量、家庭与照护）；链接 MBS/PBS/住院/癌症/死亡登记；体格与生物样本；地理空间"),
 "CUPL 慢性疾病伞式数据链接项目": dict(
   intro="CUPL 让研究者用一次审批同时获得 45 and Up 调查数据与 10 类行政健康数据（MBS、PBS、NSW 住院、出生死亡婚姻登记、死因、急诊、癌症登记、精神健康、传染病报告含 COVID），相比逐个保管方申请可将等待时间缩短至多 80%（一年以上→约 2-3 个月）。数据经 SURE 安全环境提供。",
   indicators="调查变量 + MBS 诊疗、PBS 药品、住院(APDC)、急诊(EDDC)、癌症登记(CCR)、死亡登记、精神健康(CHAMB)、传染病(NCIMS)"),
 "PLIDA 澳大利亚个人级整合数据资产（ABS DataLab）": dict(
   intro="澳大利亚统计局（ABS）的个人级整合数据资产（前身 MADIP），用 Person Linkage Spine 链接健康、教育、政府支付、收入与税收、就业与人口普查等数据，覆盖全国人口、跨年份纵向。获批研究者通过 PLIDA Modular Product 在 ABS DataLab 内按需逐模块申请并分析，数据不可带出。",
   indicators="健康模块、MBS 模块、收入与税收、教育、家庭与住户、残障、移民、社会支持、人口普查"),
 "MBS / PBS 澳大利亚医保诊疗与药品报销数据": dict(
   intro="MBS（Medicare Benefits Schedule）记录医保诊疗服务项目，PBS（Pharmaceutical Benefits Scheme，含 RPBS 退役军人药品）记录药品报销，均为处方/服务级粒度，是澳洲卫生服务利用与药物流行病学的核心。一般不直接开放下载，须经 PLIDA（ABS DataLab）或 CUPL（SURE）等受控链接途径在安全环境内使用。",
   indicators="MBS：服务项目、就诊日期、提供者类型、费用与报销；PBS：药品、剂量、数量、日期、费用；可链接住院/癌症/死亡"),
 "AIHW 澳大利亚健康与福利研究院": dict(
   intro="澳大利亚健康与福利研究院（AIHW）是官方卫生统计权威机构，发布疾病负担、医院服务、癌症、心理健康、老龄化、原住民健康与卫生支出等报告与数据集，多数可在官网免费查看/下载，适合背景论证、国际比较与生态学分析；个体级数据需另行申请。",
   indicators="疾病负担、住院与服务量、癌症发病率与生存、心理健康、老龄化、卫生支出、原住民健康等汇总指标"),
 "HILDA 澳大利亚家庭收入与劳动力动态调查": dict(
   intro="墨尔本大学墨尔本研究院的全国住户面板（2001 年起），年度随访收入、就业、家庭结构、健康与福祉、生活满意度，是澳洲版的社会经济面板，适合健康的社会决定因素、卫生服务公平与政策评估。",
   indicators="收入与财富、就业与工时、家庭结构与照料、健康与自评健康、心理健康(SF-36/MCS)、生活满意度"),
 "ALSWH 澳大利亚女性健康纵向研究": dict(
   intro="澳大利亚女性健康纵向研究（ALSWH），按出生年份分为青年、中年、老年多个队列，1996 年起长期随访健康、生活方式、医疗服务利用、心理健康与生命质量，可申请链接 MBS/PBS/住院等行政数据。",
   indicators="健康与慢病、生殖与激素、生活方式、心理健康、医疗服务利用、生命质量；可链接行政数据"),
 "Ten to Men 澳大利亚男性健康纵向研究": dict(
   intro="澳大利亚男性健康纵向研究（Ten to Men），覆盖 10 岁及以上男性，随访健康行为、心理健康、伤害、医疗服务利用与社会决定因素，弥补男性健康证据缺口。",
   indicators="健康行为、心理健康、伤害与暴力、医疗服务利用、社会决定因素、就业与教育"),
}
for nm, fields in OVR.items():
    if not fields: continue
    for d in D:
        if d["name"] == nm:
            for k, v in fields.items():
                if v: d[k] = v
            break

# 少数库的申请流程补成分步骤
USAGE_FIX = {
 "UK Biobank 英国生物样本库": "四步：① 在 Showcase 免账号浏览全部变量与分布；② 注册 AMS，提交约 2000 字研究计划（含机构 PI 与合作者信息）；③ 审批通过后按获批字段范围付费并签署数据使用协议；④ 在 UKB-RAP（基于 DNAnexus 的云平台）分析，另计算力与存储费用，结果需回传。周期约 1-6 个月。",
 "CKB 中国慢性病前瞻性研究": "分层开放：① 先在 Open Access 层获取汇总数据与部分个体数据（较快）；② 深度数据需在线提交研究申请、说明科学问题与所需变量；③ 经 CKB 科学委员会与伦理审批，通常需与 CKB 团队合作并共同署名；④ 获批后在受控环境分析。周期 1-6 个月。",
 "MCPS 墨西哥城前瞻性研究": "研究申请入口以牛津大学临床试验服务部（CTSU）官方发布为准（本条入口待核）：一般需提交研究方案、经数据持有方与伦理审批，并与团队合作；具体流程与费用请以官网/CTSU 说明为准。",
 "KoGES 韩国基因组流行病学研究": "向韩国国立保健研究院（KDCA）提交研究申请，说明研究目的与所需子队列/变量，经审批后获取；英文入口与具体流程以官网为准（本条待核），通常需韩方合作。",
 "同济东风队列": "校内与机构间合作制：① 联系华中科技大学同济医学院公共卫生学院相关团队；② 提交研究方案与所需变量；③ 签署合作协议并办理伦理审批；④ 在合作框架内分析，通常涉及共同署名。本院系引荐通常只需几次沟通。",
 "PBICR 中国居民心理与行为调查": "通过项目组申请：① 取得项目组联系方式（见近期 PBICR 论文的数据可用性声明/致谢）；② 提交研究方案与所需量表/变量；③ 经审核后按合作署名模式获取数据。具体流程与周期以项目组说明为准（待核）。",
 "泰州队列": "合作制：① 联系复旦大学公共卫生学院相关团队；② 提交研究方案与变量需求；③ 经伦理与团队审批后，在合作框架内使用生物样本与数据，通常涉及共同署名。具体流程以团队说明为准。",
 "中国高血压调查 CHS": "以官方报告与团队合作为主：① 引用已发布的患病率/知晓率/治疗率/控制率报告；② 需要个体级数据时联系阜外医院团队，提交研究方案并走合作与伦理流程。",
}
for d in D:
    if d["name"] in USAGE_FIX:
        d["usage"] = USAGE_FIX[d["name"]]

# ---------------------------------------------------------------------------
# 核心内容 / 常见坑补厚（针对内容偏薄的条目，逐条写实）
# ---------------------------------------------------------------------------
CONTENT_FIX = {
 # —— HRS 家族 ——
 "MHAS 墨西哥健康与老龄化研究":
   "50 岁及以上全国代表性样本，2001 年起多轮追踪，与美国 HRS 高度可比（同属 Gateway 调和体系）。核心模块：人口学与迁移史（含赴美移民经历、汇款、家庭分离）、健康与慢病、认知（Mex-Cog 专项含详细神经心理测验）、功能与失能、就业与养老金、收入与消费、医疗服务利用。部分轮次采集干血斑（血脂、糖化血红蛋白、CRP 等）与人体测量。",
 "ELSA 英格兰老龄化追踪调查":
   "50 岁及以上英格兰代表性样本，2002 年起每 2 年一轮（核心成员同属 HRS 国际家族）。每轮含面对面访谈 + 护士上门客观体检：血压、身高体重腰围、握力、肺功能、平衡与步速、血液生化与 DNA；认知测验（记忆、执行功能、言语流畅）、心理健康、社会参与、就业与财富、照料。可与 HES 住院、ONS 死亡登记链接。",
 "SHARE 欧洲健康、老龄与退休调查":
   "覆盖 20 余个欧洲国家的 50 岁及以上人群，2004 年起每 2 年一轮，样本量在全球老龄面板中居首。核心：健康与慢病、认知与抑郁（EURO-D）、功能与失能、就业与退休、养老金与财富、家庭与社会网络、医疗服务使用；部分国家含加速计、干血斑、基因子样本。跨国可比性是其最大价值（问卷与变量经统一调和）。",
 "LASI 印度纵向老龄化调查":
   "45 岁及以上全国代表性样本（含各邦分层），2017-2019 年首轮，与 HRS 体系可比。核心：人口学与种姓/宗教、健康与慢病、认知（LASI-DAD 提供更详细认知与痴呆评估）、功能与 ADL/IADL、就业与养老金、家庭结构与代际转移、医疗支出；部分子样本含血压、人体测量、干血斑与认知专项。",
 # —— 生物样本库 ——
 "MCPS 墨西哥城前瞻性研究":
   "墨西哥城两个城区约 15 万成年居民（1998-2004 年入组），基线问卷 + 体格测量 + 血样（含 DNA、生化、血脂），迄今随访 20 余年，通过死亡登记与死因编码获取结局。核心：生活方式（吸烟/饮酒/膳食/体力活动）、疾病史、社会经济状况；适合做肥胖-糖尿病-肾病-肿瘤的长期关联与孟德尔随机化。",
 "All of Us 美国全民健康研究":
   "目标百万人的全国性队列，刻意 oversample 少数族裔与历史上被排除的人群。核心：年度健康问卷（环境暴露、生活方式、家族史、医疗可及性）、EHR 链接（诊断、用药、检验、就诊）、可穿戴设备（Fitbit 心率/步数/睡眠）、体格测量、全基因组测序与数组分型；数据经 Researcher Workbench（云端）访问，配套 notebook 与常用表型算法。",
 "FinnGen 芬兰基因组计划":
   "整合芬兰全国生物样本库与国家登记（出生、住院、门诊、处方、死亡、癌症）的基因-表型资源，样本量达数十万。核心：全基因组分型与插补、精细表型（ICD 与药物购买记录构建的端点）、GWAS 汇总统计全量公开下载；适合做新药靶点验证、共病遗传相关、芬兰人群（遗传隔离、 founder 效应）特有变异研究。",
 "BioBank Japan 日本生物样本库":
   "由全国数十家合作医院招募、以患者为基础的生物样本库（约 20 万例，覆盖 47 类疾病），采集 DNA、血清与临床信息。核心：疾病诊断、检验、用药、随访生存；产出大量东亚人群 GWAS（如 2 型糖尿病、冠心病、肾病、肿瘤），是东亚与欧洲人群遗传效应差异比较的关键数据源。",
 "Million Veteran Program 百万退伍军人计划":
   "美国退伍军人事务部（VA）大型队列，目标百万、已完成数十万基因分型。核心：全基因组数据 + VA 电子病历（就诊、用药、检验、住院）+ 问卷（暴露史、军事服务、生活方式、PTSD/抑郁）；可通过 VA 数据访问申请，很多分析在 MVP 专用云环境完成。",
 "Estonian Biobank 爱沙尼亚生物样本库":
   "覆盖约 20% 成年人口的全国性生物样本库（约 20 万人）。核心：基因分型/全基因组/全外显子、代谢组、问卷与体检；与爱沙尼亚国家登记（医保理赔、处方、癌症、死亡）全面链接，可做长随访；向研究者开放申请，部分结果是「返回参与者」的基因组风险报告。",
 # —— 中国队列 ——
 "China-PAR 中国动脉粥样硬化性心血管病风险预测":
   "整合 China-MUCA、InterASIA、CIMIC 等多个中国前瞻队列（合计十余万人、随访十余年），产出 China-PAR 10 年与终生 ASCVD 风险预测模型，已被中国指南采纳。核心：血压、血脂、血糖、BMI、吸烟、家族史、地域（南北方差异）；可用于风险模型外部验证、危险因素归因与人群分层。",
 "China PEACE / 百万人群项目":
   "两条主线：① China PEACE 百万人群项目——35-75 岁社区居民心血管高危筛查与干预（血压、血脂、血糖、BMI、吸烟、用药），随访心血管事件；② China PEACE 回顾性研究——按两阶段随机抽样抽取全国代表性住院病历（急性心梗、心衰、冠脉造影/PCI），做医疗质量与结局评价。核心：医疗质量指标（再灌注时间、指南用药）、结局（院内死亡、再入院）、费用。",
 "CMEC 中国西南多民族队列":
   "依托四川大学华西公共卫生学院，在西南多民族地区（藏、彝、苗、白、侗等）建立的社区队列。核心：民族与遗传背景、高原/低氧环境暴露、膳食与生活方式、慢病（高血压、糖尿病、痛风、慢性肾病）、生物样本；适合研究民族间疾病谱差异、高原适应与基因-环境交互。",
 "泰州队列":
   "复旦大学与泰州市人民医院合作建立的 20 万人级社区队列（江苏泰州），基线含问卷、体格测量与生物样本（血、尿），并与当地医保/住院与肿瘤登记链接随访。核心：生活方式与膳食、慢病（高血压/糖尿病/CKD）、肿瘤发病与死亡、生物标志物；样本库规模在国内地市级队列中居前。",
 "上海女性/男性健康研究 SWHS/SMHS":
   "上海市区 1997-2000 年招募的女性约 7.5 万、男性约 6 万，迄今随访 20 余年。核心：详细膳食频率问卷（含大豆异黄酮等特色暴露）、生活方式、生育与激素史（女性）、职业与环境暴露、体格测量与血尿样本；结局通过肿瘤登记、死亡登记与出院记录捕获。适合做营养-肿瘤、内源性激素-乳腺癌/子宫内膜癌、代谢-肝癌等长期关联。",
 "C-STRIDE 中国慢性肾脏病队列":
   "由北京大学第一医院牵头、全国数十家中心参与的中国慢性肾脏病前瞻队列，入组 CKD 1-4 期患者数千例。核心：基线 eGFR、尿蛋白/白蛋白肌酐比、血压、合并症与用药、肾脏病理（部分中心）、生物样本；随访肾功能进展（eGFR 斜率、ESRD/透析）、心血管事件与死亡。是国内做 CKD 进展与风险预测最核心的数据源。",
 "CK-NET 中国肾脏疾病网络":
   "由北京大学肾脏病研究所牵头，整合国家监管性数据库（血液净化登记、透析登记）、医保给付数据与区域医疗平台，产出《中国肾脏疾病年度科学报告》。核心：CKD 与 ESRD 患病率、透析模式与充分性、住院与费用、心血管并发症；内嵌 C-STRIDE、INDEED 等子队列，可做宏观政策与个体风险两层分析。",
 "中国高血压调查 CHS":
   "2012-2015 年开展的全国代表性横断面调查（分层多阶段随机抽样，覆盖 30 余省、约 45 万人）。核心：三次血压测量、身高体重腰围、血脂血糖、 smoking/饮酒、用药与知晓情况；是引用中国高血压患病率、知晓率、治疗率、控制率（「三率」）的权威来源，也可做省级/城乡/民族分层比较。",
 "中国慢性病及危险因素监测":
   "中国 CDC 自 2004 年起每 3 年一轮的全国监测系统（2018 年起覆盖全部县区），每轮约 18 万人。核心：问卷（吸烟、饮酒、膳食、体力活动、慢病史）、体格测量（血压、身高体重腰围）、血液生化（血糖、血脂、肌酐、尿酸、血红蛋白）；是国家级慢病危险因素与主要慢病患病率的官方口径数据。",
 # —— 监测 / 公开 ——
 "BRFSS 行为危险因素监测系统":
   "美国各州电话（含手机）健康调查，每年完成 40 万份以上访谈，是全美最大的连续健康调查。核心：吸烟/电子烟、饮酒、体力活动、膳食、体重、慢病（糖尿病、高血压、哮喘、肿瘤史）、心理健康与睡眠、疫苗与筛查服务利用、医疗可及性；样本量足以做州级甚至都会区估计，适合健康公平与小地区分析。",
 "NHIS 美国国民健康访问调查":
   "美国 CDC 每年入户访谈约 3-4 万户家庭，样本量远大于 NHANES 但无体检与生物样本。核心：健康状况与功能、慢病诊断、医疗可及性与延误、保险类型与覆盖、医疗服务使用与自付、儿童与家庭模块；适合做服务利用、保险政策、健康不平等的年度趋势分析，可与 NHANES 互补（一个重问卷一个重体检）。",
 # —— 真实世界 ——
 "韩国 NHIS 国民健康保险":
   "单一支付方全民医保的理赔与健康检查数据。核心：全部诊疗与处方记录（诊断 ICD-10、手术、药品、费用）、法定定期体检（血压、空腹血糖、血脂、肌酐、尿蛋白、身高体重、影像/内镜筛查）、以及 NHIS-NSC 全国代表性抽样队列（约百万，随访十余年）；可与死亡登记、癌症登记链接。是做亚洲人群目标试验模拟（target trial emulation）与药物流行病学的首选。",
 "韩国 HIRA 健康保险审查评价院":
   "韩国健康保险审查评价院掌握的全国理赔审核数据，覆盖几乎所有医疗机构与参保人。核心：处方级用药（成分、剂量、天数）、诊疗行为、诊断、机构与地区信息、费用；可按样本队列（如 2-3% 抽样）或专项主题（如罕见病、癌症、老年）申请，用于药物安全与利用研究。",
 "CPRD 英国基层医疗数据库":
   "英国全科诊所电子病历（GOLD 与 Aurum 两套，合计数百家至上千家诊所、千万级患者，代表性覆盖约 10% 英国人口）。核心：诊断（Read/Snomed 编码）、处方（含剂量与频次）、检验结果、体格测量、转诊与专科信件、吸烟饮酒等生活方式；可链接 HES 住院、ONS 死亡、癌症登记与 IMD 剥夺指数。",
 "OpenSAFELY 英国全民健康记录分析平台":
   "覆盖英格兰约 99% 注册人口的初级保健记录（TPP 与 EMIS 系统），特点是「代码移动到数据、人不移动数据」：分析代码在 NHS 安全环境内运行，只输出汇总结果，全部分析代码事后公开。核心：诊断、处方、检验、疫苗、住院与死亡链接；COVID-19 期间产出多项高影响力研究，是透明可复现真实世界研究的范本。",
 "QResearch 英国基层医疗数据库":
   "由牛津大学与 EMIS 系统合作建立的初级保健数据库（上千家诊所、千万级患者），与死亡、癌症、住院数据链接。核心：诊断、处方、检验、体格测量与生活方式；QRISK2/QRISK3 心血管风险模型即基于该库开发，适合做风险预测模型开发与验证、药物长期安全性。",
 "北欧登记体系":
   "丹麦、瑞典、挪威、芬兰、冰岛五国的全国性登记体系。核心：以个人唯一编号贯通出生、住院与门诊（ICD 编码）、处方（ATC 编码）、癌症、死因、教育/收入/家庭等行政登记；随访完整度接近 100%、几乎无失访，是做药物流行病学、家族遗传风险、生命历程研究的「金标准」环境，多数需本国机构合作与伦理批准。",
 "台湾 NHIRD 全民健康保险研究数据库":
   "台湾地区全民健康保险（覆盖率 99% 以上）的申报数据，由卫生福利部资料科学中心管理。核心：就诊与住院诊断（ICD-9/10）、处方与费用、手术与检查、机构与地区；另有抽样百万归人档、特定主题数据库（如癌症、罕见病、精神疾病）；目前以「现场分析、不可携出」为原则，需通过中心申请与伦理审核。",
 "日本 NDB / JMDC":
   "两条数据线：① NDB——日本全国医保理赔（特定健诊、处方、诊疗行为），由厚生劳动省管理，需申请且多需在指定环境分析；② JMDC——商业化的健保组合理赔 + 体检数据（血压、血糖、血脂、肝肾功能、BMI），覆盖数百万投保人与家属，英文变量文档较完善。适合做日本人群药物利用、慢病进展与费用分析。",
 "MarketScan / Optum / IQVIA 美国商保数据":
   "美国商业保险理赔数据库集群：MarketScan（Merative）覆盖数千万至亿级人年的雇员与家属理赔；Optum Clinformatics 覆盖约数千万投保人，含住院/门诊/药房与部分检验值；IQVIA PharMetrics/LRx 兼有理赔与处方。核心：诊断、手术、处方、费用、就诊场所与时间；缺检验值、无社会行为变量、人群偏年轻在职是其通病。",
 "CMS Medicare/Medicaid (ResDAC)":
   "美国联邦医保（65 岁以上、ESRD、残疾）与低收入医疗补助的理赔与管理数据，经 ResDAC 申请获取。核心：住院、门诊、专业护理、家庭健康、处方药（Part D）、费用与共病；与 SEER 链接即 SEER-Medicare（肿瘤研究最常用组合），与 NDI 链接可得死因。适合老年人群真实世界疗效、费用与医疗利用研究。",
 # —— 重症 ——
 "eICU-CRD 重症数据库":
   "美国 200 余家医院 ICU 的多中心协作数据库（约 20 万次入住），含人口学、APACHE IV 生理与评分、诊断、护理记录、用药、补液与通气、实验室与结局。核心价值是弥补 MIMIC 单中心的局限，做外部验证与多中心异质性分析；时间分辨率为分钟级护理记录但无波形。",
 "HiRID 高分辨率重症数据库":
   "瑞士伯尔尼 Inselspital 的单中心重症数据库，数万次 ICU 入住，时间分辨率可达 1-2 分钟。核心：连续生命体征（心率、血压、SpO2、呼吸参数、通气设置）、输液与血管活性药物、实验室、评分与结局；适合做早期预警、液体复苏策略、机械通气动态与强化学习，也可作为高频时间序列算法的基准数据。",
 "INSPIRE 韩国围手术期数据库":
   "韩国首尔大学医院的围手术期数据库（数万例手术），覆盖术前评估、术中事件与用药、麻醉方式、术后并发症与 30 天结局。核心：麻醉与手术相关变量细（麻醉类型、气道管理、液体与血管活性药、术中低血压）、检验与合并症；是亚洲人群围手术期风险模型与术中低血压研究的重要开放资源。",
 "PIC 浙江大学附属儿童医院重症数据库":
   "浙江大学医学院附属儿童医院 PICU 的开放数据库（万余次入住），是中国唯一对外开放的儿科重症数据。核心：人口学与入院诊断、生命体征、实验室、用药与干预（机械通气、CRRT、ECMO）、评分与结局；儿科变量编码与成人库不同，需用其专用字典，样本为单中心三级医院、病情偏重。",
 # —— 公开仓储 ——
 "Dryad 通用数据仓储":
   "非营利通用数据仓储，主要托管已发表论文的底层原始数据（生态、进化、临床与社会科学均有）。核心：数据集可下载 CSV/Excel/R 脚本，附论文 DOI 与许可信息；多为 CC0，少量 CC-BY；不做变量标准化，字段含义须回原文核对。",
 "SRA 序列读取归档":
   "NCBI 的测序原始数据归档（Sequence Read Archive），收录全球论文的 FASTQ/BAM 原始读段与部分处理后数据。核心：可按物种、研究、样本、平台检索，支持云端（S3/GCP）直取；受控人类数据（dbGaP 授权）不在此公开；下载体积动辄数十 GB 至 TB，需先估存储与算力。",
 "ArrayExpress / BioStudies":
   "EMBL-EBI 维护的功能基因组数据仓储（现与 BioStudies 合并入口）。核心：芯片与测序的表达数据、处理后矩阵与元数据，多数可直接下载；欧洲版 GEO，变量注释常需自行整理，做整合分析要注意平台批次。",
 "Zenodo / figshare / Mendeley Data":
   "三个通用研究产物仓储：Zenodo（CERN，支持代码与数据、可发 DOI）、figshare（通用，界面友好）、Mendeley Data（Elsevier 系期刊常用）。核心：论文配套代码、清洗后数据、补充材料；许可以 CC0/CC-BY 为主，质量参差，复用前须看 README 与版本。",
 "ICPSR / IPUMS 调查与微观数据仓储":
   "ICPSR 是社会科学数据总仓库（许多老龄与社会调查在此二次分发，部分需会员机构身份）；IPUMS 提供全球普查与调查微观数据的调和版本（IPUMS USA/International/Health Surveys），变量名与编码跨国家跨年份统一。核心：人口学、教育、就业、收入、健康与保险；是做跨国比较与长期趋势最省清洗成本的选择。",
 # —— 中国平台 ——
 "NGDC 国家基因组科学数据中心":
   "中国科学院北京基因组研究所（国家生物信息中心）建设的国家级组学数据平台。核心：GSA（Genome Sequence Archive，测序原始数据）、GVM（变异）、OMIX（组学表达）、GEN（组学数据库目录）；对应国际的 SRA/GEO 角色，中国境内测序数据按规定应在此汇交，是查中国人群组学原始数据的首选。",
 "ScienceDB 科学数据银行":
   "中国科学院建设的通用科学数据仓储（可发 DOI）。核心：论文配套数据、AI 训练集、地学与生物医学数据；支持公开/受限/ embargo 多种发布方式，适合作为国内投稿的「数据可用性」落地仓库。",
 "NMDC 国家微生物科学数据中心":
   "中国科学院微生物研究所牵头建设的国家级微生物数据平台。核心：微生物基因组、微生物组（16S/宏基因组）、菌种资源与相关元数据；适合做人体/环境微生物组数据的中国来源检索与汇交。",
 "国家/卫生健康统计年鉴":
   "国家统计局《中国统计年鉴》与国家卫健委《中国卫生健康统计年鉴》的公开数据。核心：医疗卫生机构与床位数、卫生人员、诊疗人次与入院人数、卫生总费用与人均费用、期望寿命、婴儿与孕产妇死亡率、按疾病别两周就诊率与住院率；颗粒度为全国/省级，适合做生态学分析、政策背景与分母估算。",
 # —— 卫生经济 ——
 "MEPS 美国医疗支出面板调查":
   "美国卫生与公众服务部（AHRQ）的连续面板调查，同一批家庭两年内多轮访谈，每年约 3 万户。核心：医疗服务使用（就诊、住院、急诊、处方）、支出与支付来源（自付/商保/Medicare/Medicaid）、保险状态与转换、健康与功能、收入与就业；机构与雇主问卷用于交叉核验，是研究美国医疗费用与保险政策的核心微观数据。",
 "GBD / GHDx 全球疾病负担":
   "华盛顿大学 IHME 主导的全球疾病负担研究，GHDx 为其数据目录与下载门户。核心：按国家/地区/年龄/性别/年份的死亡、发病、患病、DALY/YLL/YLD、危险因素归因（含中国省级估计）；另有医疗支出、卫生人力等配套数据；模型估计值，引用须注明 GBD 版本与 IHME 来源。",
 # —— 第二批补厚 ——
 "CFPS 中国家庭追踪调查":
   "北京大学中国社会科学调查中心（ISSS）主持的全国性、综合性、长期跟踪调查，2010 年基线，覆盖 25 个省级单位、约 1.5 万户家庭及其全部成员。核心：家庭经济（收入、消费、资产、债务）、成员教育、健康与医疗支出、就业与婚姻、少儿发展与认知、主观态度；家户-个人-少儿三套问卷，可做家庭内部与代际分析。",
 "CLASS 中国老年社会追踪调查":
   "中国人民大学中国调查与数据中心主持的全国性老年社会调查，2014 年基线，覆盖 60 岁及以上老年人及其家庭。核心：社会经济地位、健康状况与慢性病、养老金与医疗保险、照料需求与提供、社会参与与数字使用、居住安排；适合研究中国老龄化的社会支持与养老服务。",
 "CGSS 中国综合社会调查":
   "中国人民大学主持的年度/双年度全国综合性社会调查（2003 年起），覆盖 28 个省级单位、约 1 万户。核心：社会分层与流动、收入与职业、教育、健康与生活方式、社会信任与网络、主观幸福感与公平感、环境与消费；是社会科学与公共卫生交叉研究常用的社会背景数据。",
 "KLoSA 韩国老龄化追踪研究":
   "韩国劳动研究院主持的 45 岁及以上人群面板（2006 年起，每 2 年一轮），与 HRS 国际家族可比。核心：人口学与家庭、健康与慢病、认知（部分轮次含详细认知测验）、功能与失能、就业与退休、收入与资产、养老金与长期照护保险；适合做韩国老龄化与长期照护政策研究。",
 "KoGES 韩国基因组流行病学研究":
   "韩国国立保健研究院（KDCA）主持的大型基因组流行病学队列集群（约 20 万人），含社区人群（Ansan/Ansung）、农村人群与城市医院体检人群三套子队列。核心：问卷（生活方式、膳食、病史）、体格测量、血液生化、基因分型、部分代谢组与随访结局；是东亚人群基因-环境交互与慢病研究的重要资源。",
 "KNHANES 韩国国民健康营养调查":
   "韩国疾病管理厅（KDCA）主持的全国代表性横断面调查（1998 年起，每年一轮），设计对标美国 NHANES。核心：健康问卷（慢病、吸烟饮酒、体力活动、心理健康）、营养调查（24 小时膳食回顾）、体检（血压、身高体重腰围、视力听力、口腔）、血液生化（血糖、血脂、肝肾功能、维生素 D）、部分年份含尿液与影像；公开下载，界面以韩文为主。",
 "NIDDK-CR 美国糖尿病消化肾病研究所中央数据仓库":
   "美国 NIDDK 建立的数据共享平台，收录其资助的多项里程碑研究的个体级数据。核心：CRIC 慢性肾功能不全队列（CKD 3-4 期，密集随访 eGFR 斜率、蛋白尿、ESRD、心血管事件与死亡，全球最重要的 CKD 进展前瞻队列）、CKiD 儿童 CKD 队列、DCCT/EDIC（1 型糖尿病强化治疗里程碑试验及其长期随访）、LookAHEAD（2 型糖尿病减重干预）、DPP（糖尿病预防计划）；提供标准化数据字典与在线申请。",
 "Vivli / YODA / CSDR 临床试验个体数据共享平台":
   "三个临床试验个体数据（IPD）共享渠道：Vivli 为非营利平台，汇集多申办方已去标识的试验数据，研究者提交 proposal 经独立评审后在线分析；YODA（耶鲁）以项目制管理，主要处理药企捐赠的试验数据，申请需经委员会审批；CSDR 为行业联合平台，按研究目的审核请求。核心：受试者级疗效与安全性变量、方案偏离、不良事件；适合做 IPD 荟萃与疗效异质性再分析。",
 "dbGaP 基因型与表型数据库":
   "NCBI 的基因型与表型数据库，收录全球多项 GWAS、测序与临床研究的受控访问数据。核心：原始与处理后基因型/测序数据、表型变量字典、研究文档（study documents）、汇总关联结果；受控数据需经机构签署数据使用协议（DUA）并取得 PI 授权，分阶段审批（PI → 机构 → NIH DAC），周期通常 1-3 个月。",
 "国家自然科学基金基础研究知识库":
   "国家自然科学基金委员会建设的资助成果开放获取仓储。核心：受基金资助论文的全文与元数据（可按学科、依托单位、项目号检索）；适合做科研产出计量、学科趋势与机构比较，也可作为查找中文研究全文的补充入口。",
 "NCMI 国家人口健康科学数据中心":
   "中国医学科学院牵头建设的国家级人口健康科学数据中心。核心：人群队列与专病数据库目录、国家临床医学研究中心数据、部分公开数据集的申请与共享入口；更像「数据目录 + 申请门户」而非可直接下载的仓储，实际取数仍需与数据持有方对接。",
 "HCUP 美国医疗成本与利用项目":
   "美国 AHRQ 主持的医疗成本与利用项目，汇集州级住院（SID）、门诊手术（SASD）、急诊（SEDD）与全国住院样本（NIS）、全国再入院（NRD）、全国急诊（NEDS）。核心：住院诊断与操作（ICD）、费用与支付方、住院日、再入院、地区与医院特征；需完成在线培训并签 DUA、付费购买，是做医疗利用、费用与再入院研究的主力数据。",
 # —— 澳洲补充 ——
 "HILDA 澳大利亚家庭收入与劳动力动态调查":
   "墨尔本大学应用经济与社会研究所主持的全国代表性家庭面板（2001 年起，每年一轮，约 1.7 万人）。核心：收入与财富、就业与工时、教育、家庭结构与育儿、健康与心理健康（SF-36）、居住与住房成本、生活满意度；适合做收入-健康梯度、就业与心理健康、家庭政策的纵向分析。",
 "ALSWH 澳大利亚女性健康纵向研究":
   "澳大利亚女性健康纵向研究，1996 年起追踪三个出生队列（1973-78、1946-51、1921-26 年出生，合计约 5.8 万人），迄今多轮随访。核心：健康与慢病、生殖与激素、心理健康、生活方式、医疗服务使用、照料与老龄；是研究女性生命历程健康（尤其更年期、慢病累积）的经典队列。",
 "Ten to Men 澳大利亚男性健康纵向研究":
   "澳大利亚男性健康纵向研究，2013-2014 年基线招募 10-55 岁男性（约 1.6 万人），此后多轮随访。核心：健康与心理健康、危险行为（饮酒、吸烟、药物）、体力活动与膳食、就业与家庭关系、社会支持、服务使用；是研究男性健康与社会角色（父职、工作压力、求助行为）的主要澳洲队列。",
}

NOTES_FIX = {
 "MHAS 墨西哥健康与老龄化研究": "移民相关变量是特色也是坑：赴美经历多为自报、跨轮缺失多；干血斑只在部分轮次、部分样本，别假设人人都有；与 HRS 可比但变量名不完全一致，须用 Gateway 调和版对照。",
 "ELSA 英格兰老龄化追踪调查": "护士体检为隔轮或部分样本，血液指标不是每轮都有；认知测验版本在轮次间有调整，纵向比较要做等值化处理；样本以社区居住人群为主，养老院人群覆盖不足。",
 "SHARE 欧洲健康、老龄与退休调查": "各国问卷模块、采集年份与样本设计不完全一致，跨国比较务必用官方 release guide 核对；部分国家轮次缺失；干血斑/加速计仅子样本。",
 "LASI 印度纵向老龄化调查": "各邦样本量与随访进度差异大，做邦级估计要看官方权重；认知测验受教育程度影响显著，未校正会严重高估痴呆；LASI-DAD 是子样本，不能当全样本用。",
 "MCPS 墨西哥城前瞻性研究": "两个城区、城市中低收入的非随机样本，全国外推受限；结局主要靠死亡登记，非致死性疾病（如 CKD 早期）捕获不全；英文变量文档需向团队索取。",
 "All of Us 美国全民健康研究": "EHR 数据取决于参与者的就诊机构是否参与网络，缺失非随机；可穿戴数据依从者偏倚明显；Workbench 有算力配额，跑大模型前先申请；不同版本的 CDR 数据集会变，务必记录版本号。",
 "FinnGen": "端点是基于 ICD 与药物购买记录构建的，与临床金标准有差异；芬兰人群 founder 效应使罕见变异富集，直接外推到其他人群风险会偏；汇总统计公开但个体级数据仍需审批。",
 "BioBank Japan": "以医院为基础、按疾病招募，无健康对照的「人群代表性」，做患病率会偏；随访以生存为主，生活方式变量较少；个体级数据需向研究所申请并通常需日方合作。",
 "Million Veteran Program": "退伍军人以男性、老年、白人比例高，性别与年龄外推差；VA 病历跨系统（VA 与 Medicare 双覆盖）可能重复计数；申请流程与 VA 内部审批链较长，预留 3-6 个月。",
 "Estonian Biobank": "约 20% 成年人口虽具代表性，但参与者更健康（健康志愿者偏倚）；登记链接需在爱沙尼亚安全环境完成，跨境分析受限；组学数据分批次发布，注意版本。",
 "China-PAR": "模型基于特定年代队列，人群危险因素水平已变化，直接用旧模型会高估风险；复发事件与竞争风险处理需谨慎；个体级数据不公开，多为合作或使用已发表模型系数。",
 "China PEACE / 百万人群项目": "回顾性部分是病历抽象，变量受记录质量限制（如 LVEF、门球时间缺失）；抽样医院以三级为主，基层代表性弱；百万人群项目随访依赖社区与医保链接，失访需评估。",
 "CMEC 中国西南多民族队列": "民族分组样本量不均，小民族组统计功效有限；高原暴露与民族遗传高度共线，别把民族效应误读为环境效应；跨民族基因-环境交互需足够样本与严格分层。",
 "泰州队列": "地市级队列，外出务工人口流动性大，失访与医保外就诊会漏结局；生物样本的采集与储存批次需核对；数据以合作为主，变量清单要提前谈。",
 "上海女性/男性健康研究 SWHS/SMHS": "男女两队列招募年份与问卷略有差异，合并分析要做变量对齐；膳食问卷为 FFQ，存在回忆与测量误差，建议用能量校正与回归校准；随访结局依赖登记链接，非致死慢病不全。",
 "C-STRIDE 中国慢性肾脏病队列": "入组为专科门诊/住院 CKD 患者，早期与社区隐匿病例覆盖不足；eGFR 用 CKD-EPI 还是 MDRD、是否用中国校正系数会显著改变斜率；随访间隔不均，做轨迹模型要用混合效应而非简单两点斜率。",
 "CK-NET 中国肾脏疾病网络": "报告为年度横截面汇总，不能直接当个体级数据做因果推断；透析登记覆盖度逐年改善，早年份漏报多；医保数据与登记库匹配存在未匹配人群。",
 "中国高血压调查 CHS": "单次横断面，血压仅测三次且部分为单日，不能做发病率；知晓率/治疗率/控制率依赖自报用药，漏报在基层更明显；不同省份抽样权重不同，合并估计须用官方权重。",
 "中国慢性病及危险因素监测": "各轮抽样框架与检测方法有调整（如血糖检测方式、血脂指标增减），跨年趋势比较要先做方法学校正；数据不公开，需通过 CDC 慢病中心合作申请。",
 "BRFSS": "电话调查（含手机）应答率低、自报变量多，患病率普遍低估；2011 年方法学调整（引入 raking 权重与手机样本）造成趋势断点，跨年比较必须分段；无体检与生物样本。",
 "NHIS": "无体检、无生物样本，慢病为自报；2019 年起问卷大幅改版，与之前年份的变量不可直接对接；家庭样本存在户内相关，分析要用复杂抽样与聚类校正。",
 "韩国 NHIS": "理赔诊断用于报销、非研究级，存在「诊断升级」与编码习惯偏差；健康检查虽含客观指标但参检率非随机（健康者更愿检）；数据不出境，须在韩国境内或指定安全环境分析，通常需韩方合作。",
 "韩国 HIRA": "与 NHIS 数据有重叠但口径不同（审核 vs 理赔），两个库不能简单拼接；处方级数据量大，抽样与索引设计要先规划；诊断编码准确性低于病历研究。",
 "CPRD": "基层记录只反映就诊者，未就诊与专科事件可能漏；编码实践在诊所间差异大，需用 codelist 并做敏感性分析；死亡日期在链接前后有滞后；GOLD 与 Aurum 人群与编码体系不同，别混用。",
 "OpenSAFELY": "只输出汇总结果，做亚组时受最小计数披露规则限制（小组会被抑制）；队列定义依赖 codelist，须公开代码以便复现；数据覆盖初级保健，专科细节有限。",
 "QResearch": "以参与 EMIS 的诊所为基础，非全国随机样本；QRISK 系列模型的系数已更新多版，验证时要对齐版本；缺失检验值需按「未检测」处理而非简单填补。",
 "北欧登记体系": "登记诊断编码准确性因疾病而异（糖尿病、心梗较好，部分精神与风湿病较差）；处方数据库记录「取药」不等于「服药」；跨国合并需各国伦理与数据保护审批，耗时半年以上。",
 "台湾 NHIRD": "只能现场分析、结果不可携出，分析窗口与算力受限；诊断编码用于申报、存在倾向性；健保覆盖率高但自费项目（部分新药、耗材）不记录。",
 "日本 NDB / JMDC": "NDB 申请门槛高、周期长且需日本国内机构；JMDC 投保人群偏在职与年轻、离职即失访；体检指标虽客观但参检者偏健康；英文文档不全，变量名需对照日文定义。",
 "MarketScan / Optum / IQVIA": "缺检验值（尤其 Optum 之外）、无社会经济与行为变量；保险切换导致左截断与失访；费用为赔付额而非真实成本；不同商保库人群重叠，合并需去重。",
 "CMS Medicare/Medicaid": "按年份与文件类型分散（住院/门诊/Part D 分文件），合并工作量大；Medicare Advantage 参保人理赔不全；申请经 ResDAC 需数周至数月并付费；小样本地区受隐私抑制。",
 "eICU-CRD": "不同医院变量完整度差异极大，做多中心模型要显式处理缺失；护理记录高频但实验室低频；部分医院病例极少，中心随机效应不可省；与 MIMIC 变量定义不同，映射需自建。",
 "HiRID": "单中心、单院区，病例构成偏外科与移植；高频数据噪声大，需先做去噪与重采样；不同版本（v1/v2）变量与时间范围有差异，务必记录版本。",
 "INSPIRE": "单中心、以手术人群为主，非内科 ICU 全貌；术中数据依赖麻醉信息系统记录质量；结局随访以院内与 30 天为主，长期结局缺失。",
 "PIC": "单中心三级儿童医院，危重比例高、病种偏复杂，社区与基层儿科外推受限；儿科变量编码与成人库不同，须用专用字典；样本期有限，做趋势分析要看版本说明。",
 "Dryad": "不是标准化数据库，字段含义差异极大；部分数据集仅有 README 无 codebook；下载前先核许可与引用要求，商用需看具体 CC 条款。",
 "SRA": "体量巨大（单项目常数十 GB 至 TB），先估存储与算力；受控人类数据需 dbGaP 授权，SRA 上只有公开部分；元数据（样本属性）质量参差，做整合分析要人工清洗。",
 "ArrayExpress / BioStudies": "平台与注释体系历经合并与改版，老项目元数据格式不一；芯片与测序平台批次效应显著，整合前须做归一化与批次校正；部分数据仅为处理后矩阵。",
 "Zenodo / figshare / Mendeley Data": "代码与数据质量无同行评审，直接复用前必须跑通；同一研究可能有多个版本，认准 DOI 与版本号；许可从 CC0 到「需申请」都有，商用前逐条确认。",
 "ICPSR / IPUMS": "ICPSR 部分数据需会员机构身份或额外申请；IPUMS 的调和变量是「统一口径」，与原始调查有差异，跨库合并要核对 universe（适用人群）；抽样权重与 strata 不可丢。",
 "NGDC": "数据多以项目为单位汇交，元数据规范度不一；受控人类遗传资源数据需按《人类遗传资源管理条例》申请，不能直接下载；镜像与版本更新频繁，引用要带访问号。",
 "ScienceDB": "通用仓储，非标准化数据库，质量取决于提交者；找数据用关键词 + 学科筛选，别期待变量字典；引用须带 DOI 与版本。",
 "NMDC": "以微生物基因组与微生物组为主，临床变量少；人体微生物组数据受控比例较高；检索需用拉丁学名或项目号，中文关键词命中率低。",
 "国家/卫生健康统计年鉴": "颗粒度只到全国/省级，做个体推断会犯生态学谬误；口径逐年调整（机构分类、统计范围），跨年比较要看指标说明；床位与诊疗人次含大量基层机构，解释需谨慎。",
 "MEPS": "两年面板太短，做长期轨迹不合适；自报支出与理赔核验值有差异，优先用核验文件；样本量按年约 3 万户，罕见病与罕见用药功效不足；复杂抽样设计必须加权。",
 "GBD / GHDx": "全部为模型估计值，不是实测数据，引用必须带 GBD 版本与 IHME；不同版本对同一指标的估计会变，跨版本比较危险；中国省级估计的 uncertainty 区间较宽。",
 "CFPS": "家户与个人问卷需按 pid/fid 关联，跨年追踪的成员进出要处理；收入与支出有大量缺失与极端值，需按官方说明做插补；2010 基线抽样不含新疆、西藏等地区，全国代表性有边界。",
 "CLASS": "只覆盖 60 岁以上、以社区居住为主，机构养老人群不足；部分模块（如数字使用）为后期加入，跨轮不可比；自报慢病与用药需与医保数据交叉验证。",
 "CGSS": "年份间抽样框与问卷模块有调整，不是每年都问同样题目；健康与医疗问题深度远不及专门健康调查；做趋势分析要先核对各年变量对应关系。",
 "KLoSA": "认知测验在轮次间有版本变化，纵向比较需等值化；45 岁以上中年样本在后期逐渐老龄化，做年龄趋势要区分队列效应；韩文变量名，英文文档需对照。",
 "KoGES": "三套子队列抽样框不同（社区/农村/医院体检），合并分析必须带队列固定效应；医院体检人群偏健康；个体级数据需向 KDCA 申请并通常需韩方合作。",
 "KNHANES": "每年轮次抽样与检测项目有调整，跨年趋势比较要核对项目是否一致；膳食为 24 小时回顾，单日数据不能代表长期摄入；韩文界面与变量名，英文文档不完全。",
 "NIDDK-CR": "各研究的变量命名与随访节奏完全不同，不能直接拼接；申请需说明具体研究名与变量清单，审批由 NIDDK 数据共享委员会把关；部分研究仅提供去标识后的受限版本。",
 "Vivli / YODA / CSDR": "不是「下载即用」：均需提交研究方案、经独立评审，且分析多在平台提供的安全环境内完成；不同申办方授权范围不同，部分试验只提供汇总结果；数据字典与变量命名逐试验不同。",
 "dbGaP": "审批是三步链（PI 授权 → 机构签署 DUA → NIH DAC 评审），任何一环卡住都拿不到数据，预留 1-3 个月；获批范围严格限定在研究方案内，改题目要重新申请；数据不得再分发，分析环境有审计。",
 "国家自然科学基金基础研究知识库": "只收录基金资助成果，覆盖面不等于全部中文文献；全文可用性依论文开放获取状态而定；做计量分析注意重复条目与机构名写法不统一。",
 "NCMI": "以目录与申请入口为主，并非可直接下载的数据仓储；实际取数需与各数据持有方单独对接，周期不可控；平台上部分链接指向内部系统，需机构账号。",
 "HCUP": "必须先完成 HCUP 在线培训并签 DUA、按数据库付费；州级数据各州年份与变量不同，跨州合并要核对；费用为「收费」而非成本，且不含院外与药房支出；再入院需自行定义时间窗。",
 "HILDA": "自报收入存在测量误差与拒答，需用官方权重与插补文件；心理健康量表（SF-36/MHI）跨轮版本有调整；样本以家庭为单位，成员分家后追踪需用官方关系文件。",
 "ALSWH": "三个出生队列年龄跨度大，合并分析必须按队列分层；随访 20 余年失访累积，后期样本偏健康、偏高教育；问卷在轮次间有增删，纵向比较需核对。",
 "Ten to Men": "基线为 10-55 岁男性，未成年子样本的问卷由家长/本人分别作答，注意区分；随访轮次间隔较长，急性事件可能漏报；样本不含女性，不能做性别比较。",
}

def _pick(dct, name):
    """先精确匹配库名，再按「最长前缀」匹配，兼容用简称写在字典里的键。"""
    if name in dct:
        return dct[name]
    cands = [k for k in dct if name.startswith(k)]
    return dct[max(cands, key=len)] if cands else None

for d in D:
    _c = _pick(CONTENT_FIX, d["name"])
    _n = _pick(NOTES_FIX, d["name"])
    if _c:
        d["content"] = _c
    if _n:
        d["notes"] = _n

# 为每个库生成可辨识别名（中文片段 / 英文缩写），供「用户点名库」加分与搜索
for d in D:
    _nm = d.get("name") or ""
    al = {_nm.lower()}
    _cn, _en = [], []
    for _t in re.split(r"[\s/]+", _nm):
        if not _t:
            continue
        if _t.isascii():
            for _seg in re.split(r"[-_]", _t):
                if len(_seg) >= 3 or _seg.upper() in ("UK", "US", "EU"):
                    _en.append(_seg.lower())
        elif len(_t) >= 4:
            _cn.append(_t.lower())
    al.update(_en)
    if _cn:                                  # 只取最长的中文片段，避免「卫生支出」这类指标词混入
        al.add(max(_cn, key=len))
    d["alias"] = sorted(x for x in al if len(x) >= 2)

# 速查表分组兜底：保证 100 个库全部出现在「总览速查表」里（曾漏 9 条澳洲/北方队列）
QR_FALLBACK = {"oceania": "oceania"}
QR_NAME = {"北方生活方式队列": "biobank"}
for d in D:
    if d.get("qr") not in QR:
        d["qr"] = QR_NAME.get(d["name"]) or QR_FALLBACK.get(d["cat"], "monitor")


# 统一升级过短申请方式；补齐缺失指标（类别级概述）
for d in D:
    u = (d.get("usage") or "").strip()
    if len(u) < 18:
        d["usage"] = GEN_USAGE[d["access"]]
    if not (d.get("indicators") or "").strip():
        d["indicators"] = GEN_IND.get(d["cat"], "详见官网 codebook / Data Dictionary。")

# ---------------------------------------------------------------------------
# 渲染
# ---------------------------------------------------------------------------
DB_JSON = json.dumps(D, ensure_ascii=False)

CAT_OPTIONS = "".join(f'<option value="{k}">{v}</option>' for k,v in CATS)

# 查询器选项
REGION_OPTS = ["中国","美国","欧洲","英国","韩国","日本","港台","墨西哥","印度","北欧","多国/国际"]
DATATYPE_OPTS = ["问卷/自报","客观体检/生化","基因/多组学","电子病历/医保","影像","死亡登记/随访","文本/NLP"]
DESIGN_OPTS = ["前瞻性队列","回顾性/横断面","RCT 数据二次利用","真实世界观察性","预测模型","IPD 荟萃","重复横断面"]
TOPIC_OPTS = ["老龄与认知","心血管与肾脏","肿瘤","营养与代谢","职业与环境","精神心理/行为","卫生经济与卫生服务","重症/ICU","妇幼与儿童","遗传/组学","罕见病","卫生政策/公平"]

REGION_CHIPS = "".join(f'<button type="button" class="chip" data-group="region" data-val="{x}">{x}</button>' for x in REGION_OPTS)
DATATYPE_CHIPS = "".join(f'<button type="button" class="chip" data-group="datatype" data-val="{x}">{x}</button>' for x in DATATYPE_OPTS)
DESIGN_CHIPS = "".join(f'<button type="button" class="chip" data-group="design" data-val="{x}">{x}</button>' for x in DESIGN_OPTS)
TOPIC_CHIPS = "".join(f'<button type="button" class="chip" data-group="topic" data-val="{x}">{x}</button>' for x in TOPIC_OPTS)

# 开放度图例
LEGEND = "".join(
    f'<div class="legend-item"><span class="stars s{a}">{ACCESS[a]}</span></div>'
    for a in sorted(ACCESS))

# 总览速查表
def overview_tables():
    out = []
    for key, title in QR.items():
        rows = [d for d in D if d.get("qr") == key]
        if not rows:
            continue
        body = ""
        for d in rows:
            stars = "★"*d["access"]
            body += (f'<tr class="ov-row" data-nm="{d["name"]}" style="cursor:pointer">'
                     f'<td><b>{d["name"]}</b><br><span class="en">{d["en"]}</span></td>'
                     f'<td>{d.get("region","")}</td><td>{d.get("scale","")}</td>'
                     f'<td>{d.get("timeSpan","")}</td>'
                     f'<td class="stars s{d["access"]}">{stars}</td></tr>')
        out.append(
            f'<h3 class="ov-title">{title}</h3>'
            f'<div class="table-wrap"><table class="ov-table"><thead><tr>'
            f'<th>数据库</th><th>地区</th><th>规模（约）</th><th>时间跨度</th><th>开放度</th>'
            f'</tr></thead><tbody>{body}</tbody></table></div>')
    return "\n".join(out)

OVERVIEW = overview_tables()

# 全部官方入口一览（按分类）
def all_links():
    out = []
    for k, label in CATS:
        lst = [d for d in D if d["cat"] == k]
        if not lst:
            continue
        out.append('<div class="lk-cat"><h3>%s <span>%d 个</span></h3><ul>' % (label, len(lst)))
        for d in lst:
            ls = "".join('<a href="%s" target="_blank" rel="noopener">%s ↗</a>' % (u["url"], u["label"])
                         for u in d.get("urls", []))
            out.append('<li><b>%s</b><span class="lk-en">%s</span><div class="lk-l">%s</div></li>'
                       % (d["name"], d.get("en") or "", ls))
        out.append('</ul></div>')
    return "".join(out)

ALL_LINKS = all_links()

# 分类锚点导航
CAT_NAV = "".join(f'<a href="#cat-{k}" class="cat-link">{i+1}. {v}</a>' for i,(k,v) in enumerate(CATS))

# 实战阶梯（第 13 章）
LADDER = [
    ("★ 零门槛，当天开工","NHANES、MEPS、BRFSS、GEO、Dryad、GBD、CDC WONDER、IPUMS、cBioPortal、NSFC 知识库、UK Biobank Showcase 浏览","几分钟","免费"),
    ("★★ 注册即下","CHARLS、CFPS、CLHLS、HRS、MHAS、CHNS、CHFS、CNSDA 系列（CGSS、CLASS）","1-3 天","免费"),
    ("★★★ 培训或签署协议","MIMIC-IV、SEER、eICU、BioLINCC（SPRINT/ALLHAT/AASK）、NIDDK-CR（CRIC）、NIA AgingResearchBiobank、Vivli","2-6 周","免费"),
    ("★★★☆ 需购买","HCUP NIS 与 NRD、CMS 经 ResDAC 申请","数周","数百至数千美元"),
    ("★★★★ 正式申请并付费","UK Biobank、CPRD、CKB 深度层、SEER-Medicare、dbGaP；中国队列共享平台 CCC（含评审）","1-6 个月","较高"),
    ("★★★★★ 必须本地合作","开滦、东风、China PEACE、CMEC、广州 GBCS / BIGCS、CMHS、NRDRS、CNRDS、泰州队列、韩国 NHIS、香港 CDARS、北欧登记、Taiwan NHIRD","半年起","通常涉及共同署名"),
]

LADDER_ROWS = ""
for i,(lvl,ex,per,cost) in enumerate(LADDER):
    LADDER_ROWS += (f'<tr><td class="stars s{6-i}">{lvl}</td><td>{ex}</td>'
                    f'<td>{per}</td><td>{cost}</td></tr>')

HTML = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>全球健康数据库整合网页 · Global Health Database Integration Platform</title>
<meta name="description" content="面向医学科研的全球健康与医学公共数据库检索、分类、研究匹配与申请导航平台：91 个数据库，含开放度分级、申请流程与费用周期、变量申请情况、论文致谢模板。创建人：杜思娴 dusixian16@163.com">
<meta name="keywords" content="医学数据库,公共数据库,队列研究,UK Biobank,CHARLS,NHANES,MIMIC-IV,dbGaP,SEER,数据申请,变量查询,数据使用协议">
<meta property="og:title" content="全球健康数据库整合网页 · Global Health Database Integration Platform">
<meta property="og:description" content="输入科学问题 → 锁定数据库 + 研究范式 + 申请指南。91 个医学与健康公共数据库。">
<meta property="og:type" content="website">
<meta property="og:url" content="https://naturedu.github.io/global-health-db-hub/">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='7' fill='%230b3a72'/%3E%3Cellipse cx='16' cy='9' rx='7' ry='3' fill='%2312b3d6'/%3E%3Cpath d='M9 9v14c0 1.7 3.1 3 7 3s7-1.3 7-3V9' fill='none' stroke='%2312b3d6' stroke-width='2'/%3E%3Cpath d='M16 13v8M12 17h8' stroke='%23fff' stroke-width='1.8'/%3E%3C/svg%3E">
<style>
:root{
  --bg:#f2f7fd; --card:#ffffff; --ink:#12263f; --muted:#5a6b82;
  --line:#dbe6f4; --primary:#2563eb; --primary-d:#1746b8; --accent:#06b6d4;
  --s1:#10b981; --s2:#06b6d4; --s3:#3b82f6; --s4:#8b5cf6; --s5:#f43f5e;
  --shadow:0 2px 6px rgba(20,60,120,.08),0 10px 26px rgba(20,60,120,.10);
}
*{box-sizing:border-box}
body{margin:0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif;
  background:var(--bg);color:var(--ink);line-height:1.65;font-size:16px}
a{color:var(--primary);text-decoration:none}
.wrap{max-width:1180px;margin:0 auto;padding:0 18px}
header.top{position:sticky;top:0;z-index:50;background:rgba(255,255,255,.94);
  backdrop-filter:blur(10px);border-bottom:1px solid var(--line)}
.top-inner{display:flex;align-items:center;gap:9px;padding:9px 16px;max-width:1400px;margin:0 auto;flex-wrap:wrap}
.brand{display:flex;align-items:center;gap:9px;font-weight:800;font-size:17px;color:var(--primary-d);white-space:nowrap}
.logo{width:34px;height:34px;flex:none;border-radius:9px;box-shadow:0 2px 8px rgba(37,99,235,.28)}
.logo-lg{width:74px;height:74px;flex:none;border-radius:18px;box-shadow:0 6px 20px rgba(6,182,212,.35)}
.brand small{display:block;font-weight:500;font-size:11.5px;color:var(--muted)}
.top nav{display:flex;gap:3px;flex-wrap:nowrap;flex:0 1 auto;min-width:0}
.top nav a{font-size:13px;color:var(--muted);padding:5px 7px;border-radius:7px;white-space:nowrap}
.top nav a:hover{background:#e8f0fb;color:var(--primary-d)}
.search-box{border:1px solid var(--line);border-radius:9px;padding:7px 11px;font-size:13.5px;min-width:140px;flex:1 1 170px}
.cat-jump{border:1px solid var(--line);border-radius:8px;padding:6px 8px;font-size:13px;color:var(--muted);
  background:#fff;font-family:inherit;max-width:130px;cursor:pointer}
.cat-jump:hover{background:#e8f0fb;color:var(--primary-d)}
@media(max-width:1000px){.top nav{display:none}.cat-jump{display:none}.search-box{flex:1 1 auto}}
@media(max-width:640px){.brand span small{display:none}.search-box{flex:1 1 130px;min-width:120px}}
/* Hero：科技感深蓝渐变 */
.hero{padding:40px 0 30px;background:linear-gradient(135deg,#0a2342,#134a8f 55%,#0e7490);color:#eaf4ff;position:relative;overflow:hidden}
.hero::after{content:"";position:absolute;right:-80px;top:-70px;width:340px;height:340px;
  background:radial-gradient(circle,rgba(6,182,212,.30),transparent 65%);pointer-events:none}
.hero-inner{display:flex;align-items:center;gap:18px;flex-wrap:wrap}
.hero h1{margin:0 0 6px;font-size:36px;font-weight:800;letter-spacing:.5px;color:#fff}
.hero p{margin:5px 0;color:#c7dcf5;max-width:860px;font-size:16px}
.badge-src{display:inline-block;background:rgba(255,255,255,.14);color:#d7ecff;font-size:13px;
  padding:4px 12px;border-radius:20px;margin-bottom:12px;border:1px solid rgba(255,255,255,.22)}
.creator{display:inline-block;margin-top:10px;background:rgba(6,182,212,.18);
  border:1px solid rgba(6,182,212,.45);color:#cfeea;font-size:14px;padding:6px 14px;border-radius:22px}
.creator{color:#d6f4fb}
.creator a{color:#fff;font-weight:700}
.creator a:hover{text-decoration:underline}
.beta-tag{display:inline-block;background:linear-gradient(90deg,#f59e0b,#f43f5e);color:#fff;font-size:12px;
  font-weight:800;padding:3px 10px;border-radius:6px;margin-left:8px;letter-spacing:.5px;vertical-align:middle}
section{padding:28px 0}
h2.sec{font-size:23px;margin:0 0 4px;display:flex;align-items:center;gap:10px}
h2.sec .num{background:linear-gradient(135deg,var(--primary),var(--accent));color:#fff;width:30px;height:30px;border-radius:9px;
  display:inline-flex;align-items:center;justify-content:center;font-size:15px;flex:none}
.sec-sub{color:var(--muted);font-size:14.5px;margin:0 0 18px}
/* 注册门（内测版） */
#gate{position:fixed;inset:0;z-index:200;display:flex;align-items:center;justify-content:center;padding:20px;
  background:linear-gradient(135deg,#08213c,#123f78);overflow:auto}
#gate .gate-card{background:#fff;border-radius:18px;padding:26px 28px;max-width:420px;width:100%;box-shadow:0 20px 50px rgba(0,0,0,.35)}
#gate h3{margin:0 0 4px;font-size:21px;color:var(--primary-d)}
#gate .sub{color:var(--muted);font-size:13.5px;margin:0 0 16px}
.field{margin-bottom:13px}
.field label{display:block;font-size:13.5px;font-weight:700;color:var(--ink);margin-bottom:5px}
.field input{width:100%;border:1px solid var(--line);border-radius:10px;padding:9px 11px;font-size:14.5px;font-family:inherit}
.field input:focus{outline:2px solid #c7dbfb;border-color:var(--primary)}
.code-row{display:flex;gap:8px}
.code-row input{flex:1}
.code-btn{border:none;border-radius:10px;background:var(--primary);color:#fff;font-weight:700;font-size:13px;
  padding:0 14px;cursor:pointer;white-space:nowrap}
.code-btn:disabled{background:#9fb4d4;cursor:not-allowed}
.gate-msg{font-size:13px;margin-top:8px;min-height:18px}
.gate-msg.ok{color:#0f9d58}.gate-msg.err{color:#e11d48}
.gate-tip{font-size:12px;color:var(--muted);margin-top:10px;line-height:1.5}
/* 详情弹窗 */
#modal{position:fixed;inset:0;z-index:150;display:none;align-items:flex-start;justify-content:center;padding:26px 16px;
  background:rgba(8,25,45,.6);overflow:auto}
#modal .modal-card{background:#fff;border-radius:18px;max-width:760px;width:100%;padding:24px 26px;
  box-shadow:0 20px 50px rgba(0,0,0,.3);margin:auto}
#modal h3{margin:0 0 2px;font-size:22px;color:var(--primary-d)}
#modal .m-en{color:var(--muted);font-size:13.5px;margin-bottom:10px}
#modal .m-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:8px;margin:12px 0}
#modal .m-cell{background:var(--bg);border:1px solid var(--line);border-radius:10px;padding:8px 11px;font-size:13.5px}
#modal .m-cell b{display:block;font-size:11.5px;color:var(--muted);font-weight:700;margin-bottom:2px}
#modal h5{margin:16px 0 6px;font-size:16px;color:var(--primary-d)}
#modal p,#modal li{font-size:14.5px;line-height:1.7}
#modal ul{margin:6px 0;padding-left:20px}
.m-close{position:sticky;float:right;top:0;background:#eef4fd;border:1px solid var(--line);border-radius:9px;
  padding:5px 12px;font-size:13px;cursor:pointer;font-weight:700;color:var(--primary-d)}
/* 引用信息 */
.cite-box{background:#fff;border:1px solid var(--line);border-radius:14px;padding:18px 20px;box-shadow:var(--shadow)}
.cite-pre{background:#0e2748;color:#d7ecff;border-radius:10px;padding:12px 14px;font-size:13px;white-space:pre-wrap;
  line-height:1.7;overflow-x:auto;margin:8px 0}
.cite-pre .k{color:#7fd1ff;font-weight:700}
.copy-btn{border:none;border-radius:8px;background:var(--primary);color:#fff;font-size:12.5px;font-weight:700;
  padding:5px 12px;cursor:pointer;margin-bottom:6px}
/* 经典指标 */
.ind{background:#eff6ff;border:1px solid #cfe0fb;border-radius:10px;padding:8px 11px;font-size:13.5px;margin:8px 0}
.ind b{color:var(--primary-d)}
.detail-btn{border:none;border-radius:8px;background:#eef4fd;color:var(--primary-d);font-size:12.5px;font-weight:700;
  padding:6px 12px;cursor:pointer;border:1px solid var(--line)}
/* 配套工具卡片 */
.tool-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:16px;margin-top:4px}
.tool-card{display:block;text-decoration:none;background:#fff;border:1px solid var(--line);border-radius:14px;
  padding:16px 18px;box-shadow:var(--shadow);transition:.15s;color:inherit}
.tool-card:hover{border-color:var(--primary);transform:translateY(-2px)}
.tool-tag{display:inline-block;background:#eef4fd;color:var(--primary-d);border:1px solid var(--line);
  border-radius:999px;font-size:12px;font-weight:700;padding:2px 10px;margin-bottom:8px}
.tool-card h3{margin:0 0 6px;font-size:17px;color:var(--primary-d)}
.tool-card p{margin:0;font-size:13.5px;color:var(--muted);line-height:1.65}
.tool-go{display:inline-block;margin-top:10px;font-size:13px;font-weight:700;color:var(--primary)}

/* 查询器（科技感墨蓝） */
#query{background:linear-gradient(135deg,#08213c,#123f78 60%,#0e7490);color:#e6f0fb}
#query h2.sec{color:#fff}
#query h2.sec .num{background:linear-gradient(135deg,#06b6d4,#2563eb);color:#fff}
#query .sec-sub{color:#a8c6e6}
.q-card{background:rgba(255,255,255,.07);border:1px solid rgba(120,180,240,.28);border-radius:18px;padding:20px;margin-top:14px}
.q-row{margin-bottom:16px}
.q-label{font-size:14px;color:#9fd4ec;margin-bottom:7px;font-weight:700;letter-spacing:.3px}
.chip-row{display:flex;flex-wrap:wrap;gap:7px}
.chip{background:rgba(255,255,255,.10);border:1px solid rgba(120,180,240,.35);color:#d7ecff;border-radius:18px;
  padding:5px 12px;font-size:13.5px;cursor:pointer;transition:.15s}
.chip:hover{background:rgba(255,255,255,.20)}
.chip.on{background:linear-gradient(135deg,#06b6d4,#2563eb);border-color:#06b6d4;color:#fff;font-weight:700}
textarea.q-text{width:100%;min-height:78px;border-radius:12px;border:1px solid rgba(120,180,240,.35);
  background:rgba(6,25,48,.55);color:#eaf4ff;padding:11px;font-size:15px;font-family:inherit;resize:vertical}
.q-actions{display:flex;gap:12px;align-items:center;flex-wrap:wrap;margin-top:4px}
.btn{border:none;border-radius:12px;padding:10px 22px;font-size:14.5px;font-weight:700;cursor:pointer}
.btn-primary{background:linear-gradient(135deg,#06b6d4,#2563eb);color:#fff}
.btn-primary:hover{filter:brightness(1.12)}
.btn-ghost{background:transparent;border:1px solid rgba(120,180,240,.45);color:#d7ecff}
.hint{font-size:12.5px;color:#9dbada}
#qResult{margin-top:18px}
.q-empty{color:#d7ecff;font-size:14.5px;padding:14px;background:rgba(255,255,255,.08);
  border:1px dashed rgba(120,180,240,.35);border-radius:12px}
.rec{border-left:5px solid #06b6d4;background:#fff;border-radius:14px;padding:15px 17px;margin-bottom:13px;box-shadow:var(--shadow);color:#12263f}
.rec.locked{border-left:5px solid #2563eb;background:#f4f9ff}
.rec h4{margin:0 0 4px;font-size:18px;color:var(--ink)}
.rec .en{font-size:12px;color:var(--muted)}
.rec .meta{font-size:13px;color:var(--muted);margin-bottom:6px}
.rec .why{font-size:14px;color:#33475e;margin:6px 0}
.rec .para{font-size:14px;color:#0f5f6b;background:#e6fbfd;border:1px solid #b6e6ee;padding:9px 11px;border-radius:10px;margin-top:7px}
.rec .stars{font-size:13px}
.rec a{color:var(--primary-d);font-size:13.5px;margin-right:12px;font-weight:600}
.match-tags{display:inline-block;background:#e8f0fb;color:var(--primary-d);border:1px solid #cfe0fb;border-radius:6px;
  padding:1px 7px;font-size:11.5px;margin:2px 4px 0 0}
.template-box{background:#fffaf0;border:1px solid #f6e3c0;border-radius:14px;padding:14px 16px;margin-top:14px;box-shadow:var(--shadow);color:#12263f}
.template-box h4{margin:0 0 8px;color:#c98a2e;font-size:15px}
.template-box table{width:100%;border-collapse:collapse;font-size:12.5px}
.template-box td{border-bottom:1px solid #f6e3c0;padding:6px 8px;vertical-align:top}
.template-box td:first-child{color:#b56a8e;font-weight:700;white-space:nowrap;width:120px}

/* 图例 */
.legend{display:flex;flex-wrap:wrap;gap:10px;margin-top:12px}
.legend-item{background:var(--card);border:1px solid var(--line);border-radius:10px;
  padding:8px 12px;font-size:13px;box-shadow:var(--shadow)}
.stars{font-weight:700;letter-spacing:1px}
.s1{color:var(--s1)} .s2{color:var(--s2)} .s3{color:var(--s3)}
.s4{color:var(--s4)} .s5{color:var(--s5)}
.s6{color:var(--s3)}

/* 统计 */
.stats{display:flex;flex-wrap:wrap;gap:14px;margin:14px 0}
.stat{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px 18px;
  box-shadow:var(--shadow);flex:1;min-width:140px}
.stat .n{font-size:26px;font-weight:800;color:var(--primary-d)}
.stat .l{font-size:12.5px;color:var(--muted)}

/* 速查表 */
.table-wrap{overflow-x:auto;margin-bottom:18px;border:1px solid var(--line);border-radius:10px}
.ov-title{font-size:15px;margin:18px 0 8px;color:var(--primary-d)}
.ov-table{border-collapse:collapse;width:100%;font-size:13px;background:var(--card)}
.ov-table th,.ov-table td{border-bottom:1px solid var(--line);padding:8px 11px;text-align:left;vertical-align:top}
.ov-table th{background:#eef4fa;color:var(--primary-d);font-weight:700;position:sticky;top:0}
.ov-table tr:hover{background:#f7fbff}
.ov-table .en{color:var(--muted);font-size:11px}

/* 分类导航 */
.cat-nav{display:flex;flex-wrap:wrap;gap:8px;margin:6px 0 0}
.cat-link{font-size:12.5px;background:#eaf2fa;color:var(--primary-d);padding:5px 11px;border-radius:20px}
.cat-link:hover{background:var(--primary);color:#fff}

/* 卡片 */
.cat-block{margin-top:30px;scroll-margin-top:70px}
.cat-head{display:flex;align-items:baseline;gap:10px;border-bottom:2px solid var(--primary);padding-bottom:6px;margin-bottom:14px}
.cat-head h3{margin:0;font-size:18px;color:var(--primary-d)}
.cat-head .cnt{font-size:12.5px;color:var(--muted)}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(360px,1fr));gap:16px}
.card{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:16px 17px;
  box-shadow:var(--shadow);display:flex;flex-direction:column;transition:.15s}
.card:hover{box-shadow:0 8px 26px rgba(16,40,70,.14);transform:translateY(-2px)}
.card h4{margin:0;font-size:16px;color:var(--ink)}
.card .en{color:var(--muted);font-size:11.5px;font-weight:500}
.card .acc{display:inline-block;font-size:12px;font-weight:700;padding:2px 9px;border-radius:20px;
  background:#f1f5f9;margin:8px 0}
.card .kv{font-size:12.5px;color:var(--muted);margin:2px 0}
.card .kv b{color:var(--ink);font-weight:600}
.card .intro{font-size:13px;margin:9px 0;color:#33414f}
.card .usage{font-size:12.5px;background:#f3f8ff;border-left:3px solid var(--primary);
  padding:7px 10px;border-radius:0 8px 8px 0;margin:6px 0}
.card .notes{font-size:12px;color:#8a5a00;background:#fff8ec;border-left:3px solid #e0a93b;
  padding:6px 10px;border-radius:0 8px 8px 0;margin:6px 0}
.card .links{margin-top:auto;padding-top:10px;display:flex;flex-wrap:wrap;gap:8px}
.card .links a{font-size:12.5px;background:var(--primary);color:#fff;padding:5px 11px;border-radius:7px}
.card .links a.alt{background:#eef4fa;color:var(--primary-d)}
.card .tagrow{margin-top:8px}
.card .tag{display:inline-block;background:#eef4fa;color:var(--primary-d);font-size:10.5px;
  padding:1px 7px;border-radius:5px;margin:2px 4px 0 0}

/* 阶梯表 */
.ladder{overflow-x:auto;border:1px solid var(--line);border-radius:10px;background:var(--card)}
.ladder table{border-collapse:collapse;width:100%;font-size:13px}
.ladder th,.ladder td{border-bottom:1px solid var(--line);padding:10px 13px;text-align:left;vertical-align:top}
.ladder th{background:#eef4fa;color:var(--primary-d)}

footer{background:#0a2342;color:#bcd3e6;font-size:13px;padding:28px 0;margin-top:30px}
footer .wrap a{color:#7fd1ff}
.disclaim{background:rgba(255,255,255,.06);border:1px solid rgba(120,180,240,.25);border-radius:12px;padding:14px 16px;margin-top:12px;color:#c3d9ef}
.disclaim b{color:#eaf4ff}
.hl{background:#fff3bf;padding:0 2px;border-radius:3px}

/* ===== 库对比 ===== */
.cmp-bar{position:fixed;left:50%;transform:translateX(-50%);bottom:18px;z-index:60;display:none;
  background:#0b3a72;color:#eaf4ff;border-radius:14px;padding:10px 14px;box-shadow:0 10px 30px rgba(8,30,60,.35);
  align-items:center;gap:10px;font-size:13.5px;max-width:94vw;flex-wrap:wrap}
.cmp-bar.on{display:flex}
.cmp-bar .tagx{background:rgba(255,255,255,.14);border-radius:8px;padding:3px 8px;font-size:12px;cursor:pointer}
.cmp-bar .tagx:hover{background:rgba(255,90,90,.5)}
.cmp-bar button{background:#12b3d6;border:0;color:#04202e;font-weight:800;border-radius:9px;padding:7px 14px;cursor:pointer;font-size:13.5px}
.cmp-bar button.clr{background:transparent;color:#9ec8e8;font-weight:600}
.cmp-chk{display:inline-flex;align-items:center;gap:5px;font-size:12.5px;color:var(--primary-d);cursor:pointer;
  background:#eef4fa;border:1px solid var(--line);border-radius:8px;padding:4px 9px}
.cmp-chk input{accent-color:var(--primary);cursor:pointer}
#cmp{display:none;position:fixed;inset:0;background:rgba(8,26,45,.62);z-index:80;padding:20px;overflow:auto}
#cmp.on{display:block}
#cmp .cmp-card{background:#fff;max-width:1120px;margin:0 auto;border-radius:16px;padding:22px 24px;box-shadow:0 20px 60px rgba(5,20,40,.4)}
#cmp .cmp-card h3{margin:0 0 4px;color:var(--primary-d);font-size:19px}
.cmp-table{width:100%;border-collapse:collapse;font-size:13px;background:#fff;margin-top:12px}
.cmp-table th,.cmp-table td{border:1px solid var(--line);padding:9px 11px;vertical-align:top;text-align:left}
.cmp-table th{background:#eef4fa;color:var(--primary-d);width:118px;font-weight:700}
.cmp-table td{min-width:180px}

/* ===== 申请材料生成器 ===== */
.ap-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px;margin-top:6px}
.ap-grid label{display:block;font-size:12.5px;color:var(--muted);margin-bottom:4px;font-weight:600}
.ap-grid input,.ap-grid select,.ap-grid textarea{width:100%;border:1px solid var(--line);border-radius:9px;padding:8px 10px;
  font-size:14px;font-family:inherit;background:#fff;color:var(--ink)}
.ap-grid textarea{min-height:64px;resize:vertical}
.ap-out{margin-top:14px}
.ap-pre{background:#0d2138;color:#d7e8f8;border-radius:10px;padding:14px 16px;font-size:12.5px;line-height:1.65;
  white-space:pre-wrap;word-break:break-word;max-height:520px;overflow:auto;font-family:ui-monospace,Consolas,monospace}

/* ===== 小按钮 / toast / 提示 ===== */
.btn-mini{font-size:12.5px;background:#eef4fa;color:var(--primary-d);border:1px solid var(--line);
  border-radius:8px;padding:5px 10px;cursor:pointer;font-family:inherit}
.btn-mini:hover{background:var(--primary);color:#fff;border-color:var(--primary)}
#toast{position:fixed;left:50%;transform:translateX(-50%);bottom:78px;z-index:120;background:#0b3a72;color:#fff;
  padding:9px 16px;border-radius:10px;font-size:13.5px;opacity:0;pointer-events:none;transition:.25s;box-shadow:0 8px 24px rgba(8,30,60,.3)}
#toast.on{opacity:1;bottom:90px}
.inv-row{display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin-top:8px}
.inv-code{font-family:ui-monospace,Consolas,monospace;font-weight:800;color:var(--primary-d);
  background:#eaf2fa;border:1px dashed var(--primary);border-radius:8px;padding:6px 12px;font-size:15px;letter-spacing:1px}


/* ===== 官方入口一览 ===== */
.lk-wrap{display:grid;grid-template-columns:repeat(auto-fill,minmax(460px,1fr));gap:16px}
.lk-cat{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:12px 14px;box-shadow:var(--shadow)}
.lk-cat h3{margin:0 0 8px;font-size:15px;color:var(--primary-d);display:flex;justify-content:space-between;align-items:baseline;gap:8px}
.lk-cat h3 span{font-size:11.5px;color:var(--muted);font-weight:500;white-space:nowrap}
.lk-cat ul{list-style:none;margin:0;padding:0}
.lk-cat li{padding:6px 0;border-bottom:1px dashed var(--line);font-size:13px}
.lk-cat li:last-child{border-bottom:0}
.lk-cat li b{font-size:13.5px;color:var(--ink)}
.lk-en{display:block;font-size:10.5px;color:var(--muted);margin:1px 0 3px}
.lk-l a{display:inline-block;font-size:11.5px;background:#eef4fa;color:var(--primary-d);border-radius:6px;padding:2px 8px;margin:2px 4px 0 0}
.lk-l a:hover{background:var(--primary);color:#fff}
@media print{.lk-wrap{grid-template-columns:1fr 1fr}}
@media(max-width:640px){.lk-wrap{grid-template-columns:1fr}}

/* ===== 打印 ===== */
@media print{
  .top,#gate,#modal,#cmp,.cmp-bar,#toast,.btn,.btn-mini,.copy-btn,.code-btn,.cmp-chk,#qResult .q-empty,footer .disclaim{display:none !important}
  body{background:#fff}
  .hero,#query,#legend{page-break-inside:avoid}
  .card{box-shadow:none;border:1px solid #ccc;break-inside:avoid}
  .sec{page-break-after:avoid}
  footer{background:#fff;color:#333}
  footer a{color:#1746b8}
}
@media(prefers-reduced-motion:reduce){*{transition:none!important;animation:none!important;scroll-behavior:auto!important}}
@media(max-width:560px){.grid{grid-template-columns:1fr}.hero h1{font-size:22px}}
</style>
</head>
<body>

<!-- 内测注册门 -->
<div id="gate">
  <div class="gate-card">
    <h3>全球健康数据库整合网页<span class="beta-tag">内测版</span></h3>
    <p class="sub">本平台处于内测阶段，登记后即可使用。信息仅用于内测身份识别与后续开通「变量查询 / 数据对接」功能。</p>
    <div class="field"><label>姓名 Name</label><input id="gName" placeholder="请输入真实姓名" autocomplete="name"></div>
    <div class="field"><label>机构 / 单位 Institution</label><input id="gOrg" placeholder="如：XX 大学公共卫生学院 / XX 医院" autocomplete="organization"></div>
    <div class="field"><label>邮箱 Email</label><input id="gMail" placeholder="you@example.com" autocomplete="email"></div>
    <div class="field"><label>邀请码 Invitation Code（选填）</label><input id="gRef" placeholder="如 GHD-7K2M，由邀请人提供"></div>
    <div class="field"><label>验证码 Verification Code</label>
      <div class="code-row"><input id="gCode" placeholder="6 位验证码"><button class="code-btn" id="gSend">获取验证码</button></div>
    </div>
    <button class="btn btn-primary" id="gSubmit" style="width:100%;margin-top:6px">注册并进入</button>
    <div class="gate-msg" id="gMsg"></div>
    <div class="gate-tip">内测阶段：验证码在页面直接生成并展示（正式版将发送至所填邮箱，并由服务端校验）。<br>
      <b>使用本平台请引用：</b>杜思娴. 全球健康数据库整合网页 [EB/OL]. 2026.<br>
      合作与引用联系：<a href="mailto:dusixian16@163.com">dusixian16@163.com</a></div>
  </div>
</div>

<!-- 数据库详情弹窗 -->
<div id="modal"><div class="modal-card">
  <button class="m-close" id="mClose">关闭 ✕</button>
  <div id="mBody"></div>
</div></div>

<header class="top">
  <div class="top-inner">
    <a class="brand" href="#top" title="回到顶部">
      <svg class="logo" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg">
        <defs><linearGradient id="lgA" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0%" stop-color="#0b3a72"/><stop offset="100%" stop-color="#12b3d6"/>
        </linearGradient></defs>
        <rect x="1.5" y="1.5" width="45" height="45" rx="12" fill="url(#lgA)"/>
        <ellipse cx="24" cy="13.5" rx="11" ry="4.3" fill="#eaf4ff" stroke="#7fd1ff" stroke-width="1.8"/>
        <path d="M13 13.5v14c0 2.4 4.9 4.3 11 4.3s11-1.9 11-4.3v-14" fill="#cfe9ff" stroke="#7fd1ff" stroke-width="1.8"/>
        <path d="M24 20.5v11M18.5 26h11" stroke="#0b3a72" stroke-width="3.2" stroke-linecap="round"/>
        <circle cx="38" cy="10" r="3.2" fill="#7fd1ff"/>
      </svg>
      <span>全球健康数据库整合网页<small>Global Health Database Integration Platform</small></span>
    </a>
    <nav>
      <a href="#query">匹配查询器</a>
      <a href="#legend">开放度</a>
      <a href="#overview">速查表</a>
      <select id="catJump" class="cat-jump" aria-label="按分类跳转">
        <option value="">分类跳转 ▾</option>
      </select>
      <a href="#ladder">实战阶梯</a>
      <a href="#links">官方入口</a>
      <a href="#varsearch">变量查询</a>
      <a href="#apply">申请材料</a>
      <a href="#tools">配套工具</a>
    </nav>
    <input class="search-box" id="globalSearch" placeholder="搜索数据库 / 主办 / 关键词…">
  </div>
</header>

<div class="hero" id="top">
  <div class="wrap">
    <div class="hero-inner">
      <svg class="logo-lg" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg">
        <defs><linearGradient id="lgB" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0%" stop-color="#0b3a72"/><stop offset="100%" stop-color="#12b3d6"/>
        </linearGradient></defs>
        <rect x="1.5" y="1.5" width="45" height="45" rx="12" fill="url(#lgB)"/>
        <ellipse cx="24" cy="13.5" rx="11" ry="4.3" fill="#eaf4ff" stroke="#7fd1ff" stroke-width="1.8"/>
        <path d="M13 13.5v14c0 2.4 4.9 4.3 11 4.3s11-1.9 11-4.3v-14" fill="#cfe9ff" stroke="#7fd1ff" stroke-width="1.8"/>
        <path d="M24 20.5v11M18.5 26h11" stroke="#0b3a72" stroke-width="3.2" stroke-linecap="round"/>
        <circle cx="38" cy="10" r="3.2" fill="#7fd1ff"/>
      </svg>
      <div style="flex:1;min-width:280px">
        <div>
          <span class="badge-src">AI for Health</span>
          <span class="badge-src">AI for Data Sharing</span>
          <span class="badge-src">内测版 Beta</span>
        </div>
        <h1>全球健康数据库整合网页<span class="beta-tag">BETA</span></h1>
        <p style="font-size:17px"><b>Global Health Database Integration Platform</b> — 全球健康与医学研究公共数据库的一站式检索、分类与申请导航。</p>
        <p><b>共收录 __TOTAL__ 个数据库与数据平台</b>：老龄追踪、生物样本库、中国本土队列、医保与电子病历（真实世界）、澳大利亚与大洋洲、重症 ICU、临床试验数据二次利用、组学仓储、卫生经济与卫生服务管理。</p>
        <div class="creator">创建人：<b>杜思娴</b> ｜ 合作与引用联系：<a href="mailto:dusixian16@163.com">dusixian16@163.com</a></div>
      </div>
    </div>
  </div>
</div>

<!-- 查询器 -->
<section id="query">
  <div class="wrap">
    <h2 class="sec"><span class="num">Q</span>研究匹配查询器</h2>
    <p class="sec-sub">描述你的科学问题，或点选条件，网站会锁定最匹配的数据库并给出「怎么做」的研究范式。</p>
    <div class="q-card">
      <div class="q-row">
        <div class="q-label">① 一句话描述你的科学问题（可留空，配合下方勾选）</div>
        <textarea class="q-text" id="qText" placeholder="例：我想研究中国老年人长期血压变化对肾功能下降的影响，需要前瞻队列和重复体检生化数据。"></textarea>
      </div>
      <div class="q-row">
        <div class="q-label">② 地区 / 人群</div>
        <div class="chip-row" id="grp-region">__REGION_CHIPS__</div>
      </div>
      <div class="q-row">
        <div class="q-label">③ 想要的数据类型</div>
        <div class="chip-row" id="grp-datatype">__DATATYPE_CHIPS__</div>
      </div>
      <div class="q-row">
        <div class="q-label">④ 研究设计 / 方法</div>
        <div class="chip-row" id="grp-design">__DESIGN_CHIPS__</div>
      </div>
      <div class="q-row">
        <div class="q-label">⑤ 主题 / 疾病领域</div>
        <div class="chip-row" id="grp-topic">__TOPIC_CHIPS__</div>
      </div>
      <div class="q-actions">
        <button class="btn btn-primary" id="qBtn">匹配数据库</button>
        <button class="btn btn-ghost" id="qReset">重置</button>
        <span class="hint">提示：条件越具体，匹配越准；也可直接写一句话让系统解析关键词。</span>
      </div>
    </div>
    <div id="qResult"><div class="q-empty">填写上方条件后点击「匹配数据库」，推荐结果将显示在这里。</div></div>
  </div>
</section>

<!-- 图例 -->
<section id="legend">
  <div class="wrap">
    <h2 class="sec"><span class="num">!</span>开放度分级（获取难度）</h2>
    <p class="sec-sub">★ 完全公开可直接下载 → ★★★★★ 必须本地合作（常含共同署名）。颜色由绿到红表示难度递增。</p>
    <div class="legend">__LEGEND__</div>
  </div>
</section>

<!-- 速查表 -->
<section id="overview">
  <div class="wrap">
    <h2 class="sec"><span class="num">1</span>总览速查表</h2>
    <p class="sec-sub">按 PDF 第 1 章分组，先快速定位「哪个库大概有什么、多难拿」。</p>
    __OVERVIEW__
  </div>
</section>

<!-- 分类卡片 -->
<section id="catalog">
  <div class="wrap">
    <h2 class="sec"><span class="num">2-12</span>分类目录（按研究性质 12 大类）</h2>
    <p class="sec-sub">点击下方分类跳转；卡片支持按「开放度」与「关键词」筛选（顶部搜索框全局可用）。</p>
    <div class="cat-nav" style="margin-bottom:6px">__CAT_NAV__</div>
    <div id="accFilter" class="chip-row" style="margin:10px 0 0">
      <button type="button" class="chip acc-chip on" data-acc="0">全部难度</button>
      <button type="button" class="chip acc-chip" data-acc="1">★ 公开</button>
      <button type="button" class="chip acc-chip" data-acc="2">★★ 注册</button>
      <button type="button" class="chip acc-chip" data-acc="3">★★★ 协议</button>
      <button type="button" class="chip acc-chip" data-acc="4">★★★★ 付费</button>
      <button type="button" class="chip acc-chip" data-acc="5">★★★★★ 合作</button>
    </div>
    <div id="cards"></div>
  </div>
</section>

<!-- 阶梯 -->
<section id="ladder">
  <div class="wrap">
    <h2 class="sec"><span class="num">13</span>按获取难度排列的实战阶梯</h2>
    <p class="sec-sub">新手常见错误是直接冲最难的库。合理路径：先用 ★★ 级把方法学跑通、选题验证掉，再去申请 ★★★★ 级。</p>
    <div class="ladder">
      <table>
        <thead><tr><th>级别</th><th>代表数据库</th><th>周期</th><th>费用</th></tr></thead>
        <tbody>__LADDER_ROWS__</tbody>
      </table>
    </div>
  </div>
</section>

<!-- 官方入口直达 -->
<section id="links">
  <div class="wrap">
    <h2 class="sec"><span class="num">L</span>官方入口直达（全部 __TOTAL__ 个库）</h2>
    <p class="sec-sub">按分类列出每个数据库的<b>全部官方链接</b>（官网 / 数据申请页 / 数据字典 / 检索入口），点名称可看详情。链接均经脚本核对，若某条失效请邮件告知 <a href="mailto:dusixian16@163.com">dusixian16@163.com</a>。</p>
    <div class="lk-wrap">__ALL_LINKS__</div>
  </div>
</section>

<!-- 变量查询 -->
<section id="varsearch">
  <div class="wrap">
    <h2 class="sec"><span class="num">V</span>变量查询（按指标反查数据库）</h2>
    <p class="sec-sub">输入你关心的<b>变量 / 指标</b>（如「肌酐」「eGFR」「血压」「PHQ-9」「MBS」），查看哪些数据库收录了该指标及其开放度——这是「提取变量」能力的第一层（元数据级）。</p>
    <div class="q-card" style="background:#fff;border-color:var(--line)">
      <div class="code-row">
        <input id="vInput" placeholder="例如：肌酐 / eGFR / 血压 / 抑郁 / PBS / 影像" style="border:1px solid var(--line);border-radius:10px;padding:9px 11px;font-size:15px">
        <button class="btn btn-primary" id="vBtn">查询变量</button>
      </div>
      <div class="hint" style="margin-top:8px">支持中英文关键词；结果为元数据级（依据各库公开的变量说明整理），具体变量名请以各库 codebook 为准。</div>
    </div>
    <div id="vResult" style="margin-top:16px"></div>
  </div>
</section>

<!-- 申请材料生成器 -->
<section id="apply">
  <div class="wrap">
    <h2 class="sec"><span class="num">A</span>申请材料生成器（一键生成研究计划草稿）</h2>
    <p class="sec-sub">选库 + 填几项基本信息，自动生成一份可直接投给数据管理方的<b>数据使用申请材料草稿</b>：研究摘要、变量需求清单、伦理与合规声明、申请步骤 checklist、致谢与数据可用性声明。生成后可复制或下载 Markdown，再按各库要求微调。</p>
    <div class="q-card" style="background:#fff;border-color:var(--line)">
      <div class="ap-grid">
        <div><label>目标数据库</label><select id="apDb"></select></div>
        <div><label>申请人姓名</label><input id="apName" placeholder="张三"></div>
        <div><label>机构 / 单位</label><input id="apOrg" placeholder="XX 大学公共卫生学院"></div>
        <div><label>联系邮箱</label><input id="apMail" placeholder="you@example.com"></div>
      </div>
      <div class="ap-grid" style="margin-top:12px">
        <div><label>项目 / 论文题目</label><input id="apTitle" placeholder="中国中老年人血压轨迹与肾功能下降的前瞻性研究"></div>
        <div><label>研究设计</label>
          <select id="apDesign">
            <option>前瞻性队列研究</option>
            <option>回顾性队列 / 真实世界研究</option>
            <option>横断面研究</option>
            <option>重复横断面 / 趋势分析</option>
            <option>病例对照研究</option>
            <option>预测模型开发与验证</option>
            <option>基因组 / 多组学关联分析</option>
            <option>IPD 荟萃分析</option>
            <option>卫生经济 / 政策评估</option>
          </select>
        </div>
        <div><label>计划申请时间</label><input id="apWhen" placeholder="如 2026 年 11 月"></div>
        <div><label>经费 / 预算</label><input id="apFee" placeholder="如 无 / 约 £6000 / 待定"></div>
      </div>
      <div class="ap-grid" style="margin-top:12px">
        <div style="grid-column:1/-1"><label>研究问题（一句话，含人群 + 暴露 + 结局）</label>
          <textarea id="apQ" placeholder="在我国 45 岁及以上人群中，长期血压变异性是否与 eGFR 下降速度独立相关。"></textarea></div>
        <div style="grid-column:1/-1"><label>拟用变量 / 数据字段（可从右侧提示复制）</label>
          <textarea id="apVars" placeholder="血压（多轮实测）、血肌酐、胱抑素C、eGFR、年龄、性别、BMI、吸烟、饮酒、基线慢病、用药"></textarea></div>
      </div>
      <div class="q-actions">
        <button class="btn btn-primary" id="apBtn">生成申请材料</button>
        <button class="btn btn-ghost" id="apReset">清空</button>
        <span class="hint">草稿为通用模板，[XXXXX] 处需替换为你的伦理批件号与批准编号。</span>
      </div>
    </div>
    <div id="apOut" class="ap-out"></div>
  </div>
</section>

<!-- 配套工具 -->
<section id="tools">
  <div class="wrap">
    <h2 class="sec"><span class="num">T</span>配套工具（学术润色与检测）</h2>
    <p class="sec-sub">找完库、拿完数据，下一步是写。下面两个是本平台同作者的自研工具，免费开源、文本只在本机处理，点开即用。</p>
    <div class="tool-grid">
      <a class="tool-card" href="https://naturedu.github.io/tracehonest/" target="_blank" rel="noopener">
        <div class="tool-tag">学术润色 · 中英双语</div>
        <h3>普贤（Puxian）· AI 学术检查助手</h3>
        <p>以 <b>中文 / English 检测</b>为主线：6 项指标加权打分，每一项都列出「你的值 / 参考区间 / 得分」，可复核；同时做简洁化润色（标点规范、去冗余、破折号统一、长句提示）。检测是概率性提示、不是结论，也不提供规避检测的功能。</p>
        <span class="tool-go">打开普贤 →</span>
      </a>
      <a class="tool-card" href="https://naturedu.github.io/tracehonest/papers.html" target="_blank" rel="noopener">
        <div class="tool-tag">语料 · 中英对照 100 篇</div>
        <h3>CSSCI 论文语料库</h3>
        <p>《中国社会科学》《管理世界》《社会科学》2026 年最新三期共 100 篇，中文摘要与英文题名逐条对照，可按「中英对照 / 中文 / English」浏览检索，一键送入润色与检测工作台。</p>
        <span class="tool-go">打开语料库 →</span>
      </a>
    </div>
    <div class="hint" style="margin-top:10px">
      引用：杜思娴. 普贤（Puxian）：AI 学术检查助手 [EB/OL]. (2026). https://naturedu.github.io/tracehonest/.
    </div>
  </div>
</section>

<!-- 引用与联系 -->
<section id="cite">
  <div class="wrap">
    <h2 class="sec"><span class="num">C</span>引用与联系（使用本站请务必引用）</h2>
    <p class="sec-sub">若您在论文、报告或标书中使用了本平台的检索与推荐结果，请引用本平台，并欢迎邮件联系合作。</p>
    <div class="cite-box">
      <div style="background:#fff4e5;border:1px solid #f6d9a0;border-radius:10px;padding:11px 14px;margin-bottom:14px;color:#8a5a00;font-size:14px">
        <b>重要：</b>凡使用「全球健康数据库整合网页 / Global Health Database Integration Platform」的检索、匹配或变量查询功能产出成果者，请按下方格式引用，并将合作/咨询邮件发送至 <a href="mailto:dusixian16@163.com" style="color:#b45309"><b>dusixian16@163.com</b></a>。
      </div>
      <button class="copy-btn" data-copy="cn">复制中文引用（GB/T 7714）</button>
      <div class="cite-pre" id="citeCn">__CITE_CN__</div>
      <button class="copy-btn" data-copy="en">复制英文引用（APA 7th）</button>
      <div class="cite-pre" id="citeEn">__CITE_EN__</div>
      <button class="copy-btn" data-copy="en2">复制英文引用（Vancouver / 数字式）</button>
      <div class="cite-pre" id="citeEn2">__CITE_EN2__</div>
      <button class="copy-btn" data-copy="bib">复制 BibTeX</button>
      <div class="cite-pre" id="citeBib">__CITE_BIB__</div>
      <div style="margin-top:10px;font-size:13.5px;color:var(--muted)">
        <b>正文夹注</b>：英文写作 <span class="hl">(Du, 2026)</span> 或 <span class="hl">Du (2026)</span>；
        中文写作 <span class="hl">（杜思娴，2026）</span>。Vancouver 体系按序号引用即可。
      </div>
      <div style="margin-top:12px;font-size:14px;color:var(--muted)">
        创建人：<b>杜思娴</b> ｜ 邮箱：<a href="mailto:dusixian16@163.com"><b>dusixian16@163.com</b></a>
      </div>
    </div>

    <!-- 邀请同行 -->
    <div class="cite-box" style="margin-top:18px">
      <h3 style="margin:0 0 6px;color:var(--primary-d);font-size:17px">邀请同行使用</h3>
      <p style="font-size:13.5px;color:var(--muted);margin:0 0 4px">
        内测期靠邀请扩散。生成你的专属邀请码与链接，发给同学 / 同事；对方注册时填入邀请码，即视为你邀请。
      </p>
      <div class="inv-row">
        <button class="btn-mini" id="invGen">生成我的邀请码 / 链接</button>
        <button class="btn-mini" id="invCopyText" style="display:none">复制邀请文案</button>
        <span id="invHint" style="font-size:12.5px;color:var(--muted)">（邀请码由你的邮箱生成，同一邮箱始终一致）</span>
      </div>
      <div id="invOut" style="margin-top:10px"></div>
    </div>

    <!-- 本机数据管理 -->
    <div class="cite-box" style="margin-top:14px">
      <h3 style="margin:0 0 6px;color:var(--primary-d);font-size:17px">本机数据管理</h3>
      <p style="font-size:13.5px;color:var(--muted);margin:0 0 8px">
        注册信息、邀请码、对比篮都只存在<b>本机浏览器</b>，不上传服务器（内测版无后端）。可导出留存或一键清除。
      </p>
      <div class="inv-row">
        <button class="btn-mini" id="dmExport">导出本机登记记录（CSV）</button>
        <button class="btn-mini" id="dmStats">查看本机统计</button>
        <button class="btn-mini" id="dmClear" style="color:#b42318;border-color:#f3c2bd">清除本机全部数据</button>
        <button class="btn-mini" id="dmPrint">打印 / 另存为 PDF</button>
      </div>
      <div id="dmOut" style="margin-top:10px;font-size:13px;color:var(--ink)"></div>
    </div>
  </div>
</section>

<footer>
  <div class="wrap">
    <b style="color:#eaf4ff">免责声明（据原 PDF）</b>
    <div class="disclaim">
      <p>本文件内容来自已有知识整理，<b>编制过程中没有联网核验</b>。各库近年频繁迁移入口（如 UK Biobank 已迁至云平台、SEER 更换过申请流程），<b>引用或投稿前请实点核对官网</b>。</p>
      <p>标注「<b>待核</b>」的条目表示把握不足，宁可留白也不虚构；只能给近似值的写作「约」。中国本土队列绝大多数不公开下载、走合作制——这不完全是缺点：正因为有门槛，选题被做烂的概率低，比拼的是选题质量与合作关系。</p>
      <p>本网站为基于该 PDF 的结构化导航与检索工具，<b>不构成任何数据库的官方入口或申请承诺</b>；具体申请流程、伦理审查与数据使用协议请以各平台官方说明为准。</p>
    </div>
    <p style="margin-top:14px;font-size:13px">创建人：<b>杜思娴</b> ｜ 联系：<a href="mailto:dusixian16@163.com">dusixian16@163.com</a></p>
    <p style="margin-top:6px">© 2026 全球健康数据库整合网页 · Global Health Database Integration Platform ｜ 数据来源：用户提供的 PDF + 联网核实</p>
  </div>
</footer>

<!-- 对比弹层 -->
<div id="cmp"><div class="cmp-card">
  <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:12px">
    <div><h3>数据库对比</h3><div style="font-size:13px;color:var(--muted)">同一维度横向比较，避免「看着都差不多」。</div></div>
    <button class="btn-mini" id="cmpClose">关闭 ✕</button>
  </div>
  <div id="cmpBody"></div>
</div></div>

<!-- 对比浮动条 -->
<div class="cmp-bar" id="cmpBar">
  <span>对比篮 <b id="cmpN">0</b>/4：</span>
  <span id="cmpTags"></span>
  <button id="cmpGo">开始对比</button>
  <button class="clr" id="cmpClear">清空</button>
</div>

<div id="toast"></div>

<script>
const DB = __DB_JSON__;
const CATS = __CATS_JSON__;
const ACCESS = __ACCESS_JSON__;

// ---------- 渲染分类卡片 ----------
function esc(s){return (s||"").replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));}

function cardHTML(d){
  let links = (d.urls||[]).map((u,i)=>{
    const cls = i===0?'':' alt';
    return `<a class="${cls.trim()}" href="${u.url}" target="_blank" rel="noopener">${esc(u.label)} ↗</a>`;
  }).join("");
  let tags = (d.tags||[]).slice(0,10).map(t=>`<span class="tag">${esc(t)}</span>`).join("");
  let kv = "";
  if(d.region) kv += `<div class="kv"><b>地区：</b>${esc(d.region)}</div>`;
  if(d.scale) kv += `<div class="kv"><b>规模：</b>${esc(d.scale)}</div>`;
  if(d.timeSpan) kv += `<div class="kv"><b>时间：</b>${esc(d.timeSpan)}</div>`;
  if(d.host) kv += `<div class="kv"><b>主办：</b>${esc(d.host)}</div>`;
  if(d.content) kv += `<div class="kv"><b>核心内容：</b>${esc(d.content)}</div>`;
  let usage = d.usage?`<div class="usage"><b>使用情况：</b>${esc(d.usage)}</div>`:"";
  let notes = d.notes?`<div class="notes"><b>常见坑：</b>${esc(d.notes)}</div>`:"";
  return `<div class="card" data-cat="${d.cat}" data-acc="${d.access}" data-text="${esc((d.name+' '+d.en+' '+d.host+' '+d.intro+' '+d.content+' '+(d.tags||[]).join(' ')).toLowerCase())}">
    <h4>${esc(d.name)}</h4>
    <div class="en">${esc(d.en)}</div>
    <span class="acc stars s${d.access}">${ACCESS[d.access]}</span>
    ${kv}
    ${d.indicators?`<div class="ind"><b>经典指标：</b>${esc(d.indicators)}</div>`:""}
    ${d.intro?`<div class="intro">${esc(d.intro)}</div>`:""}
    ${usage}${notes}
    <div class="tagrow">${tags}</div>
    <div class="links">${links}<button class="detail-btn" data-nm="${esc(d.name)}">查看详情 / 申请方式</button><label class="cmp-chk" title="加入对比篮（最多 4 个）"><input type="checkbox" class="cmp-box" data-nm="${esc(d.name)}">对比</label></div>
  </div>`;
}

function renderCards(){
  const root=document.getElementById('cards');
  let html="";
  CATS.forEach(([k,label],idx)=>{
    const list=DB.filter(d=>d.cat===k);
    if(!list.length)return;
    html+=`<div class="cat-block" id="cat-${k}"><div class="cat-head"><h3>${idx+1}. ${esc(label)}</h3><span class="cnt">${list.length} 个</span></div><div class="grid">`;
    html+=list.map(cardHTML).join("");
    html+=`</div></div>`;
  });
  root.innerHTML=html;
}
renderCards();

// ---------- 全局搜索 + 难度筛选 ----------
let accFilter=0;
document.getElementById('accFilter').addEventListener('click',e=>{
  const b=e.target.closest('.acc-chip'); if(!b)return;
  document.querySelectorAll('.acc-chip').forEach(x=>x.classList.remove('on'));
  b.classList.add('on'); accFilter=+b.dataset.acc; applyFilter();
});
document.getElementById('globalSearch').addEventListener('input',applyFilter);
function applyFilter(){
  const q=document.getElementById('globalSearch').value.trim().toLowerCase();
  document.querySelectorAll('.card').forEach(c=>{
    const okAcc = accFilter===0 || +c.dataset.acc===accFilter;
    const okQ = !q || c.dataset.text.includes(q);
    c.style.display=(okAcc&&okQ)?'':'none';
  });
  // 隐藏空分类
  document.querySelectorAll('.cat-block').forEach(b=>{
    const vis=b.querySelectorAll('.card:not([style*="display: none"])').length;
    b.style.display=vis?'':'none';
  });
}

// ---------- 查询器 ----------
const sel={region:[],datatype:[],design:[],topic:[]};
document.querySelectorAll('.chip[data-group]').forEach(ch=>{
  ch.addEventListener('click',()=>{
    const g=ch.dataset.group,v=ch.dataset.val;
    const arr=sel[g];const i=arr.indexOf(v);
    if(i>=0){arr.splice(i,1);ch.classList.remove('on');}
    else{arr.push(v);ch.classList.add('on');}
  });
});
// 把引导选项映射到库 tags 的关键词
const MAP={
  region:{'中国':['中国'],'美国':['美国'],'欧洲':['欧洲'],'英国':['英国'],'韩国':['韩国'],'日本':['日本'],'港台':['香港','台湾'],'墨西哥':['墨西哥'],'印度':['印度'],'北欧':['北欧'],'多国/国际':['全球','国际','多国']},
  datatype:{'问卷/自报':['问卷','自报','量表'],'客观体检/生化':['体检','生化','肌酐','血压','检验'],'基因/多组学':['基因','组学','测序','转录组','多组学'],'电子病历/医保':['电子病历','医保','理赔','处方','真实世界'],'影像':['影像'],'死亡登记/随访':['死亡登记','随访'],'文本/NLP':['文本','NLP']},
  design:{'前瞻性队列':['前瞻性','队列'],'回顾性/横断面':['横断面','回顾性'],'RCT 数据二次利用':['RCT','二次利用','IPD'],'真实世界观察性':['真实世界','观察性','目标试验'],'预测模型':['预测模型','风险'],'IPD 荟萃':['IPD','meta'],'重复横断面':['重复横断面']},
  topic:{'老龄与认知':['老龄','认知','痴呆','失能','长寿','衰弱'],'心血管与肾脏':['心血管','肾脏','高血压','CKD','卒中','心衰','eGFR'],'肿瘤':['肿瘤','癌症'],'营养与代谢':['营养','膳食','代谢','肥胖','糖尿病'],'职业与环境':['职业','暴露','环境'],'精神心理/行为':['心理','抑郁','焦虑','睡眠','行为'],'卫生经济与卫生服务':['卫生经济','卫生服务','费用','医疗质量','医保'],'重症/ICU':['ICU','重症'],'妇幼与儿童':['儿童','妇幼','儿科','青少年'],'遗传/组学':['基因','组学','遗传'],'罕见病':['罕见病'],'卫生政策/公平':['政策','公平','社会']}
};
document.getElementById('qReset').addEventListener('click',()=>{
  Object.keys(sel).forEach(k=>sel[k]=[]);
  document.querySelectorAll('.chip[data-group]').forEach(c=>c.classList.remove('on'));
  document.getElementById('qText').value='';
  document.getElementById('qResult').innerHTML='<div class="q-empty">已重置。填写条件后点击「匹配数据库」。</div>';
});
document.getElementById('qBtn').addEventListener('click',runQuery);

function tokenize(text){
  // 中英混合：拆中文 2-gram + 英文单词
  const out=[];
  const cn=text.match(/[一-龥]{2,}/g)||[];
  cn.forEach(w=>{out.push(w); if(w.length>2){out.push(w.slice(0,2));out.push(w.slice(1,3));}});
  const en=text.toLowerCase().match(/[a-z]{2,}/g)||[];
  en.forEach(w=>out.push(w));
  return out;
}
function paradigmTemplate(d){
  let design='观察性研究';
  if(d.cat==='trial') design='RCT / 经典队列数据二次利用（IPD）';
  else if(d.cat==='icu'||d.cat==='rwd') design='真实世界观察性研究（新使用者设计 / 目标试验模拟 / 队列）';
  else if(d.cat==='omics') design='功能基因组 / 组学分析（差异 + 整合 + 批次校正）';
  else if(d.access>=4) design='需正式申请 / 本地合作的前瞻性队列研究';
  else design='前瞻性或重复测量队列研究';
  const stat='队列→Cox 比例风险 / 广义线性模型 / 轨迹（潜类别增长）；横断面→Logistic / 线性回归；预测→C-index、校准曲线、决策曲线、NRI/IDI；荟萃→IPD 合并与异质性。';
  let ethic='';
  if(d.access<=2) ethic='注册账号即可获取；常规科研伦理审查（如涉及）按所在单位要求办理。';
  else if(d.access===3) ethic='完成指定培训（如 CITI）并取得证书 + 签署数据使用协议（DUA），部分需伦理批件或豁免。';
  else if(d.access===4) ethic='正式提交研究计划、机构审批并付费；受控数据还需机构签署官员(ISO)与 DAC 评审。';
  else ethic='必须本地合作 + 机构 PI + 伦理委员会批件；数据通常不可下载，在指定安全环境分析。';
  return `<div class="template-box"><h4>通用研究范式模板（可套用于本站的任一数据库）</h4>
   <table>
     <tr><td>研究问题 PICO</td><td>在 <b>${esc(d.region||'目标人群')}</b> 中，探讨【暴露 X】与【结局 Y】的关系——按你的科学问题替换占位。</td></tr>
     <tr><td>推荐数据库</td><td><b>${esc(d.name)}</b>（${esc(d.en)}）</td></tr>
     <tr><td>研究设计</td><td>${design}</td></tr>
     <tr><td>关键变量</td><td>${esc(d.content||'参见数据库说明书 / codebook')}</td></tr>
     <tr><td>统计方法</td><td>${stat}</td></tr>
     <tr><td>数据申请</td><td>${esc(d.usage||'—')}</td></tr>
     <tr><td>伦理 / 合规</td><td>${esc(ethic)}</td></tr>
     <tr><td>注意事项</td><td>${esc(d.notes||'遵守数据库数据使用协议，禁止再识别；发表须注明数据来源。')}</td></tr>
     <tr><td>论文致谢模板</td><td>${esc(d.ackEn||'')}<br><span style="color:#8a7a4a">${esc(d.ackCn||'')}</span></td></tr>
     <tr><td>本站引用</td><td>${esc(d.ackEn?'发表时请同时引用本平台：Dusixian. Global Health Database Integration Platform [EB/OL]. 2026.':'')}</td></tr>
   </table></div>`;
}
function recHTML(it, locked){
  const d=it.d;
  const mtags=it.reasons.map(r=>`<span class="match-tags">${esc(r)}</span>`).join("");
  const links=(d.urls||[]).map(u=>`<a href="${u.url}" target="_blank" rel="noopener">${esc(u.label)} ↗</a>`).join("");
  const para=d.paradigm?`<div class="para"><b>参考范式：</b>${esc(d.paradigm)}</div>`:"";
  const usage=d.usage?`<div class="meta">使用情况：${esc(d.usage)}</div>`:"";
  const badge=locked?`<span style="background:#e98ab0;color:#fff;font-size:11px;padding:1px 8px;border-radius:10px;margin-left:6px">已锁定</span>`:"";
  return `<div class="rec ${locked?'locked':''}">
    <h4>${esc(d.name)} <span class="en" style="font-size:11px;color:#a98ca0">${esc(d.en)}</span>${badge}</h4>
    <div class="meta stars s${d.access}">${ACCESS[d.access]} · ${esc(d.region||'')} · ${esc(d.scale||'')}</div>
    <div class="why"><b>匹配理由：</b>${mtags||'关键词命中'}</div>
    ${usage}${para}
    <div style="margin-top:8px">${links}</div>
  </div>`;
}
// 标签词频 → 权重（"队列""中国""公开"这类泛词几乎人人都有，权重必须压低）
const TAGFREQ={};
DB.forEach(d=>{ [...new Set(d.tags||[])].forEach(t=>{TAGFREQ[t]=(TAGFREQ[t]||0)+1;}); });
function tagW(t){const f=TAGFREQ[t]||1;return f<=6?3:(f<=15?2:1);}
// 同义词 / 具体病名 → 数据里真实存在的标签词
const SYN={"肾功能":"肾脏","肾病":"肾脏","慢性肾脏病":"肾脏","CKD":"肾脏","中风":"卒中","脑卒中":"卒中","心梗":"心血管","冠心病":"心血管","心肌梗死":"心血管","血糖":"糖尿病","肥胖":"代谢","老年人":"老龄","老年":"老龄","长者":"老龄","重症监护":"重症","精神":"心理","癌症":"肿瘤"};
const DISEASE={"子宫内膜异位症":["女性","妇科"],"妇科":["女性","妇科"],"卵巢":["女性","妇科"],"月经":["女性","妇科"],"妊娠":["妇幼","孕产妇","孕产"],"不孕":["女性","妇幼"],"孕产":["妇幼","孕产妇"],"肺癌":["肿瘤","癌症"],"胃癌":["肿瘤","癌症"],"肝癌":["肿瘤","癌症"],"结直肠癌":["肿瘤","癌症"],"乳腺癌":["肿瘤","癌症"],"食管癌":["肿瘤","癌症"],"宫颈癌":["肿瘤","癌症"],"前列腺癌":["肿瘤","癌症"],"淋巴瘤":["肿瘤","癌症"],"白血病":["肿瘤","癌症"],"癌":["肿瘤","癌症"],"糖尿病":["代谢","糖尿病","血糖"],"高血压":["血压","高血压","心血管"],"卒中":["卒中","脑血管"],"脓毒症":["脓毒症","感染","重症"],"感染性休克":["脓毒症","感染","重症"],"脑梗":["卒中","脑血管"],"脑出血":["卒中","脑血管"],"心衰":["心血管","心衰"],"心力衰竭":["心血管","心衰"],"肾功能":["肾脏","eGFR"],"肾衰":["肾脏","ESRD"],"透析":["肾脏","ESRD","透析"],"痴呆":["认知","痴呆"],"阿尔茨海默":["认知","痴呆","神经"],"抑郁":["心理","抑郁"],"焦虑":["心理","焦虑"],"心理健康":["心理健康","心理"],"睡眠":["睡眠","行为"],"生活方式":["生活方式","膳食","运动"],"肥胖":["肥胖","代谢"],"营养":["营养","膳食"],"膳食":["膳食","营养"],"空气污染":["环境","暴露"],"环境":["环境","暴露"],"职业":["职业","暴露"],"粉尘":["职业","暴露"],"生存分析":["随访","死亡登记","癌症登记","登记"],"预后":["随访","死亡登记"],"发病率":["登记","癌症登记","监测"],"死亡":["死亡登记","随访"],"医保":["医保","理赔"],"报销":["医保","理赔"],"费用":["费用","医疗支出"],"灾难性卫生支出":["灾难性卫生支出"],"健康公平":["公平","健康不平等"],"影像":["影像"],"基因":["基因"],"基因组":["基因","基因组"],"测序":["测序"],"单细胞":["单细胞"],"蛋白组":["蛋白组"],"代谢组":["代谢组"],"儿童":["儿童","儿科"],"儿科":["儿童","儿科"],"青少年":["儿童","青少年"],"妇幼":["妇幼","儿童"],"孕产妇":["妇幼"],"罕见病":["罕见病"],"孤儿药":["罕见病"],"失能":["失能"],"衰弱":["衰弱","老龄"],"肌少症":["肌少症","老龄"],"多病共存":["多病共存","慢病"],"慢病":["慢病"],"共病":["多病共存","慢病"],"预测模型":["预测模型","风险"],"机器学习":["预测模型","风险"],"出生队列":["出生队列","妇幼","儿童"],"抑郁症状":["心理","抑郁"]};
const LEXV=["肌酐","eGFR","胱抑素","尿蛋白","UACR","血压","血糖","血脂","糖化血红蛋白","生化","体检","基因","WGS","RNA-seq","单细胞","甲基化","蛋白组","代谢组","影像","MRI","CT","死亡登记","随访","医保","理赔","处方","住院","费用","透析","罕见病","量表"];
const INTENT=[["有哪些",["目录","平台","元数据"]],["哪些",["目录","平台"]],["平台",["平台","目录"]],["目录",["目录","平台"]],["汇总",["目录","平台"]],["清单",["目录","平台"]],["对比",["目录","平台"]]];
function expandQ(q){
  let out=(q||"").toLowerCase(), extra=[];
  for(const k in SYN){ if(out.includes(k.toLowerCase())) extra.push(SYN[k]); }
  for(const k in DISEASE){ if(out.includes(k.toLowerCase())) extra.push(...DISEASE[k]); }
  INTENT.forEach(([k,vs])=>{ if(out.includes(k)) extra.push(...vs); });
  return out+" "+extra.join(" ");
}

function runQuery(){
  const qtext=document.getElementById('qText').value.trim();
  const qx=expandQ(qtext);
  const qraw=qtext.toLowerCase();
  const scored=[];
  DB.forEach(d=>{
    let score=0; const reasons=new Set();
    const tags=[...new Set(d.tags||[])];
    // 1) 标签命中（按词频加权）
    tags.forEach(t=>{
      if(t.length>=2 && (qx.includes(t)||qx.includes(t.slice(0,2)))){score+=tagW(t);reasons.add(t);}
    });
    // 2) 该库确实拥有这个问题里的变量
    const ind=((d.indicators||"")+" "+(d.content||"")).toLowerCase();
    LEXV.forEach(v=>{
      const vl=v.toLowerCase();
      if(qx.includes(vl)&&ind.includes(vl)){score+=2;reasons.add(v);}
    });
    // 3) 勾选条件
    ['region','datatype','design','topic'].forEach(g=>{
      sel[g].forEach(sv=>{
        (MAP[g][sv]||[]).forEach(kw=>{
          if(tags.some(t=>t.includes(kw)||kw.includes(t))){score+=2;reasons.add(sv);}
        });
      });
    });
    // 4) 用户直接点名某个库（库名、英文缩写或中文片段出现在问题里）
    if(qraw.length>=2 && ((d.name||"").toLowerCase().includes(qraw)||((d.en||"").toLowerCase().includes(qraw)))){
      score+=8;reasons.add("名称命中");
    } else if((d.alias||[]).some(a=>a.length>=3&&qraw.includes(a))){
      score+=6;reasons.add("名称命中");
    }
    if(score>0)scored.push({d,score,reasons:[...reasons].slice(0,8)});
  });
  scored.sort((a,b)=>b.score-a.score);
  const res=document.getElementById('qResult');
  if(!scored.length){
    res.innerHTML='<div class="q-empty">没有匹配的数据库。试着放宽条件，或在①里用一句话描述科学问题（如「中国老人 血压 肾功能 队列」）。</div>';
    return;
  }
  const top=scored.slice(0,6);
  const locked=top[0];
  let html=`<div class="q-empty" style="background:#fff5fa;border-color:#f6d9ea;color:#9c5b7e">已为你 <b>锁定 1 个主推数据库</b>（匹配度最高），附「参考范式」与备选；下方「通用研究范式模板」可套用于本站任一数据库。</div>`;
  html+=recHTML(locked,true);
  if(top.length>1){
    html+=`<div style="margin:14px 0 6px;font-weight:700;color:#b56a8e;font-size:13.5px">备选数据库（${top.length-1}）</div>`;
    top.slice(1).forEach(it=>html+=recHTML(it,false));
  }
  html+=paradigmTemplate(locked.d);
  res.innerHTML=html;
  res.scrollIntoView({behavior:'smooth',block:'nearest'});
}

// ---------- 详情弹窗：介绍 + 网址 + 申请方式 + 变量申请情况 ----------
function varAccessText(d){
  const a=d.access;
  if(a===1) return '变量级数据可公开获取：无需申请，直接下载；个体级记录通常可在遵守许可（如 CC0/CC-BY）下使用，发表须引用来源。';
  if(a===2) return '注册账号并说明用途后即可下载变量级数据（免费）；部分受限变量需额外协议。建议先下载官方 codebook / Data Dictionary 核对变量名。';
  if(a===3) return '需完成指定培训（如 CITI）并取得证书、签署数据使用协议（DUA）后方可获取变量级数据；通常在安全环境或经授权账号下载，周期约 2-6 周，免费。';
  if(a===4) return '需正式提交研究计划、机构审批并付费；按获批的变量字段范围提供数据（部分库按字段计费）。受控数据还需机构签署官员(ISO)与 DAC 评审。周期约 1-6 个月。';
  return '不公开下载，走合作制：需联系数据持有团队、提交研究方案、通常涉及共同署名；变量级数据（个体记录）须在合作框架内获取，周期半年起。';
}
function openModalByName(nm){
  const d=DB.find(x=>x.name===nm); if(d) openModal(d);
}
let currentDB=null;
function openModal(d){
  currentDB=d;
  const cells=[['开放度',ACCESS[d.access]],
    ['地区',d.region||'—'],['规模',d.scale||'—'],
    ['时间跨度',d.timeSpan||'—'],['主办单位',d.host||'—']]
    .map(([k,v])=>`<div class="m-cell"><b>${k}</b>${esc(v)}</div>`).join("");
  const ind=d.indicators?`<div class="ind"><b>${esc(d.indicators)}</b></div>`
    :`<p style="color:var(--muted)">本条目未整理指标清单，请以官网 codebook / Data Dictionary 为准。</p>`;
  const papers=(d.papers&&d.papers.length)?`<ul>${d.papers.map(p=>`<li>${esc(p)}</li>`).join("")}</ul>`
    :`<p style="color:var(--muted)">建议在官网 Publications / Data Users 页面核对代表性文献。</p>`;
  const links=(d.urls||[]).map(u=>`<a href="${u.url}" target="_blank" rel="noopener" style="margin-right:14px;font-weight:700">${esc(u.label)} ↗</a>`).join("");
  document.getElementById('mBody').innerHTML=`
    <h3>${esc(d.name)}</h3>
    <div class="m-en">${esc(d.en)}</div>
    <div class="m-grid">${cells}</div>
    <h5>数据库介绍</h5><p>${esc(d.intro||d.content||'—')}</p>
    <h5>核心内容</h5><p>${esc(d.content||'—')}</p>
    <h5>经典指标 / 主要变量</h5>${ind}
    <h5>注册与申请方式（流程 / 费用 / 周期）</h5><p>${esc(d.usage||'—')}</p>
    <h5>变量申请情况</h5><p>${esc(varAccessText(d))}</p>
    <h5>官方入口直达</h5><p>${links}</p>
    <h5>代表性 / 里程碑文献（建议核对官网 Publications）</h5>${papers}
    <p style="margin-top:10px"><a href="${d.pubmed}" target="_blank" rel="noopener">在 PubMed 检索该数据库相关研究 ↗</a></p>
    <h5>论文致谢 / 数据可用性声明模板（[XXXXX] 处填你的批准项目编号）</h5>
    <div class="cite-pre" id="mAckEn">${esc(d.ackEn||'')}</div>
    <div class="cite-pre" id="mAckCn">${esc(d.ackCn||'')}</div>
    <button class="copy-btn" id="mAckCopy">复制英文致谢</button>
    <button class="btn-mini" id="mAckCopyCn">复制中文致谢</button>
    <div style="margin-top:12px;display:flex;gap:8px;flex-wrap:wrap">
      <button class="btn-mini" id="mCopyLink">复制本库链接</button>
      <button class="btn-mini" id="mExport">导出本库为 Markdown</button>
      <button class="btn-mini" id="mApply">用此库生成申请材料</button>
      <button class="btn-mini" id="mAddCmp">加入对比</button>
    </div>
    <p style="margin-top:8px;color:var(--muted);font-size:13px">提示：发表时请<b>同时</b>引用本平台（见页面「引用与联系」区），并按各库要求注明版本号与数据来源。</p>
    ${d.notes?`<h5>常见坑 / 注意事项</h5><p>${esc(d.notes)}</p>`:""}
    ${d.paradigm?`<h5>研究范式建议</h5><div style="color:#0f5f6b;background:#e6fbfd;border:1px solid #b6e6ee;padding:9px 11px;border-radius:10px;font-size:14px">${esc(d.paradigm)}</div>`:""}
  `;
  document.getElementById('modal').style.display='flex';
  document.body.style.overflow='hidden';
  try{history.replaceState(null,'','?db='+encodeURIComponent(d.name));}catch(e){}
}
document.getElementById('mClose').onclick=closeModal;
document.getElementById('modal').onclick=e=>{if(e.target.id==='modal')closeModal();};
function closeModal(){
  document.getElementById('modal').style.display='none';
  document.body.style.overflow='';
  currentDB=null;
  try{history.replaceState(null,'',location.pathname+location.hash);}catch(e){}
}
document.addEventListener('click',e=>{
  const b=e.target.closest('.detail-btn'); if(b){openModalByName(b.dataset.nm);return;}
  const r=e.target.closest('.ov-row'); if(r){openModalByName(r.dataset.nm);}
});

// ---------- 内测注册门（姓名 / 邮箱 / 验证码） ----------
let sentCode='';
const gMsg=document.getElementById('gMsg');
function mailOK(m){return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(m);}
document.getElementById('gSend').onclick=function(){
  const m=document.getElementById('gMail').value.trim();
  if(!mailOK(m)){gMsg.className='gate-msg err';gMsg.textContent='请先填写有效的邮箱地址。';return;}
  sentCode=String(Math.floor(100000+Math.random()*900000));
  gMsg.className='gate-msg ok';
  gMsg.innerHTML='验证码已生成（内测演示）：<b>'+sentCode+'</b>　正式版将发送至 '+esc(m);
  let left=60;const btn=this;btn.disabled=true;btn.textContent=left+'s 后重发';
  const t=setInterval(()=>{left--;if(left<=0){clearInterval(t);btn.disabled=false;btn.textContent='获取验证码';}else{btn.textContent=left+'s 后重发';}},1000);
};
document.getElementById('gSubmit').onclick=()=>{
  const n=document.getElementById('gName').value.trim();
  const o=document.getElementById('gOrg').value.trim();
  const m=document.getElementById('gMail').value.trim();
  const c=document.getElementById('gCode').value.trim();
  const r=(document.getElementById('gRef').value||'').trim().toUpperCase();
  if(!n){gMsg.className='gate-msg err';gMsg.textContent='请填写姓名。';return;}
  if(!o){gMsg.className='gate-msg err';gMsg.textContent='请填写所在机构 / 单位。';return;}
  if(!mailOK(m)){gMsg.className='gate-msg err';gMsg.textContent='请填写有效的邮箱地址。';return;}
  if(!sentCode){gMsg.className='gate-msg err';gMsg.textContent='请先点击「获取验证码」。';return;}
  if(c!==sentCode){gMsg.className='gate-msg err';gMsg.textContent='验证码不正确，请重新输入。';return;}
  const rec={name:n,org:o,mail:m,ref:r||'',invite:inviteCode(m),ts:Date.now()};
  try{
    localStorage.setItem('ghdip_user',JSON.stringify(rec));
    const all=JSON.parse(localStorage.getItem('ghdip_users')||'[]');
    if(!all.some(x=>x.mail&&x.mail.toLowerCase()===m.toLowerCase())){all.push(rec);localStorage.setItem('ghdip_users',JSON.stringify(all));}
  }catch(e){}
  showUser(n,o);
  document.getElementById('gate').style.display='none';
  document.body.style.overflow='';
  if(r){toast('已登记，邀请码 '+r+' 已记录');}
};
function showUser(n,o){
  let el=document.getElementById('userChip');
  if(!el){el=document.createElement('span');el.id='userChip';
    el.style.cssText='font-size:12.5px;background:#e8f0fb;color:#1746b8;padding:4px 10px;border-radius:16px;font-weight:700;cursor:pointer';
    el.title='点击可退出登录（清除登记）';
    el.onclick=()=>{if(confirm('退出并清除本机登记信息？')){try{localStorage.removeItem('ghdip_user');}catch(e){}location.reload();}};
    document.querySelector('.top-inner').appendChild(el);}
  el.textContent='已登记：'+n+(o?' · '+o:'');
}
(function(){
  let u=null;
  try{u=JSON.parse(localStorage.getItem('ghdip_user')||'null');}catch(e){}
  if(u&&u.name){showUser(u.name,u.org);document.getElementById('gate').style.display='none';}
  else{document.getElementById('gate').style.display='flex';document.body.style.overflow='hidden';}
})();

// ---------- 变量查询 ----------
function runVarSearch(){
  const q=document.getElementById('vInput').value.trim().toLowerCase();
  const res=document.getElementById('vResult');
  if(!q){res.innerHTML='<div class="q-empty" style="color:var(--muted);background:#fff;border-color:var(--line)">请输入要查询的变量 / 指标关键词，例如：肌酐、eGFR、血压、PHQ-9、PBS、影像。</div>';return;}
  const hits=[];
  DB.forEach(d=>{
    const src=((d.indicators||'')+' '+(d.content||'')+' '+(d.tags||[]).join(' ')+' '+d.name+' '+d.en).toLowerCase();
    if(src.includes(q)) hits.push({d:d,snip:d.indicators||d.content||''});
  });
  if(!hits.length){res.innerHTML='<div class="q-empty" style="color:var(--muted);background:#fff;border-color:var(--line)">未收录含该关键词的指标，可换更通用的词（如「血压」「基因」「费用」「抑郁」）。</div>';return;}
  hits.sort((a,b)=>a.d.access-b.d.access);
  let html=`<div class="q-empty" style="color:var(--primary-d);background:#eef6ff;border-color:#cfe0fb">共 <b>${hits.length}</b> 个数据库收录与「<b>${esc(q)}</b>」相关的指标（按开放度从易到难）。</div>`;
  hits.slice(0,20).forEach(h=>{
    const d=h.d;
    html+=`<div class="rec" style="margin-bottom:10px">
      <h4 style="font-size:16.5px">${esc(d.name)} <span class="en">${esc(d.en)}</span></h4>
      <div class="meta stars s${d.access}">${ACCESS[d.access]} · ${esc(d.region||'')}</div>
      <div class="ind" style="margin-top:6px"><b>匹配指标：</b>${esc(h.snip||'—')}</div>
      <div class="why" style="font-size:13px"><b>变量申请情况：</b>${esc(varAccessText(d))}</div>
      <div style="margin-top:8px"><button class="detail-btn" data-nm="${esc(d.name)}">查看详情 / 申请方式</button></div>
    </div>`;
  });
  res.innerHTML=html;
}
document.getElementById('vBtn').onclick=runVarSearch;
document.getElementById('vInput').addEventListener('keydown',e=>{if(e.key==='Enter')runVarSearch();});

// 弹窗内致谢复制
function copyTxt(t,btn){
  const done=()=>{const o=btn.textContent;btn.textContent='已复制 ✓';setTimeout(()=>{btn.textContent=o;},1500);};
  if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(t).then(done,done);}else{done();}
}
document.addEventListener('click',e=>{
  const b=e.target.closest('#mAckCopy');
  if(b){const s=document.getElementById('mAckEn');if(s)copyTxt(s.innerText,b);}
});

// ---------- 引用复制 ----------
document.querySelectorAll('.copy-btn[data-copy]').forEach(b=>{
  b.onclick=()=>{
    const MAPC={cn:'citeCn',en:'citeEn',en2:'citeEn2',bib:'citeBib'};
    const id=MAPC[b.dataset.copy]||'citeCn';
    const t=document.getElementById(id).innerText;
    const done=()=>{const o=b.textContent;b.textContent='已复制 ✓';setTimeout(()=>{b.textContent=o;},1500);};
    if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(t).then(done,done);}
    else{done();}
  };
});

/* ==================================================================
   增强功能：对比篮 / 深链 / 导出 / 申请材料生成 / 邀请 / 本机数据
   ================================================================== */
function toast(msg){
  let t=document.getElementById('toast');
  t.textContent=msg; t.classList.add('on');
  clearTimeout(window._tt); window._tt=setTimeout(()=>t.classList.remove('on'),2200);
}
function copyText(t){
  if(navigator.clipboard&&navigator.clipboard.writeText){return navigator.clipboard.writeText(t);}
  const ta=document.createElement('textarea');ta.value=t;document.body.appendChild(ta);ta.select();
  try{document.execCommand('copy');}catch(e){}document.body.removeChild(ta);
  return Promise.resolve();
}
function download(filename, text, mime){
  const blob=new Blob([text],{type:(mime||'text/plain')+';charset=utf-8'});
  const a=document.createElement('a');
  a.href=URL.createObjectURL(blob); a.download=filename;
  document.body.appendChild(a); a.click();
  setTimeout(()=>{URL.revokeObjectURL(a.href);a.remove();},800);
}
function baseURL(){return location.origin+location.pathname;}
function getUser(){try{return JSON.parse(localStorage.getItem('ghdip_user')||'null');}catch(e){return null;}}

/* ---------- 对比篮 ---------- */
let cmpSel=[];
const cmpBar=document.getElementById('cmpBar');
document.addEventListener('change',e=>{
  const cb=e.target.closest('.cmp-box'); if(!cb)return;
  const nm=cb.dataset.nm;
  if(cb.checked){
    if(cmpSel.length>=4){cb.checked=false;toast('最多同时对比 4 个数据库');return;}
    if(!cmpSel.includes(nm))cmpSel.push(nm);
  }else{
    cmpSel=cmpSel.filter(x=>x!==nm);
  }
  paintCmpBar();
});
function paintCmpBar(){
  document.getElementById('cmpN').textContent=cmpSel.length;
  document.getElementById('cmpTags').innerHTML=cmpSel.map(n=>
    `<span class="tagx" data-rm="${esc(n)}" title="点击移除">${esc(n.split(' ')[0])} ✕</span>`).join(' ');
  cmpBar.classList.toggle('on',cmpSel.length>0);
  document.querySelectorAll('.cmp-box').forEach(cb=>{cb.checked=cmpSel.includes(cb.dataset.nm);});
}
document.getElementById('cmpTags').addEventListener('click',e=>{
  const t=e.target.closest('[data-rm]'); if(!t)return;
  cmpSel=cmpSel.filter(x=>x!==t.dataset.rm); paintCmpBar();
});
document.getElementById('cmpClear').onclick=()=>{cmpSel=[];paintCmpBar();};
document.getElementById('cmpClose').onclick=()=>{document.getElementById('cmp').classList.remove('on');document.body.style.overflow='';};
document.getElementById('cmp').onclick=e=>{if(e.target.id==='cmp')document.getElementById('cmpClose').onclick();};
document.getElementById('cmpGo').onclick=()=>{
  if(cmpSel.length<2){toast('至少选 2 个才能对比');return;}
  const ds=cmpSel.map(n=>DB.find(d=>d.name===n)).filter(Boolean);
  const rows=[
    ['开放度',d=>ACCESS[d.access]],
    ['地区',d=>d.region||'—'],
    ['规模',d=>d.scale||'—'],
    ['时间跨度',d=>d.timeSpan||'—'],
    ['主办单位',d=>d.host||'—'],
    ['核心内容',d=>d.content||'—'],
    ['经典指标',d=>d.indicators||'—'],
    ['申请方式',d=>d.usage||'—'],
    ['变量申请情况',d=>varAccessText(d)],
    ['常见坑',d=>d.notes||'—'],
    ['官网',d=>(d.urls||[]).map(u=>`<a href="${u.url}" target="_blank" rel="noopener">${esc(u.label)} ↗</a>`).join('<br>')||'—'],
  ];
  let html=`<div class="table-wrap" style="margin-top:0"><table class="cmp-table"><thead><tr><th>维度</th>${
    ds.map(d=>`<th style="width:auto">${esc(d.name)}<div style="font-weight:400;color:var(--muted);font-size:11px">${esc(d.en)}</div></th>`).join('')}</tr></thead><tbody>`;
  rows.forEach(([k,f])=>{
    html+=`<tr><th>${k}</th>`+ds.map(d=>{const v=f(d);return `<td>${['官网'].includes(k)?v:esc(v)}</td>`;}).join('')+`</tr>`;
  });
  html+='</tbody></table></div>';
  html+=`<div style="margin-top:12px;display:flex;gap:8px;flex-wrap:wrap">
    <button class="btn-mini" id="cmpCopy">复制对比表（Markdown）</button>
    <button class="btn-mini" id="cmpDl">下载对比表（.md）</button></div>`;
  document.getElementById('cmpBody').innerHTML=html;
  document.getElementById('cmp').classList.add('on');
  document.body.style.overflow='hidden';
  document.getElementById('cmpCopy').onclick=()=>{
    let md=`# 数据库对比（${ds.length} 个）\n\n| 维度 | ${ds.map(d=>d.name).join(' | ')} |\n|---|${ds.map(()=>'---').join('|')}|\n`;
    rows.forEach(([k,f])=>{md+=`| ${k} | ${ds.map(d=>String(f(d)).replace(/<[^>]+>/g,'').replace(/\|/g,'/')).join(' | ')} |\n`;});
    md+='\n> 由「全球健康数据库整合网页」生成。引用：杜思娴. 全球健康数据库整合网页 [EB/OL]. 2026.\n';
    copyText(md).then(()=>toast('已复制对比表')); window._cmpMd=md;
  };
  document.getElementById('cmpDl').onclick=()=>{
    let md=`# 数据库对比（${ds.length} 个）\n\n| 维度 | ${ds.map(d=>d.name).join(' | ')} |\n|---|${ds.map(()=>'---').join('|')}|\n`;
    rows.forEach(([k,f])=>{md+=`| ${k} | ${ds.map(d=>String(f(d)).replace(/<[^>]+>/g,'').replace(/\|/g,'/')).join(' | ')} |\n`;});
    md+='\n> 由「全球健康数据库整合网页」生成。\n';
    download('db-compare-'+ds.length+'.md',md,'text/markdown');
  };
};

/* ---------- 弹窗内按钮 ---------- */
document.addEventListener('click',e=>{
  const c=e.target.closest('#mAckCopyCn');
  if(c){const s=document.getElementById('mAckCn');if(s)copyText(s.innerText).then(()=>toast('已复制中文致谢'));return;}
  if(e.target.closest('#mCopyLink')){
    if(!currentDB)return;
    const u=baseURL()+'?db='+encodeURIComponent(currentDB.name);
    copyText(u).then(()=>toast('已复制本库链接'));
    return;
  }
  if(e.target.closest('#mExport')){
    if(!currentDB)return;
    download(currentDB.name.split(' ')[0]+'-'+Date.now()+'.md', dbMarkdown(currentDB),'text/markdown');
    return;
  }
  if(e.target.closest('#mApply')){
    if(!currentDB)return;
    const nm=currentDB.name; closeModal();
    const sel=document.getElementById('apDb'); sel.value=nm; prefillFromDb();
    document.getElementById('apply').scrollIntoView({behavior:'smooth',block:'start'});
    return;
  }
  if(e.target.closest('#mAddCmp')){
    if(!currentDB)return;
    if(cmpSel.includes(currentDB.name)){toast('已在对比篮中');return;}
    if(cmpSel.length>=4){toast('最多同时对比 4 个数据库');return;}
    cmpSel.push(currentDB.name); paintCmpBar(); toast('已加入对比篮');
  }
});
function dbMarkdown(d){
  const L=[];
  L.push(`# ${d.name}`);
  L.push(`**${d.en||''}**\n`);
  L.push(`- 开放度：${ACCESS[d.access]}`);
  L.push(`- 地区：${d.region||'—'}｜规模：${d.scale||'—'}｜时间：${d.timeSpan||'—'}`);
  L.push(`- 主办单位：${d.host||'—'}`);
  L.push(`- 分类：${(CATS.find(c=>c[0]===d.cat)||['','—'])[1]}\n`);
  L.push(`## 数据库介绍\n${d.intro||d.content||'—'}\n`);
  L.push(`## 核心内容\n${d.content||'—'}\n`);
  L.push(`## 经典指标\n${d.indicators||'详见官网 codebook'}\n`);
  L.push(`## 注册与申请方式（流程 / 费用 / 周期）\n${d.usage||'—'}\n`);
  L.push(`## 变量申请情况\n${varAccessText(d)}\n`);
  L.push(`## 官方入口\n${(d.urls||[]).map(u=>`- [${u.label}](${u.url})`).join('\n')||'—'}\n`);
  L.push(`## 代表性文献\n${(d.papers||[]).map(p=>`- ${p}`).join('\n')||'- 建议到官网 Publications 页核对'}\n`);
  L.push(`- PubMed 检索：${d.pubmed||''}\n`);
  L.push(`## 论文致谢 / 数据可用性声明（[XXXXX] 填批准编号）\n`);
  L.push(`**EN**：${d.ackEn||''}\n`);
  L.push(`**中文**：${d.ackCn||''}\n`);
  L.push(`## 常见坑\n${d.notes||'遵守数据使用协议、禁止再识别；发表注明数据来源。'}\n`);
  L.push(`## 研究范式建议\n${d.paradigm||'—'}\n`);
  L.push(`---\n> 由「全球健康数据库整合网页」生成。引用：杜思娴. 全球健康数据库整合网页 [EB/OL]. 2026. 联系：dusixian16@163.com`);
  return L.join('\n');
}

/* ---------- 申请材料生成器 ---------- */
function fillApDb(){
  const s=document.getElementById('apDb');
  let html='';
  CATS.forEach(([k,label])=>{
    const list=DB.filter(d=>d.cat===k);
    if(!list.length)return;
    html+=`<optgroup label="${esc(label)}">`+list.map(d=>
      `<option value="${esc(d.name)}">${esc(d.name)}${d.en?' · '+esc(d.en):''}</option>`).join('')+'</optgroup>';
  });
  s.innerHTML=html;
  const u=getUser();
  if(u){document.getElementById('apName').value=u.name||'';document.getElementById('apOrg').value=u.org||'';document.getElementById('apMail').value=u.mail||'';}
  prefillFromDb();
}
function prefillFromDb(){
  const d=DB.find(x=>x.name===document.getElementById('apDb').value);
  if(!d)return;
  const v=document.getElementById('apVars');
  if(!v.value.trim()||v.dataset.auto==='1'){v.value=d.indicators||'';v.dataset.auto='1';}
}
document.getElementById('apDb').addEventListener('change',()=>{
  const v=document.getElementById('apVars');
  const d=DB.find(x=>x.name===document.getElementById('apDb').value);
  v.value=(d&&d.indicators)||''; v.dataset.auto='1';
});
document.getElementById('apVars').addEventListener('input',function(){this.dataset.auto='0';});

function stepsFor(d){
  const a=d.access;
  if(a===1)return ['确认官网许可条款（CC0 / CC-BY / 自定义）与商用限制',
    '下载 codebook / Data Dictionary，核对变量名与年份',
    '下载数据文件（可使用 R/Python 官方包直接取数）',
    '在论文中注明数据来源与版本，并按官网要求引用'];
  if(a===2)return ['在官网注册账号（建议用机构邮箱，通过更快）',
    '填写研究用途 / 项目名称 / 简要研究问题',
    '同意数据使用条款（不得再分发、不得再识别）',
    '下载 codebook + 问卷 + 数据集，核对各轮变量编码是否变化'];
  if(a===3)return ['完成 CITI「Data or Specimens Only Research」等培训并取得证书编号',
    '在平台建立项目，填写研究摘要、所需字段/表、分析计划',
    '由所在机构签署数据使用协议（DUA）——个人签无效，需科研管理部门盖章',
    '平台审核（自动 + 人工），缴费（如 UK Biobank 按项目规模收费）',
    '获得访问权限（云端/受控环境），记录 Application Number 用于论文致谢'];
  if(a===4)return ['阅读官方 Data Use Certification / 申请指南',
    '由机构签署官（Signing Official）提交申请，附 Research Use Statement',
    '准备伦理批件、研究计划、变量清单与预算说明',
    '等待 DAC 评审（月度/季度），按获批字段范围与年数计价',
    '在受控环境内分析（如 AnVIL / 安全屋），导出结果需审核',
    '签署补充协议后获取扩展变量'];
  return ['撰写 1–2 页研究意向书，说明问题、变量需求、预期产出',
    '通过官网/通讯作者联系数据持有团队，确认变量可行性',
    '双方 PI 沟通署名、知识产权与数据边界（多数要求共同署名）',
    '签署合作协议 + 双方伦理审批（IRB）',
    '派研究者驻场或远程受控环境分析，论文投稿前经数据方审阅'];
}
function buildApplyPack(){
  const nm=document.getElementById('apDb').value;
  const d=DB.find(x=>x.name===nm);
  if(!d){toast('请先选择数据库');return '';}
  const g=id=>document.getElementById(id).value.trim();
  const name=g('apName')||'【申请人姓名】', org=g('apOrg')||'【机构】', mail=g('apMail')||'【邮箱】';
  const title=g('apTitle')||'【项目/论文题目】', q=g('apQ')||'【研究问题：在 XX 人群中，XX 暴露是否与 XX 结局相关】';
  const vars=g('apVars')||d.indicators||'【拟用变量清单】';
  const design=g('apDesign'), when=g('apWhen')||'【拟申请时间】', fee=g('apFee')||'【预算】';
  const catName=(CATS.find(c=>c[0]===d.cat)||['','—'])[1];
  const today=new Date().toLocaleDateString('zh-CN');
  const FENCE='`'.repeat(3);
  const L=[];
  L.push(`# 数据使用申请材料 · ${d.name}`);
  L.push(`> 生成日期：${today}　｜　生成工具：全球健康数据库整合网页（内测版）`);
  L.push(`> 本文件为**申请草稿**，提交前请按 ${d.name} 官方最新要求逐项核对；[XXXXX] 处需替换为真实编号。\n`);
  L.push(`## 一、申请人信息`);
  L.push(`| 项目 | 内容 |`);
  L.push(`|---|---|`);
  L.push(`| 申请人 | ${name} |`);
  L.push(`| 机构 / 单位 | ${org} |`);
  L.push(`| 联系邮箱 | ${mail} |`);
  L.push(`| 拟申请时间 | ${when} |`);
  L.push(`| 经费 / 预算 | ${fee} |\n`);
  L.push(`## 二、研究摘要`);
  L.push(`**题目**：${title}\n`);
  L.push(`**研究问题**：${q}\n`);
  L.push(`**研究设计**：${design}\n`);
  L.push(`**研究背景与目的**：（补 100–150 字：该问题的公共卫生意义、现有证据缺口、本研究要回答什么）\n`);
  L.push(`**方法与分析计划**：（补：研究人群与纳排标准、暴露与结局的操作化定义、协变量、主分析模型、敏感性分析、缺失值处理）\n`);
  L.push(`**预期产出**：（补：拟投期刊/报告、对政策或临床的意义）\n`);
  L.push(`## 三、拟申请数据清单`);
  L.push(`| 项目 | 说明 |`);
  L.push(`|---|---|`);
  L.push(`| 数据库 | ${d.name}${d.en?'（'+d.en+'）':''} |`);
  L.push(`| 分类 | ${catName} |`);
  L.push(`| 主办单位 | ${d.host||'—'} |`);
  L.push(`| 开放度 | ${ACCESS[d.access]} |`);
  L.push(`| 覆盖地区 / 规模 / 时间 | ${d.region||'—'} / ${d.scale||'—'} / ${d.timeSpan||'—'} |`);
  L.push(`| 拟用变量 / 字段 | ${vars.replace(/\n/g,'；')} |`);
  L.push(`| 官方入口 | ${(d.urls||[]).map(u=>u.url).join(' ； ')||'—'} |\n`);
  L.push(`**变量级数据可得性**：${varAccessText(d)}\n`);
  L.push(`## 四、伦理与合规声明`);
  L.push(`- 本研究已/将提交 ${org} 伦理委员会审查，批件号 [XXXXX]（如为公开匿名数据，请说明豁免依据）。`);
  L.push(`- 承诺仅将数据用于本申请所述研究目的，**不尝试再识别**任何个体，不再向第三方分发原始数据。`);
  L.push(`- 数据仅存储在受控设备/环境，分析结果导出前做小样本抑制（n<10 不单独报告）。`);
  L.push(`- 涉及跨境传输的，按《人类遗传资源管理条例》等规定另行备案/审批（如适用）。`);
  L.push(`- 发表时按数据方要求撰写致谢与数据可用性声明，并注明数据版本号。\n`);
  L.push(`## 五、申请步骤清单`);
  stepsFor(d).forEach((s,i)=>L.push(`- [ ] ${i+1}. ${s}`));
  L.push('');
  L.push(`## 六、致谢与数据可用性声明（获批后使用）`);
  L.push(`**Acknowledgements（EN）**\n`);
  L.push(FENCE);L.push(d.ackEn||'');L.push(FENCE+'\n');
  L.push(`**致谢（中文）**\n`);
  L.push(FENCE);L.push(d.ackCn||'');L.push(FENCE+'\n');
  L.push(`**Data Availability Statement**\n`);
  L.push(FENCE);
  L.push(d.access>=3
    ? `The data are available from ${d.en||d.name} under a data use agreement and cannot be shared by the authors. Requests for access should be directed to the data custodian. Approval under application number [XXXXX] was obtained.`
    : `The data analyzed in this study are publicly available from ${d.en||d.name} at ${(d.urls&&d.urls[0]&&d.urls[0].url)||''}. Analysis code is available from the corresponding author on reasonable request.`);
  L.push(FENCE+'\n');
  L.push(`**引用本平台（使用了本平台的检索与匹配结果，请一并引用）**`);
  L.push(FENCE);
  L.push('杜思娴. 全球健康数据库整合网页 [EB/OL]. 2026. 联系：dusixian16@163.com');
  L.push(FENCE+'\n');
  L.push(`## 七、联系方式`);
  L.push(`${name} ｜ ${org} ｜ ${mail}`);
  return L.join('\n');
}
document.getElementById('apBtn').onclick=()=>{
  const md=buildApplyPack(); if(!md)return;
  const nm=document.getElementById('apDb').value.split(' ')[0];
  document.getElementById('apOut').innerHTML=
    `<div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:10px">
       <button class="btn-mini" id="apCopy">复制全文</button>
       <button class="btn-mini" id="apDl">下载 .md</button>
       <button class="btn-mini" id="apAgain">重新生成</button>
     </div><div class="ap-pre" id="apPre"></div>`;
  document.getElementById('apPre').textContent=md;
  document.getElementById('apCopy').onclick=()=>copyText(md).then(()=>toast('已复制申请材料'));
  document.getElementById('apDl').onclick=()=>download('apply-'+nm+'.md',md,'text/markdown');
  document.getElementById('apAgain').onclick=()=>document.getElementById('apBtn').click();
  document.getElementById('apOut').scrollIntoView({behavior:'smooth',block:'nearest'});
  toast('已生成申请材料草稿');
};
document.getElementById('apReset').onclick=()=>{
  ['apTitle','apQ','apVars','apWhen','apFee'].forEach(id=>{document.getElementById(id).value='';document.getElementById(id).dataset.auto='0';});
  document.getElementById('apOut').innerHTML='';prefillFromDb();
};

/* ---------- 邀请 ---------- */
function hash36(s){
  let h=5381;
  for(let i=0;i<s.length;i++){h=((h<<5)+h+s.charCodeAt(i))>>>0;}
  return h.toString(36).toUpperCase();
}
function inviteCode(mail){
  const s=(mail||'').toLowerCase().trim();
  if(!s)return '';
  return 'GHD-'+('000'+hash36(s).slice(-4)).slice(-4);
}
document.getElementById('invGen').onclick=()=>{
  const u=getUser();
  if(!u||!u.mail){
    document.getElementById('invOut').innerHTML='<div style="font-size:13px;color:#b45309">请先完成上方登记（需邮箱），再生成邀请码。</div>';
    return;
  }
  const code=inviteCode(u.mail);
  const link=baseURL()+'?ref='+encodeURIComponent(code);
  let hits={};
  try{hits=JSON.parse(localStorage.getItem('ghdip_refhits')||'{}');}catch(e){}
  const n=hits[code]||0;
  const text=`【邀请】全球健康数据库整合网页（内测）
一个帮医学科研选库、查变量、写申请材料的平台：91 个公共数据库，输入科学问题直接告诉你用哪个库、怎么申请、多少钱、多久、论文怎么致谢。
https://naturedu.github.io/global-health-db-hub/
我的邀请码：${code}（注册时填入即可）`;
  document.getElementById('invOut').innerHTML=
    `<div class="inv-row"><span>我的邀请码</span><span class="inv-code" id="invCode">${code}</span>
       <button class="btn-mini" id="invCopyCode">复制邀请码</button></div>
     <div class="inv-row"><input id="invLink" value="${esc(link)}" readonly
        style="flex:1;min-width:240px;border:1px solid var(--line);border-radius:8px;padding:7px 10px;font-size:12.5px">
       <button class="btn-mini" id="invCopyLink">复制链接</button></div>
     <div style="margin-top:8px;font-size:12.5px;color:var(--muted)">本机记录：该邀请码被打开/填写 <b>${n}</b> 次（仅统计本机浏览器，正式版接后端后可统计全渠道）。</div>`;
  document.getElementById('invCopyText').style.display='inline-block';
  window._invText=text;
  document.getElementById('invCopyCode').onclick=()=>copyText(code).then(()=>toast('已复制邀请码'));
  document.getElementById('invCopyLink').onclick=()=>copyText(link).then(()=>toast('已复制邀请链接'));
};
document.getElementById('invCopyText').onclick=()=>copyText(window._invText||'').then(()=>toast('已复制邀请文案'));

/* ---------- 本机数据管理 ---------- */
document.getElementById('dmExport').onclick=()=>{
  let all=[];
  try{all=JSON.parse(localStorage.getItem('ghdip_users')||'[]');}catch(e){}
  const u=getUser(); if(u&&!all.some(x=>x.mail===u.mail))all.push(u);
  if(!all.length){document.getElementById('dmOut').innerHTML='<span style="color:#b45309">本机暂无登记记录。</span>';return;}
  const head='姓名,机构,邮箱,邀请码,使用他人邀请码,登记时间\n';
  const rows=all.map(x=>[x.name,x.org,x.mail,x.invite||'',x.ref||'',new Date(x.ts||Date.now()).toLocaleString('zh-CN')]
    .map(v=>'"'+String(v).replace(/"/g,'""')+'"').join(',')).join('\n');
  download('ghdip-registrations.csv','\ufeff'+head+rows,'text/csv');
  document.getElementById('dmOut').innerHTML=`已导出 <b>${all.length}</b> 条登记记录（CSV，Excel 可直接打开）。`;
};
document.getElementById('dmStats').onclick=()=>{
  let all=[],hits={};
  try{all=JSON.parse(localStorage.getItem('ghdip_users')||'[]');}catch(e){}
  try{hits=JSON.parse(localStorage.getItem('ghdip_refhits')||'{}');}catch(e){}
  const u=getUser();
  document.getElementById('dmOut').innerHTML=
    `<div>本机登记记录：<b>${all.length}</b> 条　｜　当前登录：<b>${u?esc(u.name):'未登记'}</b>　｜　我的邀请码：<b>${u?inviteCode(u.mail):'—'}</b>　｜　对比篮：<b>${cmpSel.length}</b> 个　｜　本机累计收录库：<b>${DB.length}</b></div>`;
};
document.getElementById('dmClear').onclick=()=>{
  if(!confirm('将清除本机的登记信息、邀请记录与对比篮（不影响网站内容）。确定继续？'))return;
  ['ghdip_user','ghdip_users','ghdip_refhits'].forEach(k=>{try{localStorage.removeItem(k);}catch(e){}});
  cmpSel=[];
  location.href=location.pathname;
};
document.getElementById('dmPrint').onclick=()=>{window.print();};

/* ---------- 深链 / 邀请参数 / 键盘 ---------- */
(function initDeepLink(){
  let p;
  try{p=new URLSearchParams(location.search);}catch(e){return;}
  const ref=(p.get('ref')||'').trim().toUpperCase();
  if(ref){
    const box=document.getElementById('gRef');
    if(box)box.value=ref;
    try{
      const hits=JSON.parse(localStorage.getItem('ghdip_refhits')||'{}');
      hits[ref]=(hits[ref]||0)+1;
      localStorage.setItem('ghdip_refhits',JSON.stringify(hits));
    }catch(e){}
  }
  const db=p.get('db');
  if(db){setTimeout(()=>{const d=DB.find(x=>x.name===db);if(d)openModal(d);},120);}
})();
document.addEventListener('keydown',e=>{
  if(e.key!=='Escape')return;
  const cmp=document.getElementById('cmp');
  if(cmp.classList.contains('on')){document.getElementById('cmpClose').onclick();return;}
  if(document.getElementById('modal').style.display==='flex'){closeModal();}
});
/* ---------- 顶部分类跳转 ---------- */
(function fillCatJump(){
  const s=document.getElementById('catJump'); if(!s)return;
  CATS.forEach(([k,label])=>{
    const o=document.createElement('option');
    o.value='cat-'+k; o.textContent=label; s.appendChild(o);
  });
  s.addEventListener('change',()=>{
    if(!s.value)return;
    const el=document.getElementById(s.value);
    if(el)el.scrollIntoView({behavior:'smooth',block:'start'});
  });
})();
fillApDb();
</script>
</body>
</html>
"""

CITE_CN = ("杜思娴. 全球健康数据库整合网页：Global Health Database Integration Platform"
           "[EB/OL]. 2026[2026-10-22]. https://naturedu.github.io/global-health-db-hub/. "
           "联系邮箱: dusixian16@163.com.")

CITE_EN = ("Du, S. (2026). Global health database integration platform "
           "[Online database and research navigator]. "
           "https://naturedu.github.io/global-health-db-hub/")
# 若期刊要求标注访问日期，用这一版：
CITE_EN_ACCESS = ("Du, S. (2026). Global health database integration platform "
                  "[Online database and research navigator]. Retrieved October 22, 2026, from "
                  "https://naturedu.github.io/global-health-db-hub/")

CITE_EN2 = ("Du S. Global Health Database Integration Platform [Internet]. 2026 "
            "[cited 2026 Oct 22]. Available from: https://naturedu.github.io/global-health-db-hub/")

CITE_BIB = ("@misc{du2026ghdip,\n"
            "  author       = {Du, Sixian},\n"
            "  title        = {Global Health Database Integration Platform\n"
            "                  (全球健康数据库整合网页)},\n"
            "  year         = {2026},\n"
            "  howpublished = {\\url{https://naturedu.github.io/global-health-db-hub/}},\n"
            "  note         = {Online database and research navigator; Contact: dusixian16@163.com}\n"
            "}")

HTML = (HTML
    .replace("__DB_JSON__", DB_JSON)
    .replace("__CATS_JSON__", json.dumps(CATS, ensure_ascii=False))
    .replace("__ACCESS_JSON__", json.dumps(ACCESS, ensure_ascii=False))
    .replace("__CAT_NAV__", CAT_NAV)
    .replace("__REGION_CHIPS__", REGION_CHIPS)
    .replace("__DATATYPE_CHIPS__", DATATYPE_CHIPS)
    .replace("__DESIGN_CHIPS__", DESIGN_CHIPS)
    .replace("__TOPIC_CHIPS__", TOPIC_CHIPS)
    .replace("__LEGEND__", LEGEND)
    .replace("__OVERVIEW__", OVERVIEW)
    .replace("__LADDER_ROWS__", LADDER_ROWS)
    .replace("__ALL_LINKS__", ALL_LINKS)
    .replace("__TOTAL__", str(len(D)))
    .replace("__CITE_CN__", CITE_CN)
    .replace("__CITE_EN__", CITE_EN)
    .replace("__CITE_EN2__", CITE_EN2)
    .replace("__CITE_BIB__", CITE_BIB))

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "index.html")
with open(out, "w", encoding="utf-8") as f:
    f.write(HTML)
print("WROTE", out, "entries=", len(D), "bytes=", len(HTML))

# ---------------------------------------------------------------- 同步导出 Skill 数据
# 网页与 Skill 共用同一份数据，避免两处手工维护出现分歧。
KEYS_EXPORT = ["name", "en", "cat", "access", "urls", "region", "scale", "timeSpan",
               "host", "content", "intro", "usage", "notes", "tags", "paradigm",
               "qr", "lite", "indicators", "papers", "pubmed", "ackEn", "ackCn", "alias"]

try:
    _recs = [{k: d[k] for k in KEYS_EXPORT if k in d} for d in D]
    _nurl = sum(len(r.get("urls") or []) for r in _recs)
    _payload = {
        "meta": {
            "name": "全球健康数据库整合网页",
            "en": "Global Health Database Integration Platform",
            "count": len(_recs),
            "urls": _nurl,
            "url": "https://naturedu.github.io/global-health-db-hub/",
            "author": "杜思娴",
            "contact": "dusixian16@163.com",
            "source": "用户提供 PDF《医学与健康研究公共数据库汇总》(29 页) 全量解析 + 联网核实的中国/澳洲/香港等条目",
            "note": "本文件由 build_site.py 自动导出，请勿手改；要改数据请改 build_site.py 后重跑。",
        },
        "access": {str(k): v for k, v in ACCESS.items()},
        "cats": [[k, v] for k, v in CATS],
        "databases": _recs,
    }
    _sp = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "skill", "global-health-db-advisor", "data", "databases.json")
    if os.path.isdir(os.path.dirname(_sp)):
        with open(_sp, "w", encoding="utf-8") as f:
            json.dump(_payload, f, ensure_ascii=False, indent=1)
        print("WROTE", _sp, "entries=", len(_recs), "urls=", _nurl)
    else:
        print("SKIP skill export: skill 目录不存在")
except Exception as _ex:                                   # 导出失败不影响网页生成
    print("SKIP skill export:", _ex)
