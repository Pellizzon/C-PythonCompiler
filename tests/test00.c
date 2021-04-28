{
    i = 0;
    while (i < 4)
    {
        x = readln();
        if (x > 2 && i > 1)
        {
            println(x);
        }
        else if (!i)
        {
            println(i);
            x = x + --!i;
            println(x);
        }
        else if (!!x || !x)
        {
            println(!!x);
            x = x + x + x;
            println(x);
        }
        i = i + 1;
        println(i);
    }
}