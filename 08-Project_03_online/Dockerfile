# 拉取基础镜像
FROM project3_0614_2


# 将当前目录的所有文件添加到指定文件夹下(也可用COPY命令)
ADD . /code

# 将code文件夹设为工作目录
WORKDIR /code

# 镜像构建时需要执行的命令
# RUN pip install --no-cache-dir -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

# 运行
CMD ["python","./scripts/run_case_from_json_offline.py"]
