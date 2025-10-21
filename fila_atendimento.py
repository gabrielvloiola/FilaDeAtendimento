import sys
from paciente import PacienteNode

class FilaDeAtendimento:
    # Implementação de uma fila duplamente ligada
    def __init__(self):
        self.head = None
        self.tail = None
        self._ultimo_atendido_foi_prioritario = True 

    def _get_memoria_atual(self) -> int:
        # Calcula a memória total usada pela fila
        total_memoria = sys.getsizeof(self)
        atual = self.head
        while atual:
            total_memoria += sys.getsizeof(atual)
            atual = atual.proximo
        return total_memoria

    def _monitorar_operacao(self, operacao: str, mem_antes: int):
        # Monitora e exibe o uso de memória antes e depois de uma operação
        mem_depois = self._get_memoria_atual()
        diferenca = mem_depois - mem_antes
        
        print("\n--- Relatório de Memória ---")
        print(f"Operação: {operacao}")
        print(f"Memória Antes:   {mem_antes} bytes")
        print(f"Memória Depois:  {mem_depois} bytes")
        print(f"Diferença:       {diferenca} bytes")
        print("----------------------------\n")
    # Exibe a fila do início ao fim
    def exibir_fila(self):
        if self.head is None:
            print("Fila vazia.")
            return

        partes = []
        atual = self.head
        while atual:
            partes.append(str(atual))
            atual = atual.proximo
        
        print("Fila Atual: " + " --> ".join(partes))

    def exibir_fila_invertida(self): # Exibe a fila do fim ao início
        if self.tail is None:
            print("Fila vazia.")
            return

        partes = []
        atual = self.tail
        while atual:
            partes.append(str(atual))
            atual = atual.anterior
        
        print("Fila Invertida: " + " --> ".join(partes))

    def adicionar_paciente(self, nome: str, idade: int, prioridade: int):
       # Adiciona um paciente na fila conforme a prioridade
        mem_antes = self._get_memoria_atual()
        novo_paciente = PacienteNode(nome, idade, prioridade)

        if self.head is None:
            self.head = novo_paciente
            self.tail = novo_paciente
        
        elif prioridade == 2:
            atual = self.head
            while atual and atual.prioridade == 2:
                atual = atual.proximo
            
            if atual is None:
                self.tail.proximo = novo_paciente
                novo_paciente.anterior = self.tail
                self.tail = novo_paciente
            elif atual == self.head:
                novo_paciente.proximo = self.head
                self.head.anterior = novo_paciente
                self.head = novo_paciente
            else:
                novo_paciente.proximo = atual
                novo_paciente.anterior = atual.anterior
                atual.anterior.proximo = novo_paciente
                atual.anterior = novo_paciente
        
        else:
            self.tail.proximo = novo_paciente
            novo_paciente.anterior = self.tail
            self.tail = novo_paciente
        
        print(f"Paciente {nome} adicionado.")
        self._monitorar_operacao(f"Adicionar ({nome})", mem_antes)

    def _contar_pacientes(self):
        # Conta o número de pacientes prioritários e não prioritários na fila
        cont_p = 0
        cont_n = 0
        atual = self.head
        while atual:
            if atual.prioridade == 2:
                cont_p += 1
            else:
                cont_n += 1
            atual = atual.proximo
        return cont_p, cont_n

    def _remover_no_especifico(self, no_a_remover: PacienteNode):
        if no_a_remover == self.head:
            self.head = no_a_remover.proximo
        if no_a_remover == self.tail:
            self.tail = no_a_remover.anterior
        
        if no_a_remover.anterior:
            no_a_remover.anterior.proximo = no_a_remover.proximo
        if no_a_remover.proximo:
            no_a_remover.proximo.anterior = no_a_remover.anterior
            
        no_a_remover.proximo = None
        no_a_remover.anterior = None
        return no_a_remover
    # Remove o próximo paciente conforme as regras de prioridade
    def remover_paciente(self):
        if self.head is None:
            print("Não há pacientes para remover.")
            return

        mem_antes = self._get_memoria_atual()
        
        cont_p, cont_n = self._contar_pacientes()
        
        proporcao_ativa = cont_n > 0 and (cont_p / cont_n) >= (1/7)
        
        paciente_a_remover = None
        
        if proporcao_ativa:
            if self._ultimo_atendido_foi_prioritario:
                atual = self.head
                while atual and atual.prioridade == 2:
                    atual = atual.proximo
                
                if atual:
                    paciente_a_remover = atual
                    self._ultimo_atendido_foi_prioritario = False
                else:
                    paciente_a_remover = self.head
                    self._ultimo_atendido_foi_prioritario = True
            else:
                paciente_a_remover = self.head
                self._ultimo_atendido_foi_prioritario = True
        else:
            paciente_a_remover = self.head
            if paciente_a_remover:
                self._ultimo_atendido_foi_prioritario = (paciente_a_remover.prioridade == 2)

        if paciente_a_remover is None:
             print("Fila ficou vazia.")
             return

        paciente_removido = self._remover_no_especifico(paciente_a_remover)
        
        print(f"Paciente Atendido: {paciente_removido.nome}")
        if self.head:
            print(f"Próximo da fila: {self.head.nome}")
        else:
            print("A fila está vazia.")
            
        self._monitorar_operacao(f"Remover ({paciente_removido.nome})", mem_antes)
    # Altera os dados de um paciente e reposiciona na fila se necessário
    def alterar_dados(self, nome_busca: str, novo_nome: str, nova_idade: int, nova_prioridade: int):
        atual = self.head
        while atual and atual.nome != nome_busca:
            atual = atual.proximo
            
        if atual is None:
            print(f"Paciente '{nome_busca}' não encontrado.")
            return
    # Altera os dados do paciente e reposiciona se a prioridade mudou
        mem_antes = self._get_memoria_atual()
        
        prioridade_mudou = (atual.prioridade != nova_prioridade)

        atual.nome = novo_nome
        atual.idade = nova_idade
        atual.prioridade = nova_prioridade
        
        if prioridade_mudou:
            print(f"Prioridade de {novo_nome} mudou. Reposicionando...")
            self._remover_no_especifico(atual)
            
            if self.head is None:
                self.head = atual
                self.tail = atual
            elif atual.prioridade == 2:
                no_posicao = self.head
                while no_posicao and no_posicao.prioridade == 2:
                    no_posicao = no_posicao.proximo
                # Reinsere o nó na posição correta
                if no_posicao is None:
                    self.tail.proximo = atual
                    atual.anterior = self.tail
                    self.tail = atual
                elif no_posicao == self.head:
                    atual.proximo = self.head
                    self.head.anterior = atual
                    self.head = atual
                else:
                    atual.proximo = no_posicao
                    atual.anterior = no_posicao.anterior
                    no_posicao.anterior.proximo = atual
                    no_posicao.anterior = atual
            else:
                self.tail.proximo = atual
                atual.anterior = self.tail
                self.tail = atual
        
        print(f"Dados de {novo_nome} alterados.")
        self._monitorar_operacao(f"Alterar ({novo_nome})", mem_antes)