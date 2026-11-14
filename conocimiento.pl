% ===================================================
% Base de conocimiento del programa o del chatbot 
% ===================================================

% Materiales básicos
es_material_basico(madera).
es_material_basico(piedra).
es_material_basico(hierro).
es_material_basico(diamante).
es_material_basico(carbon).

% Herramientas y objetos
es_herramienta(pico_madera).
es_herramienta(pico_piedra).
es_herramienta(pico_hierro).
es_herramienta(pico_diamante).

% Palas
es_herramienta(pala_madera).
es_herramienta(pala_piedra).
es_herramienta(pala_hierro).
es_herramienta(pala_diamante).

% Hachas
es_herramienta(hacha_madera).
es_herramienta(hacha_piedra).
es_herramienta(hacha_hierro).
es_herramienta(hacha_diamante).

% Espadas
es_herramienta(espada_madera).
es_herramienta(espada_piedra).
es_herramienta(espada_hierro).
es_herramienta(espada_diamante).

% Azadas
es_herramienta(azada_madera).
es_herramienta(azada_piedra).
es_herramienta(azada_hierro).
es_herramienta(azada_diamante).

es_herramienta(antorcha).

% ===================================================
% Recetas de crafteo directas: receta(Resultado, listaIngredientes)
% ===================================================
receta(palo, [madera]).
receta(mesa_crafteo, [madera]).
receta(antorcha, [palo, carbon]).
receta(horno, [piedra]).

% Picos
receta(pico_madera, [palo, madera]).
receta(pico_piedra, [palo, piedra]).
receta(pico_hierro, [palo, hierro]).
receta(pico_diamante, [palo, diamante]).

% Palas
receta(pala_madera, [palo, madera]).
receta(pala_piedra, [palo, piedra]).
receta(pala_hierro, [palo, hierro]).
receta(pala_diamante, [palo, diamante]).

% Hachas
receta(hacha_madera, [palo, madera]).
receta(hacha_piedra, [palo, piedra]).
receta(hacha_hierro, [palo, hierro]).
receta(hacha_diamante, [palo, diamante]).

% Espadas
receta(espada_madera, [palo, madera]).
receta(espada_piedra, [palo, piedra]).
receta(espada_hierro, [palo, hierro]).
receta(espada_diamante, [palo, diamante]).

% Azadas
receta(azada_madera, [palo, madera]).
receta(azada_piedra, [palo, piedra]).
receta(azada_hierro, [palo, hierro]).
receta(azada_diamante, [palo, diamante]).

% ===================================================
% Utilidad de objetos: uso(Objeto, Accion)
% ===================================================
% Picos
uso(pico_madera, minar_piedra).
uso(pico_piedra, minar_hierro).
uso(pico_hierro, minar_diamante).
uso(pico_diamante, minar_obsidiana).

% Palas (excavar tierra, arena, grava o nieve con mayor rapidez)
uso(pala_madera, excavar_tierra).
uso(pala_piedra, excavar_tierra_rapido).
uso(pala_hierro, excavar_tierra_muy_rapido).
uso(pala_diamante, excavar_tierra_eficiente).

% Hachas (talar madera o descorchar troncos)
uso(hacha_madera, talar_madera).
uso(hacha_piedra, talar_madera_rapido).
uso(hacha_hierro, talar_madera_muy_rapido).
uso(hacha_diamante, talar_madera_eficiente).

% Espadas (atacar enemigos y cortar telarañas)
uso(espada_madera, combatir_monstruos).
uso(espada_piedra, combatir_monstruos_mayor_dano).
uso(espada_hierro, combatir_monstruos_alto_dano).
uso(espada_diamante, combatir_monstruos_maximo_dano).

% Azadas (arar la tierra para cultivo y romper bloques vegetales rápidamente)
uso(azada_madera, arar_tierra).
uso(azada_piedra, arar_tierra_mayor_durabilidad).
uso(azada_hierro, arar_tierra_alta_durabilidad).
uso(azada_diamante, arar_tierra_maxima_durabilidad).

% Otros objetos
uso(antorcha, iluminar).
uso(horno, fundir_minerales).

% ===================================================
% Reglas de inferencia lógica
% ===================================================

% El componente es ingrediente directo del objeto si aparece en la lista de receta del objeto
ingrediente_directo(Ingrediente, Objeto) :-
    receta(Objeto, Lista),
    member(Ingrediente, Lista).

% El componente es ingrediente indirecto recursivo del objeto
requiere_material(Ingrediente, Objeto) :-
    ingrediente_directo(Ingrediente, Objeto).
requiere_material(Ingrediente, Objeto) :-
    ingrediente_directo(Intermedio, Objeto),
    requiere_material(Ingrediente, Intermedio).