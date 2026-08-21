from langchain_text_splitters import CharacterTextSplitter

sample_text = """哔哩哔哩，简称为B站，系中国知名综合性视频社区，2009年由徐逸创立，现由上海宽娱数码科技有限公司运营，法定代表人为黄声声。平台以ACG文化起家，逐步扩展至动画、游戏、影视、科技、生活、知识等20余个分区，形成多元内容生态，2023年月活跃用户超3.36亿。其特色弹幕互动系统及虚拟形象22娘、33娘塑造了独特的社区文化，用户原创内容（PUGV）占比超90%，并通过创作者激励计划及2016年上线的充电计划扶持创作者。
2011年猎豹移动联合创始人陈睿作为天使投资人加入，2014年出任董事长兼CEO后加速商业化进程。B站持续深耕垂直领域：国产动画专区出品《三体》《灵笼》等作品，纪录片板块推出《人生一串》《守护解放西》等口碑项目。电竞领域组建BLG职业战队，2018年成立哔哩哔哩电竞公司。平台2018年于纳斯达克上市。"""

text_splitter = CharacterTextSplitter(
    # 默认分隔符为["\n\n","\n"," ",""]
    chunk_size=100,
    chunk_overlap=20,
    length_function=len
)
docs = text_splitter.create_documents([sample_text])
for i, doc in enumerate(docs):
    print(i, doc)
