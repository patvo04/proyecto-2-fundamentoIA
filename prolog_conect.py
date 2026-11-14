"""Puente entre Python y SWI-Prolog."""
from pathlib import Path
import re
import shutil
import subprocess
import unicodedata

BASE = Path(__file__).resolve().parent / 'conocimiento.pl'
FUERA = 'El objeto o material consultado no forma parte de la base de conocimiento.'

def normalizar(texto):
    texto = unicodedata.normalize('NFD', texto.lower())
    texto = ''.join(c for c in texto if unicodedata.category(c) != 'Mn')
    return re.sub(r'[^a-z0-9_]+', ' ', texto).strip()

def catalogo():
    contenido = BASE.read_text(encoding='utf-8')
    # Se extraen nombres solamente de hechos explícitos.
    return sorted(set(re.findall(r'^(?:receta|uso|es_material_basico)\(([a-z_]+)',
                                 contenido, re.MULTILINE)), key=len, reverse=True)

def identificar_objeto(pregunta):
    frase = ' ' + normalizar(pregunta).replace('_', ' ') + ' '
    frase = frase.replace(' de ', ' ').replace(' del ', ' ')
    for nombre in catalogo():
        if ' ' + nombre.replace('_', ' ') + ' ' in frase:
            # Una categoría desconocida como armadura_diamante no debe
            # confundirse con el material básico diamante.
            if '_' not in nombre and any(' ' + tipo + ' ' in frase for tipo in
                ('armadura','pico','pala','hacha','espada','azada')):
                continue
            return nombre
    return None

def clasificar(pregunta):
    p = normalizar(pregunta)
    if 'material basico' in p or 'material base?' in p or 'es basico' in p:
        return 'clasificacion'
    if any(s in p for s in ('para que sirve','que hace','que accion','utilidad')):
        return 'utilidad'
    if any(s in p for s in ('cadena','en total','prerequisito','componentes',
                            'materiales requiere','que necesito','necesito saber los materiales')):
        return 'inferencia'
    if any(s in p for s in ('como','crafteo','ingredientes','receta','hacer','hago')):
        return 'receta'
    return 'desconocida'

def consultar_prolog(consulta, objeto):
    if not shutil.which('swipl'):
        raise RuntimeError('No se encontró SWI-Prolog (swipl) en el PATH.')
    if not re.fullmatch(r'[a-z_]+', objeto):
        raise ValueError('Nombre de objeto invalido.')
    if consulta == 'receta':
        goal = f'receta({objeto},R),write_term(R,[quoted(true)])'
    elif consulta == 'utilidad':
        goal = f'uso({objeto},R),write_term(R,[quoted(true)])'
    elif consulta == 'inferencia':
        goal = (f'findall(X,requiere_material(X,{objeto}),L),'
                'sort(L,R),write_term(R,[quoted(true)])')
    elif consulta == 'clasificacion':
        goal = f'(es_material_basico({objeto})->write(true);write(false))'
    else:
        raise ValueError('Tipo de consulta desconocido.')
    p = subprocess.run(['swipl','-q','-s',str(BASE),'-g',goal,'-t','halt'],
                       capture_output=True,text=True,timeout=15,encoding='utf-8')
    if p.returncode != 0:
        if consulta in ('receta','utilidad') and not p.stdout.strip() and not p.stderr.strip():
            return None
        raise RuntimeError('Error de Prolog: ' + (p.stderr.strip() or 'consulta fallida'))
    return p.stdout.strip() or None

def responder_prolog(pregunta):
    tipo = clasificar(pregunta)
    objeto = identificar_objeto(pregunta)
    if tipo == 'desconocida':
        return {'respuesta': 'No entendi la intencion de tu pregunta.',
                'datos': None, 'tipo': tipo, 'objeto': objeto}
    if objeto is None:
        return {'respuesta': FUERA, 'datos': None, 'tipo': tipo, 'objeto': None}
    dato = consultar_prolog(tipo,objeto)
    if dato is None or (tipo == 'inferencia' and dato == '[]'):
        respuesta = FUERA
    elif tipo == 'receta':
        respuesta = f'Para fabricar {objeto} necesitas directamente: {dato}.'
    elif tipo == 'utilidad':
        respuesta = f'El objeto {objeto} sirve para: {dato}.'
    elif tipo == 'inferencia':
        respuesta = f'Los materiales directos e indirectos para {objeto} son: {dato}.'
    else:
        respuesta = (f'Sí, {objeto} es material basico.' if dato == 'true'
                     else f'No, {objeto} no es material básico.')
    return {'respuesta':respuesta,'datos':dato,'tipo':tipo,'objeto':objeto}