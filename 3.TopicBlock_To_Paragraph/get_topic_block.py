def read_and_split_file(file_path):
    # 打开文件，并读取文件内容
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # 使用"SEPARATE"作为分隔符分割文本
    text_blocks = content.split("SEPARATE\n")
    
    # 移除列表中的空字符串元素
    text_blocks = [block for block in text_blocks if block.strip()]
    
    return text_blocks

# 指定文件路径
file_path = 'rawtext.txt'

# 调用函数并获取分割后的文本块列表
text_blocks_list = read_and_split_file(file_path)

# 打印结果，查看文本块
for index, block in enumerate(text_blocks_list):
    print(f"Block {index+1}:\n{block}\n{'-'*50}\n")

# 注意：此脚本假设你的文本文件和Python脚本位于同一目录下
