import threading
import logging
import time
import openai
import asyncio
from pathlib import Path
from multiprocessing import JoinableQueue
from queue import Empty

logging.basicConfig(filename='gpt.log', level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))
logging = logging.getLogger()
logging.addHandler(console_handler)


class call_black_parameter(object):
    def __init__(self, response_str, messages, elapsed_time, completion_tokens, prompt_tokens, total_tokens, case_name):
        self.response_str = response_str
        self.messages = messages
        self.elapsed_time = elapsed_time
        self.completion_tokens = completion_tokens
        self.prompt_tokens = prompt_tokens
        self.total_tokens = total_tokens
        self.case_name = case_name


class GPTTaskManager:
    def __init__(self, num_thread, keys, stream=False, max_retries=3, key_limit=4096, model='gpt-4', temperature=0, top_p=1, presence_penalty=0, frequency_penalty=0, n=1, system_content=None, call_back=None):
        self.num_threads = num_thread
        self.stream = stream
        self.max_retries = max_retries
        self.task_queue = JoinableQueue()
        self.key_lock = threading.Lock()
        self.usable_openai_keys = self.process_token(keys=keys)
        self.key_limit = key_limit
        # 模型
        self.model = model
        # 用于控制生成文本的随机性和创造性的参数。值越高，生成文本越随机和创造性；值越低，生成文本越可预测和保守
        self.temperature = temperature
        # 用于对生成文本进行选择的参数，它表示只选择所有可能的令牌中累计概率高于给定阈值的那些令牌。默认值为1，表示选择所有可能的令牌
        self.top_p = top_p
        # 用于惩罚生成文本中未出现过的片段的参数。默认值为0，表示不进行惩罚
        self.presence_penalty = presence_penalty
        # 用于惩罚生成文本中频繁出现的重复片段的参数。默认值为0，表示不进行惩罚
        self.frequency_penalty = frequency_penalty
        # 要生成的文本的数量。默认为1，表示生成一段文本
        self.n = n
        # 是否将生成的文本作为流返回，而不是一次性返回所有文本。默认为False，表示一次性返回所有文本
        # 系统默认内容
        self.system_content = system_content
        self.total_tokens = 0
        self.prompt_tokens = 0
        self.completion_tokens = 0
        self.call_back = call_back
        self.threads = []
        self.__worker_flag = True

    def __worker(self, run_func):
        while True:
            try:
                task = self.task_queue.get(timeout=1)
                if task:
                    content = task.get("ask")
                    messages = task.get("messages")
                    run_func(task, content, messages)
                    self.task_queue.task_done()
            except Empty:
                break
            except Exception as e:
                logging.error(e)
                break

    def __run_tasks(self, tasks, run_func):
        logging.info("total tasks: %s" % len(tasks))
        for task in tasks:
            task["retry"] = False
            self.task_queue.put(task)
        if len(tasks) * 2 < self.num_threads:
            self.num_threads = len(tasks) * 2
        logging.info("Total threads: %s" % self.num_threads)
        for _ in range(self.num_threads):
            thread = threading.Thread(target=self.__worker, args=(run_func,))
            thread.start()
            self.threads.append(thread)
        for thread in self.threads:
            thread.join()
        # if self.task_is_empty():
        #     self.__worker_flag = False
        logging.info("Total tokens consumed in this round total_token: %s prompt_tokens: %s completion_tokens: %s" % (self.total_tokens, self.prompt_tokens, self.completion_tokens))

    @staticmethod
    def process_token(keys):
        usable_openai_keys = {}
        for key in keys:
            usable_openai_keys[key] = 0
        if len(usable_openai_keys) == 0:
            raise Exception("Unable to execute gpt task without token")
        return usable_openai_keys

    @staticmethod
    def read_prompt(path):
        return Path(path).read_text()

    def __retry_on_error(self, task, ask_content, messages, retries):
        retries += 1
        if retries <= self.max_retries:
            task["retry"] = True
            self.__process_task(task, ask_content, messages, retries=retries)
        else:
            self.task_queue.put(task)

    def __get_key(self):
        open_ai_key = None
        for token, token_limit in self.usable_openai_keys.items():
            if token_limit < self.key_limit:
                open_ai_key = token
                break
            else:
                logging.info("token: %s limit: %s" % (token, token_limit))
        return open_ai_key

    def __release_token(self, open_ai_key):
        self.usable_openai_keys[open_ai_key] = 0

    @staticmethod
    def get_active_thread_count():
        return threading.active_count() - 1

    def task_is_empty(self):
        return self.task_queue.empty()

    def add_task(self, tasks):
        logging.info("Successfully added tasks: %s" % len(tasks))
        for task in tasks:
            self.task_queue.put(task)

    def __process_task(self, task, ask_content, messages, retries=1):
        open_ai_key = self.__get_key()
        if open_ai_key:
            case_name = task.get("case", None)
            need_system = task.get("need_system", False)
            call_back_func = task.get("call_back", None)
            retry = task.get("retry", False)
            logging.info("case run: 【%s】" % case_name)
            if self.system_content and need_system and not retry:
                messages.append({"role": "system", "content": self.system_content})
                logging.info("auto add role = system success ")
            if not retry:
                messages.append({"role": "user", "content": ask_content})
            try:
                start_time = time.time()
                response = openai.ChatCompletion.create(
                    model=self.model,
                    messages=messages,
                    temperature=self.temperature,
                    api_key=open_ai_key
                )
                elapsed_time = time.time() - start_time
                response_str = response['choices'][0]['message']['content']
                messages.append({"role": response['choices'][0]['message']['role'], "content": response_str})
                completion_tokens = response['usage']['completion_tokens']
                prompt_tokens = response['usage']['prompt_tokens']
                total_tokens = response['usage']['total_tokens']
                self.total_tokens += total_tokens
                self.prompt_tokens += prompt_tokens
                self.completion_tokens += completion_tokens
                logging.info("request case 【%s】 cost time: %s second, prompt tokens: %s completion tokens: %s total tokens: %s" % (case_name, int(elapsed_time), prompt_tokens, completion_tokens, total_tokens))
                self.usable_openai_keys[open_ai_key] = total_tokens
                if call_back_func and self.call_back:
                    call_back_func = self.call_back.get(call_back_func, None)
                    if call_back_func:
                        call_back_func(call_black_parameter(response_str, messages, elapsed_time, completion_tokens, prompt_tokens, total_tokens, case_name))
            except openai.error.RateLimitError as e:
                logging.error(f"Retrying: {case_name}/{retries}, OpenAI API request exceeded rate limit: {e} api_key: {open_ai_key}")
                self.__release_token(open_ai_key)
                self.__retry_on_error(task, ask_content, messages, retries=retries)
            except openai.error.Timeout as e:
                logging.error(f"Retrying: {case_name}/{retries}, OpenAI API request timed out: {e} ")
                self.__retry_on_error(task, ask_content, messages, retries=retries)
            except openai.error.APIConnectionError as e:
                logging.error(f"Retrying: {case_name}/{retries}, OpenAI API request timed out, OpenAI API request failed to connect: {e}")
                self.__retry_on_error(task, ask_content, messages, retries=retries)
            except openai.error.APIError as e:
                logging.error(f"Retrying: {case_name}/{retries}, OpenAI API returned an API Error: {e}")
                self.__retry_on_error(task, ask_content, messages, retries=retries)
        else:
            self.task_queue.put(task)

    def task_run_tasks(self, tasks):
        self.__run_tasks(tasks=tasks, run_func=self.__process_task)


