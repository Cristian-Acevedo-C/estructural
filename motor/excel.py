"""Intérprete de fórmulas de Excel en Python puro (determinístico, sin dependencias).

Replica la semántica de Excel que usa la Plantilla Memoria de Cálculo:
- precedencia de Excel: negación > % > ^ > * / > + - > & > comparaciones (−2^2 = 4; ^ asocia a la izquierda)
- celdas vacías valen 0 (o "" al compararlas con texto); TRUE/FALSE valen 1/0 en aritmética
- comparación de textos sin distinguir mayúsculas; orden entre tipos: número < texto < lógico
- IF sin rama falsa devuelve FALSE; los errores (#REF!, #DIV/0!, #NUM!, #VALUE!) se propagan
- ROUND redondea las mitades alejándose del cero, con 15 cifras significativas como Excel
- funciones: IF, AND, OR, NOT, ROUND, LN, LOG10, EXP, SQRT, ABS, ATAN, MIN, MAX, SUM, PI, MMULT, MINVERSE

No llama a Excel ni a ningún modelo de lenguaje.
"""
from __future__ import annotations

import math
import re
from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal
from typing import Callable

# ---------------------------------------------------------------- valores


@dataclass(frozen=True)
class ErrorExcel:
    codigo: str

    def __repr__(self) -> str:
        return self.codigo


REF = ErrorExcel("#REF!")
DIV0 = ErrorExcel("#DIV/0!")
NUM = ErrorExcel("#NUM!")
VALUE = ErrorExcel("#VALUE!")
NA = ErrorExcel("#N/A")
NAME = ErrorExcel("#NAME?")
ERRORES = {e.codigo: e for e in (REF, DIV0, NUM, VALUE, NA, NAME)}


class Matriz(list):
    """Rango o resultado matricial: lista de filas."""


def es_error(v) -> bool:
    return isinstance(v, ErrorExcel)


def escalar(v):
    """Un rango de 1×1 (o el resultado de MMULT de 1×1) se usa como valor."""
    if isinstance(v, Matriz):
        if len(v) == 1 and len(v[0]) == 1:
            return v[0][0]
        return VALUE
    return v


def numero(v):
    v = escalar(v)
    if es_error(v):
        return v
    if v is None:
        return 0.0
    if isinstance(v, bool):
        return 1.0 if v else 0.0
    if isinstance(v, (int, float)):
        return float(v)
    if isinstance(v, str):
        try:
            return float(v.strip()) if v.strip() else VALUE
        except ValueError:
            return VALUE
    return VALUE


def logico(v):
    v = escalar(v)
    if es_error(v):
        return v
    if v is None:
        return False
    if isinstance(v, bool):
        return v
    if isinstance(v, (int, float)):
        return v != 0
    if isinstance(v, str):
        if v.upper() == "TRUE":
            return True
        if v.upper() == "FALSE":
            return False
    return VALUE


def redondear(x: float, n: int) -> float:
    """ROUND de Excel: mitades alejándose del cero, sobre 15 cifras significativas."""
    if x == 0 or math.isinf(x) or math.isnan(x):
        return x
    d = Decimal(format(x, ".15g"))
    q = Decimal(1).scaleb(-n)
    return float(d.quantize(q, rounding=ROUND_HALF_UP))


def comparar(a, b, op: str):
    a, b = escalar(a), escalar(b)
    if es_error(a):
        return a
    if es_error(b):
        return b

    def clase(v):
        if isinstance(v, bool):
            return 2
        if isinstance(v, str):
            return 1
        return 0

    # vacío: se compara como 0, "" o FALSE según el otro lado
    if a is None:
        a = "" if isinstance(b, str) else (False if isinstance(b, bool) else 0.0)
    if b is None:
        b = "" if isinstance(a, str) else (False if isinstance(a, bool) else 0.0)
    ca, cb = clase(a), clase(b)
    if ca != cb:
        x, y = ca, cb
    elif ca == 1:
        x, y = a.lower(), b.lower()
    else:
        x, y = float(a), float(b)
    return {"=": x == y, "<>": x != y, "<": x < y, ">": x > y, "<=": x <= y, ">=": x >= y}[op]


