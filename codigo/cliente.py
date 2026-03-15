import time
import rpyc

HOST = "localhost"
PORT = 18861

class StringVaziaError(Exception):
    def __init__(self, mensagem="Erro: o texto não pode ser vazio. digite algum caractere."):
        super().__init__(mensagem)


def menu():
    print("\n=== CLIENTE RPC ===")
    print("1 - Somar dois números")
    print("2 - Converter texto para maiúsculas")
    print("3 - Adicionar item na lista remota")
    print("4 - Listar itens da lista remota")
    print("5 - Limpar lista remota")
    print("6 - Chamada lenta (RPC síncrono)")
    print("7 - Multiplicar dois números")
    print("8 - Contar caracteres de uma string")
    print("0 - Sair")


def main():
    try:
        conn = rpyc.connect(HOST, PORT)
        print(f"Conectado ao servidor {HOST}:{PORT}")
    except Exception as e:
        print("Não foi possível conectar ao servidor.")
        print(f"Erro: {e}")
        return

    while True:
        menu()
        opcao = input("Escolha uma opção: ").strip()

        try:
            if opcao == "1":
                a = int(input("Digite o primeiro número: "))
                b = int(input("Digite o segundo número: "))
                resultado = conn.root.somar(a, b)
                print(f"Resultado remoto: {resultado}")

            elif opcao == "2":
                texto = input("Digite um texto: ")
                resultado = conn.root.maiusculas(texto)
                print(f"Resultado remoto: {resultado}")

            elif opcao == "3":
                item = input("Digite o item a adicionar: ")
                resultado = conn.root.adicionar_item(item)
                print(f"Lista remota atual: {resultado}")

            elif opcao == "4":
                resultado = conn.root.listar_itens()
                print(f"Lista remota atual: {resultado}")

            elif opcao == "5":
                resultado = conn.root.limpar_itens()
                print(f"Lista remota após limpeza: {resultado}")

            elif opcao == "6":
                segundos = int(input("Quantos segundos o servidor deve demorar? "))
                inicio = time.time()
                resultado = conn.root.demorar(segundos)
                fim = time.time()

                print(resultado)
                print(f"Tempo total de espera no cliente: {fim - inicio:.2f} s")

            elif opcao == "7":
                numero1 = input("Digite o primeiro número para multiplicar: ")
                numero2 = input("Digite o segundo número para multiplicar: ")
                resultado = conn.root.multiplicar(numero1, numero2)
                print(f"Resultado remoto: {resultado}")

            elif opcao == "8":
                texto = input("Digite uma string para contar os caracteres: ")
                if not texto.strip():
                    raise StringVaziaError()
                
                resultado = conn.root.contar_caracteres(texto)
                print(f"Resultado remoto: {resultado}")

            elif opcao == "0":
                print("Encerrando cliente.")
                conn.close()
                break

            else:
                print("Opção inválida.")

        except EOFError:
            print("\nConexão encerrada.")
            break

        except Exception as e:
            print(f"Erro durante a execução: {e}")


if __name__ == "__main__":
    main()