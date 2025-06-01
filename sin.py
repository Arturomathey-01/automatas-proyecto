import re
from lex import lexer, operaciones, palabras_auxiliares, ejecutar_operacion

# Reglas sintácticas extendidas
reglas_sintacticas_extendidas = [
    {
        "pattern": r"^(suma|resta|multiplicacion|division|potencia) \d+(\.\d+)? y \d+(\.\d+)?$",
        "description": "Operación aritmética con dos operandos",
        "tipo": "operacion_binaria",
        "prioridad": 1
    },
    {
        "pattern": r"^(raiz|raiz) \d+(\.\d+)?$",
        "description": "Operación aritmética con un operando",
        "tipo": "operacion_unaria",
        "prioridad": 1
    },
    {
        "pattern": r"^(asignar) \w+ (valor|igual a) \d+(\.\d+)?$",
        "description": "Asignación de variable",
        "tipo": "asignacion",
        "prioridad": 2
    },
    {
        "pattern": r"^(si) \w+ (es|igual a|mayor que|menor que) \w+ (entonces) \w+$",
        "description": "Estructura condicional",
        "tipo": "condicional",
        "prioridad": 3
    },
    {
        "pattern": r"^mostrar \w+$",
        "description": "Mostrar variable",
        "tipo": "mostrar",
        "prioridad": 2
    },
    {
        "pattern": r"^comentario .+$",
        "description": "Línea de comentario",
        "tipo": "comentario",
        "prioridad": 0
    }
]

def analizar_estructura_completa(codigo):
    """
    Análisis sintáctico más detallado con información de estructura
    """
    if not codigo or not codigo.strip():
        return {
            "error": "No se proporcionó código para analizar",
            "estructura": {},
            "es_valido": False
        }
    
    lineas = codigo.strip().split('\n')
    estructura = {
        "operaciones": [],
        "asignaciones": [],
        "condicionales": [],
        "comentarios": [],
        "errores": []
    }
    
    es_valido_global = True
    
    for i, linea in enumerate(lineas, 1):
        linea_limpia = linea.strip().lower()
        if not linea_limpia:
            continue
        
        regla_encontrada = None
        for regla in reglas_sintacticas_extendidas:
            if re.match(regla["pattern"], linea_limpia, re.IGNORECASE):
                regla_encontrada = regla
                break
        
        info_linea = {
            "numero": i,
            "contenido": linea.strip(),
            "tipo": regla_encontrada["tipo"] if regla_encontrada else "error",
            "descripcion": regla_encontrada["description"] if regla_encontrada else "Estructura no reconocida",
            "es_valida": regla_encontrada is not None
        }
        
        if regla_encontrada:
            if regla_encontrada["tipo"] == "operacion_binaria" or regla_encontrada["tipo"] == "operacion_unaria":
                estructura["operaciones"].append(info_linea)
            elif regla_encontrada["tipo"] == "asignacion":
                estructura["asignaciones"].append(info_linea)
            elif regla_encontrada["tipo"] == "condicional":
                estructura["condicionales"].append(info_linea)
            elif regla_encontrada["tipo"] == "comentario":
                estructura["comentarios"].append(info_linea)
        else:
            estructura["errores"].append(info_linea)
            es_valido_global = False
    
    return {
        "es_valido": es_valido_global,
        "estructura": estructura,
        "estadisticas": {
            "total_lineas": len([l for l in lineas if l.strip()]),
            "operaciones": len(estructura["operaciones"]),
            "asignaciones": len(estructura["asignaciones"]),
            "condicionales": len(estructura["condicionales"]),
            "comentarios": len(estructura["comentarios"]),
            "errores": len(estructura["errores"])
        }
    }

def validar_semantica_avanzada(codigo):
    """
    Validación semántica más avanzada
    """
    tokens = lexer(codigo)
    variables_declaradas = set()
    variables_usadas = set()
    operaciones_realizadas = []
    
    i = 0
    while i < len(tokens):
        token_type, token_value = tokens[i]
        
        if token_type == 'WORD':
            palabra_lower = token_value.lower()
            
            # Detectar asignaciones
            if palabra_lower == 'asignar' and i + 1 < len(tokens):
                if tokens[i + 1][0] == 'WORD':
                    variables_declaradas.add(tokens[i + 1][1])
            
            # Detectar uso de variables en condicionales
            elif palabra_lower == 'si' and i + 1 < len(tokens):
                if tokens[i + 1][0] == 'WORD':
                    variables_usadas.add(tokens[i + 1][1])
            
            # Detectar operaciones
            elif palabra_lower in operaciones:
                operaciones_realizadas.append(palabra_lower)
        
        i += 1
    
    # Variables usadas pero no declaradas
    variables_no_declaradas = variables_usadas - variables_declaradas
    
    return {
        "variables_declaradas": list(variables_declaradas),
        "variables_usadas": list(variables_usadas),
        "variables_no_declaradas": list(variables_no_declaradas),
        "operaciones_realizadas": operaciones_realizadas,
        "es_semanticamente_correcto": len(variables_no_declaradas) == 0
    }

def generar_reporte_completo(codigo):
    """
    Genera un reporte completo del análisis
    """
    if not codigo or not codigo.strip():
        return {"error": "No se proporcionó código para analizar"}
    
    # Realizar todos los análisis
    analisis_estructura = analizar_estructura_completa(codigo)
    analisis_semantico = validar_semantica_avanzada(codigo)
    tokens = lexer(codigo)
    
    # Contar tipos de tokens
    conteo_tokens = {}
    for token_type, token_value in tokens:
        conteo_tokens[token_type] = conteo_tokens.get(token_type, 0) + 1
    
    reporte = {
        "resumen": {
            "es_valido": analisis_estructura["es_valido"] and analisis_semantico["es_semanticamente_correcto"],
            "total_tokens": len(tokens),
            "lineas_procesadas": analisis_estructura["estadisticas"]["total_lineas"]
        },
        "analisis_sintactico": analisis_estructura,
        "analisis_semantico": analisis_semantico,
        "conteo_tokens": conteo_tokens,
        "recomendaciones": []
    }
    
    # Generar recomendaciones
    if analisis_estructura["estadisticas"]["errores"] > 0:
        reporte["recomendaciones"].append("Revisar la sintaxis de las líneas con errores")
    
    if len(analisis_semantico["variables_no_declaradas"]) > 0:
        reporte["recomendaciones"].append("Declarar las variables antes de usarlas")
    
    if analisis_estructura["estadisticas"]["operaciones"] == 0:
        reporte["recomendaciones"].append("Agregar operaciones aritméticas para hacer el código más funcional")
    
    return reporte

# Función principal para compatibilidad con el módulo lex
def realizar_analisis_sintactico_extendido(codigo):
    """
    Función principal que mantiene compatibilidad con lex.py pero añade funcionalidad extra
    """
    return generar_reporte_completo(codigo)