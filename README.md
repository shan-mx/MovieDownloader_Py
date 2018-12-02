# MovieDownloader_Py
电影bt下载器（需搭配py3，chrome内核浏览器，迅雷或任意下载工具使用）

common.py为通用版，输入查询关键字后会自动查询并给出结果，复制链接到迅雷内即可下载
source.py为自用版，比通用版多了几行实现全自动下载的代码，不多描述
使用前需要先安装python3，复制以下代码至某.bat文件完成依赖库安装：
pip install pyautogui
pip install selenium
pip install bs4
安装完成后，运行通用版：python common.py
运行自用版，点击moviedownloader.exe即可
