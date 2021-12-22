from asyncio import run

from src import get_result

while True:
    print(run(get_result(input())).total_formula)