def candy_claw(n: list[int], b: int, e: int) -> tuple[int, int]:
    """
     returns the optimal time of when you should lower, and riase the claw to collect the most candies on n[t:s]
    """
    # base case no negative numbers TODO: what if there is one number?
    if [x for x in n[b:e] if x < 0]:
        return (b, e - 1)

    index = min_negative_index(n, b, e)
    t1, s1 = candy_claw(n, b, index)
    t2, s2 = candy_claw(n, index+1, e)
    sum1 = sum(n[t1:s1+1])
    sum2 = sum(n[t2:s2+1])
    sum3 = sum(n[])

def min_negative_index(n: list[int], b: int, e: int):
    """returns the min index of a negative number, if no negative numbers exist"""
    min_index = b
    for i in range(b, e):
        if n[min_index] > n[i]:
            min_index = i
    return min_index
