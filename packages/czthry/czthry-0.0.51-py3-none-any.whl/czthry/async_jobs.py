'''
通过协程异步执行批量工作

给定数组，作为重复任务的执行参数
并行执行，
统一返回结果
'''
import asyncio
from concurrent.futures import ThreadPoolExecutor


class AsyncJobs(object):
    def __init__(self, concurrent_num=10):
        self._work = None
        self._loop = asyncio.get_event_loop()
        self._loop.set_default_executor(ThreadPoolExecutor(concurrent_num))  # 并行数量
        pass

    async def _do_work(self, arg):
        result = await self._loop.run_in_executor(None, self._work, arg)
        return result

    def do(self, tasks, work, finish=None):
        self._work = work
        works = [self._do_work(arg) for arg in tasks]
        jobs = asyncio.gather(*works)
        self._loop.run_until_complete(jobs)
        results = jobs.result()
        if callable(finish):
            finish(results)

    def __del__(self):
        self._work = None


def test():
    import time
    def hard_work(arg):
        print(arg)
        if arg==0:
            time.sleep(5)
        else:
            time.sleep(1)
        print(f'--{arg*2}--')
        return arg*2

    def finish(results):
        print('%s'%results)
        pass

    jobs = AsyncJobs(8)
    tasks = list(range(10))
    aaa = time.time()
    jobs.do(tasks, hard_work, finish)
    bbb = time.time()
    print('%s' % (bbb - aaa))


if __name__ == '__main__':
    test()
