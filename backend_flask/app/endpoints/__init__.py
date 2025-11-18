"""
Módulo que agrupa todos los blueprints (rutas) del backend Flask.
Cada archivo define un Blueprint diferente.
"""

from .login_bp import login_bp
from .participante_bp import participante_bp
from .programa_academico_bp import programa_academico_bp
from .participante_programa_academico_bp import participante_programa_academico_bp
from .reserva_bp import reserva_bp
from .reserva_participante_bp import reserva_participante_bp
from .sancion_participante_bp import sanciones_bp
from .edificio_bp import edificio_bp
from .facultad_bp import facultad_bp
from .sala_bp import sala_bp
from .turno_bp import turno_bp
from .reserva_reportes_bp import reserva_reportes_bp


__all__ = [
    "login_bp",
    "participante_bp",
    "programa_academico_bp",
    "participante_programa_academico_bp",
    "reserva_bp",
    "reserva_participante_bp",
    "sanciones_bp",
    "edificio_bp",
    "facultad_bp",
    "sala_bp",
    "turno_bp",
    "reserva_reportes_bp"
]
