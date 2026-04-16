import os
import pandas as pd
import jieba
import numpy as np
import re
from collections import Counter
import matplotlib.pyplot as plt
import networkx as nx
from wordcloud import WordCloud

# def read_files(folder_path):
#     dfs = []
#     for filename in os.listdir(folder_path):
#         if filename.endswith('.txt'):
#             with open(os.path.join(folder_path, filename),encoding='utf-8') as f:
#                 df_temp = pd.read_csv(f, delimiter='\t' or ",",header=None,on_bad_lines='skip')
#             dfs.append(df_temp)
#     return pd.concat(dfs)
# all_data = read_files(r"E:\phdresearch\caltransfer\data\all_data\all")
# all_data.to_csv('all_data_merge.txt', sep='\t', index=False) E:\python\pythonProject\all_data_merge.txt
with open(r'E:\python\pythonProject\2024_merge.txt',encoding='utf-8') as f:  # 打开文件
# with open(r'E:\phdresearch\caltransfer\data\importantpolicy\全国一体化大数据中心协同创新体系算力枢纽实施方案.txt',encoding='utf-8') as f:  # 打开文件
    all_data = f.read() # 读取文件
    # print(all_data)
# print(all_data.dtypes)
pattern = re.compile(r'\t|\n|\.|-|:|;|,|、|。|，|\)|\(|\?|') # 定义正则表达式匹配模式
string_data = re.sub(pattern, '', all_data) # 将符合模式的字符去除
jieba.load_userdict(r'E:\python\pythonProject\dict.txt')#加载自建词表
seg_list_exact = jieba.cut(string_data, cut_all = False)
# seg_list_exact = list(seg_list_exact)
object_list = []
remove_words = [u'的', u'，',u'和', u'是', u'随着', u'对于', u'对',u'等',u'能',u'都',u'。',u' ',u'、',u'中',u'在',u'了',
                u'通常',u'如果',u'我们',u'需要',u'国家',u'\u3000',u'发展',u'应用',u'（',u'）',u'建设',u'网络',u'协同',u'资源',u'加强'
                ,u'推动',u'提升',u'与',u'“',u'”',u'开展',u'需求',u'打造',u'实现',u'强化',u'加快',u'推进',u'鼓励',
                u'面向',u'各类',u'水平',u'促进',u'部署',u'部门',u'构建',u'行业',u'持续',u'支撑',u'综合',u'体系',
                u'局',u'及',u'大',u'按',u'各',u'全',u'办',u'为',u'使用',u'部',u'业务',u'降低',u'委',u'三',u'之间',u'积极',
                u'二',u'低',u'委员会',u'；利用',u'实施',u'上报',u'建立',u'能力',u'基础',u'引导',u'关键',u'方面',u'优化',u'模式',u'制定',
                u'支持',u'分析',u'管理',u'工程',u'实施',u'要求',u'\n',u'重点',u'"',u'市',u'产业',u'.',u'；',u'项目',u'经济',u'技术',u'新'
                ,u'：',u'省',u'领域',u'年',u'工作',u'相关',u'应当',u'专项',u'区',u'政策',u'机制',u'完善',u'改革',u'中心',u'以',u'以上'
                ,u'万元',u'有关',u'培育',u'政府',u'监察',u'不',u'提供',u'/',u'按照',u'给予',u'责任',u'社会',u'《',u'》',u'产品',u'1'
                ,u'组织',u'新型',u'产品',u'一',u'有限公司',u'系统',u'治理',u'2',u'二',u'机构',u'落实',u'并',u'市场',u'转型',u'形成'
                ,u'通过',u'关于',u'探索',u'保护',u'制造',u'单位',u'数字',u'要素',u'资金',u'本',u'好',u'示范',u'重大',u'研究'
                ,u'生产',u'规划',u'全面',u'申报',u'进行',u'互联网',u'信息',u'合作',u'一批',u'区域',u'或',u'3',u'三',u'提高',u'个',u'利用'
                ,u'规定',u'厅',u'可',u'制度',u'加大',u'方式',u'可',u'超过',u'布局',u'评估',u'升级',u'国际',u'向',u'情况',u'改造'
                ,u'月',u'将',u'监测',u'最高',u'交易',u'负责',u'统一',u'全国',u'省级',u'牵头',u'基地',u'试点',u'地区',u'化',u'重要'
                ,u'以及',u'全省',u'运行',u'开发',u'主体',u'到',u'深化',u'高效',u'作用',u'力度',u'特色',u'环境',u'全市',u'措施',u'依法'
                ,u'—',u'四',u'5',u'推广',u'中国',u',',u'核心',u'设计',u'条件',u'根据',u'依托',u'进一步',u'五',u'4',u'其他',u'行动'
                ,u'要',u'围绕',u'有',u'坚持',u'内',u'2023',u'参与',u'发挥',u'主要',u'具有',u'实际',u'（',u'）',u'健全',u'战略',u'专业'
                ,u'号',u'评价',u'自治区',u'优势',u'先进',u'意见',u'活动',u'深入',u'达到',u'规模',u'〔',u'〕',u'印发',u'-',u'深度'
                ,u'目标',u'引进',u'计划',u'通知',u'质量',u'10',u'功能',u'装备',u'基本',u'年度',u'县',u'地方',u'公司',u'＋',u'材料'
                ,u'公共' ,u'职责' ,u'集聚',u'2022',u'对接',u'县级',u'上',u'后',u'纳入',u'日',u'应',u'任务',u'应',u'跨',u'由',u'或者'
                ,u'认定' ,u'流通' ,u'完成' ,u'有效' ,u'范围',u'问题',u'目录',u'覆盖',u'有序',u'引领',u'建成',u'原则',u'增强',u'多'
                ,u'链',u'做好',u'结合',u'．',u'赋能',u'下',u'成果',u'建立健全',u'方案',u'及其',u'确保',u'市级',u'处理',u'包括',u'采集'
                ,u'\xa0',u'拓展',u'园区',u'指导',u'2025',u'配合',u'高',u'内容',u'每年',u'办法',u'平台',u'亿元',u'联合',u'100',u'科学'
                ,u':',u'符合',u'转化',u'自主',u'以下',u'不得',u'服务业',u'物',u'精准',u'6',u'及时',u'扩大',u'2024',u'高端',u'设立'
                ,u'汇聚',u'法律',u'本市',u'生活',u'聚焦',u'区块',u'+',u'移动',u'监督',u'授权',u'不断',u'联动',u'投入',u'地',u'发布'
                ,u'国家级',u'加工',u'共建',u'明确',u'基于',u'带动',u'现代',u'决策',u'增长',u'新建',u'业态',u'执行',u'条例',u'2019'
                ,u'未来',u'(',u'www',u'获得',u'其',u'级',u'所',u'前',u'html',u'【',u'】',u'CLI.12',u')',u'（',u'）',u'2021',u'2020']