class GPTAsyncTaskManager(GPTTaskManager):
    def __init__(self, num_thread, keys, stream, max_retries, key_limit, model, temperature, top_p, presence_penalty, frequency_penalty, n, system_content, call_back=None):
        self.loop = asyncio.get_event_loop()
        self.task_queue = asyncio.Queue(maxsize=0)
        super(GPTAsyncTaskManager, self).__init__(num_thread, keys, stream=stream, max_retries=max_retries, key_limit=key_limit, model=model, temperature=temperature, top_p=top_p, presence_penalty=presence_penalty, frequency_penalty=frequency_penalty, n=n, system_content=system_content, call_back=call_back)


class GPT4(GPTAsyncTaskManager):
    def __init__(self, keys=None, model='gpt-4', temperature=0, top_p=1, presence_penalty=0, frequency_penalty=0, n=1, stream=False, system_content=None, num_threads=50, key_limit=4096, max_retries=3, call_back=None):
        self.keys = keys
        super(GPT4, self).__init__(num_thread=num_threads, keys=keys, stream=stream, max_retries=max_retries, key_limit=key_limit, model=model, temperature=temperature, top_p=top_p, presence_penalty=presence_penalty, frequency_penalty=frequency_penalty, n=n, system_content=system_content, call_back=call_back)

    def run_tasks(self, tasks):
        if not self.stream:
            logging.info("Mode: Multi threaded synchronous request gpt")
            logging.info("total tokens: %s" % len(self.keys))
            self.task_run_tasks(tasks=tasks)
