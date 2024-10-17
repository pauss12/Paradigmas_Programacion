from requests import get
import json

#FUNCION QUE HACE LA PETICION GET -----------------------------------------------------------------------------------------------------------------
def make_get_request(url, onsuccess, onerror, hash):
    response = get(url)
    if response.status_code == 200 and hash != "":
        onsuccess(response.text, hash)
    elif response.status_code == 200 and hash == "":
        onsuccess(json.loads(response.text))
    else:
        onerror()
    return 

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

#FUNCION QUE COMPRUEBA SI LA CONTRASEÑA HA SIDO COMPROMETIDA O SI EL DOMINIO HA SIDO COMPROMETIDO ---------------------------------------------------
def check_if_pwned(hash, tipo_hash, domain):
    if (tipo_hash == "" and tipo_hash == ""):
        make_get_request(create_url("", "", domain), print_domain, lambda: print("\033[91mError al hacer la petición\033[0m\n"), hash="")
    else:
        make_get_request(create_url(hash, tipo_hash, domain=""), print_line, lambda: print("\033[91mError al hacer la petición\033[0m\n"), hash)

#FUNCION PRINCIPAL -----------------------------------------------------------------------------------------------------------------------------------
def main():
    while True:
        print("Seleccione el modo de operación: ")
        print("1. Verificar contraseñas ")
        print("2. Verificar dominios ")
        op = input("\nIngrese su elección (1 o 2 o exit): ").strip()

        if (op == "1"):
            tipo_hash = mostrar_opcion_hashes()
            hash = input("\nIntroduce el hash de la contraseña: ").strip()
            check_if_pwned(hash, tipo_hash, "")
            print("\n")
        elif (op == "2"):
            domain = input("\nIntroduce el dominio a verificar: ").strip()
            check_if_pwned("", "", domain)
            print("\n")
        elif (op == "exit"):
            print("\033[93m¡Hasta luego!\033[0m")
            break 
        else:
            print("\033[91mOPCIÓN INVÁLIDA\033[0m\n")

#SI QUIERES HACER TUS PROPIAS PRUEBAS DESCOMENTA LA SIGUIENTE LINEA
#main()

#SI QUIERES EJECUTAR EL PROGRAMA DESDE LA TERMINAL DESCOMENTA LA SIGUIENTE LINEA
def pruebas():
    hashes_sha1 = [
        "21BD1000F6468C6E4D09C0C239A4C2769501B3DD",  # se que ha sido comprometida
        "21BD1000F6468C6E4D09C0C239A4C2769501B3DL",  # Es el anterior pero cambiando la ultima letra
        "21BD102551CADE5DDB7F0819C22BFBAAC6705182",  # se que ha sido comprometida
    ]

    hashes_ntlm = [
        "21BD101446FFE612E7650459D4B1B67A", # se que ha sido comprometida
        "21BD101446FFE612E7650459D4B1B67B", # Es el anterior pero cambiando la ultima letra
        "21BD10543DDE8E9AB06E8536DBFDDEB6"
    ]


    for hash in hashes_sha1:
        print(f"Probando con el hash: {hash}")
        check_if_pwned(hash, "SHA1", "")
        print("\n")

    for hash in hashes_ntlm:
        print(f"Probando con el hash: {hash}")
        check_if_pwned(hash, "NTLM", "")
        print("\n")

    dominios = [
        "adobe.com",
        "linkedin.com",
        "tumblr.com",
        "dropbox.com",
        "yahoo.com",
        "u-tad.com"
    ]

    for dominio in dominios:
        print(f"Probando con el dominio: {dominio}")
        check_if_pwned("", "", dominio)
        print("\n")

pruebas()