# ---------------------------------------------------------------- análisis léxico y sintáctico

TOKEN = re.compile(
    r"""
    (?P<espacio>\s+)
  | (?P<texto>"(?:[^"]|"")*")
  | (?P<error>\#REF!|\#DIV/0!|\#NUM!|\#VALUE!|\#N/A|\#NAME\?)
  | (?P<ref>(?:(?:'(?:[^']|'')+'|[A-Za-zÁÉÍÓÚÑáéíóúñ_][\wÁÉÍÓÚÑáéíóúñ.]*)!)?\$?[A-Z]{1,3}\$?\d+(?::\$?[A-Z]{1,3}\$?\d+)?)
  | (?P<numero>\d+(?:\.\d*)?(?:[Ee][-+]?\d+)?|\.\d+(?:[Ee][-+]?\d+)?)
  | (?P<funcion>[A-Z][A-Z0-9.]*(?=\())
  | (?P<logico>TRUE|FALSE)
  | (?P<op><>|<=|>=|[-+*/^&=<>%(),;{}])
    """,
    re.VERBOSE,
)


def tokens(formula: str) -> list[tuple[str, str]]:
    out, i = [], 0
    while i < len(formula):
        m = TOKEN.match(formula, i)
        if not m:
            raise SyntaxError(f"no entiendo '{formula[i:i + 20]}' en {formula!r}")
        tipo = m.lastgroup
        if tipo != "espacio":
            out.append((tipo, m.group(tipo)))
        i = m.end()
    return out


def col_num(letras: str) -> int:
    n = 0
    for ch in letras:
        n = n * 26 + ord(ch) - 64
    return n


def col_letras(n: int) -> str:
    s = ""
    while n:
        n, r = divmod(n - 1, 26)
        s = chr(65 + r) + s
    return s


def partir_ref(texto: str, hoja_actual: str):
    """'Hoja'!$A$1:B2 → (hoja, (col1, fila1), (col2, fila2) | None)."""
    hoja = hoja_actual
    if "!" in texto:
        h, texto = texto.rsplit("!", 1)
        hoja = h[1:-1].replace("''", "'") if h.startswith("'") else h
    partes = texto.replace("$", "").split(":")

    def cf(p):
        m = re.match(r"([A-Z]+)(\d+)$", p)
        return col_num(m.group(1)), int(m.group(2))

    return hoja, cf(partes[0]), (cf(partes[1]) if len(partes) > 1 else None)


