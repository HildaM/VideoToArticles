from timeframe import TimeFrame
from topic_block import TopicBlock
from constant import TIMEFRAME_FILE



if __name__ == '__main__':
    from langchain.globals import set_debug
    set_debug(True)

    video_path = input("Input video path: ")
    timeframe = TimeFrame(video_path).process()
    topic_block = TopicBlock(TIMEFRAME_FILE).process()
