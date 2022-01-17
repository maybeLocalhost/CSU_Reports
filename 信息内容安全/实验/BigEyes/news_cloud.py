import jieba
import wordcloud
import snownlp
import imageio

mk = imageio.imread("feel/chinamap.png")

# 构建并配置两个词云对象w1和w2，分别存放积极词和消极词
w1 = wordcloud.WordCloud(width=800,
                        height=500,
                        background_color='white',
                        font_path='msyh.ttc',
                        mask=mk,
                        scale=15,
                         stopwords={'孝金波', '赵玉晓', '阮光锋'})
w2 = wordcloud.WordCloud(width=800,
                        height=500,
                        background_color='white',
                        font_path='msyh.ttc',
                        # mask=mk,
                        scale=15,
                         )

# 对来自外部文件的文本进行中文分词
txt = open('feel/news.txt','r', encoding='utf-8').read()
txtlist = jieba.lcut(txt)
positivelist = []
negativelist = []

# 下面对文本中的每个词进行情感分析，情感>0.90判为积极词，情感<0.10判为消极词
print('开始进行情感分析，程序崩溃中。。。')
# 导入自然语言处理第三方库snownlp
for each in txtlist:
    each_word = snownlp.SnowNLP(each)
    feeling = each_word.sentiments
    if feeling > 0.90:
        positivelist.append(each)
    elif feeling < 0.10:
        negativelist.append(each)
    else:
        pass
# 将积极和消极的两个列表各自合并成积极字符串和消极字符串，字符串中的词用空格分隔
positive_string = " ".join(positivelist)
negative_string = " ".join(negativelist)


# 将string变量传入w的generate()方法，给词云输入文字
w1.generate(positive_string)
w2.generate(negative_string)

# 将积极、消极的两个词云图片导出到当前文件夹
w1.to_file('positive4.png')
w2.to_file('negative4.png')
print('词云生成完成')