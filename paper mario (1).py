import sys
import os
import time

# Manejo de entrada de teclado sin Enter (Windows y Linux/macOS)
try:
    import msvcrt
    def leer_tecla():
        if msvcrt.kbhit():
            ch = msvcrt.getch()
            try:
                return ch.decode('utf-8').lower()
            except UnicodeDecodeError:
                return ""
        return None
except ImportError:
    import tty
    import termios
    import select
    def leer_tecla():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            rlist, _, _ = select.select([sys.stdin], [], [], 0.02)
            if rlist:
                ch = sys.stdin.read(1)
                return ch.lower()
            return None
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

# ==========================================
# NIVEL 1: BATALLA CONTRA EL JEFE
# ==========================================

def jugar_nivel_1():
    ANCHO_MAPA = 35
    jugador_x = 3
    jugador_saltando = False
    duracion_salto = 0
    
    jefe_x = 30
    jefe_vida = 3
    
    proyectiles_jugador = []  
    fuegos_jefe = []          
    
    cooldown_disparo_jefe = 0
    frame_animacion = 0
    animacion_impacto_jefe = 0
    
    limpiar_pantalla()
    print("==================================================")
    print("   🏰 === NIVEL 1: LA PRINCESA CORROMPIDA === 👑")
    print("==================================================")
    print("  🎮 Controles:")
    print("  [A] ⬅️ Izquierda | [D] ➡️ Derecha | [Espacio] ⬆️ Saltar")
    print("  [L] 💥 Disparar  | [Q] 🚪 Salir")
    input("\n▶️ Presione Enter para iniciar la batalla...")

    limpiar_pantalla()
    while True:
        frame_animacion += 1
        tecla = leer_tecla()
        
        if tecla == 'a':
            if jugador_x > 1:
                jugador_x -= 1
        elif tecla == 'd':
            if jugador_x < ANCHO_MAPA - 3:
                jugador_x += 1
        elif tecla == ' ' and not jugador_saltando:
            jugador_saltando = True
            duracion_salto = 4  
        elif tecla == 'l':
            if len(proyectiles_jugador) < 2:
                proyectiles_jugador.append(jugador_x + 2)
        elif tecla == 'q':
            print("\n🏃 Has abandonado la batalla.")
            time.sleep(1)
            break

        # Lógica de salto
        if jugador_saltando:
            duracion_salto -= 1
            if duracion_salto <= 0:
                jugador_saltando = False

        # Lógica del jefe (Ataque)
        cooldown_disparo_jefe += 1
        if cooldown_disparo_jefe >= 7:  
            fuegos_jefe.append(jefe_x - 1)
            cooldown_disparo_jefe = 0

        # Movimiento de proyectiles
        proyectiles_jugador = [x + 2 for x in proyectiles_jugador if x < ANCHO_MAPA]
        fuegos_jefe = [x - 1 for x in fuegos_jefe if x > 0]

        # Colisiones e impactos en jefe
        nuevos_proyectiles = []
        for x in proyectiles_jugador:
            if x >= jefe_x:
                jefe_vida -= 1
                animacion_impacto_jefe = 3
            else:
                nuevos_proyectiles.append(x)
        proyectiles_jugador = nuevos_proyectiles

        # Colisión con el jugador
        for x in fuegos_jefe:
            if (x == jugador_x or x == jugador_x + 1) and not jugador_saltando:
                limpiar_pantalla()
                print("\n" + "=" * 42)
                print("   💀 ¡HAS SIDO ALCANZADO POR EL FUEGO! 💀")
                print("               --- GAME OVER 🪦 ---")
                print("=" * 42)
                input("\n🔄 Presione Enter para volver al Menú Principal...")
                return

        # Condición de Victoria
        if jefe_vida <= 0:
            limpiar_pantalla()
            print("\n" + "=" * 46)
            print("   🏆 ¡HAS DERROTADO A LA PRINCESA CORROMPIDA! 🏆")
            print("    🎉 ¡FELICIDADES! ¡COMPLETATE EL NIVEL 1! ⭐")
            print("=" * 46)
            input("\n🔄 Presione Enter para volver al Menú Principal...")
            return

        # RENDERIZADO SIN PARPADEO
        sys.stdout.write("\033[H")
        
        if animacion_impacto_jefe > 0:
            estado_jefe = "⚡ ¡DAÑO! ⚡"
            animacion_impacto_jefe -= 1
        else:
            estado_jefe = "👑 CORROMPIDA"

        corazones = "❤️ " * jefe_vida + "🖤 " * (3 - jefe_vida)
        print(f" 👿 PRINCESA [{estado_jefe}]: {corazones}".ljust(50))
        print("┌" + "─" * (ANCHO_MAPA * 2) + "┐")

        linea_aire = ["  "] * ANCHO_MAPA
        if jugador_saltando:
            linea_aire[jugador_x] = "🪽 " if (frame_animacion % 2 == 0) else "🧍"

        print("│" + "".join(linea_aire) + "│")

        linea_suelo = ["  "] * ANCHO_MAPA

        if not jugador_saltando:
            linea_suelo[jugador_x] = "🏃" if (frame_animacion % 2 == 0) else "🧍"

        if animacion_impacto_jefe > 0:
            linea_suelo[jefe_x] = "💥"
        else:
            linea_suelo[jefe_x] = "🪞" if (frame_animacion % 2 == 0) else "👸"

        for px in proyectiles_jugador:
            if px < jefe_x and px < ANCHO_MAPA:
                linea_suelo[px] = "⚡"

        for fx in fuegos_jefe:
            if fx > 0 and fx < ANCHO_MAPA and (fx != jugador_x or jugador_saltando):
                linea_suelo[fx] = "🔥"

        print("│" + "".join(linea_suelo) + "│")
        print("└" + "─" * (ANCHO_MAPA * 2) + "┘")
        print(" 🎮 [A] ⬅️ | [D] ➡️ | [Espacio] ⬆️ | [L] 💥 Disparar | [Q] 🚪 Salir")

        time.sleep(0.06)


