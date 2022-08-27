import java.util.Base64;
import java.security.MessageDigest;
import javax.crypto.Cipher;
import javax.crypto.spec.IvParameterSpec;
import javax.crypto.spec.SecretKeySpec;

// Context : 
// in the CTF, i had an apk file, decompiled it, and found that i need to decrypt an AES cipher to get the flag.
// However, the encryption key was not hardcoded. The key was based on the pin code, so i wrote this small script to brute force the decryption key, based on the pin. 
// The pin is composed of 4 digits, used as a String ("0000" instead of 0). 


public class Main {
    public static void main(String[] args) {
        for (int i = 1000; i < 10000; i++) {
            String pin = Integer.toString(i);
            String decrypted = Crypto.decryptcipher("ED1nf3uLW4Hkwr1aGw+NpN5sgcRMPCFuk0XgtW181m4o6d0Ml3D/j6h1NSyOh4dbcGsbK6rcZOUyzHxWVb4QkA", pin);
            if (!decrypted.isEmpty() && decrypted.length() == 36) {
                System.out.println("The flag is : " + decrypted);
            }

        }
    }
}

public class Crypto {

    static String decryptcipher(String str, String pin) {
        try {
            byte[] bArr1 = Base64.getDecoder().decode(str);

            // Extracting first 16 bytes of IV
            byte[] iv = new byte[16];
            System.arraycopy(bArr1, 0, iv, 0, 16);
            IvParameterSpec ivp = new IvParameterSpec(iv);
            int l = bArr1.length - 16;
            byte[] bArr2 = new byte[l];
            System.arraycopy(bArr1, 16, bArr2, 0, l);

            // Generating the encryption key from the pin
            MessageDigest instance = MessageDigest.getInstance("MD5");
            instance.update(pin.getBytes("UTF-8"));
            byte[] key = new byte[16];
            System.arraycopy(instance.digest(), 0, key, 0, 16);
            SecretKeySpec aeskey = new SecretKeySpec(key, "AES");

            // AES Encryption
            Cipher obj = Cipher.getInstance("AES/CBC/PKCS5Padding");
            obj.init(2, aeskey, ivp);
            return new String(obj.doFinal(bArr2));
        } catch (Exception unused) {
            return "";
        }
    }
}