# 自定义去除词库

for word in seg_list_exact: # 循环读出每个分词
    if word not in remove_words: # 如果不在去除词库中
        object_list.append(word) # 分词追加到列表
# # length = len(object_list)
# # print(length)
# # print(object_list)


# # 再进行基础的停词处理为了LDA分析做准备
stop_words_file = r"E:\python\pythonProject\stop_words.txt"
with open(stop_words_file, "r", encoding="utf - 8") as file:
    stop_words = set(file.read().splitlines())
processed_texts = []
for word in object_list:
    if word not in stop_words:
        processed_texts.append(word)

# # 1、统计最新文本的词频
word_counts = Counter(processed_texts) # 对分词做词频统计
word_counts_top100 = word_counts.most_common(100) # 获取前100最高频的词
total_word_count = len(processed_texts)
#
# # print (word_counts_top100) # 输出检查
df_count = pd.DataFrame(word_counts_top100, columns=['高频词','词频数'])
keywords = df_count['高频词'].tolist()
# df_count.to_csv('词频.csv', encoding='utf-8-sig')
# print(df_count)
#画柱状图
# plt.rcParams['font.sans-serif'] = ['SimHei']  # 解决中文显示
# plt.rcParams['axes.unicode_minus'] = False  # 解决符号无法显示
# x = [item[0] for item in word_counts_top100[:10]]
# y = [item[1] for item in word_counts_top100[:10]]
# plt.bar(x, y)
# plt.title('Top10高频词')
# plt.xlabel('词语')
# plt.ylabel('频次')
# plt.show()

# 2.构建共现矩阵，前两种方法都无效了
# 方法一：
# keywords = df_count['高频词'].tolist()
# print(keywords)
# 构建共现矩阵空矩阵
# word_counts = Counter(object_list) # 对分词做词频统计
# word_counts_text = word_counts.most_common(100)
# df_count_test = pd.DataFrame(word_counts_text, columns=['高频词','词频数'])
# keywords = df_count_test['高频词'].tolist()

