"""模型调用封装 — 基于 OpenAI 兼容接口。"""

from openai import OpenAI


class ModelClient:
    """单个模型的调用客户端。"""

    def __init__(self, name: str, api_key: str, base_url: str, timeout: int = 30):
        self.name = name
        self.client = OpenAI(api_key=api_key, base_url=base_url, timeout=timeout)

    def generate_code(self, prompt: str) -> str:
        """调用模型生成代码。返回原始响应文本。"""
        response = self.client.chat.completions.create(
            model=self.name,
            messages=[
                {
                    "role": "system",
                    "content": "你是一个专业的 Python 程序员。只返回代码，不要任何解释。",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.0,  # 保证可复现
            max_tokens=1024,
        )
        return response.choices[0].message.content or ""


def load_clients(config: dict) -> list[ModelClient]:
    """从配置文件加载所有模型客户端。"""
    clients = []
    for model_cfg in config.get("models", []):
        clients.append(
            ModelClient(
                name=model_cfg["name"],
                api_key=model_cfg["api_key"],
                base_url=model_cfg["base_url"],
                timeout=config.get("timeout", 30),
            )
        )
    return clients
