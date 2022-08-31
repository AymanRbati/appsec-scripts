import java.util.Base64;
import java.security.MessageDigest;
import javax.crypto.Cipher;
import javax.crypto.spec.IvParameterSpec;
import javax.crypto.spec.SecretKeySpec;

// Context : 
// in the CTF, i had an apk file, decompiled it, and found that i need to decrypt an AES cipher to get the flag.
// while i managed to find the encryption key, the decryption method below needs the right 4 digits pin. 
// In order to get the flag, i wrote the following code to bruteforce the pin.


public class Main {
    public static void main(String[] args) {


        for (int i = 0; i <= 9999; i++) {
            String pin = String.format("%04d",i);
            String decrypted = Crypto.decrypt("G38zckAufW4B9A6sywz28kzgW8CCx1UWugLUTjKlo/kwV1CVesmr0tPX/JZOW0aik0TlkrcAIZZ/G0BigUtmeg==", pin, "PD09PSBQM250M3N0M3JMNGIgPT09Pg==");
            if (!decrypted.isEmpty() && decrypted.length() == 36) {
               System.out.println("The flag is : " + decrypted);
           }
                
        }
    }
}

public class Crypto {


 public static String decrypt(String enc, String pin, String key) {
        try {
           
            key = new String(Base64.getDecoder().decode(key));
            byte[] decode = Base64.getDecoder().decode(enc); 
            byte[] bArr = new byte[decode.length];
            byte[] bArr2 = new byte[16];
            byte[] bArr3 = new byte[16];
            System.arraycopy(decode, 0, bArr2, 0, bArr2.length);
            IvParameterSpec ivParameterSpec = new IvParameterSpec(bArr2);
            int length = decode.length - 16;
            byte[] bArr4 = new byte[length];
            System.arraycopy(decode, 16, bArr4, 0, length);
            MessageDigest instance = MessageDigest.getInstance("MD5");
            instance.update(key.getBytes("UTF-8"));
            instance.update(pin.getBytes("UTF-8"));
            System.arraycopy(instance.digest(), 0, bArr3, 0, bArr3.length);
            SecretKeySpec secretKeySpec = new SecretKeySpec(bArr3, "AES");
            Cipher instance2 = Cipher.getInstance("AES/CBC/PKCS5Padding");
            instance2.init(2, secretKeySpec, ivParameterSpec);
            return new String(instance2.doFinal(bArr4));
        } catch (Exception e) {
           
            return "";
        }
    }

}