class Analizador:
    """Fórmula → árbol (tuplas). Nodos: ('num', x) ('txt', s) ('bool', b) ('err', e) ('ref', hoja, c, f)
    ('rango', hoja, c1, f1, c2, f2) ('neg', a) ('pct', a) ('bin', op, a, b) ('fn', nombre, [args])."""

    def __init__(self, formula: str, hoja: str):
        f = formula.strip()
        if f.startswith("{") and f.endswith("}"):
            f = f[1:-1]
        if f.startswith("="):
            f = f[1:]
        self.t = tokens(f)
        self.i = 0
        self.hoja = hoja

    def ver(self):
        return self.t[self.i] if self.i < len(self.t) else (None, None)

    def tomar(self, valor=None):
        tk = self.ver()
        if valor is not None and tk[1] != valor:
            raise SyntaxError(f"esperaba {valor!r} y vino {tk[1]!r}")
        self.i += 1
        return tk

    def analizar(self):
        n = self.comparacion()
        if self.i != len(self.t):
            raise SyntaxError(f"sobra {self.t[self.i:]}")
        return n

    def comparacion(self):
        n = self.concat()
        while self.ver()[1] in ("=", "<>", "<", ">", "<=", ">="):
            op = self.tomar()[1]
            n = ("bin", op, n, self.concat())
        return n

    def concat(self):
        n = self.suma()
        while self.ver()[1] == "&":
            self.tomar()
            n = ("bin", "&", n, self.suma())
        return n

    def suma(self):
        n = self.producto()
        while self.ver()[1] in ("+", "-"):
            op = self.tomar()[1]
            n = ("bin", op, n, self.producto())
        return n

    def producto(self):
        n = self.potencia()
        while self.ver()[1] in ("*", "/"):
            op = self.tomar()[1]
            n = ("bin", op, n, self.potencia())
        return n

    def potencia(self):
        n = self.unario()
        while self.ver()[1] == "^":
            self.tomar()
            n = ("bin", "^", n, self.unario())
        return n

    def unario(self):
        if self.ver()[1] == "-":
            self.tomar()
            return ("neg", self.unario())
        if self.ver()[1] == "+":
            self.tomar()
            return self.unario()
        n = self.primario()
        while self.ver()[1] == "%":
            self.tomar()
            n = ("pct", n)
        return n

    def primario(self):
        tipo, v = self.tomar()
        if tipo == "numero":
            return ("num", float(v))
        if tipo == "texto":
            return ("txt", v[1:-1].replace('""', '"'))
        if tipo == "logico":
            return ("bool", v == "TRUE")
        if tipo == "error":
            return ("err", ERRORES[v])
        if tipo == "ref":
            hoja, a, b = partir_ref(v, self.hoja)
            if b:
                return ("rango", hoja, a[0], a[1], b[0], b[1])
            return ("ref", hoja, a[0], a[1])
        if tipo == "funcion":
            self.tomar("(")
            args = []
            if self.ver()[1] != ")":
                while True:
                    if self.ver()[1] in (",", ";"):
                        args.append(None)  # argumento vacío
                    else:
                        args.append(self.comparacion())
                    if self.ver()[1] in (",", ";"):
                        self.tomar()
                        continue
                    break
            self.tomar(")")
            return ("fn", v, args)
        if v == "(":
            n = self.comparacion()
            self.tomar(")")
            return n
        raise SyntaxError(f"token inesperado {v!r}")


# ---------------------------------------------------------------- evaluación


def _minversa(m):
    n = len(m)
    if any(len(f) != n for f in m):
        return VALUE
    a = [[float(x) for x in f] + [1.0 if i == j else 0.0 for j in range(n)] for i, f in enumerate(m)]
    for c in range(n):
        piv = max(range(c, n), key=lambda r: abs(a[r][c]))
        if abs(a[piv][c]) < 1e-300:
            return NUM
        a[c], a[piv] = a[piv], a[c]
        p = a[c][c]
        a[c] = [x / p for x in a[c]]
        for r in range(n):
            if r != c and a[r][c] != 0:
                k = a[r][c]
                a[r] = [x - k * y for x, y in zip(a[r], a[c])]
    return Matriz([f[n:] for f in a])


def _mmult(x, y):
    if len(x[0]) != len(y):
        return VALUE
    return Matriz([[sum(float(x[i][k]) * float(y[k][j]) for k in range(len(y))) for j in range(len(y[0]))] for i in range(len(x))])


class Libro:
    """Celdas de una plantilla (fórmulas y constantes) con evaluación perezosa y memoria por cálculo."""

    def __init__(self, celdas: dict[str, dict[str, dict]]):
        # celdas[hoja][celda] = {"f": "=...", "v": constante}
        self.celdas = celdas
        self._arbol: dict[tuple[str, str], tuple] = {}

    def arbol(self, hoja: str, celda: str):
        k = (hoja, celda)
        if k not in self._arbol:
            self._arbol[k] = Analizador(self.celdas[hoja][celda]["f"], hoja).analizar()
        return self._arbol[k]

    def calculo(self, entradas: dict[tuple[str, str], object] | None = None) -> "Calculo":
        return Calculo(self, entradas or {})


