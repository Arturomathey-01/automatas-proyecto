import re
import math

# Diccionarios de términos reconocidos
operaciones = {
    "suma": "suma", 
    "resta": "resta",
    "mult": "multiplicacion", 
    "div": "division",
    "pot": "potencia",
    "RAIZ": "raiz", 
}

palabras_auxiliares = {
    "y": "operador",
    
}

# Funciones matemáticas
def ejecutar_suma(a, b):
    return a + b

def ejecutar_resta(a, b):
    return a - b

def ejecutar_multiplicacion(a, b):
    return a * b

def ejecutar_division(a, b):
    if b == 0:
        raise ValueError("División por cero no permitida")
    return a / b

def ejecutar_potencia(a, b):
    return math.pow(a, b)

def ejecutar_raiz(a):
    if a < 0:
        raise ValueError("No se puede calcular la raíz de un número negativo")
    return math.sqrt(a)

funciones_operaciones = {
    "suma": ejecutar_suma, "suma": ejecutar_suma,
    "resta": ejecutar_resta, "resta": ejecutar_resta, "res": ejecutar_resta,
    "multiplicacion": ejecutar_multiplicacion, "mult": ejecutar_multiplicacion,
    "divsion": ejecutar_division, "div": ejecutar_division,
    "potencia": ejecutar_potencia, "pot": ejecutar_potencia,
    "raiz": ejecutar_raiz, "RAIZ": ejecutar_raiz
}

def lexer(codigo):
    """
    Analizador léxico que tokeniza el código de entrada
    """
    if not codigo or not codigo.strip():
        return []
    
    # Especificación de tokens
    token_specification = [
        ('NUMBER', r'\d+(\.\d*)?'),           # Números enteros y decimales
        ('WORD', r'\b[a-zA-Záéíóúñ]+\b'),    # Palabras (incluye acentos)
        ('SKIP', r'[ \t]+'),                  # Espacios y tabs
        ('NEWLINE', r'\n'),                   # Saltos de línea
        ('MISMATCH', r'.'),                   # Cualquier otro carácter
    ]
    
    # Crear regex combinada
    tok_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_specification)
    
    tokens = []
    for mo in re.finditer(tok_regex, codigo):
        kind = mo.lastgroup
        value = mo.group()
        
        if kind == 'SKIP':
            continue
        elif kind == 'NUMBER':
            tokens.append(('NUM', float(value)))
        elif kind == 'WORD':
            tokens.append(('WORD', value))
        elif kind == 'NEWLINE':
            tokens.append(('NEWLINE', value))
        elif kind == 'MISMATCH':
            tokens.append(('UNKNOWN', value))
    
    return tokens

def realizar_analisis_lexico(codigo):
    """
    Realiza el análisis léxico completo del código
    """
    if not codigo or not codigo.strip():
        return {
            'error': 'No se proporcionó código para analizar',
            'tokens': [],
            'estadisticas': {'total': 0, 'validos': 0, 'invalidos': 0}
        }
    
    tokens = lexer(codigo)
    tokens_analizados = []
    palabras_desconocidas = []
    
    for token_type, token_value in tokens:
        if token_type == 'WORD':
            palabra_lower = token_value.lower()
            if palabra_lower in operaciones:
                tokens_analizados.append({
                    'tipo': operaciones[palabra_lower],
                    'operando': token_value,
                    'valido': True,
                    'categoria': 'operacion'
                })
            elif palabra_lower in palabras_auxiliares:
                tokens_analizados.append({
                    'tipo': palabras_auxiliares[palabra_lower],
                    'operando': token_value,
                    'valido': True,
                    'categoria': 'auxiliar'
                })
            else:
                tokens_analizados.append({
                    'tipo': 'DESCONOCIDO',
                    'valor': token_value,
                    'valido': False,
                    'categoria': 'desconocido'
                })
                palabras_desconocidas.append(token_value)
        
        elif token_type == 'NUM':
            tokens_analizados.append({
                'tipo': 'NUMERO',
                'valor': token_value,
                'valido': True,
                'categoria': 'numero'
            })
        
        elif token_type == 'NEWLINE':
            tokens_analizados.append({
                'tipo': 'SALTO_LINEA',
                'valor': '\\n',
                'valido': True,
                'categoria': 'control'
            })
        
        else:
            tokens_analizados.append({
                'tipo': 'DESCONOCIDO',
                'valor': token_value,
                'valido': False,
                'categoria': 'desconocido'
            })
    
    # Estadísticas
    validos = sum(1 for t in tokens_analizados if t['valido'])
    invalidos = len(tokens_analizados) - validos
    
    return {
        'tokens': tokens_analizados,
        'palabras_desconocidas': palabras_desconocidas,
        'estadisticas': {
            'total': len(tokens_analizados),
            'validos': validos,
            'invalidos': invalidos
        }
    }