# ==========================================
# NIVEL 2: PLATAFORMAS, DISPAROS Y META
# ==========================================

def jugar_nivel_2():
    ANCHO_MAPA = 40
    jugador_x = 2
    jugador_saltando = False
    duracion_salto = 0
    
    # Proyectiles del jugador
    proyectiles_jugador = []

    # Obstáculos (posiciones fijas)
    obstaculos = [10, 22]
    
    # Enemigos: lista de diccionarios
    enemigos = [
        {"x": 15, "dir": 1, "limite_izq": 12, "limite_der": 18},
        {"x": 28, "dir": -1, "limite_izq": 25, "limite_der": 32}
    ]
    
    bandera_x = 36
    frame_animacion = 0

    limpiar_pantalla()
    print("==================================================")
    print("   🌲 === NIVEL 2: EL CAMINO A LA META === 🏁")
    print("==================================================")
    print("  🎮 Controles:")
    print("  [A] ⬅️ Izquierda | [D] ➡️ Derecha | [Espacio] ⬆️ Saltar")
    print("  [L] 💥 Disparar  | [Q] 🚪 Salir")
    print("\n  💡 Esquiva obstáculos (🧱), dispara o salta sobre")
    print("     enemigos (👾) y llega a la bandera final (🏁).")
    input("\n▶️ Presione Enter para iniciar...")

    limpiar_pantalla()
    while True:
        frame_animacion += 1
        tecla = leer_tecla()
        
        pos_siguiente = jugador_x

        if tecla == 'a':
            pos_siguiente = max(1, jugador_x - 1)
        elif tecla == 'd':
            pos_siguiente = min(ANCHO_MAPA - 2, jugador_x + 1)
        elif tecla == ' ' and not jugador_saltando:
            jugador_saltando = True
            duracion_salto = 4
        elif tecla == 'l':
            if len(proyectiles_jugador) < 2:
                proyectiles_jugador.append(jugador_x + 1)
        elif tecla == 'q':
            print("\n🏃 Has abandonado el nivel.")
            time.sleep(1)
            break

        # Colisión de movimiento con obstáculos
        if pos_siguiente not in obstaculos or jugador_saltando:
            jugador_x = pos_siguiente

        # Lógica de salto
        if jugador_saltando:
            duracion_salto -= 1
            if duracion_salto <= 0:
                jugador_saltando = False

        # Avanzar proyectiles
        proyectiles_jugador = [x + 2 for x in proyectiles_jugador if x < ANCHO_MAPA]

        # Movimiento de enemigos (cada 2 frames)
        if frame_animacion % 2 == 0:
            for enemigo in enemigos:
                enemigo["x"] += enemigo["dir"]
                if enemigo["x"] >= enemigo["limite_der"] or enemigo["x"] <= enemigo["limite_izq"]:
                    enemigo["dir"] *= -1

        # Colisión de proyectiles con obstáculos
        proyectiles_activos = []
        for px in proyectiles_jugador:
            if px in obstaculos:
                continue # El disparo choca contra la pared y desaparece
            proyectiles_activos.append(px)
        proyectiles_jugador = proyectiles_activos

        # Colisión de proyectiles con enemigos
        enemigos_vivos = []
        for enemigo in enemigos:
            eliminado = False
            for px in proyectiles_jugador:
                if px >= enemigo["x"] and px <= enemigo["x"] + 1:
                    eliminado = True
                    proyectiles_jugador.remove(px)
                    break
            if not eliminado:
                enemigos_vivos.append(enemigo)
        enemigos = enemigos_vivos

        # Colisiones del jugador con enemigos
        enemigos_tras_salto = []
        for enemigo in enemigos:
            if jugador_x == enemigo["x"]:
                if jugador_saltando:
                    continue # Lo aplasta si salta
                else:
                    limpiar_pantalla()
                    print("\n" + "=" * 42)
                    print("   💀 ¡UN ENEMIGO TE HA DERROTADO! 💀")
                    print("               --- GAME OVER 🪦 ---")
                    print("=" * 42)
                    input("\n🔄 Presione Enter para volver al Menú Principal...")
                    return
            enemigos_tras_salto.append(enemigo)
        enemigos = enemigos_tras_salto

        # Condición de Victoria
        if jugador_x >= bandera_x:
            limpiar_pantalla()
            print("\n" + "=" * 46)
            print("   🏁 ¡HAS LLEGADO A LA BANDERA DE META! 🏁")
            print("     🎉 ¡NIVEL 2 COMPLETADO CON ÉXITO! ⭐")
            print("=" * 46)
            input("\n🔄 Presione Enter para volver al Menú Principal...")
            return

        # RENDERIZADO SIN PARPADEO
        sys.stdout.write("\033[H")

        print(" 🌲 NIVEL 2: CAMINO A LA META                        ")
        print("┌" + "─" * (ANCHO_MAPA * 2) + "┐")

        # 1. LÍNEA DE AIRE
        linea_aire = ["  "] * ANCHO_MAPA
        if jugador_saltando:
            linea_aire[jugador_x] = "🪽 " if (frame_animacion % 2 == 0) else "🧍"

        print("│" + "".join(linea_aire) + "│")

        # 2. LÍNEA DEL SUELO
        linea_suelo = ["  "] * ANCHO_MAPA

        # Dibujar bandera
        linea_suelo[bandera_x] = "🏁"

        # Dibujar obstáculos
        for obs in obstaculos:
            linea_suelo[obs] = "🧱"

        # Dibujar enemigos
        for enemigo in enemigos:
            linea_suelo[enemigo["x"]] = "👾"

        # Dibujar disparos del jugador
        for px in proyectiles_jugador:
            if px < ANCHO_MAPA:
                linea_suelo[px] = "⚡"

        # Dibujar jugador si está en el suelo
        if not jugador_saltando:
            linea_suelo[jugador_x] = "🏃" if (frame_animacion % 2 == 0) else "🧍"

        print("│" + "".join(linea_suelo) + "│")
        print("└" + "─" * (ANCHO_MAPA * 2) + "┘")
        print(" 🎮 Controles: [A] ⬅️ | [D] ➡️ | [Espacio] ⬆️ | [L] 💥 Disparar | [Q] Salir")

        time.sleep(0.06)


