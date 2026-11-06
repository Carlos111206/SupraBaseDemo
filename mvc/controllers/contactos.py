import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()


class ModelContactos:

    def __init__(self) -> None:
        try:
            self.supabase: Client = create_client(
                os.environ.get("SUPABASE_URL"),
                os.environ.get("SUPABASE_KEY")
            )

        except Exception as error:
            print(f"ERROR 100: {error}")

    def obtenerContactos(self):
        # SELECT * FROM contactos;
        response = self.supabase.table("contactos").select("*").execute()
        return response.data
    
    def bucarContacto(self,id_contacto:int):
        response = self.supabase.table("contactos").select("*").eq("id_contacto",id_contacto).execute()

    def insertarContacto(self, nombre,email,telefono):
        try:
            response = self.supabase.table("contactos").insert({
            "nombre":nombre,
            "email":email,
            "telefono":telefono
        }).execute()

            return response.data

        except Exception as error:
            print (f"ERROR 101:{error}")
            return None

    def borrarContacto(self,id_contacto:int):
        try:
            response = self.supabase.table("contactos").delete().eq("id_contacto",id_contacto).execute()

            return response.data
        
        except Exception as error:
            print (f"ERROR 101:{error}")
            return None

    def actuzalizarContacto(self, id_contacto,nombre,email,telefono):
        try:
            response = self.supabase.table("contactos").update({
            "nombre":nombre,
            "email":email,
            "telefono":telefono
        }).eq("id_contacto",id_contacto).execute()

            return response.data

        except Exception as error:
            print (f"ERROR 101:{error}")
            return None

            
if __name__ == "__main__":
    contactos = ModelContactos()
    print(contactos.obtenerContactos())

    contactos = contactos.obtenerContactos()

    #Almacena los datos los requisitos recibidos en Supabase 
    datos  = contactos.obetnerContactos

    print(datos)

    #Envia contactos.html los datos supabase


    resultado = contactos.actuzalizarContacto(
        "Edder",
        "Nuevo@gmail.com",
        "7777777" 
    )
    print(resultado)
