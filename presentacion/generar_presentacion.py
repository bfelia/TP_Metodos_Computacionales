import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.image as mpimg
from matplotlib.patches import FancyBboxPatch, Rectangle

os.environ["MPLCONFIGDIR"] = "/tmp/mpl"

# Configuración de página 16:9 en alta resolución
W, H = 13.333, 7.5
DPI = 200

# Paleta editorial limpia y profesional
NAVY_HEADER = "#0f172a"
BG_PAGE = "#f8fafc"
TEXT_DARK = "#1e293b"
TEXT_MUTED = "#64748b"
PRIMARY_BLUE = "#1d4ed8"
ACCENT_GREEN = "#059669"
ACCENT_RED = "#dc2626"
CARD_BG = "#ffffff"
CARD_BORDER = "#e2e8f0"
FOOTER_BG = "#eff6ff"
FOOTER_BORDER = "#bfdbfe"

def crear_base_slide(fig, tag_seccion, titulo_slide, numero_slide):
    fig.patch.set_facecolor(BG_PAGE)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis("off")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    # Barra superior
    ax.fill_between([0, 1], 0.88, 1.0, color=NAVY_HEADER)
    ax.text(0.045, 0.945, tag_seccion.upper(), color="#94a3b8", fontsize=9, fontweight="bold")
    ax.text(0.045, 0.905, titulo_slide, color="#ffffff", fontsize=15, fontweight="bold")
    ax.text(0.955, 0.925, f"{numero_slide:02d} / 13", color="#cbd5e1", fontsize=11, fontweight="bold", ha="right")

    return ax

def agregar_caja_oral(ax, texto_clave):
    # Caja inferior con la clave para defender en el oral
    rect = FancyBboxPatch((0.045, 0.035), 0.91, 0.075, boxstyle="round,pad=0.015",
                          fc=FOOTER_BG, ec=FOOTER_BORDER, lw=1.2)
    ax.add_patch(rect)
    ax.text(0.065, 0.082, "CLAVE PARA EL COLOQUIO ORAL (PUNCHLINE):", color=PRIMARY_BLUE, fontsize=8.5, fontweight="bold")
    ax.text(0.065, 0.052, texto_clave, color="#1e3a8a", fontsize=9)

os.makedirs("presentacion_slides", exist_ok=True)

def agregar_tarjeta(ax, x, y, w, h, bg=CARD_BG, ec=CARD_BORDER):
    card = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.015", fc=bg, ec=ec, lw=1.0)
    ax.add_patch(card)

slide_idx = [0]
def guardar_slide(fig, pdf):
    slide_idx[0] += 1
    pdf.savefig(fig, dpi=DPI)
    fig.savefig(f"presentacion_slides/slide_{slide_idx[0]:02d}.png", dpi=150)
    plt.close()

