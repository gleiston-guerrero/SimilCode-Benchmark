package Java.Funcional;

import java.util.regex.Pattern;

public class CODE_FUN_JAVA_002 {
    private String clave;
    
    public CODE_FUN_JAVA_002(String clave) {
        this.clave = clave;
    }
    
    public boolean validarLongitud() {
        return clave.length() >= 8;
    }
    
    public boolean contieneMayusculas() {
        return Pattern.compile("[A-Z]").matcher(clave).find();
    }
    
    public boolean contieneMinusculas() {
        return Pattern.compile("[a-z]").matcher(clave).find();
    }
    
    public boolean contieneDigitos() {
        return Pattern.compile("[0-9]").matcher(clave).find();
    }
    
    public boolean esSegura() {
        return validarLongitud() && contieneMayusculas() && 
               contieneMinusculas() && contieneDigitos();
    }
    
    public static void main(String[] args) {
        CODE_FUN_JAVA_002 verificador = new CODE_FUN_JAVA_002("MiClave123");
        System.out.println(verificador.esSegura() ? "Contraseña válida" : "Contraseña inválida");
    }
}