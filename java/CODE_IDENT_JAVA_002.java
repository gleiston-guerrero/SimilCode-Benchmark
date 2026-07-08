package Java.Idéntico;

public class CODE_IDENT_JAVA_002 {
    public static void main(String[] args) {
        String password = "MiClave123";
        boolean tieneMinuscula = false;
        boolean tieneMayuscula = false;
        boolean tieneNumero = false;
        
        for(int i = 0; i < password.length(); i++) {
            char c = password.charAt(i);
            if(c >= 'a' && c <= 'z') tieneMinuscula = true;
            if(c >= 'A' && c <= 'Z') tieneMayuscula = true;
            if(c >= '0' && c <= '9') tieneNumero = true;
        }
        
        if(password.length() >= 8 && tieneMinuscula && tieneMayuscula && tieneNumero) {
            System.out.println("Contraseña válida");
        } else {
            System.out.println("Contraseña inválida");
        }
    }
}