# cut_word_list = list(map(lambda x: ''.join(x), df_count_test['高频词'].tolist()))
# keywords = pd.Series(cut_word_list)
# matrix = np.zeros((len(keywords) + 1) * (len(keywords) + 1)).reshape(len(keywords) + 1, len(keywords) + 1).astype(str)
# matrix[0][0] = np.NaN
# matrix[1:, 0] = matrix[0, 1:] = keywords
# # print(matrix)
# # object_list_test = pd.Series(object_list)
# cont_list = [cont.split() for cont in object_list]
# print(cont_list[0:3])
# print(object_list[0:3])
# print(keywords[0:3])
# for i, w1 in enumerate(keywords):
#     for j, w2 in enumerate(keywords):
#         count = 0
#         for cont in object_list:
#             if w1 in cont and w2 in cont:
#                 if abs(i - j) <= 10000:
#                 # if abs(cont.index(w1) - cont.index(w2)) <= 10000:
#                     count += 1
#         matrix[i + 1][j + 1] = count
# kwdata = pd.DataFrame(matrix)
# # # # print(kwdata)
# kwdata.to_csv('关键词共现矩阵3.csv', index=False, header=None, encoding='utf-8-sig')

# # # kwdata= pd.read_csv('关键词共现矩阵.csv')

# # # kwdata.index = kwdata .iloc[:, 0].tolist()
# # # kwdata_ = kwdata .iloc[:20, 1:21]
# # # kwdata_.astype(int)
#方法2：
# matrix_2 = np.zeros((len(keywords), len(keywords)))
# df_object = pd.DataFrame(object_list,columns=['所有词汇'])
# for i in range(len(keywords)):
#     for j in range(len(keywords)):
#         matrix_2[i, j] = sum(df_object['所有词汇'].str.contains(keywords[i]) & df_object['所有词汇'].str.contains(keywords[j]))
# co_occurrence_df = pd.DataFrame(matrix_2, index=keywords, columns=keywords)
# co_occurrence_df.to_csv('关键词共现矩阵2.csv', encoding='utf-8-sig')
'''
我们尝试方法三成功了：
'''
#
# from collections import defaultdict
# co_occurrence_dict = defaultdict(lambda: defaultdict(int))
# for i in range(len(processed_texts)):
#     for j in range(i + 1, min(i + 101, len(processed_texts))):
#         word1 = processed_texts[i]
#         word2 = processed_texts[j]
#         if word1 in keywords and word2 in keywords:
#             co_occurrence_dict[word1][word2] += 1
#             co_occurrence_dict[word2][word1] += 1
# # 获取关键词在列表中的索引映射
# keyword_index_map = {keyword: index for index, keyword in enumerate(keywords)}
#
# # 构建二维列表形式的共现矩阵，并将词频赋值到对角线元素
# co_occurrence_matrix = [[0] * len(keywords) for _ in range(len(keywords))]
# for word1 in keywords:
#     # index_value = df_count[df_count['高频词'] == word1].index[0]
#     for word2 in keywords:
#         if word1 == word2:
#             # co_occurrence_matrix[keyword_index_map[word1]][keyword_index_map[word2]] = df_count.loc[index_value, '词频数']
#             co_occurrence_matrix[keyword_index_map[word1]][keyword_index_map[word2]] = 0
#         else:
#             co_occurrence_matrix[keyword_index_map[word1]][keyword_index_map[word2]] = co_occurrence_dict[word1][word2]
#
# # 使用numpy将二维列表转换为二维数组（可选操作，方便后续使用pandas处理）
# co_occurrence_matrix_np = np.array(co_occurrence_matrix)
#
# # 使用pandas将二维数组转换为DataFrame，行列索引设置为关键词
# co_occurrence_df = pd.DataFrame(co_occurrence_matrix_np, index=keywords, columns=keywords)
#
# # 输出DataFrame形式的共现矩阵
# # print(co_occurrence_df)
# co_occurrence_df.to_csv('关键词共现矩阵（2024年政策100）.csv', encoding='utf-8-sig')
'''
手动共现矩阵的画图
'''
# import matplotlib.pyplot as plt
# import networkx as nx
# # plt.rcParams['font.sans-serif']=['SimHei']
# # plt.figure(figsize=(7, 7), dpi=512)
# # graph1 = nx.from_pandas_adjacency(co_occurrence_df)
# # nx.draw(graph1, with_labels=True, node_color='blue', font_size=25, edge_color='tomato')
# # plt.savefig('共现网络图2.jpg')
'''
热力图
'''
# import seaborn as sns
# # x_ticks = keywords
# # ax = sns.heatmap(co_occurrence_df,cmap="YlGnBu",linewidths=.5)
# plt.rcParams['font.sans-serif'] = ['SimHei']
# mask = np.zeros_like(co_occurrence_df.iloc[0:29,0:29])
# mask[np.triu_indices_from(mask)] = True
# ax = plt.subplots(figsize=(55, 55))
# with sns.axes_style("white"):
#     ax = sns.heatmap(co_occurrence_df.iloc[0:29,0:29], mask=mask,  square=True,cmap="YlGnBu",linewidths=.5)
# plt.xticks(rotation=45,fontsize=47)
# plt.yticks(rotation=45,fontsize=47)
# plt.title('高频关键词共现矩阵（2024年政策）',fontsize=60) #图片标题文本和字体大小
# plt.xlabel('算力调度政策高频词汇',fontsize=60) #x轴label的文本和字体大小
# plt.ylabel('算力调度政策高频词汇',fontsize=60) #y轴label的文本和字体大小
# # ax.set_title('高频关键词共现矩阵')  # 图标题
# # ax.set_xlabel('算力调度政策高频词汇')  # x轴标题
# # ax.set_ylabel('算力调度政策高频词汇')
# # plt.figure(figsize=(20, 20))
# plt.show()
# figure = ax.get_figure()
# figure.savefig('sns_heatmap2024年政策30.jpg')

