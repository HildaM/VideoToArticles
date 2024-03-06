def read_file(file_path):
    """从给定的文件路径读取内容"""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def write_file(file_path, content):
    """将内容写入到给定的文件路径"""
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

def preprocess_textB(textB):
    """预处理文本B，确保每个主题标题后跟时间范围"""
    # 将文本按行分割，并移除空行
    lines = [line for line in textB.split('\n') if line.strip() != '']
    processed_lines = []
    for line in lines:
        # 直接添加处理过的行到结果中
        processed_lines.append(line)
    return '\n'.join(processed_lines)

def process_text(textA, textB):
    """处理文本A和文本B，返回格式化的输出"""
    # 解析文本A
    segments_a = {}
    for line in textA.strip().split('\n'):
        time_range, text = line.split(': ', 1)
        start, end = time_range.split('-')
        segments_a[(float(start), float(end))] = text  # 使用元组作为键，存储开始和结束时间

    # 解析文本B并提取相应文本
    output = []
    # 确保文本B按正确的格式被分割
    topics = preprocess_textB(textB).split('\n')
    for i in range(0, len(topics), 2):  # 每两行一组，第一行是标题，第二行是时间范围
        if i+1 < len(topics):  # 确保有时间范围行存在
            title = topics[i]
            time_range = topics[i+1]
            start, end = map(float, time_range.split('-'))

            output.append("SEPARATE")
            output.append(title)
            for (segment_start, segment_end), segment_text in segments_a.items():
                # 检查段落是否至少部分位于指定范围内
                if not (end < segment_start or start > segment_end):
                    output.append(f"{segment_start}-{segment_end}: {segment_text}")

    return '\n'.join(output)

# 输入文件和输出文件的路径
input_file_path_a = 'transcription.txt'  # 替换为文本A的文件路径
input_file_path_b = 'topic_timeframe.txt'  # 替换为文本B的文件路径
output_file_path = 'output.txt'   # 替换为你希望保存输出的文件路径

# 读取输入文件
textA = read_file(input_file_path_a)
textB_raw = read_file(input_file_path_b)

# 预处理文本B
textB = preprocess_textB(textB_raw)

# 处理文本并获取输出
output_text = process_text(textA, textB)

# 将输出保存到文件
write_file(output_file_path, output_text)

print(f"Output has been saved to {output_file_path}")
