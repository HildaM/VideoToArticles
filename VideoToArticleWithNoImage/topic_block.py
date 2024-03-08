from openai import OpenAI
from langchain_core.prompts import ChatPromptTemplate
from constant import TOPIC_BLOCK_TIMELINE
from config import Config

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def write_file(file_path, content):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

def preprocess_textB(textB):
    """Preprocess text B to ensure each topic title is followed by a time range"""
    # Split the text into lines and remove empty lines
    lines = [line for line in textB.split('\n') if line.strip() != '']
    processed_lines = []
    for line in lines:
        if line.startswith('```'):
            continue
        # Directly add the processed lines to the result
        processed_lines.append(line)
    return '\n'.join(processed_lines)

def process_text(textA, textB):
    """Process textA(timeframe_text) and textB(topic_timeline), returning a formatted output"""
    # Parse textA
    segments_a = {}
    for line in textA.strip().split('\n'):
        time_range, text = line.split(': ', 1)
        start, end = time_range.split('-')
        segments_a[(float(start), float(end))] = text  # 使用元组作为键，存储开始和结束时间

    # Parse text B and extract the relevant text
    output = []
    # Ensure text B is split in the correct format
    topics = preprocess_textB(textB).split('\n')
    for i in range(0, len(topics), 2):  # In groups of two lines each, the first line is the title, the second line is the time range
        if i+1 < len(topics):  # Ensure that a time range line exists.
            title = topics[i]
            time_range = topics[i+1]
            start, end = map(float, time_range.split('-'))

            output.append("SEPARATE")
            output.append(title)
            for (segment_start, segment_end), segment_text in segments_a.items():
                # Check if the paragraph is at least partially within the specified range
                if not (end < segment_start or start > segment_end):
                    output.append(f"{segment_start}-{segment_end}: {segment_text}")

    return '\n'.join(output)


CN_TIMELINE_PROMPT = ChatPromptTemplate.from_template(
"""接下来我将跟你一大段“带有时间戳的文本”，这些文本是从一段视频截取下来的。你需要根据文本的内容进行分析总结，“按时间顺序”将其拆分为不同的话题主题，然后在该话题主题下放置对应的“时间戳的开始与结束时间“，例如：
```
# 主题1
0.0-14.6
# 主题2
14.6-22.28
# 主题3
start-end
```
start和end，以及主题，都需要你通读下面的全文才能得出。
接下来是你需要处理的文本：
```
{context}
```
请直接输出处理后的结果，不需要附带额外的分析:
"""
)

TIMELINE_PROMPT = ChatPromptTemplate.from_template(
"""
Next, I will present you with a lengthy section of "timestamped text," sourced from a video segment. You are required to analyze and summarize the content, "in chronological order," breaking it down into different thematic topics. Then, under each thematic topic, place the corresponding "start and end times" of the timestamps, for example:
```
# Topic 1
0.0-14.6
# Topic 2
14.6-22.28
# Topic 3
start-end
```
Determining the start and end, as well as the topics, necessitates a thorough reading of the following text.
Here is the text you need to process:
```
{context}
```
Please directly output the processed result, without any additional analysis:
"""
)


class TopicBlock:
    def __init__(self, timeframe_path: str, config: Config):
        self.config = config
        self._client = OpenAI(base_url=self.config.openai_api_base, api_key=self.config.openai_api_key)
        self.timeframe_text = read_file(timeframe_path)

    def process(self):
        topic_timeline = self._get_topic_timeline(self.timeframe_text)
        output_text = process_text(self.timeframe_text, topic_timeline)
        write_file(TOPIC_BLOCK_TIMELINE, output_text)

    def _get_topic_timeline(self, timeframe_text):
        if timeframe_text is None or timeframe_text == "":
            raise ValueError("timeframe_text is Empty: " + timeframe_text)
        prompt = TIMELINE_PROMPT.invoke({"context": timeframe_text})
        completion = self._client.chat.completions.create(
            model=self.config.openai_model_name,
            messages=[
                {"role": "user", "content": prompt.to_string()}
            ]
        )

        raw_topic_timeline = completion.choices[0].message.content
        return preprocess_textB(raw_topic_timeline)
    
    def get_topic_blocks(self):
        with open(TOPIC_BLOCK_TIMELINE, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Split the text using "SEPARATE" as the delimiter.
        text_blocks = content.split("SEPARATE\n")
        
        # Remove empty string elements from the list.
        text_blocks = [block for block in text_blocks if block.strip()]
        
        return text_blocks
    



if __name__=='__main__':
    from langchain.globals import set_debug
    set_debug(True)

    config = Config()
    client = OpenAI(base_url=config.openai_api_base, api_key=config.openai_api_key)
    prompt = TIMELINE_PROMPT.invoke({"context": "timeframe_text"})
    completion = client.chat.completions.create(
        model=config.openai_model_name,
        messages=[
            {"role": "user", "content": prompt.to_string()}
        ]
    )

    print(completion.choices[0].message.content)
