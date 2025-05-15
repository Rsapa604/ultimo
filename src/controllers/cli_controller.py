from src.services.user_service import UserService
from src.services.poll_service import PollService
from src.services.nft_service import NFTService

class CLIController:
    def __init__(self):
        self.user_service = UserService()
        self.poll_service = PollService()
        self.nft_service = NFTService()
        self.current_user = None
        self.session_token = None

    
    def run(self):
        print("=== Plataforma de Streaming CLI ===")
        while True:
            if not self.current_user:
                print("Comandos: registrar | login | salir")
            else:
                print(f"Usuario: {self.current_user}")
                print("Comandos: crear_encuesta | votar | cerrar_encuesta | resultados | mis_tokens | transferir_token | logout | salir")

            comando = input("> ").strip()

            if comando == "salir":
                print("Saliendo...")
                break

            if not self.current_user:
                if comando == "registrar":
                    self.registrar_usuario()
                elif comando == "login":
                    self.login_usuario()
                else:
                    print("Debes registrarte o iniciar sesión primero.")
            else:
                if comando == "crear_encuesta":
                    self.crear_encuesta()
                elif comando == "votar":
                    self.votar()
                elif comando == "cerrar_encuesta":
                    self.cerrar_encuesta()
                elif comando == "resultados":
                    self.mostrar_resultados()
                elif comando == "mis_tokens":
                    self.mostrar_tokens()
                elif comando == "transferir_token":
                    self.transferir_token()
                elif comando == "logout":
                    self.logout()
                else:
                    print("Comando no reconocido.")

    
    def registrar_usuario(self):
        username = input("Usuario: ").strip()
        password = input("Contraseña: ").strip()
        try:
            self.user_service.register(username, password)
            print(f"Usuario '{username}' registrado con éxito.")
        except Exception as e:
            print(f"Error: {e}")

    def login_usuario(self):
        username = input("Usuario: ").strip()
        password = input("Contraseña: ").strip()
        try:
            token = self.user_service.login(username, password)
            self.current_user = username
            self.session_token = token
            print(f"Login exitoso. Bienvenido {username}!")
        except Exception as e:
            print(f"Error: {e}")
    def crear_encuesta(self):
        pregunta = input("Pregunta: ").strip()
        opciones_str = input("Opciones (separadas por coma): ").strip()
        duracion = int(input("Duración (segundos): ").strip())
        tipo = input("Tipo (simple/multiple): ").strip().lower()
        opciones = [opt.strip() for opt in opciones_str.split(",")]
        try:
            poll_id = self.poll_service.create_poll(pregunta, opciones, duracion, tipo)
            print(f"Encuesta creada con ID: {poll_id}")
        except Exception as e:
            print(f"Error al crear encuesta: {e}")

    def votar(self):
        poll_id = input("ID de encuesta: ").strip()
        if self.poll_service.is_multiple_choice(poll_id):
            opciones_str = input("Opciones a votar (separadas por coma): ").strip()
            opciones = [opt.strip() for opt in opciones_str.split(",")]
        else:
            opcion = input("Opción a votar: ").strip()
            opciones = opcion
        try:
            self.poll_service.vote(poll_id, self.current_user, opciones)
            print("Voto registrado con éxito.")
        except Exception as e:
            print(f"Error al votar: {e}")

    def cerrar_encuesta(self):
        poll_id = input("ID de encuesta a cerrar: ").strip()
        try:
            self.poll_service.close_poll(poll_id)
            print("Encuesta cerrada.")
        except Exception as e:
            print(f"Error al cerrar encuesta: {e}")

    def mostrar_resultados(self):
        poll_id = input("ID de encuesta: ").strip()
        try:
            resultados = self.poll_service.get_final_results(poll_id)
            print("Resultados finales:")
            for opcion, datos in resultados.items():
                print(f"  {opcion}: {datos['count']} votos ({datos['percent']:.2f}%)")
        except Exception as e:
            print(f"Error al obtener resultados: {e}")