# ==========================================
# NIVEL 3: EL DRAGÓN DE FUEGO (JEFE INTERMEDIO)
# ==========================================

def jugar_nivel_3():
    limpiar_pantalla()
    print("==================================================")
    print("   🐉 === NIVEL 3: LA GUARIDA DEL DRAGÓN === 🐉")
    print("==================================================")
    print("\n🔮 ¡Elige el PODER que llevarás a la batalla! 🔮")
    print("1. ❄️  Rayo de Hielo   (Congela temporalmente los ataques)")
    print("2. 🛡️  Escudo Mágico   (Inmunidad temporal en momentos críticos)")
    print("3. ⚡  Súper Rayo     (Realiza doble daño por cada disparo)")
    
    poder_elegido = ""
    while poder_elegido not in ["1", "2", "3"]:
        poder_elegido = input("👉 Elige tu poder (1-3): ")

    nombres_poderes = {"1": "❄️ Rayo de Hielo", "2": "🛡️ Escudo Mágico", "3": "⚡ Súper Rayo"}
    print(f"\n✅ ¡Has seleccionado: {nombres_poderes[poder_elegido]}!")
    print("\n🎮 Mecánicas de la batalla:")
    print(" • El Dragón realiza ataques por ABAJO (🔥) y por ARRIBA (🪨).")
    print(" • Salta (Espacio) para esquivar por abajo.")
    print(" • Permanece abajo/agachado (No saltes) para esquivar por arriba.")
    print(" • Tienes 3 vidas (❤️ ❤️ ❤️).")
    input("\n▶️ Presione Enter para iniciar la batalla...")

    ANCHO_MAPA = 35
    jugador_x = 3
    jugador_saltando = False
    duracion_salto = 0
    jugador_vidas = 3

    dragon_x = 30
    dragon_vida = 6
    
    proyectiles_jugador = []
    ataques_altos = []   # Proyectiles por arriba
    ataques_bajos = []   # Proyectiles por abajo
    
    cooldown_dragon = 0
    frame_animacion = 0
    animacion_impacto = 0
    tipo_ataque_siguiente = 0  # Alterna tipos de ataque

    limpiar_pantalla()
    while True:
        frame_animacion += 1
        tecla = leer_tecla()

        if tecla == 'a':
            if jugador_x > 1:
                jugador_x -= 1
        elif tecla == 'd':
            if jugador_x < ANCHO_MAPA - 4:
                jugador_x += 1
        elif tecla == ' ' and not jugador_saltando:
            jugador_saltando = True
            duracion_salto = 4
        elif tecla == 'l':
            if len(proyectiles_jugador) < 2:
                proyectiles_jugador.append({"x": jugador_x + 2, "y": "alto" if jugador_saltando else "bajo"})
        elif tecla == 'q':
            print("\n🏃 Has abandonado la batalla.")
            time.sleep(1)
            break

        # Lógica de salto
        if jugador_saltando:
            duracion_salto -= 1
            if duracion_salto <= 0:
                jugador_saltando = False

        # Generación de ataques del Dragón (lentitud intermedia: cada 10 frames)
        cooldown_dragon += 1
        if cooldown_dragon >= 10:
            if tipo_ataque_siguiente % 2 == 0:
                ataques_bajos.append(dragon_x - 1)  # Ataque por abajo
            else:
                ataques_altos.append(dragon_x - 1)  # Ataque por arriba
            tipo_ataque_siguiente += 1
            cooldown_dragon = 0

        # Movimiento de ataques del dragón (ritmo pausado)
        if frame_animacion % 2 == 0:
            ataques_bajos = [x - 1 for x in ataques_bajos if x > 0]
            ataques_altos = [x - 1 for x in ataques_altos if x > 0]

        # Movimiento de proyectiles del jugador
        proyectiles_activos = []
        for p in proyectiles_jugador:
            p["x"] += 2
            if p["x"] >= dragon_x:
                # Daño al dragón según el poder elegido
                daño = 2 if poder_elegido == "3" else 1
                dragon_vida -= daño
                animacion_impacto = 3
            else:
                proyectiles_activos.append(p)
        proyectiles_jugador = proyectiles_activos

        # Colisión de ataques del Dragón con el Jugador
        # Ataques por abajo: dañan si el jugador NO está saltando
        nuevos_bajos = []
        for x in ataques_bajos:
            if (x == jugador_x or x == jugador_x + 1) and not jugador_saltando:
                if poder_elegido != "2": # Escudo evita daño de un golpe
                    jugador_vidas -= 1
            else:
                nuevos_bajos.append(x)
        ataques_bajos = nuevos_bajos

        # Ataques por arriba: dañan SI EL JUGADOR ESTÁ SALTANDO
        nuevos_altos = []
        for x in ataques_altos:
            if (x == jugador_x or x == jugador_x + 1) and jugador_saltando:
                if poder_elegido != "2":
                    jugador_vidas -= 1
            else:
                nuevos_altos.append(x)
        ataques_altos = nuevos_altos

        # Derrota del jugador
        if jugador_vidas <= 0:
            limpiar_pantalla()
            print("\n" + "=" * 42)
            print("   💀 ¡EL DRAGÓN TE HA DERROTADO! 💀")
            print("               --- GAME OVER 🪦 ---")
            print("=" * 42)
            input("\n🔄 Presione Enter para volver al Menú Principal...")
            return

        # Victoria contra el Dragón
        if dragon_vida <= 0:
            limpiar_pantalla()
            print("\n" + "=" * 48)
            print("   🏆 ¡HAS DERROTADO AL DRAGÓN INFERNAL! 🏆")
            print("    🎉 ¡COMPLETATE EL NIVEL 3 CON ÉXITO! ⭐")
            print("=" * 48)
            input("\n🔄 Presione Enter para volver al Menú Principal...")
            return

        # RENDERIZADO
        sys.stdout.write("\033[H")

        vidas_txt = "❤️ " * jugador_vidas + "🖤 " * (3 - jugador_vidas)
        corazones_dragon = "🟢 " * dragon_vida + "🖤 " * (6 - dragon_vida)

        print(f" 🧍 JUGADOR: {vidas_txt} | 🐉 DRAGÓN: {corazones_dragon}".ljust(50))
        print("┌" + "─" * (ANCHO_MAPA * 2) + "┐")

        # LÍNEA DE AIRE (Arriba)
        linea_aire = ["  "] * ANCHO_MAPA
        if jugador_saltando:
            linea_aire[jugador_x] = "🪽 " if (frame_animacion % 2 == 0) else "🧍"

        for ax in ataques_altos:
            if ax < ANCHO_MAPA:
                linea_aire[ax] = "🪨 "

        for p in proyectiles_jugador:
            if p["y"] == "alto" and p["x"] < dragon_x and p["x"] < ANCHO_MAPA:
                linea_aire[p["x"]] = "⚡" if poder_elegido != "1" else "❄️ "

        print("│" + "".join(linea_aire) + "│")

        # LÍNEA DEL SUELO (Abajo)
        linea_suelo = ["  "] * ANCHO_MAPA

        if not jugador_saltando:
            linea_suelo[jugador_x] = "🏃" if (frame_animacion % 2 == 0) else "🧍"

        if animacion_impacto > 0:
            linea_suelo[dragon_x] = "💥"
            animacion_impacto -= 1
        else:
            linea_suelo[dragon_x] = "🐉"

        for bx in ataques_bajos:
            if bx < ANCHO_MAPA:
                linea_suelo[bx] = "🔥"

        for p in proyectiles_jugador:
            if p["y"] == "bajo" and p["x"] < dragon_x and p["x"] < ANCHO_MAPA:
                linea_suelo[p["x"]] = "⚡" if poder_elegido != "1" else "❄️ "

        print("│" + "".join(linea_suelo) + "│")
        print("└" + "─" * (ANCHO_MAPA * 2) + "┘")
        print(" 🎮 Controles: [A] ⬅️ | [D] ➡️ | [Espacio] ⬆️ | [L] 💥 Disparar | [Q] Salir")

        time.sleep(0.06)


