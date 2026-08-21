from transformers import  pipeline
from typing import Dict, Any
import re
# 1. 你的原始模型路径和加载逻辑
model_path = r"C:\Users\Administrator\.cache\huggingface\hub\models--openbmb--MiniCPM5-1B\snapshots\4e9de7a0778dc1c362e983e6858f0e77542cbdca"

ReAct_Message = [
    {
"role":"system",
"content":"""
你现在是一个游戏里的角色,可以打怪。你和游戏的怪物都是轮流行动的,第一回合是你的回合
角色参数:血量为100,攻击力25

可以调用的工具如下:
工具名:observe() 作用:立刻获取当前回合数,自身血量,敌人血量,敌人下一回合意图,不消耗行动
工具名:defend()  作用:使即将到来的伤害减少75%,在进入下一回合释放
工具名:attack()  作用:攻击敌人,伤害为角色攻击力,在进入下一回合释放

你回复必须严格遵循以下格式:
    Thought: 你的思考过程，用于分析问题、拆解任务和规划下一步行动。
    Action: 你决定采取的行动，必须是以下格式之一:
        '{{工具名}}[{{工具输入}}]`:调用一个可用工具。
        `Finish[最终答案]`:当你选择好本回合的行动后使用。
"""

    },
    {
"role":"user",
"content":"现在你碰到100血的怪物,请击败他"
    }
]

class ToolExecutor():
    def __init__(self):
        self.tools: Dict[str,Dict[str,Any]] = {}
    def registerTool(self,name:str,description:str,func:callable):
        if name in self.tools:
            print("️⚠️️Tool {} already registered".format(name))
        self.tools[name] = {'description':description,'func':func}
        print(f"⭐Tool registered: {name}")
    def getTool(self,name:str)->callable:
        if name in self.tools:
            return self.tools[name]['func']
        else:
            print("⚠️Tool {} not registered".format(name))
    def getAvailableTools(self)->str:
        """
        获取所有已注册工具的格式化字符串
        """
        return "\n".join(f"💫{name}:{info['description']}" for name,info in self.tools.items())

class ReActAgent:
    def __init__(self,chat_model,toolexectuor,max_steps = 15):
        self.chat_model = chat_model
        self.toolexectuor = toolexectuor
        self.max_steps = max_steps
        self.all_message = ReAct_Message
    def run(self):
        for step in range(self.max_steps):
            print(f"😀第{step}步")
            result_message = self.chat_model(self.all_message)
            print(result_message)
            if result_message is None:
                print("⚠️指令生成失败")

            thought, action = self._parse_output(result_message)

            if thought:
                print(f"😀思考:{thought}")
            else:
                print("解析思考失败")

            if not action:
                print("解析行动失败")
                break
            else:
                print(f"😀行动:{action}")

            if action.startswith("Finish"):
                final_answer = re.search(r"Finish:\[(.*)\]",action,re.DOTALL).group(1)
                print(f"🌷最终答案:{final_answer}")
                break

            func_name, param = self._parse_action(action)

            if not func_name:
                print("⚠️无效处理函数名格式")
                continue

            tool_func = self.toolexectuor.getTool(func_name)
            if not tool_func:
                print("⚠️没有找到该工具")
                observation = ("⚠️没有找到该工具")
                continue
            else:
                observation = tool_func(param)

            self.all_message.append({"role": "user", "content": {"thought":thought, "action":action, "observation":observation}})

    def _parse_output(self,output):
        thought_match = re.search(r"Thought:\s*(.*?)(?=\nAction:|$)",output, re.DOTALL)
        # Action: 匹配到文本末尾
        action_match = re.search(r"Action:\s*(.*?)$",output, re.DOTALL)
        thought = thought_match.group(1).strip() if thought_match else None
        action = action_match.group(1).strip() if action_match else None
        return thought, action

    def _parse_action(self,action):
        """解析Action字符串，提取工具名称和输入。
        """
        match = re.match(r"(\w+)\[(.*)\]", action, re.DOTALL)
        if match:
            return match.group(1), match.group(2)
        return None, None

class Character():
    def __init__(self,health = 100,attack_power = 25):
        self.health =health
        self.attack_power = attack_power
        self.determation = "attack"

    def defend(self):
        self.determation = "defend"

    def attack(self):
        self.determation = "attack"

class Enemy():
    def __init__(self,health,attack_power,booth_health):
        self.health =health
        self.attack_power = attack_power
        self.booth_health = 10
        self.determation = {"attack":self.attack_power}

    def enemy_turn(self):
        if self.determation == "attack":
            self.determation = {"defend":0.5}
        elif self.determation == "defend":
            self.determation = {"booth_health":self.booth_health}
        else: self.determation ="attack"

def observe(curret_round:int,main_character:Character,enemy:Enemy):
    """
    获取当前回合数,自身血量,敌人血量,敌人下一回合意图
    """
    return f"当前回合数:{curret_round};自身血量:{main_character.health};敌人血量:{enemy.health};敌人下一回合意图:{enemy.determation.keys()},数值为{enemy.determation.values()}"



if __name__ == "__main__":

    pipe = pipeline(
        "text-generation",
        model=model_path,
        tokenizer=model_path,
        max_new_tokens=160,
        # 如果需要更丰富的生成控制，可以加这些参数：
        # do_sample=True,
        # temperature=0.1,
        # top_p=0.9,
    )

    main_character = Character(health = 100,attack_power = 25)

    enemy = Enemy(health = 200,attack_power = 10,booth_health = 10)

    toolexecutor = ToolExecutor()

    curret_round = 1

    toolexecutor.registerTool(name="attack",description="作用:攻击敌人,伤害为角色攻击力,进入下一回合",func=main_character.attack())
    toolexecutor.registerTool(name="defend",description="作用:使即将到来的伤害减少75%,进入下一回合",func=main_character.defend())
    toolexecutor.registerTool(name="observe", description="作用:使即将到来的伤害减少75%,进入下一回合",func=observe(curret_round=curret_round,main_character=main_character,enemy=enemy))

    reactagent = ReActAgent(pipe,toolexecutor)

    while True:
        print(f"第{curret_round}回合")
        if enemy.health <=0 or main_character.health<=0:
            print("游戏已结束")
            break

        reactagent.run()
#检测玩家意图,并做出相应的行动

#检测敌人意图,并做出相应的行动

        curret_round += 1