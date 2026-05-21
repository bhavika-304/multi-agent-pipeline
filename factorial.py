def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)

test_case = 5
result = factorial(test_case)
print(f'The factorial of {test_case} is {result}')
