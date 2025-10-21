class PacienteNode: # Cada nó armazena os dados de um paciente
    def __init__(self, nome: str, idade: int, prioridade: int):
        self.nome = nome
        self.idade = idade
        self.prioridade = prioridade
        
        self.proximo = None
        self.anterior = None

    def __str__(self):
        label = "(P)" if self.prioridade == 2 else "(N)"
        return f"[{self.nome} ({self.idade} anos) {label}]"