# # 可以交互的热力图
# import plotly.express as px
# fig = px.imshow(co_occurrence_df, color_continuous_scale="YlGnBu")
# fig.update_layout(title="Network Correlation Heatmap")
# fig.show()
# fig.savefig('sns_heatmap3.jpg')
#
# #3.进行聚类分析
#
#
#
#
'''
3.LDA主题分析
'''
#
import gensim
from gensim import corpora
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import warnings
#
# warnings.filterwarnings('ignore')  # To ignore all warnings that arise here to enhance clarity
#

'''
首先是获得字典和语料库
'''
# word_counts = Counter(processed_texts) # 对分词做词频统计
# word_counts_top10000 = word_counts.most_common(10000) # 获取前100最高频的词
#
# # print (word_counts_top100) # 输出检查
# df_count = pd.DataFrame(word_counts_top10000, columns=['高频词','词频数']) random_state=100 no_below=0.05no_above=0.2keep_n=1000000
# keywords = df_count['高频词'].tolist()


from gensim import corpora
from gensim.models.ldamodel import LdaModel
import matplotlib.pyplot as plt
from gensim.models.coherencemodel import CoherenceModel
import multiprocessing as mp
# filtered_text = []
# for word in processed_texts:
#     frequency = word_counts[word] / total_word_count
#     if frequency <= 0.01 and word_counts[word] >= 5:
#         filtered_text.append(word)
# processed_texts = filtered_text
dictionary = corpora.Dictionary([processed_texts])
corpus = [dictionary.doc2bow(text) for text in [processed_texts]]

# 检查
# # 获取词汇表中的词语到ID的映射
# word_to_id = dictionary.token2id
#
# # 获取ID到词语的映射
# id_to_word = {v: k for k, v in word_to_id.items()}
#
# # 打印ID到词语的映射
# print("ID到词语的映射:")
# for word_id, word in id_to_word.items():
#     print(f"ID: {word_id}, 词语: {word}")
# print("----------------------------------------------")
# for doc in corpus:
#     print(doc)
# print(list(corpus)) alpha=0.1,eta=0.01

'''
尝试不同主题数并计算困惑度
'''
topic_num_range = range(2, 11)
perplexity_scores = []
for num_topics in topic_num_range:
    lda_model = LdaModel(corpus, num_topics = num_topics, id2word = dictionary,passes=50, alpha=0.1,eta=0.01)
    perplexity = lda_model.log_perplexity(corpus)
    perplexity_scores.append(perplexity)
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.plot(topic_num_range, perplexity_scores)
plt.xlabel("主题数")
plt.ylabel("困惑度")
plt.show()

