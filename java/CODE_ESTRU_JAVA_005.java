package Java.Estructural;

public class CODE_ESTRU_JAVA_005 {
    public static void main(String[] args) {
        String registro = "100,250,300,150,400,200,350";
        String[] ventas = registro.split(",");
        int totalVentas = ventas.length;
        int sumaTotal = 0;
        
        for(String venta : ventas) {
            sumaTotal += Integer.parseInt(venta);
        }
        
        System.out.println("Registro: " + registro);
        System.out.println("Total ventas: " + totalVentas);
        System.out.println("Suma total: " + sumaTotal);
        System.out.println("Promedio: " + (sumaTotal / totalVentas));
        
        for(String venta : ventas) {
            int valor = Integer.parseInt(venta);
            if(valor > 250) {
                System.out.println("Venta alta: " + valor);
            }
        }
    }
}
