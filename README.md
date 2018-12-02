# qqmusic
# 使用Scrapy结合Selenium，通过爬虫绕过qq音乐收费问题，获取所有音乐下载地址以及歌曲歌手信息
# 爬取范围：qq音乐全站歌曲
# 存储方式：MongoDB数据库
# 1. 首先使用Scrapy中间件结合Selenium获取歌手列表页面 https://y.qq.com/portal/singer_list 的所有歌手唯一标识singermid信息，这是进入歌手页面的入口标识
# 2. 分析歌手的歌曲页面Ajax信息，获取歌手所有歌曲真正的请求url
# 3. 歌曲下载前，分析歌曲播放页面，点击Netword里的Media选项卡，找到真正的url，如 C400003kLvu04bLGzi.m4a开头的，在新页面中打开即可以播放。而完整的歌曲下载url是 http://dl.stream.qqmusic.qq.com/ 加上purl值，purl值可以通过分析歌曲播放页面得到
# 4. 将获取到的歌曲信息及下载链接存储在MongoDB数据库中