# coherence_scores = []
# for num_topics in topic_num_range:
#     lda_model = LdaModel(corpus, num_topics = num_topics, id2word = dictionary, passes = 10)
#     coherence_model = CoherenceModel(model = lda_model, texts = [processed_texts], dictionary = dictionary, coherence = 'c_v')
#     coherence_score = coherence_model.get_coherence()
#     coherence_scores.append(coherence_score)
# plt.plot(topic_num_range, coherence_scores)
# plt.xlabel("主题数")
# plt.ylabel("连贯性得分")
# plt.show()

# random_state=120，alpha=0.05,eta=0.01 alpha=np.array([0.1] * num_topics),eta=0.001
'''
LDA主题分析+可视化
'''
# num_topics = 6
# lda_model = LdaModel(corpus=corpus, id2word=dictionary, num_topics=num_topics,iterations=20,random_state=110)
# for topic in lda_model.print_topics(num_words=100):
#     print(topic)
# # #
# import pyLDAvis
# import pyLDAvis.gensim
# lda_display = pyLDAvis.gensim.prepare(lda_model, corpus, dictionary)
# pyLDAvis.display(lda_display)
# pyLDAvis.save_html(lda_display, "lda_visualization_special.html")
print("---------------------------------------------------------")

'''
换一种文本处理方式看看是否主题还会不会高度同质化:Tf-IDF
'''
from gensim import corpora,models
# import math
# # # 假设corpus是词袋模型形式的语料库，例如：[(词汇编号1, 词频1), (词汇编号2, 词频2),...]
# new_corpus = []
# for doc in corpus:
#     new_doc = []
#     for word_id, freq in doc:
#         # 对词频进行取对数操作（模拟sublinear_tf=True），可以添加一个小的常数避免对数为0,
#         new_freq = math.log(freq + 10)
#         new_doc.append((word_id, new_freq))
#     new_corpus.append(new_doc)
# # # 手动计算IDF并构建TfidfModel
# num_docs = len(new_corpus)
# idf_dict = {}
# for doc in new_corpus:
#     for word_id, _ in doc:
#         if word_id in idf_dict:
#             continue
#         doc_freq = sum([1 for other_doc in new_corpus if word_id in [w_id for w_id, _ in other_doc]])
#         # 手动进行平滑处理的IDF计算
#         idf = math.log((num_docs + 1) / (doc_freq + 1)) + 1
#         idf_dict[word_id] = idf
# corpus_tfidf = []
# for doc in new_corpus:
#     new_doc = []
#     for word_id, freq in doc:
#         tfidf_value = freq * idf_dict[word_id]
#         new_doc.append((word_id, tfidf_value))
#     corpus_tfidf.append(new_doc)
# 现在tfidf_corpus是经过手动IDF平滑处理后的语料库，可以用于LDA模型
#使用tfidf
# tfidf = models.TfidfModel(corpus=corpus,id2word=dictionary,smartirs='ltc')
# corpus_tfidf = tfidf[corpus]

# if __name__ == '__main__':
#     lda_multi = models.ldamulticore.LdaMulticore(corpus=corpus, id2word=dictionary, num_topics=7,iterations=40, workers=1, batch=True)
#
#     for topic in lda_multi.print_topics(num_words=10):
#         print(topic)

# lda = LdaModel(corpus_tfidf,id2word=dictionary, num_topics=7,iterations=40,random_state=110,alpha=np.array([0.1] * 7),eta=0.001)
# # # # # for topic in lda.print_topics(num_words=80,num_topics=5):
# # # # #     print(topic)
# for topic in lda.print_topics(num_words=100):
#     print(topic)
# import pyLDAvis.gensim
# lda_display = pyLDAvis.gensim.prepare(lda, corpus_tfidf, dictionary)
# pyLDAvis.display(lda_display)
# pyLDAvis.save_html(lda_display, "lda_visualization2.html")
# print(corpus_tfidf[0])

# from gensim.models.tfidfmodel import TfidfModel
# # # 假设已经有了词袋模型形式的corpus和dictionary
# tfidf_model = TfidfModel(corpus)

# tfidf_corpus = tfidf_model[corpus]
# lda_model = LdaModel(tfidf_corpus, num_topics = 5, id2word = dictionary, passes = 10,alpha=1.5)
# for topic in lda_model.print_topics(num_words=10):
#     print(topic)

