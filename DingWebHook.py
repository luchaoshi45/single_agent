from dingtalk_stream import AckMessage, ChatbotMessage, DingTalkStreamClient, Credential, ChatbotHandler, CallbackMessage
from src.Agents import AgentClass
from src.Storage import add_user
from dotenv import load_dotenv as _load_dotenv
_load_dotenv()
import os, shutil
import logging

##### 日志系统
def setup_logging():
    """设置日志配置"""
    log_name = "MagicCat.log"
    log_dir = "log"
    log_path = os.path.join(log_dir, log_name)
    shutil.rmtree(log_dir, ignore_errors=True)
    if not os.path.exists(log_path):
        os.makedirs(log_dir, exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(log_path, encoding="utf-8"),
        ]
    )
    return logging.getLogger(log_name)


##### 用户表存储系统
user_storage = {}
class EchoTextHandler(ChatbotHandler):
    def __init__(self):
        super(ChatbotHandler, self).__init__()

    async def process(self, callback: CallbackMessage):
        """
        处理回调消息的主要方法
        Args:
            callback: 钉钉回调消息对象
        Returns:
            状态码和状态消息
        """
        logger = setup_logging()

        # 从回调数据中获取聊天消息
        incoming_message = ChatbotMessage.from_dict(callback.data)
        logger.info(incoming_message)
        logger.info(callback.data)

        # 提取消息文本内容并去掉前后空白
        text = incoming_message.text.content.strip()

        # 获取发送者的用户ID
        userid = callback.data['senderStaffId']

        # 将用户添加到存储中
        add_user("userid", userid)

        # # 使用代理处理用户消息
        # msg = AgentClass().run_agent(text)
        # logger.info(msg)

        # # 回复处理后的消息
        # self.reply_text(msg['output'], incoming_message)
        self.reply_text("你说的是" + text, incoming_message)

        return AckMessage.STATUS_OK, 'OK'
    



def main():
    logger = setup_logging()
    logger.info("启动钉钉客户端")

    # 从环境变量中获取应用 ID 和 Secret
    logger.info(f"应用ID: {os.getenv('DINGDING_ID')}")
    logger.info(f"使用凭证连接钉钉")

    try:
        credential = Credential(os.getenv("DINGDING_ID"), os.getenv("DINGDING_SECRET"))
        client = DingTalkStreamClient(credential, logger=logger)
        logger.info("钉钉客户端创建成功")

        # 注册回调处理器
        client.register_callback_handler(ChatbotMessage.TOPIC, EchoTextHandler())
        logger.info("已注册ChatbotMessage的回调处理器")

        # 启动客户端
        logger.info("正在启动钉钉客户端...")
        client.start_forever()

    except Exception as e:
        logger.error(f"连接钉钉时出错: {e}", exc_info=True)


if __name__ == "__main__":
    main()