import requests  # 导入requests库，用于发送HTTP请求
from bs4 import BeautifulSoup  # 导入BeautifulSoup库，用于解析HTML文档
import pandas as pd  # 导入pandas库，用于数据处理和保存为CSV文件
import time  # 导入time库，用于添加延时

# 目标URL（豆瓣电影《哪吒》的评论页）
base_url = "https://movie.douban.com/subject/26794435/comments"

# 设置请求头，模拟浏览器访问，避免被网站封禁
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# 初始化一个空列表，用于存储提取的评论数据
comments = []

# 爬取多页评论
for page in range(0, 5):  # 爬取前5页评论，每页20条
    # 构造每一页的URL,其中f-string 是 Python 3.6 引入的一种字符串格式化方式，用于在字符串中嵌入表达式（如变量、计算等），例如x = 10
    # y = 20
    # result = f"The sum of {x} and {y} is {x + y}."-> :The sum of 10 and 20 is 30.
    url = f"{base_url}?start={page * 20}&limit=20&status=P&sort=new_score"

    # 发送HTTP GET请求，获取网页内容
    response = requests.get(url, headers=headers)

    # 使用BeautifulSoup解析网页内容，指定解析器为html.parser
    soup = BeautifulSoup(response.text, "html.parser")

    # 查找所有评论项，class为"comment-item"的div标签
    for item in soup.find_all("div", class_="comment-item"):
        # 提取用户名：找到class为"comment-info"的span标签，再找到其中的a标签，获取文本内容
        user = item.find("span", class_="comment-info").find("a").text

        # 提取评分：找到class为"rating"的span标签，获取其title属性值（如果有）
        rating = item.find("span", class_="rating").get("title") if item.find("span", class_="rating") else "无评分"

        # 提取评论内容：找到class为"short"的span标签，获取文本内容
        content = item.find("span", class_="short").text

        # 将提取的用户名、评分和评论内容添加到comments列表中
        comments.append({"用户": user, "评分": rating, "评论": content})

    # 打印当前页的爬取进度
    print(f"已爬取第 {page + 1} 页评论，共 {len(comments)} 条评论")

    # 添加延时，避免频繁请求被封禁
    time.sleep(2)  # 每次请求后暂停2秒

# 将comments列表转换为pandas的DataFrame，方便后续处理
df = pd.DataFrame(comments)

# 将DataFrame保存为CSV文件，文件名为"哪吒_评论.csv"，编码为utf-8-sig（支持中文）
df.to_csv("哪吒_评论.csv", index=False, encoding="utf-8-sig")

# 打印提示信息，表示评论已保存
print("评论已保存为 哪吒_评论.csv")