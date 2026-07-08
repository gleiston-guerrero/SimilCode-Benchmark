package Java.Idéntico;

public class CODE_IDENT_JAVA_003 {
    public static void main(String[] args) {
        int[] numeros = {64, 34, 25, 12, 22, 11, 90};
        int n = numeros.length;
        
        for(int i = 0; i < n-1; i++) {
            for(int j = 0; j < n-i-1; j++) {
                if(numeros[j] > numeros[j+1]) {
                    int temp = numeros[j];
                    numeros[j] = numeros[j+1];
                    numeros[j+1] = temp;
                }
            }
        }
        
        System.out.print("Números ordenados: ");
        for(int num : numeros) {
            System.out.print(num + " ");
        }
    }
}