def realizar_analisis_sintactico(codigo):
    """
    Realiza el análisis sintáctico del código
    """
    if not codigo or not codigo.strip():
        return {
            'error': 'No se proporcionó código para analizar',
            'lineas_analizadas': [],
            'es_valido': False
        }
    
    # Reglas sintácticas
    reglas_sintacticas = [
        {
            "pattern": r"^(sum|suma|rest|resta|res|mult|multiplicacion|div|division|pote|potencia) \d+(\.\d+)? y \d+(\.\d+)?$",
            "description": "Operación aritmética binaria",
            "tipo": "operacion_binaria"
        },
        {
            "pattern": r"^(raiz|raizc) \d+(\.\d+)?$",
            "description": "Operación de raíz cuadrada",
            "tipo": "operacion_unaria"
        },
        {
            "pattern": r"^asignar \w+ (valor|igual a) \d+(\.\d+)?$",
            "description": "Asignación de variable",
            "tipo": "asignacion"
        },
        {
            "pattern": r"^si \w+ (es|igual a|mayor que|menor que) \w+ entonces \w+$",
            "description": "Estructura condicional",
            "tipo": "condicional"
        }
    ]
    
    lineas = codigo.strip().split('\n')
    lineas_analizadas = []
    todas_validas = True
    
    for i, linea in enumerate(lineas, 1):
        linea_limpia = linea.strip().lower()
        if not linea_limpia:  # Saltar líneas vacías
            continue
        
        es_valida = False
        regla_coincidente = None
        
        # Verificar cada regla sintáctica
        for regla in reglas_sintacticas:
            if re.match(regla["pattern"], linea_limpia, re.IGNORECASE):
                es_valida = True
                regla_coincidente = regla
                break
        
        if not es_valida:
            todas_validas = False
        
        lineas_analizadas.append({
            'numero': i,
            'contenido': linea.strip(),
            'es_valida': es_valida,
            'tipo': regla_coincidente['tipo'] if regla_coincidente else None,
            'descripcion': regla_coincidente['description'] if regla_coincidente else 'Estructura sintáctica no reconocida'
        })
    
    # Análisis semántico básico
    tokens = lexer(codigo)
    palabras_desconocidas = []
    
    for token_type, token_value in tokens:
        if token_type == 'WORD':
            palabra_lower = token_value.lower()
            if not (palabra_lower in operaciones or palabra_lower in palabras_auxiliares):
                if token_value not in palabras_desconocidas:
                    palabras_desconocidas.append(token_value)
    
    return {
        'es_valido': todas_validas and len(palabras_desconocidas) == 0,
        'lineas_analizadas': lineas_analizadas,
        'validacion_semantica': {
            'palabras_desconocidas': len(palabras_desconocidas),
            'lista_desconocidas': palabras_desconocidas,
            'todas_palabras_validas': len(palabras_desconocidas) == 0
        },
        'estadisticas': {
            'total_lineas': len(lineas_analizadas),
            'lineas_validas': sum(1 for l in lineas_analizadas if l['es_valida']),
            'lineas_invalidas': sum(1 for l in lineas_analizadas if not l['es_valida'])
        }
    }