class Calculo:
    def __init__(self, libro: Libro, entradas: dict[tuple[str, str], object]):
        self.libro = libro
        self.entradas = entradas
        self.memo: dict[tuple[str, str], object] = {}
        self._pila: set[tuple[str, str]] = set()

    def valor(self, hoja: str, celda: str):
        k = (hoja, celda)
        if k in self.entradas:
            return self.entradas[k]
        if k in self.memo:
            return self.memo[k]
        c = self.libro.celdas.get(hoja, {}).get(celda)
        if hoja not in self.libro.celdas:
            return REF
        if c is None:
            return None
        if c.get("f") is None:
            return c.get("v")
        if k in self._pila:
            raise RecursionError(f"referencia circular en {hoja}!{celda}")
        self._pila.add(k)
        v = self.ev(self.libro.arbol(hoja, celda))
        self._pila.discard(k)
        if isinstance(v, Matriz):  # fórmula matricial de una celda: valor de arriba a la izquierda
            v = v[0][0] if v and v[0] else VALUE
        self.memo[k] = v
        return v

    def rango(self, hoja, c1, f1, c2, f2):
        return Matriz([[self.valor(hoja, f"{col_letras(c)}{f}") for c in range(c1, c2 + 1)] for f in range(f1, f2 + 1)])

    # -- evaluación de nodos
    def ev(self, n):
        t = n[0]
        if t == "num" or t == "txt" or t == "bool" or t == "err":
            return n[1]
        if t == "ref":
            return self.valor(n[1], f"{col_letras(n[2])}{n[3]}")
        if t == "rango":
            return self.rango(*n[1:])
        if t == "neg":
            x = numero(self.ev(n[1]))
            return x if es_error(x) else -x
        if t == "pct":
            x = numero(self.ev(n[1]))
            return x if es_error(x) else x / 100
        if t == "bin":
            return self.binario(n[1], n[2], n[3])
        if t == "fn":
            return self.funcion(n[1], n[2])
        raise ValueError(n)

    def binario(self, op, a, b):
        x, y = self.ev(a), self.ev(b)
        if op in ("=", "<>", "<", ">", "<=", ">="):
            return comparar(x, y, op)
        if op == "&":
            x, y = escalar(x), escalar(y)
            for v in (x, y):
                if es_error(v):
                    return v

            def txt(v):
                if v is None:
                    return ""
                if isinstance(v, bool):
                    return "TRUE" if v else "FALSE"
                if isinstance(v, float) and v.is_integer():
                    return str(int(v))
                return str(v)

            return txt(x) + txt(y)
        x, y = numero(x), numero(y)
        if es_error(x):
            return x
        if es_error(y):
            return y
        if op == "+":
            return x + y
        if op == "-":
            return x - y
        if op == "*":
            return x * y
        if op == "/":
            return DIV0 if y == 0 else x / y
        if op == "^":
            if x == 0 and y < 0:
                return DIV0
            if x < 0 and not float(y).is_integer():
                return NUM
            try:
                r = x**y
            except OverflowError:
                return NUM
            return NUM if isinstance(r, complex) or math.isinf(r) else r
        raise ValueError(op)

    def funcion(self, nombre: str, args: list):
        if nombre == "IF":
            c = logico(self.ev(args[0]))
            if es_error(c):
                return c
            if c:
                return self.ev(args[1]) if len(args) > 1 and args[1] is not None else 0.0
            if len(args) > 2:
                return self.ev(args[2]) if args[2] is not None else 0.0
            return False
        valores = [self.ev(a) if a is not None else None for a in args]
        f: dict[str, Callable] = {
            "AND": self._and,
            "OR": self._or,
            "NOT": lambda v: (lambda x: x if es_error(x) else not x)(logico(v[0])),
            "ROUND": self._round,
            "LN": lambda v: self._mat1(v[0], lambda x: NUM if x <= 0 else math.log(x)),
            "LOG10": lambda v: self._mat1(v[0], lambda x: NUM if x <= 0 else math.log10(x)),
            "EXP": lambda v: self._mat1(v[0], math.exp),
            "SQRT": lambda v: self._mat1(v[0], lambda x: NUM if x < 0 else math.sqrt(x)),
            "ABS": lambda v: self._mat1(v[0], abs),
            "ATAN": lambda v: self._mat1(v[0], math.atan),
            "MIN": lambda v: self._agregado(v, min),
            "MAX": lambda v: self._agregado(v, max),
            "SUM": lambda v: self._agregado(v, sum),
            "PI": lambda v: math.pi,
            "MMULT": self._mmult,
            "MINVERSE": self._minverse,
            "INDEX": self._index,
            "TRANSPOSE": self._transpose,
        }.get(nombre)
        if f is None:
            return NAME
        return f(valores)

    @staticmethod
    def _plano(v):
        if isinstance(v, Matriz):
            return [x for fila in v for x in fila]
        return [v]

    def _and(self, vals):
        hubo = False
        res = True
        for v in vals:
            for x in self._plano(v):
                if es_error(x):
                    return x
                if x is None or isinstance(x, str):
                    continue
                hubo = True
                res = res and bool(x)
        return res if hubo else VALUE

    def _or(self, vals):
        hubo = False
        res = False
        for v in vals:
            for x in self._plano(v):
                if es_error(x):
                    return x
                if x is None or isinstance(x, str):
                    continue
                hubo = True
                res = res or bool(x)
        return res if hubo else VALUE

    def _round(self, vals):
        x, n = numero(vals[0]), numero(vals[1])
        if es_error(x):
            return x
        if es_error(n):
            return n
        return redondear(x, int(n))

    @staticmethod
    def _mat1(v, fn):
        x = numero(v)
        if es_error(x):
            return x
        return fn(x)

    def _agregado(self, vals, fn):
        nums = []
        for v in vals:
            for x in self._plano(v):
                if es_error(x):
                    return x
                if isinstance(x, (int, float)) and not isinstance(x, bool):
                    nums.append(float(x))
        if not nums:
            return 0.0
        return fn(nums)

    @staticmethod
    def _matriz(v):
        if isinstance(v, Matriz):
            for f in v:
                for x in f:
                    if es_error(x):
                        return x
                    if not isinstance(x, (int, float)) or isinstance(x, bool):
                        return VALUE
            return v
        x = numero(v)
        return x if es_error(x) else Matriz([[x]])

    def _mmult(self, vals):
        a, b = self._matriz(vals[0]), self._matriz(vals[1])
        if es_error(a):
            return a
        if es_error(b):
            return b
        return _mmult(a, b)

    def _minverse(self, vals):
        a = self._matriz(vals[0])
        if es_error(a):
            return a
        return _minversa(a)

    def _index(self, vals):
        a = vals[0]
        if es_error(a):
            return a
        if not isinstance(a, Matriz):
            a = Matriz([[a]])
        f = numero(vals[1]) if len(vals) > 1 and vals[1] is not None else 0.0
        c = numero(vals[2]) if len(vals) > 2 and vals[2] is not None else 0.0
        for x in (f, c):
            if es_error(x):
                return x
        f, c = int(f), int(c)
        if len(a) == 1 and c == 0:  # vector fila: el índice es la columna
            f, c = 1, f
        if c == 0 and len(a[0]) == 1:
            c = 1
        if not (1 <= f <= len(a)) or not (1 <= c <= len(a[0])):
            return REF
        return a[f - 1][c - 1]

    @staticmethod
    def _transpose(vals):
        a = vals[0]
        if not isinstance(a, Matriz):
            return a
        return Matriz([list(col) for col in zip(*a)])
