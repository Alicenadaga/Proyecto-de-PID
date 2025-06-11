dinero = prompt("cunato dinero tienes");
palitoHeladoA = 0.6;
palitoHeladoC= 1;
bombonHeladix =1.6;
bombonHeladovich=1.7;
bombonHelardo=1.8;
potecitoConfites=2.9;
poteEnKilogramo=2.9;
vuelto=0;

if(dinero<=1.5){
    vuelto=dinero-palitoHeladoC;
    document.write("el helado mas caro que puedes comprar es palitoHeladoC" + "y el vuelto es de " + vuelto + " USD");
}
else if(dinero<=1.7){
    vuelto=dinero-bombonHeladovich;
    document.write("el helado mas caro que puedes comprar es bombonHeladovich "  + "y el vuelto es de " + vuelto + " USD");
}
else if(dinero<=3){
    vuelto=dinero-2.9;
    document.write("el helado mas caro que puedes comprar es potecitoConfites y poteEnKilogramo " + "ademas el vuelto en cualquiera de los dos casos es de" + vuelto + " USD");
}

