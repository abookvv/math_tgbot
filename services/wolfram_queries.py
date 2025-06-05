import wolframalpha
from config.settings_wolfram import wolfram_config
import asyncio

class WolframClient:
    def __init__(self):
        self.client = wolframalpha.Client(wolfram_config.myanimelist_client_id)
        self.cache = {}

    async def ask(self, query: str) -> str:
        try:
            loop = asyncio.get_event_loop()
            res = await asyncio.wait_for(
                loop.run_in_executor(None, self.client.query, query),
                timeout=5  # ⏱️ Ограничиваем время ожидания
            )
            answer = next(res.results).text
            self.cache[query] = answer
            return answer
        except asyncio.TimeoutError:
            return "⏱️ Превышено время ожидания ответа от WolframAlpha."
        except StopIteration:
            return "❌ Ответ не найден."
        except Exception as e:
            return f"⚠️ Произошла ошибка: {e}"


