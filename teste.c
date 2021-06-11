int exibe(int x)
{
    println(x);
}

int fib(int n)
{
    exibe(n);
    if (n < 1 || n == 1)
        return n;
    return fib(n - 1) + fib(n - 2);
}

int main()
{
    int x;
    x = fib(9);
    exibe(x);
}