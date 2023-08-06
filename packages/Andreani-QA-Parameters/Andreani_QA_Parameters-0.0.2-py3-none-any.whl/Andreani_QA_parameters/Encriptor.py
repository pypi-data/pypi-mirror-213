import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import base64
from cryptography.fernet import Fernet
from functions.Parameters import Parameters
import xml.etree.ElementTree as ET
import bz2
import xml.dom.minidom

PATH_FUNCTIONS = os.path.join(Parameters.current_path, 'functions\\src\\')
NAME_FILE_ENCRIPTED = 'environment_access.xml'
NAME_FILE_TEMPORAL = 'environment_access.xml'
ENVIROMENT_VAR = 'PYBOT_KEY'


class Encriptor:

    @staticmethod
    def get_enviroment_key_to_bytes():

        """

            Returns:
                Devuelve la variable de entonrno de PresentacionPybot convertida a formato bytes en base64.

        """

        enviroment_key = os.getenv(ENVIROMENT_VAR)
        backend = default_backend()
        salt = b's\xa5\xd8\\Yw\xfc\xf9\xb4\xb1\xa2(\x96\xf8\xd9\x8a'

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=backend
        )
        key = base64.urlsafe_b64encode(kdf.derive(enviroment_key.encode("utf-8")))
        return key

    @staticmethod
    def get_enviroment_key_from_file():

        """

            Description:
                Obtiene la key (bytes) de la variable de entorno "PYBOT_KEY".

            Returns:
                Devuelve la key en bytes.

        """

        key = ""
        enviroment_key = os.getenv(ENVIROMENT_VAR)
        if enviroment_key is not None:
            try:
                with open(enviroment_key, 'rb') as file:
                    key = file.read()
            except FileNotFoundError:
                print(f"No existe el archivo '{enviroment_key}'")
        else:
            print(f"No se encuentra cargada correctamente la variable de entorno f{ENVIROMENT_VAR}")
        return key

    def encrypt_file(self, file_origin=NAME_FILE_TEMPORAL, file_target=NAME_FILE_ENCRIPTED):

        """

            Description:
                Realiza la enctriptación de un archivo.

            Args:
                file_origin: Nombre del archivo origen que debe ser enctriptado.
                file_target: Nombre del archivo destino que sera encriptado.

        """

        path_origin = os.path.join(PATH_FUNCTIONS, file_origin)
        path_target = os.path.join(PATH_FUNCTIONS, file_target)

        key = self.get_enviroment_key_from_file()
        fe = Fernet(key)
        try:
            with open(path_origin, 'rb') as file:
                data = file.read()
            encrypted_data = fe.encrypt(data)
            with open(path_target, 'wb') as file:
                file.write(encrypted_data)
        except FileNotFoundError:
            print("El archivo buscado no existe en el directorio especificado.")

    def get_list_from_data_file(self, origin=NAME_FILE_ENCRIPTED):

        """

            Description:
                Genera una lista.

            Args:
                origin: Nombre del archivo encriptado.

            Returns:
                Devuelve una lista con todos los datos desencriptados.

        """

        key = self.get_enviroment_key_from_file()
        fe = Fernet(key)
        path_origin = os.path.join(PATH_FUNCTIONS, origin)

        with open(path_origin, 'rb') as file:
            encrypte_data = file.read()

        decrypted_data = fe.decrypt(encrypte_data)
        return decrypted_data.decode('utf-8').split('\r\n')

    def decrypt_file(self, origin=NAME_FILE_ENCRIPTED, target=NAME_FILE_TEMPORAL):

        """

            Description:
                Realiza la deseenctriptación de un archivo.

            Args:
                origin: Nombre del archivo origen que debe ser desenctriptado.
                target: Nombre del archivo destino que sera desencriptado.

        """

        data_list = self.get_list_from_data_file(origin)
        path_target = os.path.join(PATH_FUNCTIONS, target)
        try:
            with open(path_target, 'w') as file:
                for data in data_list:
                    file.write(f"{data}")
                    if data is not data_list[-1]:
                        file.write("\r")

        except Exception as e:
            print(f"Ah ocurrido un error al intentar guardar el archivo... {e.__class__.__name__}: {e}")

    def get_password_from_file_encrypted(self, enviroment, user):

        """

            Description:
                Busca una password en un archivo encriptado.

            Args:
                enviroment: Nombre del ambiente asociado al usuario del cual se pretende recuperar la password.
                user: Nombre del usuario del que se pretende recuperar la password.

            Returns:
                Devuelve la password del usuario.

        """

        password = None
        key = self.get_enviroment_key_from_file()
        fe = Fernet(key)
        path_origin = os.path.join(PATH_FUNCTIONS, NAME_FILE_ENCRIPTED)

        with open(path_origin, 'rb') as file:
            encrypte_data = file.read()

        decrypted_data = fe.decrypt(encrypte_data)
        pass_list = decrypted_data.decode('utf-8').split('\r')
        if 'AMBIENTE;IP;BASE;USUARIO;PASS' in pass_list:
            for row in pass_list:
                list_data_row = row.split(';')
                if enviroment and user in list_data_row:
                    password = list_data_row[-1]
                    break

        if password is None:
            raise Exception("Formato del archivo no es el correcto")

        else:
            return password
    #leer archivo XML
    def get_password_from_xml_file_encrypted(self,father_attribute ,atribute_to_search, dato_a_buscar, inner_search):
        key = self.get_enviroment_key_from_file()
        fe = Fernet(key)
        return_data = None
        path_origin = os.path.join(PATH_FUNCTIONS, NAME_FILE_ENCRIPTED)
        try:
            with open(path_origin, 'rb') as file:
                data = file.read()
            deencrypted_data = fe.decrypt(data)
            decompressed_data = bz2.decompress(deencrypted_data)
            file.close()
            read_xml_file = ET.fromstring(decompressed_data)
            # el siguiente for revisa utilizando un formato XPATH los datos requeridos por el usuario
            # y lo retorna si este existe
            for element in read_xml_file.findall(f"./{father_attribute}[@{atribute_to_search}='{dato_a_buscar}']/"):
                if element.tag == inner_search and (element.text != None or element.text != ""
                                                    or element.text != " "):
                    return_data = element.text
        except:
            raise "Ha Ocurrido un Error en el Tiempo de Ejecución -> ERROR CODE 204 (Encriptor)"

        return return_data

    @staticmethod
    def generate_key_pybot():

        """

            Description:
                Genera una clave y la guarda en un archivo.

            Returns:
                Devuelve pybot_key.key.

        """

        key = Fernet.generate_key()
        with open("../Proyectos/EscuelitaAutomatizacion/src/test/pybot_key.key", 'wb') as file:
            file.write(key)


    def compress_and_encrypt_xml(self, file_origin=NAME_FILE_TEMPORAL, file_target=NAME_FILE_ENCRIPTED):
        path_origin = os.path.join(PATH_FUNCTIONS, file_origin)
        path_target = os.path.join(PATH_FUNCTIONS, file_target)

        key = self.get_enviroment_key_from_file()
        fe = Fernet(key)
        try:
            with open(path_origin, 'rb') as file:
                data = file.read()
            compressed_data = bz2.compress(data)
            #print(compressed_data)
            encrypted_data = fe.encrypt(compressed_data)
            #print(encrypted_data)
            with open(path_target, 'wb') as output_file:
                output_file.write(encrypted_data)
        except FileNotFoundError:
            print("El archivo buscado no existe en el directorio especificado.")


    def decompress_and_deencrypt_xml(self, file_origin=NAME_FILE_TEMPORAL, file_target=NAME_FILE_ENCRIPTED):
        path_origin = os.path.join(PATH_FUNCTIONS, file_origin)
        path_target = os.path.join(PATH_FUNCTIONS, file_target)

        key = self.get_enviroment_key_from_file()
        fe = Fernet(key)
        try:
            with open(path_origin, 'rb') as file:
                data = file.read()
            deencrypted_data = fe.decrypt(data)
            decompressed_data = bz2.decompress(deencrypted_data)
            with open(path_target, 'wb') as output_file:
                output_file.write(decompressed_data)
        except FileNotFoundError:
            print("El archivo buscado no existe en el directorio especificado.")

    def get_all_data_from_xml_file_encrypted(self):
        key = self.get_enviroment_key_from_file()
        fe = Fernet(key)
        return_data = None
        path_origin = os.path.join(PATH_FUNCTIONS, NAME_FILE_ENCRIPTED)
        try:
            with open(path_origin, 'rb') as file:
                data = file.read()
            deencrypted_data = fe.decrypt(data)
            decompressed_data = bz2.decompress(deencrypted_data)
            print(xml.dom.minidom.parseString(decompressed_data).toprettyxml())
        except:
            raise "Ha Ocurrido un Error en el Tiempo de Ejecución -> ERROR CODE 204 (Encriptor)"





if __name__ == '__main__':
    pass
    #TXT
    #Encriptor().decrypt_file("environment_access.txt", "environment_access.txt")  # DESENCRIPTA
    #Encriptor().encrypt_file("environment_access.txt", "environment_access.txt")  # ENCRIPTA
    #XML
    Encriptor().compress_and_encrypt_xml() # ENCRIPTA
    #Encriptor().decompress_and_deencrypt_xml() # DESENCRIPTA
    #Encriptor().get_all_data_from_xml_file_encrypted()