with PdfPages("presentacion.pdf") as pdf:

    # -------------------------------------------------------------
    # SLIDE 1: PORTADA
    # -------------------------------------------------------------
    fig = plt.figure(figsize=(W, H), facecolor=NAVY_HEADER)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis("off")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    # Fondo oscuro con degradado sutil en tarjetas
    ax.text(0.08, 0.82, "UNIVERSIDAD TORCUATO DI TELLA", color="#38bdf8", fontsize=12, fontweight="bold")
    ax.text(0.08, 0.77, "Departamento de Matemática y Ciencias • Métodos Computacionales (S2 2026)", color="#94a3b8", fontsize=11)
    
    ax.text(0.08, 0.63, "Reconstrucción y Regularización\nen Imágenes Tomográficas", color="#ffffff", fontsize=26, fontweight="bold", linespacing=1.2)
    ax.text(0.08, 0.52, "De la física de rayos X al álgebra lineal numérica: problemas inversos,\noptimización cuadrática y balance de regularización", color="#cbd5e1", fontsize=12.5, linespacing=1.4)

    # 3 Tarjetas de Pilares
    pilares = [
        ("1. Álgebra Lineal & Unicidad", "Discretización b = Ax\nRango columna y Teorema de Nulidad\nEspacio nulo y 'fantasmas invisibles' SVD", "#1e293b", "#38bdf8"),
        ("2. Ruido & Métodos Iterativos", "Incompatibilidad y Proyección Ortogonal\nGradiente Descendiente vs. Newton\nCota crítica de estabilidad alpha < 2/mu_max", "#1e293b", "#34d399"),
        ("3. Regularización & Escala", "Penalización de suavidad Tikhonov (D)\nCompromiso sesgo-varianza (lambda)\nPrincipio de Morozov y Matrices Dispersas", "#1e293b", "#fbbf24")
    ]
    for idx, (tit, desc, bg, acc) in enumerate(pilares):
        x_pos = 0.08 + idx * 0.295
        card = FancyBboxPatch((x_pos, 0.16), 0.265, 0.26, boxstyle="round,pad=0.015", fc=bg, ec="#334155", lw=1.2)
        ax.add_patch(card)
        ax.plot([x_pos+0.015, x_pos+0.06], [0.38, 0.38], color=acc, lw=3)
        ax.text(x_pos+0.015, 0.34, tit, color="#ffffff", fontsize=10.5, fontweight="bold")
        ax.text(x_pos+0.015, 0.23, desc, color="#94a3b8", fontsize=8.5, linespacing=1.4)

    ax.text(0.08, 0.08, "Presentación de Defensa Oral • Resumen de Soluciones y Marco Teórico", color="#64748b", fontsize=9.5)
    guardar_slide(fig, pdf)

    # -------------------------------------------------------------
    # SLIDE 2: DEL FENÓMENO FÍSICO A LA MATRIZ b = Ax
    # -------------------------------------------------------------
    fig = plt.figure(figsize=(W, H))
    ax = crear_base_slide(fig, "Introducción al Modelo Físico • Ejercicios 1 y 2", "1. De la Física de Rayos X al Sistema Lineal $b = Ax$", 2)
    
    # Tarjeta Izquierda (Teoría y conceptos)
    agregar_tarjeta(ax, 0.045, 0.13, 0.44, 0.72)
    ax.text(0.07, 0.80, "Ley de Beer-Lambert y Discretización", color=TEXT_DARK, fontsize=12, fontweight="bold")
    
    bullets_s2 = (
        r"$\bullet$ $\mathbf{Modelo\ Físico:}$ La intensidad detectada decae exponencialmente según" "\n"
        r"  la atenuación acumulada: $I = I_0 \exp\left(-\int_\ell \mu(r) dr\right)$." "\n\n"
        r"$\bullet$ $\mathbf{Linealización:}$ Al aplicar logaritmo, cada detector entrega" "\n"
        r"  una integral lineal de la atenuación del objeto: $-\ln(I/I_0) = \int_\ell \mu(r) dr$." "\n\n"
        r"$\bullet$ $\mathbf{Discretización\ de\ la\ Imagen:}$ La sección se divide en $n \times n$ píxeles." "\n"
        r"  La matriz $X \in \mathbb{R}^{n \times n}$ se vectoriza por filas en $x \in \mathbb{R}^{n^2}$:" "\n"
        r"  $\quad \mathrm{Posición\ vector:\ } k = i \cdot n + j \quad (k = 8i + j\ \mathrm{para\ } 8\times 8)$." "\n\n"
        r"$\bullet$ $\mathbf{Sistema\ Matricial:}$ Cada rayo $r$ suma los píxeles atravesados:" "\n"
        r"  $\quad b_r = \sum_j a_{rj} x_j \Rightarrow \mathbf{b = Ax} \quad (A \in \mathbb{R}^{m \times 64}, x \in \mathbb{R}^{64}, b \in \mathbb{R}^m)$." "\n\n"
        r"$\bullet$ $\mathbf{Problema\ Inverso:}$ Conocemos $A$ (geometría de rayos) y $b$ (sensores)." "\n"
        r"  El objetivo es deducir la variable oculta $x$ (el interior del paciente)."
    )
    ax.text(0.07, 0.44, bullets_s2, color="#334155", fontsize=9.2, linespacing=1.28)

    # Tarjeta Derecha (Gráfico fantoma)
    agregar_tarjeta(ax, 0.51, 0.13, 0.445, 0.72)
    ax.text(0.535, 0.80, "El Fantoma de Prueba (8x8 píxeles)", color=TEXT_DARK, fontsize=12, fontweight="bold")
    img_s2 = mpimg.imread("figuras/ej1_fantoma.png")
    ax_img = fig.add_axes([0.55, 0.24, 0.365, 0.50])
    ax_img.imshow(img_s2)
    ax_img.axis("off")

    ax.text(0.535, 0.18, 
            r"Valores de $\mu$: 0.8 (alta densidad, hueso/corteza), 0.3 a 0.5 (tejido blando), 0.0 (fondo libre).", 
            color=TEXT_MUTED, fontsize=8.5)

    agregar_caja_oral(ax, "La tomografía es un problema inverso: no podemos mirar x directamente. Disparamos rayos desde afuera y a partir de las sumas b intentamos despejar la foto interior.")
    guardar_slide(fig, pdf)

    # -------------------------------------------------------------
    # SLIDE 3: GEOMETRÍA DE ADQUISICIÓN Y EL SINOGRAMA
    # -------------------------------------------------------------
    fig = plt.figure(figsize=(W, H))
    ax = crear_base_slide(fig, "Adquisición Tomográfica • Ejercicio 3", "2. Geometría de Rayos, Proyecciones y Sinograma", 3)

    agregar_tarjeta(ax, 0.045, 0.13, 0.44, 0.72)
    ax.text(0.07, 0.80, "Parametrización y Familias de Rayos", color=TEXT_DARK, fontsize=12, fontweight="bold")
    
    bullets_s3 = (
        r"$\bullet$ $\mathbf{Parametrización\ Continua:}$ Recta normal al haz perpendicular a $n_\theta$:" "\n"
        r"  $\quad u \cos\theta + v \sin\theta = s$  $(\theta \in [0, \pi),\ s = \mathrm{posición\ detector})$." "\n\n"
        r"$\bullet$ $\mathbf{Modelo\ Discreto\ Binario:}$ El rayo selecciona los centros $(i, j)$ tales que:" "\n"
        r"  $\quad \alpha i + \beta j = s$." "\n"
        r"  Cada fila $a_r^T$ de $A$ tiene 1s en píxeles cruzados y 0s en el resto." "\n\n"
        r"$\bullet$ $\mathbf{El\ Sinograma\ } S \in \mathbb{R}^{K \times q}\mathbf{:}$" "\n"
        r"  Reúne todas las mediciones ordenadas: cada fila es un ángulo $\theta_k$ y cada" "\n"
        r"  columna es un detector $s_j$. Al apilarlo por filas se forma el vector $b \in \mathbb{R}^{Kq}$." "\n\n"
        r"$\bullet$ $\mathbf{Ambigüedad\ de\ un\ solo\ rayo:}$ Dos rayos distintos pueden medir la" "\n"
        r"  misma atenuación total sumando píxeles diferentes. Para resolver la imagen" "\n"
        r"  se requiere combinar múltiples orientaciones angulares."
    )
    ax.text(0.07, 0.45, bullets_s3, color="#334155", fontsize=9.2, linespacing=1.28)

    agregar_tarjeta(ax, 0.51, 0.13, 0.445, 0.72)
    ax.text(0.535, 0.80, "Verificación: Señales 1D de Filas y Columnas (A2)", color=TEXT_DARK, fontsize=12, fontweight="bold")
    img_s3 = mpimg.imread("figuras/ej3_sinograma.png")
    ax_img = fig.add_axes([0.525, 0.32, 0.415, 0.42])
    ax_img.imshow(img_s3)
    ax_img.axis("off")

    ax.text(0.535, 0.22, 
            r"Verificación numérica: Las primeras 8 filas de $A_2$ suman exactamente las filas de $X$;" "\n"
            r"las 8 siguientes suman las columnas de $X$. Coinciden con $X.\mathrm{sum(axis=1)}$ y $X.\mathrm{sum(axis=0)}$.", 
            color=TEXT_MUTED, fontsize=8.5, linespacing=1.3)

    agregar_caja_oral(ax, "Cada ángulo de rayos genera una 'sombra' 1D del objeto. El sinograma es la colección de todas esas sombras. La matriz A contiene la máscara estirada de cada rayo.")
    guardar_slide(fig, pdf)

    # -------------------------------------------------------------
    # SLIDE 4: UNICIDAD DE RECONSTRUCCIÓN Y ESPACIO NULO
    # -------------------------------------------------------------
    fig = plt.figure(figsize=(W, H))
    ax = crear_base_slide(fig, "Álgebra Lineal & Rango • Ejercicio 4a y 4b", "3. ¿Cuándo la Reconstrucción es Única? Teorema Rango-Nulidad", 4)

    agregar_tarjeta(ax, 0.045, 0.13, 0.44, 0.72)
    ax.text(0.07, 0.80, "Condición Matemática de Unicidad", color=TEXT_DARK, fontsize=12, fontweight="bold")
    
    bullets_s4 = (
        r"$\bullet$ $\mathbf{Ecuación\ del\ Sistema:}$ $A x = b$, con $A \in \mathbb{R}^{m \times 64}$ y $x \in \mathbb{R}^{64}$." "\n\n"
        r"$\bullet$ $\mathbf{Espacio\ Nulo\ } \mathrm{Nul}(A)\mathbf{:}$ Conjunto de vectores tales que $A v = 0$." "\n"
        r"  Si existe $v \neq 0$ en el núcleo, entonces:" "\n"
        r"  $\quad A(x + v) = Ax + Av = b + 0 = b$." "\n"
        r"  $\Rightarrow$ Las imágenes $x$ y $x+v$ producen exactamente las mismas mediciones." "\n\n"
        r"$\bullet$ $\mathbf{Teorema\ de\ Rango\ y\ Nulidad:}$" "\n"
        r"  $\quad \mathrm{rango}(A) + \dim(\mathrm{Nul}(A)) = n^2 = 64$." "\n\n"
        r"$\bullet$ $\mathbf{Condición\ de\ Unicidad:}$ $\dim(\mathrm{Nul}(A)) = 0 \Leftrightarrow \mathbf{rango}(A) = 64$." "\n"
        r"  Se requiere rango columna completo. Esto exige como mínimo $m \geq 64$ rayos."
    )
    ax.text(0.07, 0.44, bullets_s4, color="#334155", fontsize=9.2, linespacing=1.28)

    agregar_tarjeta(ax, 0.51, 0.13, 0.445, 0.72)
    ax.text(0.535, 0.80, "Comparación de Configuraciones de Adquisición", color=TEXT_DARK, fontsize=12, fontweight="bold")
    
    # Tabla comparativa
    ax.fill_between([0.535, 0.93], 0.69, 0.74, color="#f1f5f9")
    ax.text(0.545, 0.705, "Configuración", color=TEXT_DARK, fontsize=8.5, fontweight="bold")
    ax.text(0.66, 0.705, "Dimensiones", color=TEXT_DARK, fontsize=8.5, fontweight="bold")
    ax.text(0.77, 0.705, "Rango", color=TEXT_DARK, fontsize=8.5, fontweight="bold")
    ax.text(0.83, 0.705, "Nulidad", color=TEXT_DARK, fontsize=8.5, fontweight="bold")
    ax.text(0.89, 0.705, "Única?", color=TEXT_DARK, fontsize=8.5, fontweight="bold")

    rows_s4 = [
        ("A2 (H, V: 2 dir.)", "16 x 64", "15", "49", "NO", "#dc2626"),
        ("A4 (H, V, Diag: 4 dir.)", "46 x 64", "39", "25", "NO", "#dc2626"),
        ("A7 (+Oblicuas: 7 dir.)", "119 x 64", "64", "0", "SÍ", "#059669"),
    ]
    for i, (cfg, dims, rnk, nul, unq, col) in enumerate(rows_s4):
        y_r = 0.63 - i * 0.055
        ax.plot([0.535, 0.93], [y_r-0.015, y_r-0.015], color="#e2e8f0", lw=0.8)
        ax.text(0.545, y_r, cfg, color=TEXT_DARK, fontsize=8)
        ax.text(0.66, y_r, dims, color="#475569", fontsize=8)
        ax.text(0.77, y_r, rnk, color=TEXT_DARK, fontsize=8, fontweight="bold")
        ax.text(0.83, y_r, nul, color=TEXT_DARK, fontsize=8)
        ax.text(0.89, y_r, unq, color=col, fontsize=8.5, fontweight="bold")

    ax.text(0.535, 0.46, 
            r"$\mathbf{Mediciones\ Redundantes:}$" "\n"
            r"$\bullet$ $A_2$: 16 filas vs. rango 15 $\Rightarrow$ 1 medición linealmente dependiente." "\n"
            r"$\bullet$ $A_4$: 46 filas vs. rango 39 $\Rightarrow$ 7 mediciones redundantes." "\n"
            r"$\bullet$ $A_7$: 119 filas vs. rango 64 $\Rightarrow$ 55 mediciones redundantes." "\n\n"
            r"$\mathbf{Conclusión:}$ Más rayos no implican directamente unicidad. Solo cuando" "\n"
            r"incorporamos ángulos oblicuos ($A_7$) cubrimos todas las direcciones necesarias.",
            color="#334155", fontsize=8.8, linespacing=1.28, va="top")

    agregar_caja_oral(ax, "Para que la reconstrucción sea única, el espacio nulo debe ser cero (rango columna completo = 64). Si hay espacio nulo, hay infinitas imágenes distintas que dan la misma medición.")
    guardar_slide(fig, pdf)

    # -------------------------------------------------------------
    # SLIDE 5: LO INVISIBLE PARA EL TOMÓGRAFO (SVD)
    # -------------------------------------------------------------
    fig = plt.figure(figsize=(W, H))
    ax = crear_base_slide(fig, "Descomposición en Valores Singulares • Ejercicio 4c", "4. Lo Invisible para el Tomógrafo: Vectores Nulos y SVD", 5)

    agregar_tarjeta(ax, 0.045, 0.13, 0.44, 0.72)
    ax.text(0.07, 0.80, "SVD y Extracción de Modos Nulos", color=TEXT_DARK, fontsize=12, fontweight="bold")
    
    bullets_s5 = (
        r"$\bullet$ $\mathbf{Descomposición\ SVD:}$ $A_4 = U \Sigma V^T$." "\n"
        r"  Como $\mathrm{rango}(A_4) = 39 < 64$, existen exactamente $64 - 39 = 25$ valores" "\n"
        r"  singulares nulos ($\sigma_j = 0$ para $j > 39$)." "\n\n"
        r"$\bullet$ $\mathbf{Base\ del\ Núcleo:}$ Las columnas de $V$ (filas de $V^T$) asociadas a $\sigma_j = 0$" "\n"
        r"  forman una base ortonormal de $\mathrm{Nul}(A_4)$. En NumPy: $v = V^T[-1]$." "\n\n"
        r"$\bullet$ $\mathbf{Verificación\ Numérica:}$ $\|A_4 v\|_2 \approx 9.46 \times 10^{-16} \approx 0$." "\n\n"
        r"$\bullet$ $\mathbf{La\ Trampa\ Visual:}$ Construimos la imagen alterada:" "\n"
        r"  $\quad x_{\mathrm{alt}} = x_{\mathrm{fantoma}} + \gamma v \quad (\mathrm{con\ } \gamma = 0.8)$." "\n"
        r"  Al escanear: $A_4 x_{\mathrm{alt}} = A_4 x + \gamma A_4 v = b_4 + 0 = b_4$." "\n"
        r"  Diferencia en mediciones: $\|A_4 x_{\mathrm{alt}} - b_4\| \approx 1.56 \times 10^{-15}$."
    )
    ax.text(0.07, 0.44, bullets_s5, color="#334155", fontsize=9.2, linespacing=1.28)

    agregar_tarjeta(ax, 0.51, 0.13, 0.445, 0.72)
    ax.text(0.535, 0.80, "Demostración Visual del 'Modo Fantasma'", color=TEXT_DARK, fontsize=12, fontweight="bold")
    img_s5 = mpimg.imread("figuras/ej4_svd_invisible.png")
    ax_img = fig.add_axes([0.525, 0.35, 0.415, 0.38])
    ax_img.imshow(img_s5)
    ax_img.axis("off")

    ax.text(0.535, 0.20, 
            r"$\mathbf{¿Por\ qué\ A_4\ no\ lo\ ve?:}$ El vector $v$ tiene alternancia de signos (+ y -) que se" "\n"
            r"cancelan exactamente a lo largo de cada fila, columna y diagonal a 45°. El tomógrafo $A_4$" "\n"
            r"es ciego a esas oscilaciones finas de alta frecuencia.", 
            color=TEXT_MUTED, fontsize=8.5, linespacing=1.3)

    agregar_caja_oral(ax, "El vector v es una imagen que suma cero en todos los rayos de A4. Sumárselo a la imagen original cambia lo que vemos nosotros, pero para el tomógrafo es exactamente idéntica.")
    guardar_slide(fig, pdf)

    # -------------------------------------------------------------
    # SLIDE 6: RECONSTRUCCIÓN IDEAL Y NORMA MÍNIMA
    # -------------------------------------------------------------
    fig = plt.figure(figsize=(W, H))
    ax = crear_base_slide(fig, "Reconstrucción sin Ruido • Ejercicio 5", "5. Reconstrucción Ideal y Solución de Norma Mínima (`lstsq`)", 6)

    agregar_tarjeta(ax, 0.045, 0.13, 0.44, 0.72)
    ax.text(0.07, 0.80, "¿Por qué Residuo Cero NO Implica Buena Imagen?", color=TEXT_DARK, fontsize=12, fontweight="bold")
    
    bullets_s6 = (
        r"$\bullet$ $\mathbf{Mediciones\ Ideales:}$ $b_k = A_k x_{\mathrm{fantoma}}$ (sin ruido)." "\n"
        r"  Resolvemos con `np.linalg.lstsq(A_k, b_k)`." "\n\n"
        r"$\bullet$ $\mathbf{Solución\ de\ Norma\ Mínima:}$ Cuando hay infinitas soluciones, `lstsq`" "\n"
        r"  elige la única solución que minimiza la norma euclídea: $\hat{x}_k = \arg\min \|x\|_2$." "\n\n"
        r"$\bullet$ $\mathbf{Proyección\ sobre\ el\ Espacio\ Fila:}$" "\n"
        r"  Toda imagen se descompone como $x = x_{\mathrm{fila}} + x_{\mathrm{nulo}}$, con $x_{\mathrm{nulo}} \in \mathrm{Nul}(A_k)$." "\n"
        r"  `lstsq` descarta por completo la componente $x_{\mathrm{nulo}}$ (la hace 0)." "\n\n"
        r"$\bullet$ $\mathbf{Resultados\ Numéricos:}$" "\n"
        r"  $\quad A_2$: Residuo $= 3.97 \times 10^{-15} \approx 0$, Error Relativo $= \mathbf{46.89\%}$." "\n"
        r"  $\quad A_4$: Residuo $= 1.59 \times 10^{-14} \approx 0$, Error Relativo $= \mathbf{13.65\%}$." "\n"
        r"  $\quad A_7$: Residuo $= 1.30 \times 10^{-14} \approx 0$, Error Relativo $= \mathbf{0.00\%}$."
    )
    ax.text(0.07, 0.44, bullets_s6, color="#334155", fontsize=9.2, linespacing=1.28)

    agregar_tarjeta(ax, 0.51, 0.13, 0.445, 0.72)
    ax.text(0.535, 0.80, "Comparativa Visual de Reconstrucciones", color=TEXT_DARK, fontsize=12, fontweight="bold")
    img_s6 = mpimg.imread("figuras/ej5_reconstrucciones_ideales.png")
    ax_img = fig.add_axes([0.525, 0.36, 0.415, 0.36])
    ax_img.imshow(img_s6)
    ax_img.axis("off")

    ax.text(0.535, 0.22, 
            r"En $A_2$ y $A_4$ la reconstrucción se ve borrosa y lavada porque `lstsq` eliminó la" "\n"
            r"porción de la imagen que vivía en el espacio nulo. Solo en $A_7$ ($\mathrm{Nul}=\{0\}$)" "\n"
            r"se recupera la totalidad de la información original.", 
            color=TEXT_MUTED, fontsize=8.5, linespacing=1.3)

    agregar_caja_oral(ax, "El residuo mide si la solución coincide con los rayos del escáner, no con la imagen real. Un residuo cero con espacio nulo descarta los detalles invisibles y produce una imagen lavada.")
    guardar_slide(fig, pdf)

    # -------------------------------------------------------------
    # SLIDE 7: MEDICIONES CON RUIDO Y MÍNIMOS CUADRADOS
    # -------------------------------------------------------------
    fig = plt.figure(figsize=(W, H))
    ax = crear_base_slide(fig, "Mediciones Ruidosas • Ejercicio 6", "6. Adquisición Real con Ruido e Incompatibilidad del Sistema", 7)

    agregar_tarjeta(ax, 0.045, 0.13, 0.44, 0.72)
    ax.text(0.07, 0.80, "Impacto del Ruido Gaussiano en Detectores", color=TEXT_DARK, fontsize=12, fontweight="bold")
    
    bullets_s7 = (
        r"$\bullet$ $\mathbf{Modelo\ Perturbado:}$ $b_\sigma = b_7 + \eta_\sigma$, con $\eta_\sigma = \sigma \cdot \mathrm{escala} \cdot z$." "\n"
        r"  $z \sim \mathcal{N}(0, 1)$ es un vector único; $\sigma \in \{0, 0.01, 0.03, 0.06, 0.10\}$." "\n\n"
        r"$\bullet$ $\mathbf{Incompatibilidad\ del\ Sistema:}$" "\n"
        r"  El vector de mediciones limpias $b_7$ pertenece a $\mathrm{Col}(A_7) \subset \mathbb{R}^{119}$ (dimensión 64)." "\n"
        r"  El ruido $\eta_\sigma$ saca a $b_\sigma$ fuera del subespacio. Como $119 > 64$, no existe ningún $x$" "\n"
        r"  capaz de satisfacer las 119 ecuaciones ruidosas simultáneamente." "\n\n"
        r"$\bullet$ $\mathbf{Mínimos\ Cuadrados:}$ Buscamos $\hat{x}_\sigma$ que minimice la distancia euclídea:" "\n"
        r"  $\quad \hat{x}_\sigma = \arg\min \|A_7 x - b_\sigma\|_2^2$." "\n\n"
        r"$\bullet$ $\mathbf{Por\ qué\ aparecen\ valores\ negativos:}$ La atenuación real es $\mu \geq 0$." "\n"
        r"  `lstsq` no tiene restricciones físicas; para compensar el ruido y acercar las" "\n"
        r"  sumas a $b_\sigma$, fuerza a píxeles del fondo a tomar valores negativos (hasta -0.13)."
    )
    ax.text(0.07, 0.44, bullets_s7, color="#334155", fontsize=9.2, linespacing=1.28)

    agregar_tarjeta(ax, 0.51, 0.13, 0.445, 0.72)
    ax.text(0.535, 0.80, "Evolución Visual del Error con el Ruido", color=TEXT_DARK, fontsize=12, fontweight="bold")
    img_s7 = mpimg.imread("figuras/ej6_ruido_vs_error.png")
    ax_img = fig.add_axes([0.525, 0.40, 0.415, 0.33])
    ax_img.imshow(img_s7)
    ax_img.axis("off")

    ax.text(0.535, 0.22, 
            r"$\mathbf{Tendencias\ Cuantitativas:}$" "\n"
            r"$\bullet$ El error relativo crece linealmente con $\sigma$ (de 0% a 24.5%)." "\n"
            r"$\bullet$ El residuo deja de ser nulo (pasa de $10^{-14}$ a 0.9070) porque mide la" "\n"
            r"  distancia ortogonal mínima desde $b_\sigma$ hasta el plano $\mathrm{Col}(A_7)$.",
            color=TEXT_MUTED, fontsize=8.5, linespacing=1.3)

    agregar_caja_oral(ax, "El ruido hace que las 119 ecuaciones se contradigan entre sí. Mínimos cuadrados encuentra el punto más cercano, pero deja un residuo inevitable y genera valores negativos por falta de restricciones.")
    guardar_slide(fig, pdf)

    # -------------------------------------------------------------
    # SLIDE 8: LA RECONSTRUCCIÓN COMO PROYECCIÓN ORTOGONAL
    # -------------------------------------------------------------
    fig = plt.figure(figsize=(W, H))
    ax = crear_base_slide(fig, r"Geometría de Mínimos Cuadrados • Ejercicio 7", r"7. La Reconstrucción como Proyección Ortogonal en $\mathbb{R}^{119}$", 8)

    agregar_tarjeta(ax, 0.045, 0.13, 0.44, 0.72)
    ax.text(0.07, 0.80, "Ortogonalidad del Residuo y Ecuaciones Normales", color=TEXT_DARK, fontsize=12, fontweight="bold")
    
    bullets_s8 = (
        r"$\bullet$ $\mathbf{Comprobación\ Numérica\ (\sigma = 0.06):}$" "\n"
        r"  $\quad \|A_7^T r_\sigma\|_2 = \|A_7^T (b_\sigma - A_7 \hat{x}_\sigma)\|_2 \approx \mathbf{3.33 \times 10^{-14} \approx 0}$." "\n\n"
        r"$\bullet$ $\mathbf{Interpretación\ Geométrica:}$" "\n"
        r"  $A_7^T r_\sigma$ es el producto escalar de $r_\sigma$ contra cada una de las 64 columnas de $A_7$." "\n"
        r"  Como da cero contra todas, el residuo es ortogonal a cada columna $\Rightarrow r_\sigma \perp \mathrm{Col}(A_7)$." "\n"
        r"  Por definición, el punto del subespacio cuya distancia a $b_\sigma$ cae a 90° es" "\n"
        r"  la $\mathbf{proyección\ ortogonal}$: $\operatorname{Proy}_{\mathrm{Col}(A_7)}(b_\sigma) = A_7 \hat{x}_\sigma$." "\n\n"
        r"$\bullet$ $\mathbf{Ecuaciones\ Normales:}$" "\n"
        r"  $\quad A_7^T(b_\sigma - A_7 \hat{x}_\sigma) = 0 \Leftrightarrow \mathbf{A_7^T A_7 \hat{x}_\sigma = A_7^T b_\sigma}$."
    )
    ax.text(0.07, 0.45, bullets_s8, color="#334155", fontsize=9.2, linespacing=1.28)

    agregar_tarjeta(ax, 0.51, 0.13, 0.445, 0.72)
    ax.text(0.535, 0.80, "Distinción Crucial: Dos Conceptos de 'Proyección'", color=TEXT_DARK, fontsize=12, fontweight="bold")
    img_s8 = mpimg.imread("figuras/ej7_geometria_proyeccion.png")
    ax_img = fig.add_axes([0.525, 0.38, 0.415, 0.36])
    ax_img.imshow(img_s8)
    ax_img.axis("off")

    ax.text(0.535, 0.20, 
            r"$\mathbf{1.\ Proyección\ Tomográfica\ (Física):}$ El escáner proyecta la atenuación de una" "\n"
            r"sección 2D sobre una línea 1D de detectores para cada ángulo ($x \mapsto Ax$)." "\n"
            r"$\mathbf{2.\ Proyección\ Ortogonal\ (Matemática):}$ Mapeo en $\mathbb{R}^{119}$ que baja el dato ruidoso" "\n"
            r"$b_\sigma$ perpendicularmente sobre $\mathrm{Col}(A_7)$ para encontrar la mejor aproximación.", 
            color=TEXT_MUTED, fontsize=8.5, linespacing=1.3)

    agregar_caja_oral(ax, "Hacer A7.T @ residuo calcula el producto escalar contra las columnas. Como da 0, el residuo forma 90 grados con el espacio de mediciones y A7 @ x_hat es la sombra perpendicular exacta.")
    guardar_slide(fig, pdf)

    # -------------------------------------------------------------
    # SLIDE 9: GRADIENTE DESCENDIENTE Y ESTABILIDAD
    # -------------------------------------------------------------
    fig = plt.figure(figsize=(W, H))
    ax = crear_base_slide(fig, "Optimización Iterativa • Ejercicio 8a, 8b y 8c", "8. Métodos Iterativos: Gradiente Descendiente y Tasa Crítica", 9)

    agregar_tarjeta(ax, 0.045, 0.13, 0.44, 0.72)
    ax.text(0.07, 0.80, "Función de Costo y Análisis de Convergencia", color=TEXT_DARK, fontsize=12, fontweight="bold")
    
    bullets_s9 = (
        r"$\bullet$ $\mathbf{Función\ Objetivo:}$ $E(x) = \frac{1}{2}\|A_7 x - b_\sigma\|^2$ (parábola en $\mathbb{R}^{64}$)." "\n\n"
        r"$\bullet$ $\mathbf{Gradiente\ y\ Hessiana:}$" "\n"
        r"  $\quad \nabla E(x) = A_7^T(A_7 x - b_\sigma)$  (apunta al máximo crecimiento)." "\n"
        r"  $\quad H = \nabla^2 E(x) = A_7^T A_7$  (simétrica, constante y definida positiva)." "\n\n"
        r"$\bullet$ $\mathbf{Algoritmo\ Gradiente\ Descendiente:}$" "\n"
        r"  $\quad x_0 = \mathbf{0}, \qquad x_{t+1} = x_t - \alpha \nabla E(x_t)$." "\n\n"
        r"$\bullet$ $\mathbf{Cota\ Crítica\ de\ Estabilidad:}$ El mayor autovalor de $H$ es $\mu_{\max} \approx 47.6$." "\n"
        r"  La contracción del error exige: $|1 - \alpha \mu_{\max}| < 1 \Leftrightarrow \mathbf{0 < \alpha < \frac{2}{\mu_{\max}}} \approx 0.042$." "\n"
        r"  $\bullet$ Si $\alpha < 2/\mu_{\max}$: el costo desciende de forma estable al mínimo." "\n"
        r"  $\bullet$ Si $\alpha > 2/\mu_{\max}$: el paso se pasa de largo del valle y $\mathbf{diverge\ exponencialmente}$."
    )
    ax.text(0.07, 0.44, bullets_s9, color="#334155", fontsize=9.2, linespacing=1.28)

    agregar_tarjeta(ax, 0.51, 0.13, 0.445, 0.72)
    ax.text(0.535, 0.80, "Convergencia Estable vs. Explosión Numérica", color=TEXT_DARK, fontsize=12, fontweight="bold")
    img_s9 = mpimg.imread("figuras/ej8_convergencia_gd.png")
    ax_img = fig.add_axes([0.525, 0.35, 0.415, 0.38])
    ax_img.imshow(img_s9)
    ax_img.axis("off")

    ax.text(0.535, 0.20, 
            r"Que las curvas se aplanen indica que el algoritmo alcanzó el fondo del cuenco" "\n"
            r"donde el gradiente vale cero ($\|\nabla E(x)\| \approx 0$). Cuando $\alpha > 2/\mu_{\max}$, el costo salta" "\n"
            r"hacia las paredes externas del valle cuadrático y explota hacia infinito.", 
            color=TEXT_MUTED, fontsize=8.5, linespacing=1.3)

    agregar_caja_oral(ax, "mu_max mide la pendiente más empinada del cuenco. Si el paso alfa es mayor a 2/mu_max, el algoritmo rebota de pared en pared y diverge. Por debajo de esa cota, siempre converge.")
    guardar_slide(fig, pdf)

    # -------------------------------------------------------------
    # SLIDE 10: MÉTODO DE NEWTON Y COMPARACIÓN
    # -------------------------------------------------------------
    fig = plt.figure(figsize=(W, H))
    ax = crear_base_slide(fig, "Optimización de Segundo Orden • Ejercicio 8d y 8e", "9. Método de Newton y Comparación de Métodos de Inversión", 10)

    agregar_tarjeta(ax, 0.045, 0.13, 0.44, 0.72)
    ax.text(0.07, 0.80, "¿Por qué Newton Resuelve en 1 Sola Iteración?", color=TEXT_DARK, fontsize=12, fontweight="bold")
    
    bullets_s10 = (
        r"$\bullet$ $\mathbf{Paso\ de\ Newton:}$ Resuelve $H p_t = \nabla E(x_t)$ mediante `solve(H, g)` y actualiza:" "\n"
        r"  $\quad x_{t+1} = x_t - p_t$." "\n\n"
        r"$\bullet$ $\mathbf{Convergencia\ en\ 1\ Paso:}$" "\n"
        r"  Newton aproxima la función por su polinomio de Taylor cuadrático:" "\n"
        r"  $\quad E(x_t + p) \approx E(x_t) + \nabla E(x_t)^T p + \frac{1}{2} p^T H p$." "\n"
        r"  Como $E(x) = \frac{1}{2}\|A_7 x - b_\sigma\|^2$ $\mathbf{ya\ es\ una\ parábola\ exacta}$, la aproximación" "\n"
        r"  coincide al 100% con la función real. Al igualar el gradiente del modelo a cero," "\n"
        r"  salta directamente al mínimo en la primera iteración desde cualquier punto:" "\n"
        r"  $\quad x_1 = x_0 - H^{-1} \nabla E(x_0) = (A_7^T A_7)^{-1} A_7^T b_\sigma = \hat{x}_{\mathrm{ls}}$." "\n\n"
        r"$\bullet$ La diferencia numérica entre la iteración 1 y 2 es de orden $10^{-14}$."
    )
    ax.text(0.07, 0.45, bullets_s10, color="#334155", fontsize=9.2, linespacing=1.28)

    agregar_tarjeta(ax, 0.51, 0.13, 0.445, 0.72)
    ax.text(0.535, 0.80, "Comparación Integral de Algoritmos", color=TEXT_DARK, fontsize=12, fontweight="bold")
    
    # Tabla comparativa métodos
    ax.fill_between([0.535, 0.93], 0.69, 0.74, color="#f1f5f9")
    ax.text(0.545, 0.705, "Método", color=TEXT_DARK, fontsize=8.5, fontweight="bold")
    ax.text(0.68, 0.705, "Tipo", color=TEXT_DARK, fontsize=8.5, fontweight="bold")
    ax.text(0.79, 0.705, "Iteraciones", color=TEXT_DARK, fontsize=8.5, fontweight="bold")
    ax.text(0.88, 0.705, "Costo / Paso", color=TEXT_DARK, fontsize=8.5, fontweight="bold")

    rows_s10 = [
        ("np.linalg.lstsq", "Directo (SVD)", "1 paso", "O(n^3) factoriz."),
        ("Método de Newton", "2do orden", "1 paso", "O(n^3) solve H"),
        ("Gradiente Desc.", "1er orden", "~150 pasos", "O(m n) matriz-vec"),
    ]
    for i, (mth, typ, iters, cst) in enumerate(rows_s10):
        y_r = 0.63 - i * 0.055
        ax.plot([0.535, 0.93], [y_r-0.015, y_r-0.015], color="#e2e8f0", lw=0.8)
        ax.text(0.545, y_r, mth, color=TEXT_DARK, fontsize=8, fontweight="bold")
        ax.text(0.68, y_r, typ, color="#475569", fontsize=8)
        ax.text(0.79, y_r, iters, color=PRIMARY_BLUE if "1" in iters else TEXT_DARK, fontsize=8, fontweight="bold")
        ax.text(0.88, y_r, cst, color=TEXT_MUTED, fontsize=7.5)

    ax.text(0.535, 0.46, 
            r"$\mathbf{¿Cuál\ es\ mejor\ para\ tomografía\ real?:}$" "\n"
            r"$\bullet$ En $8 \times 8$, Newton y `lstsq` son instantáneos." "\n"
            r"$\bullet$ En $128 \times 128$ ($n^2 = 16.384$), armar $H$ de $16.384 \times 16.384$ requiere" "\n"
            r"  2 GB de memoria y resolver $H p = g$ cuesta billones de operaciones." "\n"
            r"$\bullet$ $\mathbf{Gradiente\ Descendiente}$ es el único escalable porque solo requiere" "\n"
            r"  multiplicar matrices dispersas $A x$ y $A^T r$ sin almacenar nunca $H$.",
            color="#334155", fontsize=8.8, linespacing=1.28, va="top")

    agregar_caja_oral(ax, "Newton resuelve en 1 paso porque la función ya es una parábola cuadrática exacta. Pero no escala a imágenes grandes porque invertir H cuesta O(n^3). Por eso en tomografía real se usa Gradiente.")
    guardar_slide(fig, pdf)

    # -------------------------------------------------------------
    # SLIDE 11: REGULARIZACIÓN CUADRÁTICA DE TIKHONOV
    # -------------------------------------------------------------
    fig = plt.figure(figsize=(W, H))
    ax = crear_base_slide(fig, "Regularización Espacial • Ejercicio 9", "10. Regularización Cuadrática: Prior de Suavidad y Trade-Off", 11)

    agregar_tarjeta(ax, 0.045, 0.13, 0.44, 0.72)
    ax.text(0.07, 0.80, "El Operador de Diferencias y el Costo Regularizado", color=TEXT_DARK, fontsize=12, fontweight="bold")
    
    bullets_s11 = (
        r"$\bullet$ $\mathbf{Motivación:}$ Mínimos cuadrados con ruido produce imágenes con granulado" "\n"
        r"  y saltos bruscos entre píxeles adyacentes. Incorporamos un prior de suavidad." "\n\n"
        r"$\bullet$ $\mathbf{Matriz\ de\ Diferencias\ } D = \binom{D_h}{D_v} \in \mathbb{R}^{112 \times 64}\mathbf{:}$" "\n"
        r"  $D_h$ calcula diferencias horizontales $X_{i, j+1} - X_{i, j}$ (-1 en $k$, +1 en $k+1$)." "\n"
        r"  $D_v$ calcula diferencias verticales $X_{i+1, j} - X_{i, j}$ (-1 en $k$, +1 en $k+n$)." "\n"
        r"  $\|Dx\|_2^2$ mide la falta de suavidad / rugosidad. Si la imagen es constante, $Dx = 0$." "\n\n"
        r"$\bullet$ $\mathbf{Función\ de\ Costo\ Regularizada:}$" "\n"
        r"  $\quad J_{\sigma, \lambda}(x) = \frac{1}{2} \|A_7 x - b_\sigma\|^2 + \frac{\lambda}{2} \|Dx\|^2$." "\n\n"
        r"$\bullet$ $\mathbf{Gradiente:}$ $\nabla J_{\sigma, \lambda}(x) = A_7^T(A_7 x - b_\sigma) + \lambda D^T D x$."
    )
    ax.text(0.07, 0.45, bullets_s11, color="#334155", fontsize=9.2, linespacing=1.28)

    agregar_tarjeta(ax, 0.51, 0.13, 0.445, 0.72)
    ax.text(0.535, 0.80, "El Compromiso del Hiperparámetro lambda", color=TEXT_DARK, fontsize=12, fontweight="bold")
    img_s11 = mpimg.imread("figuras/ej9_regularizacion_tradeoff.png")
    ax_img = fig.add_axes([0.525, 0.38, 0.415, 0.35])
    ax_img.imshow(img_s11)
    ax_img.axis("off")

    ax.text(0.535, 0.20, 
            r"$\mathbf{Impacto\ de\ \lambda:}$" "\n"
            r"$\bullet$ $\lambda = 0$ (Sub-regularizado): Ajusta el ruido; artefactos y error alto (24.5%)." "\n"
            r"$\bullet$ $\lambda = 0.3$ (Óptimo): Elimina el ruido en el fondo y reduce el error a 16.8%." "\n"
            r"$\bullet$ $\lambda = 3.0$ (Sobre-regularizado): Suaviza en exceso, difumina bordes anatómicos.", 
            color=TEXT_MUTED, fontsize=8.5, linespacing=1.3)

    agregar_caja_oral(ax, "La matriz D mide los saltos entre vecinos. El término lambda * ||Dx||^2 frena las oscilaciones causadas por el ruido. Si lambda es muy chico queda ruido; si es muy grande queda borrosa.")
    guardar_slide(fig, pdf)

    # -------------------------------------------------------------
    # SLIDE 12: APLICACIÓN 128x128 Y PRINCIPIO DE MOROZOV
    # -------------------------------------------------------------
    fig = plt.figure(figsize=(W, H))
    ax = crear_base_slide(fig, r"Aplicación a Gran Escala • Ejercicio 10", r"11. Reconstrucción en Alta Resolución y Selección de $\lambda$ a Ciegas", 12)

    agregar_tarjeta(ax, 0.045, 0.13, 0.44, 0.72)
    ax.text(0.07, 0.80, "Desafíos de Escala y Matrices Dispersas", color=TEXT_DARK, fontsize=12, fontweight="bold")
    
    bullets_s12 = (
        r"$\bullet$ $\mathbf{Salto\ de\ Escala:}$ Imagen desconocida de $128 \times 128$ píxeles." "\n"
        r"  Vector $x \in \mathbb{R}^{16.384}$, matriz $A \in \mathbb{R}^{Kq \times 16.384}$." "\n\n"
        r"$\bullet$ $\mathbf{Estructura\ Rala\ (Sparse):}$ Cada rayo solo atraviesa $\approx 128$ píxeles;" "\n"
        r"  el 99% de $A$ son ceros. Usar matrices densas colapsaría la memoria." "\n"
        r"  Se opera con `scipy.sparse.csr_matrix` y productos encadenados:" "\n"
        r"  $\quad \nabla J_\lambda(x) = A^T(Ax - b) + \lambda D^T(Dx)$." "\n\n"
        r"$\bullet$ $\mathbf{Principio\ de\ Discrepancia\ de\ Morozov:}$" "\n"
        r"  ¿Cómo elegimos $\lambda$ si la imagen original permanece oculta?" "\n"
        r"  Sabemos que las mediciones reales cumplen $b = A x_{\mathrm{real}} + \eta$." "\n"
        r"  $\Rightarrow$ La reconstrucción óptima no debe forzar residuo 0, sino hacer que:" "\n"
        r"  $\quad \|\mathbf{A \hat{x}_\lambda - b}\|_2 \approx \|\mathbf{\eta}\|_2 \quad (\mathrm{estimación\ de\ ruido})$."
    )
    ax.text(0.07, 0.44, bullets_s12, color="#334155", fontsize=9.2, linespacing=1.28)

    agregar_tarjeta(ax, 0.51, 0.13, 0.445, 0.72)
    ax.text(0.535, 0.80, "Criterio de Selección de Hiperparámetros", color=TEXT_DARK, fontsize=12, fontweight="bold")
    img_s12 = mpimg.imread("figuras/ej10_pipeline_128.png")
    ax_img = fig.add_axes([0.525, 0.42, 0.415, 0.35])
    ax_img.imshow(img_s12)
    ax_img.axis("off")

    ax.text(0.535, 0.38, 
            r"$\mathbf{Regla\ Práctica\ de\ Morozov:}$" "\n"
            r"$\bullet$ Si $\|A\hat{x} - b\| \ll \|\eta\| \Rightarrow \lambda$ es chico: estamos ajustando ruido." "\n"
            r"$\bullet$ Si $\|A\hat{x} - b\| \gg \|\eta\| \Rightarrow \lambda$ es excesivo: perdimos detalles de la imagen." "\n"
            r"$\bullet$ El $\lambda^*$ ideal iguala el residuo con la cota de ruido físico de los detectores.",
            color=TEXT_MUTED, fontsize=8.5, linespacing=1.3, va="top")

    agregar_caja_oral(ax, "En la vida real no conocemos la imagen original. Elegimos lambda comparando la norma del residuo con la estimación del ruido (Morozov): el residuo debe ser del mismo tamaño que el ruido.")
    guardar_slide(fig, pdf)

    # -------------------------------------------------------------
    # SLIDE 13: CONCLUSIONES Y SÍNTESIS GENERAL
    # -------------------------------------------------------------
    fig = plt.figure(figsize=(W, H))
    ax = crear_base_slide(fig, "Reflexión Final • Ejercicio 11", "12. Síntesis Conceptual del Proyecto Aplicado", 13)

    # 4 Cuadros de Síntesis en grilla 2x2
    bloques_s13 = [
        ("1. Problema Inverso y Modelo Discreto", 
         "• La tomografía infiere una causa oculta (distribución de atenuación x)\n  a partir de sus efectos integrados (mediciones de detectores b).\n• La discretización b = Ax traduce las leyes físicas continuas a un marco\n  algebraico riguroso.", 
         0.045, 0.50, 0.44, 0.35, "#38bdf8"),
        
        ("2. Identificabilidad: Rango y Espacio Nulo", 
         "• La geometría de rayos determina la solubilidad única del problema.\n• Rango completo (rango=n^2, Nul={0}) es indispensable para no tener\n  patrones invisibles o fantasmas SVD que confundan al tomógrafo.\n• La redundancia angular es preferible a la redundancia paralela.", 
         0.51, 0.50, 0.445, 0.35, "#34d399"),
        
        ("3. Ruido e Incompatibilidad Geométrica", 
         "• Los errores de medición sacan a b de Col(A), volviendo el sistema incompatible.\n• Mínimos cuadrados resuelve la incompatibilidad mediante una proyección\n  ortogonal exacta en R^m (A^T r = 0).\n• Aparecen valores negativos al ser un ajuste sin restricciones físicas.", 
         0.045, 0.13, 0.44, 0.34, "#fbbf24"),
        
        ("4. Computación Escalable y Regularización", 
         "• GD es el método de elección para alta resolución con matrices ralas,\n  siempre que el paso respete la cota de estabilidad alpha < 2/mu_max.\n• Tikhonov resuelve el mal condicionamiento: filtra oscilaciones de ruido\n  y estabiliza la reconstrucción mediante el principio de Morozov.", 
         0.51, 0.13, 0.445, 0.34, "#a78bfa"),
    ]

    for tit, desc, x_c, y_c, w_c, h_c, acc_col in bloques_s13:
        agregar_tarjeta(ax, x_c, y_c, w_c, h_c)
        ax.plot([x_c+0.02, x_c+0.08], [y_c+h_c-0.035, y_c+h_c-0.035], color=acc_col, lw=3)
        ax.text(x_c+0.02, y_c+h_c-0.07, tit, color=TEXT_DARK, fontsize=10.5, fontweight="bold")
        ax.text(x_c+0.02, y_c+h_c-0.11, desc, color="#475569", fontsize=9.0, linespacing=1.45, va="top")

    agregar_caja_oral(ax, "Mensaje final: Para reconstruir tomografías reales se combinan tres pilares: adquisición angular variada (rango), optimización iterativa liviana (GD) y priors de suavidad física (Tikhonov).")
    guardar_slide(fig, pdf)

print("presentacion.pdf generada exitosamente con 13 diapositivas completas.")
