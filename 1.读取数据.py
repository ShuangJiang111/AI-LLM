# 定义文件路径
file_path = 'D:/code/test code/AILLM_Project/3/运动鞋店铺知识库.txt'

# 批次大小（每次读取的行数）
batch_size = 5

# 使用 open() 来逐行读取文件并处理批次
with open(file_path, 'r', encoding='utf-8') as file:
    batch = []
    for line_number, line in enumerate(file, 1):
        batch.append(line.strip())  # 去掉每行末尾的换行符

        # 当达到批次大小时，处理该批次
        if len(batch) == batch_size:
            print(f"当前批次的行数: {len(batch)}")
            for i, line in enumerate(batch):
                print(f"第{i + 1}行: {line}")
            batch = []  # 清空批次，准备下一个

    # 处理最后剩下的行
    if batch:
        print(f"当前批次的行数: {len(batch)}")
        for i, line in enumerate(batch):
            print(f"第{i + 1}行: {line}")