# ==========================================
# MENÚ Y OPCIONES SECUNDARIAS
# ==========================================

def habilidades_especiales():
    print("\n🔮 [Módulo Habilidades Especiales]: Función pendiente de desarrollo.")
    input("\n⏎ Presione Enter para volver al Menú Principal...")

def galeria_atuendos():
    print("\n--- 👗 GALERÍA DE ATUENDOS 🎭 ---")
    print("👤 Personajes disponibles: 🔴 Mario, 🟢 Luigi, 💖 Peach")
    print("🛠️ [Módulo Atuendos]: Función pendiente de desarrollo.")
    input("\n⏎ Presione Enter para volver al Inventario...")

def inventario():
    while True:
        print("\n--- 🎒 INVENTARIO ---")
        print("1. 📦 Ver objetos")
        print("2. 👗 Vestuario (Galería de atuendos)")
        print("3. ⬅️ Volver al Menú Principal")
        opcion = input("👉 Seleccione una opción: ")

        if opcion == "1":
            print("\n📦 [Ver Objetos]: Función pendiente de desarrollo.")
            input("⏎ Presione Enter para continuar...")
        elif opcion == "2":
            galeria_atuendos()
        elif opcion == "3":
            break
        else:
            print("⚠️ Opción inválida. Intente de nuevo.")

