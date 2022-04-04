# B站动态自动点赞脚本

### 功能

- 给指定用户的全部动态点赞

### 使用

- 修改文件中的cookie和UID

    ```python
    cookie = ""  # 这里填写自己的B站cookie
    host_id = ""  # 这里填写需要点赞的用户的B站UID
    interval = 2  # 这里填写点赞时间间隔，默认为2秒
    ```

- 运行

    `python biliThumpsUp.py`