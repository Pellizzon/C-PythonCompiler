{
    int x;
    bool y;
    string z;
    x = 0;
    y = 3 > 2;
    z = "b";
    println(x);
    println(x + y);
    println(z);
    println(z == "a");

    while (x < 10 && y)
    {
        x = x + 1;
        println(x + y);
        if (x == 4 && y)
        {
            y = !y;
            println("y inverteu valor");
        }
    }
    println("saiu do while");

    /*ERRO:*/
    println(z > x);
    println(z == y);
    while (z)
    {
        println(z);
    }
}