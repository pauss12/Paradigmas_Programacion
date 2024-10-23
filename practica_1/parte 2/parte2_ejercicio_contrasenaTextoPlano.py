from requests import get
import json
import hashlib
from Crypto.Hash import MD4

#FUNCION QUE IMPRIME SI LA CONTRASEÑA HA SIDO COMPROMETIDA O NO --------------------------------------------------------------------------------------------
def print_line(line, hash):
    hash = hash.upper()
    hash = hash[5:] #Quitar los 5 primeros caracteres del hash

    line = list(map(lambda x: x.split(":"), line.split("\n")))
    line = list(filter(lambda x: x[0] == hash, line))

    if len(line) == 0:
        print("\033[92m¡Tu contraseña no ha sido comprometida!\033[0m")
    else:
        print("\033[91m¡Tu contraseña ha sido comprometida!\033[0m")
        print(f"Veces que ha sido comprometida: {line[0][1]}")

#FUNCION QUE IMPRIME SI EL DOMINIO HA SIDO COMPROMETIDO O NO --------------------------------------------------------------------------------------------
def print_domain(line):

    if len(line) == 0:
        print("\033[92m¡El dominio no ha sido comprometido!\033[0m")
    else:
        print("\033[91m¡El dominio ha sido comprometido!\033[0m\n")
        list(map(lambda item: print(json.dumps(item, ensure_ascii=False, indent=4)), line))
        

#FUNCION QUE CREA LA URL DEPENDIENDO DEL TIPO DE HASH Y DEL DOMINIO --------------------------------------------------------------------------------------------
def create_url(hash, tipo_hash, domain):
    if tipo_hash == "SHA1" and domain == "":
        return  f"https://api.pwnedpasswords.com/range/{hash[:5]}"
    elif tipo_hash == "NTLM" and domain == "":
        return f"https://api.pwnedpasswords.com/range/{hash[:5]}?mode=ntlm"
    elif domain != "":
        return f"https://haveibeenpwned.com/api/v3/breaches?Domain={domain}"

#FUNCION QUE MUESTRA LAS OPCIONES DE HASHES --------------------------------------------------------------------------------------------
def mostrar_opcion_hashes():
    print("\nAhora: Seleccione el formato de hash: ")
    print("1. SHA1 ")
    print("2. NTLM (Windows) ")
    op = input("\nIngrese su elección (1 o 2): ").strip()
    if (op == "1"):
        return "SHA1"
    elif (op == "2"):
        return "NTLM"
    else:
        print("\033[91mOPCIÓN INVÁLIDA\033[0m\n")

#FUNCION QUE HACE LA PETICIÓN GET --------------------------------------------------------------------------------------------
def make_get_request(url, onsuccess, onerror, hash):
    response = get(url)
    if response.status_code == 200 and hash != "":
        onsuccess(response.text, hash)
    elif response.status_code == 200 and hash == "":
        onsuccess(json.loads(response.text))
    else:
        onerror()
    return 

#FUNCION QUE GENERA EL HASH DE LA CONTRASEÑA EN SHA1 ----------------------------------------------------------------------------------------
def sha1_hash(password):
    pass_encode = password.encode('utf-8')
    hash_no_digest = hashlib.sha1(pass_encode)
    hash = hash_no_digest.hexdigest()
    return hash

#FUNCION QUE GENERA EL HASH DE LA CONTRASEÑA EN NTLM ----------------------------------------------------------------------------------------
def ntlm_hash(password):
    pass_encode = password.encode('utf-16le')
    hash_no_digest = MD4.new(pass_encode)
    hash = hash_no_digest.hexdigest()
    return hash

#FUNCION QUE GENERA EL HASH DE LA CONTRASEÑA --------------------------------------------------------------------------------------------
def generate_hash(hash_func, password):
    hash = hash_func(password)
    return hash

#FUNCION QUE COMPRUEBA SI LA CONTRASEÑA HA SIDO COMPROMETIDA O SI EL DOMINIO HA SIDO COMPROMETIDO ---------------------------------------------------
def check_if_pwned(password, tipo_hash, domain):
    if (tipo_hash == "" and tipo_hash == ""):
        make_get_request(create_url("", "", domain), print_domain, lambda: print("\033[91mError al hacer la petición\033[0m\n"), hash="")
    elif tipo_hash == "SHA1":
        hash = generate_hash(sha1_hash, password)
        make_get_request(create_url(hash, tipo_hash, domain=""), print_line, lambda: print("\033[91mError al hacer la petición\033[0m\n"), hash)
    elif tipo_hash == "NTLM":
        hash = generate_hash(ntlm_hash, password)
        make_get_request(create_url(hash, tipo_hash, domain=""), print_line, lambda: print("\033[91mError al hacer la petición\033[0m\n"), hash)
   

# PRUEBAS ----------------------------------------------------------------
def pruebas():
    
    pass_sha1 = [
        "qwerty",
        "password",
        "1234567",
        "welcome",
        "123qwe",
        "G@t0r4d3@@"
    ]

    pass_ntlm = [
        "qwerty",
        "password",
        "1234567",
        "welcome",
        "123qwe",
        "G@t0r4d3@@"
    ]

    dominios = [
        "adobe.com",
        "linkedin.com",
        "tumblr.com",
        "dropbox.com",
        "yahoo.com",
        "u-tad.com"
    ]

    
    while True:
        print("\nSeleccione el modo de operación: ")
        print("1. Verificar contraseñas ")
        print("2. Verificar dominios ")
        op = input("\nIngrese su elección (1 o 2 o exit): ").strip()

        if (op == "1"):
            tipo_hash = mostrar_opcion_hashes()
            if (tipo_hash == "SHA1"):
                op = input("\n¿Quieres introducir un hash propio [Si no selecciona nada o algo q no sea si, se asignara automaticamente]? (si/no): ").strip()
                if (op == "si"):
                    password = input("\nIntroduce la contraseña: ").strip()
                    check_if_pwned(password, tipo_hash, "")
                else:
                    for password in pass_sha1:
                            print(f"Probando con el hash: {password}")
                            check_if_pwned(password, tipo_hash, "")
                            print("\n")

            elif (tipo_hash == "NTLM"):
                op = input("\n¿Quieres introducir un hash propio [Si no selecciona nada o algo q no sea si, se asignara automaticamente]? (si/no): ").strip()
                if (op == "si"):
                    password = input("\nIntroduce la contraseña: ").strip()
                    check_if_pwned(password, tipo_hash, "")
                else:
                    for password in pass_ntlm:
                            print(f"Probando con el hash: {password}")
                            check_if_pwned(password, tipo_hash, "")
                            print("\n")

        elif (op == "2"):
            op = input("\n¿Quieres introducir un dominio propio [Si no selecciona nada o algo q no sea si, se asignara automaticamente]? (si/no): ").strip()
            if (op == "si"):
                domain = input("\nIntroduce el dominio a verificar: ").strip()
                check_if_pwned("", "", domain)
            else:
                for domain in dominios:
                    print(f"Probando con el dominio: {domain}")
                    check_if_pwned("", "", domain)
                    print("\n")
                    
        elif (op == "exit"):
            print("\033[93m¡Hasta luego!\033[0m")
            break 
        else:
            print("\033[91mOPCIÓN INVÁLIDA\033[0m\n")


pruebas()