def ejecutar_operacion(tokens):
    """
    Ejecuta una operación aritmética basada en los tokens
    """
    operador = None
    operandos = []
    
    # Encontrar operador y operandos
    for token_type, token_value in tokens:
        if token_type == 'WORD' and token_value.lower() in funciones_operaciones:
            operador = token_value.lower()
        elif token_type == 'NUM':
            operandos.append(token_value)
    
    if not operador:
        return {'error': 'No se encontró una operación válida'}
    
    try:
        # Ejecutar operación según el tipo
        if operador in ['raiz', 'raiz']:
            if len(operandos) < 1:
                return {'error': 'La operación raíz requiere un operando'}
            resultado = funciones_operaciones[operador](operandos[0])
        else:
            if len(operandos) < 2:
                return {'error': f'La operación {operador} requiere dos operandos'}
            resultado = funciones_operaciones[operador](operandos[0], operandos[1])
        
        return {
            'exito': True,
            'operacion': operador,
            'operandos': operandos[:2] if operador not in ['raiz', 'raizc'] else [operandos[0]],
            'resultado': resultado
        }
    
    except Exception as e:
        return {'error': f'Error al ejecutar la operación: {str(e)}'}

def ejecutar_codigo(codigo):
    """
    Ejecuta el código proporcionado línea por línea
    """
    if not codigo or not codigo.strip():
        return {
            'error': 'No se proporcionó código para ejecutar',
            'resultados': []
        }
    
    # Primero verificar sintaxis
    analisis_sintactico = realizar_analisis_sintactico(codigo)
    if not analisis_sintactico['es_valido']:
        return {
            'error': 'El código contiene errores sintácticos y no puede ejecutarse',
            'detalles_sintaxis': analisis_sintactico,
            'resultados': []
        }
    
    lineas = codigo.strip().split('\n')
    resultados = []
    
    for i, linea in enumerate(lineas, 1):
        linea_limpia = linea.strip()
        if not linea_limpia:  # Saltar líneas vacías
            continue
        
        tokens = lexer(linea_limpia)
        resultado_linea = {
            'numero_linea': i,
            'contenido': linea_limpia,
            'exito': False,
            'mensaje': '',
            'resultado': None
        }
        
        try:
            # Determinar tipo de operación
            primera_palabra = None
            for token_type, token_value in tokens:
                if token_type == 'WORD':
                    primera_palabra = token_value.lower()
                    break
            
            if primera_palabra in funciones_operaciones:
                # Es una operación aritmética
                resultado_op = ejecutar_operacion(tokens)
                if 'error' in resultado_op:
                    resultado_linea['mensaje'] = resultado_op['error']
                else:
                    resultado_linea['exito'] = True
                    resultado_linea['mensaje'] = f'Operación {primera_palabra} ejecutada correctamente'
                    resultado_linea['resultado'] = resultado_op['resultado']
                    resultado_linea['detalles'] = resultado_op
            
            elif primera_palabra == 'asignar':
                # Simulación de asignación
                nombre_variable = None
                valor_variable = None
                
                for j, (token_type, token_value) in enumerate(tokens):
                    if token_type == 'WORD' and token_value.lower() == 'asignar' and j+1 < len(tokens):
                        if tokens[j+1][0] == 'WORD':
                            nombre_variable = tokens[j+1][1]
                    elif token_type == 'NUM':
                        valor_variable = token_value
                
                if nombre_variable and valor_variable is not None:
                    resultado_linea['exito'] = True
                    resultado_linea['mensaje'] = f'Variable "{nombre_variable}" asignada correctamente'
                    resultado_linea['resultado'] = valor_variable
                    resultado_linea['detalles'] = {
                        'variable': nombre_variable,
                        'valor': valor_variable,
                        'tipo': 'asignacion'
                    }
                else:
                    resultado_linea['mensaje'] = 'Error en la sintaxis de asignación'
            
            elif primera_palabra == 'si':
                # Simulación de condicional
                resultado_linea['exito'] = True
                resultado_linea['mensaje'] = 'Estructura condicional procesada (simulación)'
                resultado_linea['detalles'] = {
                    'tipo': 'condicional',
                    'estado': 'simulado'
                }
            
            else:
                resultado_linea['mensaje'] = f'Operación "{primera_palabra}" no reconocida'
        
        except Exception as e:
            resultado_linea['mensaje'] = f'Error de ejecución: {str(e)}'
        
        resultados.append(resultado_linea)
    
    # Estadísticas de ejecución
    exitosas = sum(1 for r in resultados if r['exito'])
    fallidas = len(resultados) - exitosas
    
    return {
        'exito': exitosas > 0,
        'resultados': resultados,
        'estadisticas': {
            'total_lineas': len(resultados),
            'exitosas': exitosas,
            'fallidas': fallidas
        }
    }