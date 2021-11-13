from asyncio import run

from src import get_result

while True:
    try:
        print(run(get_result(input()))["total"])
    except Exception as e:
        print(e)
