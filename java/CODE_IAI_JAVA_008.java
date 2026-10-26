package Java.Nuevo;

public class CONVERSION_METROS {
    public static void main(String[] args) {
        double valorMetros = 1500.0;
        String operacion = "metros_a_kilometros";
        double resul = 0.0;
        
        switch(operacion) {
            case "metros_a_kilometros":
                resul = valorMetros / 1000.0;
                break;
            case "metros_a_millas":
                resul = valorMetros / 1609.34;
                break;
            case "metros_a_pies":
                resul = valorMetros * 3.28084;
                break;
            case "metros_a_pulgadas":
                resul = valorMetros * 39.3701;
                break;
        }
        
        System.out.println(valorMetros + " metros = " + resul + " en " + operacion);
        
        if(resul > 1.0) {
            System.out.println("Resultado grande");
        } else {
            System.out.println("Resultado pequeño");
        }
    }
}
