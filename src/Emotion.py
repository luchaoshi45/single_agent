from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv as _load_dotenv
_load_dotenv()

class EmotionClass:
    def __init__(self):
        self.chat_model = ChatOpenAI()
        # 结构化输出
        self.json_schema = {
            "title": "emotions",
            "description": "emotion analysis with feeling type and negativity score",
            "type": "object",
            "properties": {
                "feeling": {
                "type": "string",
                "description": "the emotional state detected in the input",
                "enum": [
                    "default", 
                    "upbeat", 
                    "angry", 
                    "cheerful", 
                    "depressed", 
                    "friendly"
                ]
                },
                "score": {
                "type": "string",
                "description": "negativity score from 1 to 10, where 10 represents extremely negative emotions",
                "enum": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
                }
            },
            "required": ["feeling", "score"]
        }
        self.llm = self.chat_model.with_structured_output(self.json_schema)

        # prompt
        self.prompt = """
        分析用户输入的文本情绪，返回情绪类型和负面程度评分。

        评分规则：
        - 分数范围为1-10
        - 分数越高表示情绪越负面
        - 1-3分：积极正面的情绪
        - 4-5分：中性或轻微情绪波动
        - 6-8分：明显的负面情绪
        - 9-10分：强烈的负面情绪

        情绪类型对应：
        - default: 中性，平静的情绪状态
        - upbeat: 极积极向上，充满活力的情绪
        - angry: 愤怒，生气的情绪
        - cheerful: 开心愉快，充满欢乐的情绪
        - depressed: 沮丧，压抑的情绪
        - friendly: 友好，亲切的情绪

        情绪分类指南：
        1. default: 用于表达中性或普通的情绪状态
        2. upbeat: 用于表达极积极向上，充满活力的状态
        3. angry: 用于表达愤怒、不满、生气的情绪
        4. cheerful: 用于表达欢快、喜悦的情绪
        5. depressed: 用于表达消极、低落、压抑的情绪
        6. friendly: 用于表达友好、亲切的情绪

        示例：
        - "我将别生气!"  --> {{"feeling": "angry", "score": "8"}}
        - "今天天气真好"  --> {{"feeling": "cheerful", "score": "2"}}
        - "随便吧，能接受" --> {{"feeling": "default", "score": "5"}}
        - "我很难过" --> {{"feeling": "depressed", "score": "9"}}
        - "谢谢你的帮助!" --> {{"feeling": "friendly", "score": "1"}}

        用户输入内容：{input}

        请根据以上规则分析情绪并返回相应的feeling和score。
        """

        self.chain = ChatPromptTemplate.from_messages([
            ("system", self.prompt),
            ("user", "{input}")
        ]) | self.llm

    def emotion_sensing(self, input):
        try:
            if not input.strip():
                return None

            if self.chain is not None:
                result = self.chain.invoke({"input": input})
            else:
                raise ValueError("EmotionChain is not properly instantiated.")

            self.Emotion = result
            return result
        except Exception as e:
            return None
