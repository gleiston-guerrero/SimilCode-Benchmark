package Java.Estructural;

public class CODE_ESTRU_JAVA_001 {
    public static void main(String[] args) {
        int[] productos = {25, 30, 15, 40, 35};
        int total = 0;
        
        for(int i = 0; i < productos.length; i++) {
            total += productos[i];
        }
        
        double promedio = total / (double)productos.length;
        
        if(promedio >= 35) {
            System.out.println("Stock alto: " + promedio);
        } else if(promedio >= 25) {
            System.out.println("Stock medio: " + promedio);
        } else {
            System.out.println("Stock bajo: " + promedio);
        }
    }
}