from timeframe import TimeFrame
from topic_block import TopicBlock
from article import Article
from constant import TIMEFRAME_FILE
from config import Config


if __name__ == '__main__':
    # from langchain.globals import set_debug
    # set_debug(True)

    video_path = input("Input video path: ")
    config = Config()
    timeframe = TimeFrame(video_path, config).process()
    topic_block = TopicBlock(TIMEFRAME_FILE, config)
    topic_block.process()
    
    article = Article(topic_block.get_topic_blocks(), config).save_as_markdown()
