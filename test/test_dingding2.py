import os, shutil
import logging
from dotenv import load_dotenv, find_dotenv
from dingtalk_stream import AckMessage, ChatbotMessage, DingTalkStreamClient, Credential, ChatbotHandler, CallbackMessage

def setup_logging():
    log_name = "MagicCat.log"
    log_dir = "log"
    log_path = os.path.join(log_dir, log_name)
    shutil.rmtree(log_dir, ignore_errors=True)
    if not os.path.exists(log_path):
        os.makedirs(log_dir, exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - MagicCat - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(), logging.FileHandler(log_path, encoding="utf-8")]
    )
    return logging.getLogger("MagicCat")

logger = setup_logging()

# 1) 可靠加载 .env（不在当前目录也能找到）
load_dotenv(find_dotenv(), override=False)

# 2) 读取并校验环境变量
APP_KEY = os.getenv("DINGDING_ID")           # 你的 appKey
APP_SECRET = os.getenv("DINGDING_SECRET")    # 你的 appSecret

def _mask(s, keep=6):
    if not s:
        return "None"
    return s[:keep] + "..." + str(len(s))

if not APP_KEY or not APP_SECRET:
    logger.error("环境变量未加载：请在 .env 中设置 DINGDING_ID / DINGDING_SECRET")
    logger.error(f"DINGDING_ID={_mask(APP_KEY)}, DINGDING_SECRET={_mask(APP_SECRET)}")
    raise SystemExit(1)

logger.info(f"应用ID: {_mask(APP_KEY)}   # 钉钉机器人 appkey")
logger.info("使用凭证连接钉钉")

class EchoTextHandler(ChatbotHandler):
    async def process(self, callback: CallbackMessage):
        msg = ChatbotMessage.from_dict(callback.data)
        text = msg.text.content.strip()
        # TODO: 调用你的 Agent
        self.reply_text(f"echo: {text}", msg)
        return AckMessage.STATUS_OK, "OK"

def main():
    try:
        # 3) 确保顺序正确：Credential(appKey, appSecret)
        credential = Credential(APP_KEY, APP_SECRET)
        client = DingTalkStreamClient(credential, logger=logger)
        logger.info("钉钉客户端创建成功")
        client.register_callback_handler(ChatbotMessage.TOPIC, EchoTextHandler())
        logger.info("已注册ChatbotMessage的回调处理器")
        logger.info("正在启动钉钉客户端...")
        client.start_forever()
    except Exception as e:
        logger.error(f"连接钉钉失败：{e}", exc_info=True)

if __name__ == "__main__":
    main()
