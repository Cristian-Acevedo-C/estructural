"""Motor de verificación estructural de postes ORBE.

Replica la "Plantilla Memoria de Cálculo" (docs/ESPECIFICACION.md): las fórmulas salen de la planilla y se evalúan
con un intérprete de fórmulas de Excel en Python puro (motor/excel.py). Sin Excel y sin modelos de lenguaje.

Uso:
  from motor import validar
  resultado = validar(config)        # config: dict (ver ejemplos/ y docs/MOTOR.md)
"""
from .validador import validar, tipos_disponibles

__all__ = ["validar", "tipos_disponibles"]
