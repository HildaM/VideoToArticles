from openai import OpenAI
from langchain_core.prompts import ChatPromptTemplate
from config import Config
from constant import RESULT_FOLDER
import time
import os


CN_NO_CONTEXT_PROMPT = ChatPromptTemplate.from_template(
"""给出一个带有”标题+时间戳文本“的文段，你需要通读整个文段，并根据标题的内容输出一篇文章。你需要以第三人称进行阐述，输出的文章要附带有原有的标题。以txt格式进行输出。
以下是所给文本:
‍```
{context}
‍```
"""
)

NO_CONTEXT_PROMPT = ChatPromptTemplate.from_template(
"""Given a text segment with "title + timestamped text," you are required to read through the entire segment and produce an article based on the content of the titles. You must narrate in the third person, and the output article should include the original titles. Output should be in txt format.
Below is the provided text:
‍```
{context}
‍```
"""
)

CN_CONTEXT_PROMPT = ChatPromptTemplate.from_template(
"""以下有2个文本A和B，A的时间在B之前，B的内容收到A影响。B文本是一个带有”标题+时间戳文本“的文段，你需要通读整个B文段，并根据标题的内容输出一篇文段，同时要参考B时间戳原文的叙事角度。输出的文章要附带有原有的标题。以txt格式进行输出。
以下是所给A文本:
‍```
{previous}
‍```
B文本:
‍```
{current}
‍```
"""
)

CONTEXT_PROMPT = ChatPromptTemplate.from_template(
"""Below are two texts, A and B, with A's events occurring before those of B. The content of B is influenced by A. Text B is a segment with "title + timestamped text," and you are required to read through the entire segment of B, producing a text based on the content of the titles while also considering the narrative perspective of the original timestamps in B. The output article should include the original titles and be formatted as a txt file.
Below is the given text for A:
‍```
{previous}
‍```
Text for B:
‍```
{current}
‍```
"""
)



class Article:

    def __init__(self, topics, config: Config):
        self._topics = topics
        self._paragraphs = [""] * len(topics)
        self._config = config
        self._client = OpenAI(base_url=self._config.openai_api_base, api_key=self._config.openai_api_key)
        # self._client = OpenAI(base_url="http://localhost:1234/v1", api_key="not-needed")  # test with LM Studio locally

        self._language = config.article_language
        self._long_context = config.long_context

    def _generate_single_without_context(self, template: ChatPromptTemplate):
        prompt = template.invoke({"context": self._topics[0]})
        completion = self._client.chat.completions.create(
            model=self._config.openai_model_name,
            messages=[
                {"role": "user", "content": prompt.to_string()}
            ]
        )

        self._paragraphs[0] = completion.choices[0].message.content
        # debug
        print(self._paragraphs[0])


    def _generate_multiple_with_context(self, template: ChatPromptTemplate):
        for i in range(1, len(self._paragraphs)):
            previous = self._paragraphs[i - 1]
            current = self._topics[i]
            prompt = template.invoke({"previous": previous, "current": current})
            self._paragraphs[i] = self._completions(prompt)

    def _generate_multiple_without_context(self, template: ChatPromptTemplate):
        for i in range(1, len(self._paragraphs)):
            prompt = template.invoke({"context": self._topics[i]})
            self._paragraphs[i] = self._completions(prompt)


    def _completions(self, prompt): 
        completion = self._client.chat.completions.create(
            model=self._config.openai_model_name,
            messages=[
                {"role": "user", "content": prompt.to_string()}
            ]
        )
        return completion.choices[0].message.content
    
    
    """
        param context:
            Subsequent paragraph generation will reference paragraphs that have already been generated, 
            increasing the contextual coherence of the generated paragraphs.
    """
    def _generate(self, language: str, context: bool = False):
        match language:
            case 'cn':
                self._generate_single_without_context(CN_NO_CONTEXT_PROMPT)
                if context:
                    self._generate_multiple_with_context(CN_CONTEXT_PROMPT)
                else:
                    self._generate_multiple_without_context(CN_NO_CONTEXT_PROMPT)
            case 'en':
                self._generate_single_without_context(NO_CONTEXT_PROMPT)
                if context:
                    self._generate_multiple_with_context(CONTEXT_PROMPT)
                else:
                    self._generate_multiple_without_context(NO_CONTEXT_PROMPT)



    """The commented-out method below is only suitable for use when OpenAI has not enabled throttling. 
        If throttling is enabled, a ConnectionError may occur, disconnecting the session partway through the call.
    """
    # def _generate_with_context(self):
    #     length = len(self._paragraphs)
    #     messages = []
    #     for i in range(1, length):
    #         previous = self._paragraphs[i - 1]
    #         current = self._topics[i]
    #         prompt = CONTEXT_PROMPT.invoke({"previous": previous, "current": current})
    #         msg = {"role": "user", "content": prompt.to_string()}
    #         messages.append(msg)

    #     choices = self._completions(messages)
    #     for i in range(1, length):
    #         self._paragraphs[i] = choices[i - 1].message.content
        

    # def _completions(self, messages):
    #     completion = self._client.chat.completions.create(
    #         model=self._config.openai_model_name,
    #         messages=messages
    #     )
    #     return completion.choices
    

    def save_as_markdown(self):
        self._generate(self._language, self._long_context)

        file_path = os.path.join(RESULT_FOLDER, "articles_" + str(time.time()) + ".md")
        with open(file_path, 'w', encoding='utf-8') as file:
            for item in self._paragraphs:
                file.write(f"{item}\n\n")


    