from parser import get_result
from asyncio import run

while True:
    try:
        print(run(get_result(input()))["total"])
    except Exception as e:
        print(e)
