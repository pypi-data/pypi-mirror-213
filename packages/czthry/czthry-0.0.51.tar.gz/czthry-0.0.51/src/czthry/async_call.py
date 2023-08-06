'''
异步执行
'''
import asyncio


async def make_async(func, it, i, count, semaphore):
    '''
    会把同步方法如`requests`异步化
    '''
    async with semaphore:
        await asyncio.to_thread(func, it, i, count)


async def make_tasks(task_func, task_data, sem):
    '''
    把需要处理的数据，循环提供给处理方法
    并用信号量进行限制
    '''
    semaphore = asyncio.Semaphore(sem)
    tasks = []
    count = len(task_data)
    for i in range(count):
        it = task_data[i]
        task = make_async(task_func, it, i, count, semaphore)
        tasks.append(task)
    await asyncio.gather(*tasks)


def async_call(task_func, task_data, sem):
    '''
    task_func: 数据处理的方法
        `func(item, index, total)`
        item: 每个要处理的数据
        index: 当前索引 - 便于掌握进度
        total: 数据总数
    task_data: 需要处理的数据列表
    sem: 同时最多处理的数量
    '''
    asyncio.run(make_tasks(task_func, task_data, sem))


if __name__ == '__main__':
    import requests
    result = []
    def go(it, index, total):
        print(index)
        requests.get('http://www.baidu.com')
        result.append([it, index, total])

    async_call(go, range(10), 3)
    for p in result:
        print(p)

