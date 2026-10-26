package Java.Original;

public class PasswordValidator {
    public static void main(String[] args) {
        String claveSegura = "MiClave123";
        boolean contieneMinuscula = false;
        boolean contieneMayuscula = false;
        boolean incluyeNumero = false;
        
        for(int indice = 0; indice < claveSegura.length(); indice++) {
            char caracter = claveSegura.charAt(indice);
            if(caracter >= 'a' && caracter <= 'z') contieneMinuscula = true;
            if(caracter >= 'A' && caracter <= 'Z') contieneMayuscula = true;
            if(caracter >= '0' && caracter <= '9') incluyeNumero = true;
        }
        
        if(claveSegura.length() >= 8 && contieneMinuscula && contieneMayuscula && incluyeNumero) {
            System.out.println("Contraseña válida");
        } else {
            System.out.println("Contraseña inválida");
        }
    }
}
