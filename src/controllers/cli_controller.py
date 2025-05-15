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
