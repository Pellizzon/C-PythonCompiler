int soma(int x, int y, string z)
{
    int a;
    a = x + y;
    if (z == "a")
        println(a);
    return a;
}
int main()
{
    int a;
    int b;
    a = 3;
    b = soma(a, 5, "aa");
    println(a);
    println(b);
}