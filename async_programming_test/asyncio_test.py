import asyncio 

# async def async_func1():
#     print("Hello")

# asyncio.run(async_func1())

# asyncio.run(async_func1())을 해체하면 아래와 같음
# loop = asyncio.get_event_loop()
# loop.run_until_complete(async_func1())
# loop.close()



##### 값을 리턴하지 않는 async 함수 #####
async def make_americano():
    print("Americano Start")
    await asyncio.sleep(3)
    # time.sleep가 CPU를 점유하면서 기다리는 것과 달리 asyncio.sleep은 CPU가 다른 코루틴을 처리할 수 있도록 CPU점유를 해제한 상태로 기다림.
    # 즉, 어떤 코루틴이 asyncio.sleep 함수를 실행하는 순간 이벤트 루프는 다른 코루틴을 실행시킴.
    # asyncio.sleep 또한 코루틴이며, 코루틴 내에서 다른 코루틴을 호출할 때 await 구문을 사용함.
    print("Americano End")

async def make_latte():
    print("Latte Start")
    await asyncio.sleep(5)
    print("Latte End")

async def main():
    coro1 = make_americano()
    coro2 = make_latte()
    await asyncio.gather( # 아메리카노를 만드는 코루틴과 라떼를 만드는 코루틴을 동시에 실행함.
        coro1, 
        coro2
    )

print("Main Start")
asyncio.run(main()) # 이벤트 루프를 생성하여 main 코루틴을 처리하고 이벤트 루프를 닫음.
print("Main End")
########################################



##### 값을 리턴하는 async 함수 #####
async def make_americano():
    print("Americano Start")
    await asyncio.sleep(3) 
    print("Americano End")
    return "Americano"

async def make_latte():
    print("Latte Start")
    await asyncio.sleep(5)
    print("Latte End")
    return "Latte"

async def main():
    coro1 = make_americano()
    coro2 = make_latte()
    result = await asyncio.gather(
        coro1, 
        coro2
    )
    print(result)

print("Main Start")
asyncio.run(main())
print("Main End")
###################################
