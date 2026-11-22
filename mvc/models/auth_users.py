import os 
from supabase import create_client, Client
from dotenv import load_dotenv
import logging

#Lee las variables de entorno
load_dotenv()

#Configura el sistema Logging
logger = logging.getLogger(__name__)

class Authenuser:

    def __init__(self) -> None:
        try:
            self.supabase: Client = create_client(
                os.environ.get("SUPABASE_URL" , ""),
                os.environ.get("SUPABASE_KEY" , "")
            )
        except Exception as error:
            logger.error(f"ERROR 100: {str(error)}")
            print(f"ERROR 100: {str(error)}")

    def iniciarSesion(self,email: str, password: str) -> dict[str,Any]|None:
        try:
            # Llamada a la función de autenticación de Supabase
            response = self.supabase.auth.sign_in_with_password(
                {
                "email": email,
                "password": password
                }
            )

            # Verifica si la respuesta contiene un error
            if response.get("error"):
                logger.error(f"ERROR 101: {response['error']['message']}")
                return None

            # Devuelve el usuario autenticado
            return response.get("data", {}).get("user")
        except Exception as error:
            logger.error(f"ERROR 102: {str(error)}")
            print(f"ERROR 102: {str(error)}")
            return None

if __name__ == "__main__":
    print("Autenticación de usuarios con Supabase")
    objeto = Authenuser()
    print(objeto.iniciarSesion("dejah@thark.org", "password123"))
    print(objeto.iniciarSesion("john@doe.com", "password456"))