{
    int x;
    bool y;
    string z;
    x = 1;
    y = x || true;
    z = "x:";
    println(x + y);
    println(z);
    println(x + z); /* ERROR */
}