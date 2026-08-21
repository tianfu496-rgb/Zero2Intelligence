# from transformers import pipeline
#
# pipe = pipeline("text-generation", model="openbmb/MiniCPM5-1B")
# messages = [
#     {"role": "user", "content": "Who are you?"},
# ]
# pipe(messages)

# from transformers import AutoTokenizer, AutoModelForCausalLM
#
# model_path = r"C:\Users\Administrator\.cache\huggingface\hub\models--openbmb--MiniCPM5-1B\snapshots\4e9de7a0778dc1c362e983e6858f0e77542cbdca"
#
# tokenizer = AutoTokenizer.from_pretrained(model_path)
# model = AutoModelForCausalLM.from_pretrained(model_path,device_map="auto")
# messages = [
#     {"role": "user", "content": "6*9=?"},
# ]
# inputs = tokenizer.apply_chat_template(
# 	messages,
# 	add_generation_prompt=True,
# 	tokenize=True,
# 	return_dict=True,
# 	return_tensors="pt",
# ).to(model.device)
#
# outputs = model.generate(**inputs, max_new_tokens=160)
# print(tokenizer.decode(outputs[0][inputs["input_ids"].shape[-1]:]))

from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from langchain_huggingface import HuggingFacePipeline, ChatHuggingFace
from langchain_core.messages import HumanMessage

# 1. 你的原始模型路径和加载逻辑
model_path = r"C:\Users\Administrator\.cache\huggingface\hub\models--openbmb--MiniCPM5-1B\snapshots\4e9de7a0778dc1c362e983e6858f0e77542cbdca"

# tokenizer = AutoTokenizer.from_pretrained(model_path)
# model = AutoModelForCausalLM.from_pretrained(model_path, device_map="auto")

# 2. 创建 transformers 的 text-generation pipeline
# 把你之前的 max_new_tokens=160 等参数放这里
pipe = pipeline(
    "text-generation",
    model=model_path,
    tokenizer=model_path,
    max_new_tokens=160,
    # 如果需要更丰富的生成控制，可以加这些参数：
    # do_sample=True,
    temperature=0.7,
    # top_p=0.9,
)

# 3. 将 transformers pipeline 包装成 LangChain 的 LLM
llm = HuggingFacePipeline(pipeline=pipe)

# 4. 包装成 Chat 模型 (关键步：它会自动处理 apply_chat_template)
chat_model = ChatHuggingFace(llm=llm)

# 5. 使用 LangChain 的标准消息格式调用
# 你不需要再手动 apply_chat_template 和切片解码了
messages = [
    HumanMessage(content="6*9=?"),
    # 也可以直接用字典格式：{"role": "user", "content": "6*9=?"}
]

# 调用模型
response = chat_model.invoke(messages)

# 打印结果
print(response.content)