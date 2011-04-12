import time
if __name__ == "__main__":
    start_time = time.clock()
    ans = -1
    for i in range(100, 1000):
        for j in range(100, i):
            if str(i * j) == str(i * j)[::-1] and ans < i * j:
                ans = i * j
    print(ans)
    print(time.clock() - start_time, "secs")

