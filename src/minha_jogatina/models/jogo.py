from abc import ABC
from typing import Optional
from .status import StatusJogo

class Jogo(ABC):    
    def __init__(self, titulo: str, genero: str, plataforma: str):
        self._titulo = titulo
        self.genero = genero
        self.plataforma = plataforma
        self._horas_jogadas = 0.0
        self._status = StatusJogo.NAO_INICIADO
        self._avaliacao: Optional[float] = None

    @property
    def titulo(self) -> str:
        return self._titulo

    @titulo.setter
    def titulo(self, valor: str):
        if not valor or not valor.strip():
            raise ValueError("O título do jogo não pode ser vazio.")
        self._titulo = valor

    @property
    def horas_jogadas(self) -> float:
        return self._horas_jogadas

    @horas_jogadas.setter
    def horas_jogadas(self, valor: float):
        if valor < 0:
            raise ValueError("Horas jogadas não podem ser negativas.")
        self._horas_jogadas = valor

    @property
    def status(self) -> StatusJogo:
        return self._status

    @status.setter
    def status(self, novo_status: StatusJogo):
        # Requer ao menos 1 hora para finalizar
        if novo_status == StatusJogo.FINALIZADO and self.horas_jogadas < 1.0:
            raise ValueError("Não é possível finalizar um jogo com menos de 1h jogada.")
        self._status = novo_status

    @property
    def avaliacao(self) -> Optional[float]:
        return self._avaliacao

    @avaliacao.setter
    def avaliacao(self, nota: float):
        # Só permite avaliar jogos finalizados
        if self.status != StatusJogo.FINALIZADO:
            raise ValueError("O jogo só pode receber avaliação após ser marcado como 'FINALIZADO'.")
        if not (0 <= nota <= 10):
            raise ValueError("A avaliação deve ser entre 0 e 10.")
        self._avaliacao = nota

    def __str__(self):
        """Retorna resumo do jogo."""
        return f"{self.titulo} ({self.plataforma}) - {self.status.value}"

    def __repr__(self):
        """Retorna representação para debug."""
        return (f"Jogo(titulo='{self.titulo}', plataforma='{self.plataforma}', "
                f"status='{self.status.value}', horas={self.horas_jogadas})")

    def __eq__(self, outro):
        """Compara por título e plataforma."""
        if not isinstance(outro, Jogo):
            return False
        return (self.titulo.lower() == outro.titulo.lower() and 
                self.plataforma.lower() == outro.plataforma.lower())

    def __lt__(self, outro):
        """Ordena por horas jogadas."""
        if not isinstance(outro, Jogo):
            return NotImplemented
        return self.horas_jogadas < outro.horas_jogadas
