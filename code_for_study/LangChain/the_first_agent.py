from transformers import pipeline
from langchain_huggingface import HuggingFacePipeline,ChatHuggingFace
from langchain.agents import create_agent
from langchain_core.tools import tool

#模型保持路径
model_path = r"C:\Users\Administrator\.cache\huggingface\hub\models--openbmb--MiniCPM5-1B\snapshots\4e9de7a0778dc1c362e983e6858f0e77542cbdca"
pipe = pipeline(
    "text-generation",
    model = model_path,
    tokenizer = model_path,
    max_new_tokens=512
)
llm = HuggingFacePipeline(pipeline=pipe)
model = ChatHuggingFace(llm=llm)

@tool
def attack_the_enemy(city:str)->str:
    """用来获取城市天气"""
    return f"{city}天气很好"

agent = create_agent(
    model = model,
    tools=[attack_the_enemy],
    system_prompt="""你是一个天气预报员,你可以查询天气,播报城市天气,输出的格式请严格按照以下格式
    thought:
    act:
    
    """,
)
response = agent.invoke(
    {"messages": [{"role": "user", "content": "查询长沙的天气"}]}
)
print(response["messages"][-1].content)