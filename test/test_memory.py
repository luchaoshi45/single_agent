# test_memory.py

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
# from langchain_core.runnables import RunnablePassthrough # 不再需要
from langchain_openai import ChatOpenAI
from src.Memory import MemoryClass # 确保导入正确
import os

# 测试使用
def test_memory():
    # 创建记忆
    memory_manager = MemoryClass()
    memory = memory_manager.set_memory(session_id="test_user")

    # 创建提示模板
    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一只可爱的魔法猫猫，记住之前的对话。"),
        MessagesPlaceholder(variable_name="chat_history"), # 期望一个 BaseMessage 列表
        ("user", "{input}")
    ])

    # 创建模型
    model = ChatOpenAI(model=os.getenv("BASE_MODEL", "gpt-3.5-turbo"))

    # --- 修改链的定义 ---
    # 不再使用 RunnablePassthrough.assign 来处理 memory
    # 而是在 invoke 时手动处理
    # 创建一个简单的链：prompt -> model
    chain = prompt | model

    # --- 修改调用方式 ---
    user_input = "你好，我是小明！"
    # 1. 获取内存变量 (这是一个字典 {'chat_history': [...]})
    memory_variables = memory.load_memory_variables({})
    # 2. 准备输入给链的字典，显式地将列表赋值给 'chat_history'
    chain_input = {
        "input": user_input,
        "chat_history": memory_variables["chat_history"] # 提取列表
    }

    # 调用链
    response = chain.invoke(chain_input) # <-- 传递正确的格式
    print("AI回复:", response.content)

    # 保存到记忆
    # 注意：save_context 期望的是原始输入和原始输出字典
    # 通常输入是 {"input": ...}，输出是 {"output": ...}
    memory.save_context({"input": user_input}, {"output": response.content})

    return memory

# 运行测试
if __name__ == "__main__": # 添加这个好习惯
    print(test_memory())