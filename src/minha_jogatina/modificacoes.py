from models.status import StatusJogo

def reiniciar_jogo(self) -> None:
    """Reinicia o jogo, voltando ao status JOGANDO e zerando as horas."""
    if self.status == StatusJogo.NAO_INICIADO:
        raise ValueError(
            "Não é possível reiniciar um jogo que não foi iniciado.")
    self._horas_jogadas = 0.0
    self._status = StatusJogo.JOGANDO
    self._avaliacao = None


def __hash__(self) -> int:
    """Permite usar Jogo em sets e como chave de dicionário."""
    return hash((self.titulo.lower(), self.plataforma.lower()))
