import urllib.request as req
import urllib.parse
import bs4 as soup
import string
import jieba
import jieba.analyse
from wordcloud import WordCloud, STOPWORDS
from PIL import Image
import numpy as np
from collections import Counter
import os
import io
import base64
# Jieba------------------------------------------------------------
stopwords = []
punctuations = []

# 使用繁體中文詞庫
jieba.set_dictionary('./extra_dict/dict.txt.big')
jieba.analyse.set_stop_words('./stop_words/stop-word-zh_TW.txt')
# 讀入標點符號檔
with open('./stop_words/punctuations.txt', mode='r', encoding='utf-8') as file:
    for data in file.readlines():
        data = data.strip()
        punctuations.append(data)

# 讀入停用詞檔
with open('./stop_words/stop-word-zh_TW.txt', mode='r',
          encoding='utf-8') as file:
    for data in file.readlines():
        data = data.strip()
        stopwords.append(data)


# Public method------------------------------------------------------------
def httpRead(url):
    url = urllib.parse.quote(url, safe=string.printable)
    request = req.Request(
        url,
        headers={
            "user-agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"
        })
    with req.urlopen(request) as response:
        data = response.read().decode('utf-8')
    return data


def writeFile(data, path):
    myfile = open(path, 'w')
    myfile.write(data)
    myfile.close()


# Dcard method------------------------------------------------------------
# 抓出所有文章標題
def getAllTitles(data):
    root = soup.BeautifulSoup(data, "html.parser")
    allArticles = root.find_all("article", {"class": "sc-1v1d5rx-0 lmtfq"})
    return allArticles


# 抓出所有文章內文
def getArticleText(data):
    try:
        root = soup.BeautifulSoup(data, "html.parser")
        articleText = root.find("div", {
            "class": "Post_content_NKEl9d"
        }).getText()
        return articleText
    except Exception as e:  # avoid exception such as deleted article
        return ''


# 抓出所有文章留言
def getArticleComment(data):
    root = soup.BeautifulSoup(data, "html.parser")
    articleCommentList = []
    elementList = root.find_all("div",
                                {"class": "CommentEntry_content_1ATrw1"})
    for element in elementList:
        articleCommentList.append(element.getText())
    return articleCommentList


# main------------------------------------------------------------
def analyse(key):
    textToWrite = ''
    data = httpRead("https://www.dcard.tw/f/" + key)
    articleList = getAllTitles(data)

    print(str(len(articleList)) + " 篇文章")
    # 爬蟲----------------------------------------------------
    cloudWordList = []
    for article in articleList:

        # 擷取文章標題的關鍵字
        title = article.find("h2", {
            "class": "sc-1v1d5rx-2 kZjhSU"
        }).getText()
        terms = jieba.posseg.cut(title)
        cloudWordList += list(
            filter(
                lambda x: x.word not in stopwords and x.word not in
                punctuations and x.word != '\n' and x.word[0] != "B" and x.flag
                in ('ns', 'n', 'vn', 'nr', 'nt', 'nz', 'nrfg') and len(
                    x.word) >= 2, terms))
        print('\n\n\n 文章標題: ' + title)
        textToWrite += '\n\n\n' + title

        # 擷取文章內容的關鍵字
        articleSubHref = article.find(
            "a", {"class": "sc-1v1d5rx-3 kPUUNB"})['href']
        articleHref = "https://www.dcard.tw" + articleSubHref
        articleData = httpRead(articleHref)
        articleText = getArticleText(articleData)
        terms = jieba.posseg.cut(articleText)
        cloudWordList += list(
            filter(
                lambda x: x.word not in stopwords and x.word not in
                punctuations and x.word != '\n' and x.word[0] != "B" and x.flag
                in ('ns', 'n', 'vn', 'nr', 'nt', 'nz', 'nrfg') and len(
                    x.word) >= 2, terms))
        print('\n內文:\n' + articleText)
        textToWrite += '\n\n' + articleText

        # 擷取文章留言的關鍵字
        articleCommentList = getArticleComment(articleData)
        for comment in articleCommentList:
            terms = jieba.posseg.cut(comment)
            print('\n留言:\n' + comment)
            textToWrite += '\n\n' + comment
        cloudWordList += list(
            filter(
                lambda x: x.word not in stopwords and x.word not in
                punctuations and x.word != '\n' and x.word[0] != "B" and x.flag
                in ('ns', 'n', 'vn', 'nr', 'nt', 'nz', 'nrfg') and len(
                    x.word) >= 2, terms))

    # ----------------------------------------------------
    wordListForCloud = []
    for word in cloudWordList:
        wordListForCloud.append(word.word)
        print("<" + word.word + ', ' + word.flag + ">")
    resultArr = []

    # TF-IDF
    keywords = jieba.analyse.extract_tags(textToWrite,
                                          topK=20,
                                          withWeight=True,
                                          allowPOS=('ns', 'n', 'vn', 'nr',
                                                    'nt', 'nz', 'nrfg'))
    print("\nTF-IDF: ")
    tups = []
    for item in keywords:
        tups.append([item[0], '{:12.10f}'.format(item[1])])
        print(item[0] + '\t' + str(item[1]))
    resultArr.append(tups)

    # TextRank
    keywords = jieba.analyse.textrank(textToWrite,
                                      topK=20,
                                      withWeight=True,
                                      allowPOS=('ns', 'n', 'vn', 'nr', 'nt',
                                                'nz', 'nrfg'))
    print("\nTextRank: ")
    tups = []
    for item in keywords:
        tups.append([item[0], '{:12.10f}'.format(item[1])])
        print(item[0] + '\t' + str(item[1]))
    resultArr.append(tups)

    # generate wordcloud
    font = r"./font/msjhbd.ttc"
    mask = np.array(Image.open(r"./image/cloud.jpg"))
    my_wordcloud = WordCloud(background_color="white",
                             mask=mask,
                             stopwords=set(STOPWORDS),
                             font_path=font,
                             collocations=False,
                             max_words=200,
                             width=1600,
                             height=900,
                             margin=2)
    my_wordcloud.generate_from_frequencies(
        frequencies=Counter(wordListForCloud))
    # my_wordcloud.to_file("./static/wordcloud.png") #儲存到static資料夾以呈現在網頁上
    my_wordcloud.to_file("./wordclouds/" + key + ".png")  # 儲存檔案到wordclouds資料夾

    # convert image to numpy array then send to front-end
    np_img = my_wordcloud.to_array()
    img = Image.fromarray(np_img.astype('uint8'))
    img_object = io.BytesIO()
    img.save(img_object, 'PNG')
    img_object.seek(0)
    resultArr.append("data:image/png;base64," +
                     base64.b64encode(img_object.getvalue()).decode("utf-8"))
    return resultArr
