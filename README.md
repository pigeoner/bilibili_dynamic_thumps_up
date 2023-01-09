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

- 安装依赖

    ```shell
    pip install -r requirements.txt
    ```
    
- 运行

    `python biliThumpsUp.py`

### 注意事项

- 由于每次运行需要**遍历用户所有的动态**，因此在开始执行点赞操作之前需要等待一段时间（用户动态数量越多则等待时间越长），如果没有报错说明程序仍在收集动态信息