def efectos_sonido():
    print("\n🔊 [Efectos de Sonido]: Apagar/Encender (Pendiente de desarrollo).")
    input("⏎ Presione Enter para continuar...")

def musica():
    print("\n🎵 [Música]: Apagar/Encender (Pendiente de desarrollo).")
    input("⏎ Presione Enter para continuar...")

def sonido():
    while True:
        print("\n--- 🔊 CONFIGURACIÓN DE SONIDO ---")
        print("1. 🔔 Efectos")
        print("2. 🎶 Música")
        print("3. ⬅️ Volver a Opciones")
        opcion = input("👉 Seleccione una opción: ")

        if opcion == "1":
            efectos_sonido()
        elif opcion == "2":
            musica()
        elif opcion == "3":
            break
        else:
            print("⚠️ Opción inválida. Intente de nuevo.")

def pedir_soporte():
    print("\n--- 📩 PEDIR SOPORTE ---")
    print("📧 Contacto: soporte@juego.com")
    input("\n⏎ Presione Enter para volver a Opciones...")

def notificaciones():
    print("\n--- 🔔 NOTIFICACIONES ---")
    print("🛠️ [Notificaciones]: Función pendiente de desarrollo.")
    input("\n⏎ Presione Enter para volver a Opciones...")

def creditos():
    print("\n--- 📜 CRÉDITOS ---")
    print("⭐ Paper Mario: The Origami King - Fan Remake ⭐")
    input("\n⏎ Presione Enter para volver a Opciones...")

