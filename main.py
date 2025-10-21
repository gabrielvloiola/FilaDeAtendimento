from fila_atendimento import FilaDeAtendimento

def popular_fila_inicial(fila: FilaDeAtendimento):
    print("--- adicionando a primeira fila para testes ---")
    pacientes = [
        ("João", 30, 2),
        ("Maria", 25, 1),
        ("Carlos", 45, 2),
        ("Ana", 22, 1),
        ("Pedro", 65, 2),
        ("Julia", 33, 1),
        ("Marcos", 50, 2),
        ("Laura", 28, 1),
        ("Lucas", 70, 2),
        ("Sofia", 19, 1)
    ]
    
    for nome, idade, prioridade in pacientes:
        fila.adicionar_paciente(nome, idade, prioridade)
    
    print("--- Fila inicial adicionada ---")
    fila.exibir_fila()

def demonstracao_automatica(fila: FilaDeAtendimento):
    print("\n--- Inicio da Demonstração ---")
    # Exibe o estado inicial da fila
    print("\n[Estado Inicial da Fila]")
    fila.exibir_fila()
    fila.exibir_fila_invertida()
# Remove alguns pacientes
    print("\n[Removendo 3 pacientes]")
    fila.remover_paciente()
    fila.remover_paciente()
    fila.remover_paciente()
    fila.exibir_fila()
# Adiciona novos pacientes
    print("\n[Adicionando 2 novos pacientes]")
    fila.adicionar_paciente("Ricardo", 41, 1)
    fila.adicionar_paciente("Beatriz", 68, 2)
    fila.exibir_fila()
# Altera dados de um paciente
    print("\n[Alterando 'Ana' para Prioritário]")
    fila.alterar_dados("Ana", "Ana Silva", 23, 2)
    fila.exibir_fila()

    print("\n[Teste Regra 1:7 - 4 P / 5 N]")
    fila.remover_paciente()
    fila.exibir_fila()
    
    print("\n--- Fim da Demonstração ---")
    # Exibe o estado final da fila
def modo_interativo(fila: FilaDeAtendimento):
    print("\n--- Modo edição ---")
    print("Comandos: add [nome] [idade] [P/N], assist, edit [nome_atual] [novo_nome] [nova_idade] [P/N], show, show_inv, demo, exit")
    
    while True:
        try:
            comando_raw = input("> ").strip()
            if not comando_raw:
                continue
                
            partes = comando_raw.split()
            cmd = partes[0].lower()

            if cmd == "add":
                nome = partes[1]
                idade = int(partes[2])
                prio_str = partes[3].upper()
                prioridade = 2 if prio_str == "P" else 1
                fila.adicionar_paciente(nome, idade, prioridade)
            
            elif cmd == "assist":
                fila.remover_paciente()
            
            elif cmd == "edit":
                nome_busca = partes[1]
                novo_nome = partes[2]
                nova_idade = int(partes[3])
                prio_str = partes[4].upper()
                nova_prioridade = 2 if prio_str == "P" else 1
                fila.alterar_dados(nome_busca, novo_nome, nova_idade, nova_prioridade)
            
            elif cmd == "show":
                fila.exibir_fila()
            
            elif cmd == "show_inv":
                fila.exibir_fila_invertida()
            
            elif cmd == "demo":
                demonstracao_automatica(fila)

            elif cmd == "exit":
                print("Encerrando...")
                break
            
            else:
                print("Comando inválido.")
        
        except (IndexError, ValueError):
            print("Erro: Formato de comando incorreto.")
        except Exception as e:
            print(f"Ocorreu um erro inesperado: {e}")

if __name__ == "__main__":
    fila_principal = FilaDeAtendimento()
    
    popular_fila_inicial(fila_principal)
    
    modo_interativo(fila_principal)