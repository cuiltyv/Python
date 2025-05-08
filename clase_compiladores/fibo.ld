program fibo_sequence;

var prev, prevprev, num, nthNumber : int;

main {

    num = 1 
    prev = 0

    if(nthNumber > 1){
      do {
        prevprev = prev;
        prev = num;
        num = prev + prevprev;
        nthNumber = nthNumber - 1;
      } while (nthNumber > 1);
    } 

    print(num);
}
end

# El programa te da el resultado de la sequencia de fibonacci del numero n


