# 链接核对报告

- 检查链接：**145** 条（覆盖 100 个库的条目）
- 正常 **107**　反爬/需登录 **18**　真失效(404/410) **0**　网关错误(5xx) **4**　网络失败 **13**　其他 **1**

## 二、异常状态，需人工复点（5xx / 其他）

- SICdb 萨尔茨堡重症数据库 → https://www.sicdb.com（500，Internal Server Error）
- 国家自然科学基金基础研究知识库 → http://ir.nsfc.gov.cn（502，Bad Gateway）
- CCC 中国队列共享平台 → http://chinacohort.bjmu.edu.cn（502，Bad Gateway）
- BIGCS 广州出生队列 → http://gdbig.bigcs.com.cn（502，Bad Gateway）
- 国家/卫生健康统计年鉴 → https://www.nhc.gov.cn（412，Precondition Failed）

## 三、网络失败（本机 DNS/代理问题，不能判定失效）

- KLoSA 韩国老龄化追踪研究 → https://survey.keis.or.kr（Tunnel connection failed: 502 Bad Gateway）
- LASI 印度纵向老龄化调查 → https://www.lasi-india.org（Tunnel connection failed: 502 Bad Gateway）
- Million Veteran Program 百万退伍军人计划 → https://www.research.va.gov/mvp（Tunnel connection failed: 502 Bad Gateway）
- 开滦队列 → https://www.kailuanhospital.com（Tunnel connection failed: 502 Bad Gateway）
- 同济东风队列 → https://en.tjmu.edu.cn（Tunnel connection failed: 502 Bad Gateway）
- China PEACE / 百万人群项目 → https://www.fuwai.com（[WinError 10053] 你的主机中的软件中止了一个已建立的连接。）
- 中国高血压调查 CHS → https://www.fuwai.com（[SSL: UNEXPECTED_EOF_WHILE_READING] EOF occurred in violatio）
- 台湾 NHIRD 全民健康保险研究数据库 → https://dep.mohw.gov.tw/dos/（Tunnel connection failed: 502 Bad Gateway）
- AmsterdamUMCdb 重症数据库 → https://github.com/AmsterdamUMC/AmsterdamUMCdb（Tunnel connection failed: 502 Bad Gateway）
- INSPIRE 韩国围手术期数据库 → https://inspire.re.kr（Tunnel connection failed: 502 Bad Gateway）
- BioLINCC 美国心肺血研究所数据仓库 → https://biolincc.nhlbi.nih.gov（[SSL: UNEXPECTED_EOF_WHILE_READING] EOF occurred in violatio）
- HCUP 美国医疗成本与利用项目 → https://hcup-us.ahrq.gov（Tunnel connection failed: 502 Bad Gateway）
- MBS / PBS 澳大利亚医保诊疗与药品报销数据 → https://www.servicesaustralia.gov.au/（timeout）

## 四、站点存在但拒绝脚本访问（反爬/需登录，**不算错**）

- HRS 健康与退休研究 → https://hrs.isr.umich.edu（403）
- UK Biobank 英国生物样本库 → https://www.ukbiobank.ac.uk（403）
- All of Us 美国全民健康研究 → https://allofus.nih.gov（403）
- CMEC 中国西南多民族队列 → https://wcsph.scu.edu.cn（403）
- NHANES 美国国家健康与营养检查调查 → https://www.cdc.gov/nchs/data-linkage/mortality-public.htm（403）
- BRFSS 行为危险因素监测系统 → https://www.cdc.gov/brfss（403）
- NHIS 美国国民健康访问调查 → https://www.cdc.gov/nchs/nhis/（403）
- CPRD 英国基层医疗数据库 → https://cprd.com（403）
- 北欧登记体系 → https://www.norden.org（403）
- TriNetX 全球联邦式研究网络 → https://trinetx.com（403）
- MarketScan / Optum / IQVIA 美国商保数据 → https://www.optum.com（406）
- ICPSR / IPUMS 调查与微观数据仓储 → https://www.ipums.org（403）
- WHO 全球卫生观察站 / 卫生支出 / OECD / 世界银行 → https://wonder.cdc.gov（403）
- AIHW 澳大利亚健康与福利研究院 → https://www.aihw.gov.au/（403）
- HILDA 澳大利亚家庭收入与劳动力动态调查 → https://melbourneinstitute.unimelb.edu.au/hilda（403）
- Ten to Men 澳大利亚男性健康纵向研究 → https://tentomen.org.au/（403）
- CCC 中国队列共享平台 → https://academic.oup.com/ije/article/49/5/1436/5899247（403）
- ChiCTR 中国临床试验注册中心 → https://www.chictr.org.cn/searchproj.html（405）

> 判读：401/403/405/406/429 属反爬，浏览器通常能正常打开；5xx 与超时多为本机网络/代理，请手动复点后再决定是否改链接。
> 由「全球健康数据库整合网页 / global-health-db-advisor」生成。联系：dusixian16@163.com