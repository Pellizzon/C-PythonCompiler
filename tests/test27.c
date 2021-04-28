{
    i = 0;
    while (i < 10)
    {
        if (i > 3)
            println(0);
        else if (i > 1)
        {
            println(1);
            i = i + 2;
        }
        else
        {
            println(9);
            i = i + 1;
        }
        i = i + 1;
    }
}