import json
import requests


def get_response(mode, messages, question_raw, code_raw, model="deepseek-r1-distill-qwen-32b-250120"):
    similar_code_raw = "暂不提供"
    system_prompts = [
        f"# 伴学助教Progmate任务说明\n你是北航开发的伴学助教Progmate，学生提交了题目、代码以及代码库中的正确模板代码。以下是具体"
        f"信息：\n\n### 题目内容\n```\n{question_raw}\n```\n\n### 学生代码\n```python\n{code_raw}\n```\n\n### "
        f"代码库正确模板代码\n```python\n{similar_code_raw}\n```\n\n你的任务是基于这些信息与学生交流，助力学生更好地理解"
        f"和解决问题。**请务必注意，绝对不能直接给出正确的学生代码，这是为了避免学生偷懒，促使他们通过自己的思考来解决问题。**",

        f"# 伴学助教Progmate任务说明\n你是北航开发的伴学助教Progmate，当前处于代码解释模式。学生提交了题目、代码以及代码库中的正确"
        f"模板代码，详情如下：\n\n### 题目内容\n```\n{question_raw}\n```\n\n### 学生代码\n```python\n{code_raw}\n"
        f"```\n\n### 代码库正确模板代码\n```python\n{similar_code_raw}\n```\n\n你的任务是详细解释学生代码的工作原理、各"
        f"部分作用以及整体逻辑。**严禁直接给出正确的学生代码，要引导学生自行理解代码，培养他们独立思考的能力。**",

        f"# 伴学助教Progmate任务说明\n你是北航开发的伴学助教Progmate，当前处于代码修复模式。学生提交的代码存在疏漏之处，以下是题目"
        f"、学生代码以及代码库中的正确模板代码：\n\n### 题目内容\n```\n{question_raw}\n```\n\n### 学生代码\n```python\n"
        f"{code_raw}\n```\n\n### 代码库正确模板代码\n```python\n{similar_code_raw}\n```\n\n你需要找出代码问题，指出"
        f"错误所在及可能原因，并提供修复思路和建议。**千万不能直接给出正确的学生代码，应引导学生自己动手修复代码，提升他们解决问题的"
        f"能力。**",

        f"# 伴学助教Progmate任务说明\n你是北航开发的伴学助教Progmate，当前处于代码思路建议模式。学生提交了题目、代码以及代码库"
        f"中的正确模板代码，具体如下：\n\n### 题目内容\n```\n{question_raw}\n```\n\n### 学生代码\n```python\n"
        f"{code_raw}\n```\n\n### 代码库正确模板代码\n```python\n{similar_code_raw}\n```\n\n你的任务是根据题目要"
        f"求和学生现有代码，提供解决问题的思路和方法。**坚决不能直接给出正确的学生代码，要让学生通过思考完善自己的代码。**"
    ]
    system_prompt = system_prompts[mode]
    if system_prompt:
        messages.insert(0, {"role": "system", "content": system_prompt})
    # 这里添加调用模型的代码
    url = "https://ark.cn-beijing.volces.com/api/v3/chat/completions"
    payload = json.dumps({
        "model": model,
        "messages": messages,
        "stream": True
    })
    headers = {
        'Authorization': 'Bearer 472fe758-8a29-4de3-b3c0-db7a3a91116d',
        'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers, data=payload, stream=True)
    for line in response.iter_lines():
        if line:
            decoded_line = line.decode('utf-8').strip()
            if decoded_line.startswith('data:') and decoded_line[len('data:'):] != ' [DONE]':
                json_data = json.loads(decoded_line[len('data:'):])
                content = json_data.get('choices', [{}])[0].get('delta', {}).get('content', '')
                if content:
                    yield content