# print(list(corpus_tfidf))
# print("-------------------------------------------------------------------------")
#
# tfidf2 = models.TfidfModel(corpus,dictionary=dictionary,smartirs='ltc',normalize=True)
# corpus_tfidf2 = tfidf2[corpus]
# lda2 = LdaModel(corpus_tfidf2,id2word=dictionary, num_topics=7,iterations=40,alpha=1.5)
# # # for topic in lda.print_topics(num_words=80,num_topics=5):
# # #     print(topic)
# for topic in lda2.print_topics(num_words=10):
#     print(topic)
# print("-------------------------------------------------------------------------")
# tfidf3 = models.TfidfModel(corpus,dictionary=dictionary,id2word=dictionary,smartirs='ltc',pivot= 1)
# corpus_tfidf3 = tfidf3[corpus]
# lda3 = LdaModel(corpus_tfidf3,id2word=dictionary, num_topics=7,iterations=40,alpha=1.5)
# # # for topic in lda.print_topics(num_words=80,num_topics=5):
# # #     print(topic)
# for topic in lda3.print_topics(num_words=10):
#     print(topic)
'''
尝试聚类或者分层
'''
# from gensim.models import HdpModel
# hdp_model = HdpModel(corpus, id2word=dictionary)
# for topic_id, topic_words in hdp_model.show_topics():
#     print("主题ID:", topic_id)
#     print("主题词:", topic_words)
# topic_word_matrix = []
# for topic_id in range(num_topics):
#     topic_words = lda_model.show_topic(topic_id)
#     topic_word_vector = [prob for _, prob in topic_words]
#     topic_word_matrix.append(topic_word_vector)
# from sklearn.cluster import KMeans
# # 假设聚成3个类，可根据实际情况调整
# kmeans = KMeans(n_clusters=6)
# cluster_labels = kmeans.fit_predict(topic_word_matrix)
# for cluster_id in range(len(set(cluster_labels))):
#     cluster_topic_ids = [topic_id for topic_id, label in enumerate(cluster_labels) if label == cluster_id]
#     print(f"Cluster {cluster_id} Topics:")
#     for topic_id in cluster_topic_ids:
#         topic_words = lda_model.show_topic(topic_id)
#         print(f"Topic {topic_id}: {topic_words}")
# from sklearn.decomposition import PCA
# pca = PCA(n_components=2)
# topic_word_matrix_pca = pca.fit_transform(topic_word_matrix)
# import matplotlib.pyplot as plt
# plt.figure(figsize=(8, 6))
# for cluster_id in set(cluster_labels):
#     cluster_indices = [i for i, label in enumerate(cluster_labels) if label == cluster_id]
#     plt.scatter(topic_word_matrix_pca[cluster_indices, 0], topic_word_matrix_pca[cluster_indices, 1], label=f'Cluster {cluster_id}')
# plt.xlabel('Principal Component 1')
# plt.ylabel('Principal Component 2')
# plt.legend()
# plt.show()

'''
单独尝试LDA后聚类，观测主题词是否还存在明显重复
'''
# from sklearn.cluster import KMeans
# from sklearn.decomposition import PCA
# import matplotlib.pyplot as plt
# # 假设我们已经完成了前面的步骤，得到了 dictionary 和 corpus
# # 假设 dictionary 和 corpus 是前面筛选后的结果
#
# topic_word_matrix = np.zeros((num_topics, len(dictionary)))
# for topic_id in range(num_topics):
#     topic_words = lda_model.show_topic(topic_id)
#     for word, prob in topic_words:
#         word_id = dictionary.token2id[word]
#         topic_word_matrix[topic_id, word_id] = prob
#
# # 使用 K-Means 聚类主题词
# kmeans = KMeans(n_clusters=num_topics)
# cluster_labels = kmeans.fit_predict(topic_word_matrix)
#
# # 重新分配主题词
# reassigned_topics = [[] for _ in range(num_topics)]
# for topic_id, cluster_id in enumerate(cluster_labels):
#     reassigned_topics[cluster_id].append(lda_model.show_topic(topic_id))
# # 展示每个簇的主题词
# print("Reassigned Topics by Cluster:")
# for cluster_id, topics in enumerate(reassigned_topics):
#     print(f"Cluster {cluster_id}:")
#     for topic in topics:
#         print(topic)
# # 使用 PCA 进行降维以便可视化
# pca = PCA(n_components=2)
# topic_word_matrix_pca = pca.fit_transform(topic_word_matrix)
# # 可视化聚类结果
# plt.scatter(topic_word_matrix_pca[:, 0], topic_word_matrix_pca[:, 1], c=cluster_labels)
# plt.xlabel('Principal Component 1')
# plt.ylabel('Principal Component 2')
# plt.title('K-Means Clustering of Topic Words')
# plt.colorbar()
# plt.show()