def informacion_legal():
    print("\n--- ⚖️ INFORMACIÓN LEGAL ---")
    print("©️ Todos los derechos reservados.")
    input("\n⏎ Presione Enter para volver a Opciones...")

def opciones():
    while True:
        print("\n--- ⚙️ OPCIONES ---")
        print("1. 🔊 Sonido")
        print("2. 📩 Pedir soporte")
        print("3. 🔔 Notificaciones")
        print("4. 📜 Créditos")
        print("5. ⚖️ Información legal")
        print("6. ⬅️ Volver al Menú Principal")
        opcion = input("👉 Seleccione una opción: ")

        if opcion == "1":
            sonido()
        elif opcion == "2":
            pedir_soporte()
        elif opcion == "3":
            notificaciones()
        elif opcion == "4":
            creditos()
        elif opcion == "5":
            informacion_legal()
        elif opcion == "6":
            break
        else:
            print("⚠️ Opción inválida. Intente de nuevo.")

def salir():
    print("\n❓ ¿Está seguro de que desea salir?")
    print("1. ✅ Sí")
    print("2. ❌ No")
    confirmacion = input("👉 Seleccione una opción: ")
    if confirmacion == "1":
        print("👋 ¡Gracias por jugar! Saliendo del juego...")
        sys.exit()
    else:
        print("🔄 Regresando al Menú Principal...")

def menu_principal():
    limpiar_pantalla()
    print("========================================")
    print(" 🌟 Paper Mario: The Origami King 🌟 ")
    print("========================================")
    input("▶️ Presione ENTER para iniciar el juego...")

    while True:
        limpiar_pantalla()
        print("================ 🎮 MENÚ ================")
        print("1. ⚔️ Nivel 1: La Princesa Corrompida (Jefe)")
        print("2. 🌲 Nivel 2: Camino a la Meta (Plataformas)")
        print("3. 🐉 Nivel 3: La Guarida del Dragón (Jefe Intermedio)")
        print("4. ✨ Sectores Habilidades Especiales")
        print("5. 🎒 Inventario")
        print("6. ⚙️ Opciones")
        print("7. 🚪 Salir")
        print("=========================================")
        
        opcion = input("👉 Seleccione una opción (1-7): ")

        if opcion == "1":
            jugar_nivel_1()
        elif opcion == "2":
            jugar_nivel_2()
        elif opcion == "3":
            jugar_nivel_3()
        elif opcion == "4":
            habilidades_especiales()
        elif opcion == "5":
            inventario()
        elif opcion == "6":
            opciones()
        elif opcion == "7":
            salir()
        else:
            print("⚠️ Opción inválida. Ingrese un número entre 1 y 7.")
            time.sleep(1)

if __name__ == "__main__":
    menu_principal()