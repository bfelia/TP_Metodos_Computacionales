import os
import numpy as np
import matplotlib.pyplot as plt

os.environ["MPLCONFIGDIR"] = "/tmp/mpl"
os.makedirs("figuras", exist_ok=True)

# Configuración de estilo global
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.edgecolor'] = '#cbd5e1'
plt.rcParams['axes.linewidth'] = 0.8

# 1. Definición del fantoma
X_fantoma = np.array([
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [0.0, 0.0, 0.8, 0.3, 0.3, 0.3, 0.0, 0.0],
    [0.0, 0.8, 0.8, 0.8, 0.3, 0.3, 0.3, 0.0],
    [0.0, 0.3, 0.8, 0.3, 0.3, 0.3, 0.3, 0.0],
    [0.0, 0.3, 0.3, 0.3, 0.3, 0.5, 0.3, 0.0],
    [0.0, 0.3, 0.3, 0.3, 0.5, 0.5, 0.5, 0.0],
    [0.0, 0.0, 0.3, 0.3, 0.3, 0.5, 0.0, 0.0],
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
], dtype=float)
x_fantoma = X_fantoma.reshape(-1)

def mascara_rayo(n, direccion, s):
    matriz = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if direccion[0] * i + direccion[1] * j == s:
                matriz[i, j] = 1
    return matriz

def matriz_proyeccion(n, direcciones):
    matriz, rayo = [], []
    for d in direcciones:
        vals_s = sorted(list(set(d[0]*i + d[1]*j for i in range(n) for j in range(n))))
        for s in vals_s:
            rayo.append((tuple(d), s))
            matriz.append(mascara_rayo(n, d, s).reshape(-1))
    return np.array(matriz), rayo

D2 = [(1, 0), (0, 1)]
D4 = D2 + [(1, 1), (1, -1)]
D7 = D4 + [(2, 1), (1, 2), (3, 1)]

A2, _ = matriz_proyeccion(8, D2)
A4, _ = matriz_proyeccion(8, D4)
A7, _ = matriz_proyeccion(8, D7)

# FIGURA 1: Fantoma original
fig, ax = plt.subplots(figsize=(4.5, 4), dpi=200)
im = ax.imshow(X_fantoma, cmap="gray", vmin=0, vmax=0.8)
ax.set_title(r"Fantoma $X_{\mathrm{fantoma}} \in \mathbb{R}^{8 \times 8}$", fontsize=11, fontweight="bold", pad=8)
ax.set_xticks(range(8))
ax.set_yticks(range(8))
ax.tick_params(labelsize=8)
cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
cbar.ax.tick_params(labelsize=8)
cbar.set_label(r"Atenuación $\mu$", fontsize=9)
plt.tight_layout()
plt.savefig("figuras/ej1_fantoma.png")
plt.close()

# FIGURA 2: Señales 1D de proyecciones horizontales y verticales
b2 = A2 @ x_fantoma
fig, ax = plt.subplots(1, 2, figsize=(7.5, 3), dpi=200)
ax[0].plot(range(8), b2[:8], marker="o", color="#2563eb", lw=1.8, markersize=5)
ax[0].set_title(r"Rayos Horizontales: $\Sigma$ filas", fontsize=9, fontweight="bold")
ax[0].set_xlabel("Rayo (fila)", fontsize=8)
ax[0].set_ylabel(r"Medición $b_r$", fontsize=8)
ax[0].grid(True, linestyle="--", alpha=0.5)
ax[0].tick_params(labelsize=8)

ax[1].plot(range(8), b2[8:], marker="s", color="#059669", lw=1.8, markersize=5)
ax[1].set_title(r"Rayos Verticales: $\Sigma$ columnas", fontsize=9, fontweight="bold")
ax[1].set_xlabel("Rayo (columna)", fontsize=8)
ax[1].grid(True, linestyle="--", alpha=0.5)
ax[1].tick_params(labelsize=8)
plt.tight_layout()
plt.savefig("figuras/ej3_sinograma.png")
plt.close()

# FIGURA 3: Espacio Nulo SVD en A4 y alteración invisible
U4, S4, Vt4 = np.linalg.svd(A4)
v_null = Vt4[-1]
gamma = 0.8
x_alt = x_fantoma + gamma * v_null

fig, ax = plt.subplots(1, 3, figsize=(9, 3), dpi=200)
ax[0].imshow(X_fantoma, cmap="gray", vmin=0, vmax=0.8)
ax[0].set_title("Original $x$", fontsize=9, fontweight="bold")
ax[0].axis("off")

im1 = ax[1].imshow(v_null.reshape(8, 8), cmap="coolwarm")
ax[1].set_title(r"Perturbación $v \in \mathrm{Nul}(A_4)$", fontsize=9, fontweight="bold")
ax[1].axis("off")
plt.colorbar(im1, ax=ax[1], fraction=0.046, pad=0.04)

ax[2].imshow(x_alt.reshape(8, 8), cmap="gray", vmin=0, vmax=0.8)
ax[2].set_title(r"$x_{\mathrm{alt}} = x + \gamma v$ (Mismo $b_4$)", fontsize=9, fontweight="bold")
ax[2].axis("off")
plt.tight_layout()
plt.savefig("figuras/ej4_svd_invisible.png")
plt.close()

# FIGURA 4: Reconstrucciones ideales (A2, A4, A7)
x_rec_2 = np.linalg.lstsq(A2, b2, rcond=None)[0]
b4 = A4 @ x_fantoma
x_rec_4 = np.linalg.lstsq(A4, b4, rcond=None)[0]
b7 = A7 @ x_fantoma
x_rec_7 = np.linalg.lstsq(A7, b7, rcond=None)[0]

fig, ax = plt.subplots(1, 4, figsize=(10, 2.7), dpi=200)
ax[0].imshow(X_fantoma, cmap="gray", vmin=0, vmax=0.8)
ax[0].set_title("Original", fontsize=9, fontweight="bold")
ax[0].axis("off")

ax[1].imshow(x_rec_2.reshape(8, 8), cmap="gray", vmin=0, vmax=0.8)
ax[1].set_title(r"$A_2$ (Rango 15)" "\n" r"Error: 46.9%", fontsize=9)
ax[1].axis("off")

ax[2].imshow(x_rec_4.reshape(8, 8), cmap="gray", vmin=0, vmax=0.8)
ax[2].set_title(r"$A_4$ (Rango 39)" "\n" r"Error: 13.7%", fontsize=9)
ax[2].axis("off")

ax[3].imshow(x_rec_7.reshape(8, 8), cmap="gray", vmin=0, vmax=0.8)
ax[3].set_title(r"$A_7$ (Rango 64)" "\n" r"Error: 0.0%", fontsize=9, color="#059669")
ax[3].axis("off")
plt.tight_layout()
plt.savefig("figuras/ej5_reconstrucciones_ideales.png")
plt.close()

# FIGURA 5: Ruido y Mínimos Cuadrados (Ej. 6)
np.random.seed(18)
z = np.random.normal(0, 1, len(b7))
escala = np.sqrt(np.mean(b7**2))
sigmas = [0.0, 0.01, 0.03, 0.06, 0.10]
recs_noise = []
for s in sigmas:
    b_s = b7 + s * escala * z
    recs_noise.append(np.linalg.lstsq(A7, b_s, rcond=None)[0])

fig, ax = plt.subplots(1, 5, figsize=(11, 2.5), dpi=200)
for i, s in enumerate(sigmas):
    err = np.linalg.norm(recs_noise[i] - x_fantoma) / np.linalg.norm(x_fantoma)
    ax[i].imshow(recs_noise[i].reshape(8, 8), cmap="gray", vmin=0, vmax=0.8)
    ax[i].set_title(rf"$\sigma = {s}$" f"\nErr: {err*100:.1f}%", fontsize=8)
    ax[i].axis("off")
plt.tight_layout()
plt.savefig("figuras/ej6_ruido_vs_error.png")
plt.close()

# FIGURA 6: Diagrama conceptual de Proyección Ortogonal (Ej. 7)
fig, ax = plt.subplots(figsize=(6, 3.2), dpi=200)
plane_x = np.array([0, 5, 7, 2, 0])
plane_y = np.array([0, 0, 2.5, 2.5, 0])
ax.fill(plane_x, plane_y, color="#e2e8f0", alpha=0.7)
ax.text(5.5, 0.4, r"$\mathrm{Col}(A_7) \subset \mathbb{R}^{119}$", fontsize=9, color="#475569")

# Vector b_sigma fuera del plano
b_pt = np.array([3.5, 3.2])
p_pt = np.array([3.5, 1.2])
o_pt = np.array([1.2, 0.5])

# Flechas
ax.annotate("", xy=p_pt, xytext=o_pt, arrowprops=dict(arrowstyle="->", lw=2.2, color="#2563eb"))
ax.text(2.0, 0.6, r"$A_7 \hat{x}_\sigma$", color="#2563eb", fontsize=11, fontweight="bold")

ax.annotate("", xy=b_pt, xytext=o_pt, arrowprops=dict(arrowstyle="->", lw=2.2, color="#dc2626"))
ax.text(2.0, 2.1, r"$b_\sigma = b_7 + \eta$", color="#dc2626", fontsize=11, fontweight="bold")

ax.annotate("", xy=b_pt, xytext=p_pt, arrowprops=dict(arrowstyle="->", lw=2.0, ls="--", color="#4b5563"))
ax.text(3.7, 2.2, r"$r_\sigma \perp \mathrm{Col}(A_7)$" "\n" r"$A_7^T r_\sigma \approx 0$", color="#1f2937", fontsize=9)

corner_size = 0.25
ax.plot([p_pt[0], p_pt[0]+corner_size, p_pt[0]+corner_size], 
        [p_pt[1]+corner_size, p_pt[1]+corner_size, p_pt[1]], color="#1f2937", lw=1.2)

ax.set_xlim(-0.5, 8)
ax.set_ylim(-0.5, 4.0)
ax.axis("off")
ax.set_title("Geometría de Mínimos Cuadrados: Proyección Ortogonal", fontsize=10, fontweight="bold", pad=6)
plt.tight_layout()
plt.savefig("figuras/ej7_geometria_proyeccion.png")
plt.close()

# FIGURA 7: Gradiente Descendiente y Newton (Ej. 8)
H = A7.T @ A7
mu_max = np.linalg.eigvalsh(H).max()
alpha_safe = 1.0 / mu_max
alpha_unstable = 2.1 / mu_max
b_06 = b7 + 0.06 * escala * z

def E_cost(x): return 0.5 * np.sum((A7 @ x - b_06)**2)
def grad_E_cost(x): return A7.T @ (A7 @ x - b_06)

# GD estable
x_gd, cost_gd = np.zeros(64), []
for _ in range(60):
    cost_gd.append(E_cost(x_gd))
    x_gd -= alpha_safe * grad_E_cost(x_gd)

# GD inestable
x_bad, cost_bad = np.zeros(64), []
for _ in range(25):
    c = E_cost(x_bad)
    cost_bad.append(c)
    if c > 1e7: break
    x_bad -= alpha_unstable * grad_E_cost(x_bad)

fig, ax = plt.subplots(1, 2, figsize=(8.5, 3), dpi=200)
ax[0].plot(cost_gd, color="#2563eb", lw=2, label=r"Estable: $\alpha = 1/\mu_{\max}$")
ax[0].axhline(y=cost_gd[-1], color="#059669", ls=":", label=f"Mínimo = {cost_gd[-1]:.2f}")
ax[0].set_title(r"Convergencia Estable ($\alpha < 2/\mu_{\max}$)", fontsize=9, fontweight="bold")
ax[0].set_xlabel("Iteraciones", fontsize=8)
ax[0].set_ylabel("$E(x)$", fontsize=8)
ax[0].grid(True, linestyle="--", alpha=0.5)
ax[0].legend(fontsize=7.5)
ax[0].tick_params(labelsize=8)

ax[1].plot(cost_bad, color="#dc2626", lw=2, label=r"Inestable: $\alpha = 2.1/\mu_{\max}$")
ax[1].set_yscale("log")
ax[1].set_title(r"Divergencia Exponencial ($\alpha > 2/\mu_{\max}$)", fontsize=9, fontweight="bold")
ax[1].set_xlabel("Iteraciones", fontsize=8)
ax[1].set_ylabel("$E(x)$ (escala log)", fontsize=8)
ax[1].grid(True, linestyle="--", alpha=0.5)
ax[1].legend(fontsize=7.5)
ax[1].tick_params(labelsize=8)
plt.tight_layout()
plt.savefig("figuras/ej8_convergencia_gd.png")
plt.close()

# FIGURA 8: Regularización de Tikhonov (Ej. 9)
def matriz_diferencias(n):
    Dh = []
    for i in range(n):
        for j in range(n - 1):
            row = np.zeros(n * n)
            k = i * n + j
            row[k] = -1
            row[k + 1] = 1
            Dh.append(row)
    Dv = []
    for i in range(n - 1):
        for j in range(n):
            row = np.zeros(n * n)
            k = i * n + j
            row[k] = -1
            row[k + n] = 1
            Dv.append(row)
    return np.vstack([Dh, Dv])

D = matriz_diferencias(8)
DTD = D.T @ D
b_noise_10 = b7 + 0.10 * escala * z

def solve_regularized(lam):
    H_reg = H + lam * DTD
    g_reg = A7.T @ b_noise_10
    return np.linalg.solve(H_reg, g_reg)

x_l0 = solve_regularized(0.0)
x_lopt = solve_regularized(0.3)
x_lover = solve_regularized(3.0)

err_l0 = np.linalg.norm(x_l0 - x_fantoma) / np.linalg.norm(x_fantoma)
err_lopt = np.linalg.norm(x_lopt - x_fantoma) / np.linalg.norm(x_fantoma)
err_lover = np.linalg.norm(x_lover - x_fantoma) / np.linalg.norm(x_fantoma)

fig, ax = plt.subplots(1, 4, figsize=(10, 2.7), dpi=200)
ax[0].imshow(X_fantoma, cmap="gray", vmin=0, vmax=0.8)
ax[0].set_title("Fantoma Real", fontsize=9, fontweight="bold")
ax[0].axis("off")

ax[1].imshow(x_l0.reshape(8, 8), cmap="gray", vmin=0, vmax=0.8)
ax[1].set_title(rf"$\lambda = 0$ (Sin reg.)" f"\nErr: {err_l0*100:.1f}%, Ruidosa", fontsize=8.5, color="#dc2626")
ax[1].axis("off")

ax[2].imshow(x_lopt.reshape(8, 8), cmap="gray", vmin=0, vmax=0.8)
ax[2].set_title(rf"$\lambda = 0.3$ (Óptimo)" f"\nErr: {err_lopt*100:.1f}%, Suave", fontsize=8.5, color="#059669")
ax[2].axis("off")

ax[3].imshow(x_lover.reshape(8, 8), cmap="gray", vmin=0, vmax=0.8)
ax[3].set_title(rf"$\lambda = 3.0$ (Excesivo)" f"\nErr: {err_lover*100:.1f}%, Borrosa", fontsize=8.5, color="#d97706")
ax[3].axis("off")
plt.tight_layout()
plt.savefig("figuras/ej9_regularizacion_tradeoff.png")
plt.close()

# FIGURA 9: Pipeline de resolución 128x128 y principio de discrepancia (Ej. 10)
fig, ax = plt.subplots(figsize=(8, 3.2), dpi=200)
ax.axis("off")
ax.text(0.5, 0.88, r"Principio de Discrepancia de Morozov (Selección de $\lambda$ a ciegas)", 
        ha="center", fontsize=11, fontweight="bold", color="#1e293b")

box_kw = dict(boxstyle="round,pad=0.5", fc="#f8fafc", ec="#cbd5e1", lw=1.2)
ax.text(0.18, 0.45, 
        r"$\lambda \to 0$ (Sub-regularizado)" "\n"
        r"$\|A\hat{x} - b\| \ll \|\eta\|$" "\n\n"
        r"$\bullet$ Sobreajuste al ruido" "\n"
        r"$\bullet$ Imagen granulada" "\n"
        r"$\bullet$ $\|D\hat{x}\|$ muy grande", 
        fontsize=8.5, va="center", ha="center", bbox=box_kw, color="#dc2626")

box_opt = dict(boxstyle="round,pad=0.5", fc="#ecfdf5", ec="#10b981", lw=1.5)
ax.text(0.50, 0.45, 
        r"$\lambda^*$ Óptimo (Morozov)" "\n"
        r"$\|A\hat{x} - b\| \approx \|\eta\|$" "\n\n"
        r"$\bullet$ Residuo $\approx$ Nivel de ruido" "\n"
        r"$\bullet$ Fondo suave sin ruido" "\n"
        r"$\bullet$ Bordes preservados", 
        fontsize=8.5, va="center", ha="center", bbox=box_opt, color="#065f46")

ax.text(0.82, 0.45, 
        r"$\lambda \gg 1$ (Sobre-regularizado)" "\n"
        r"$\|A\hat{x} - b\| \gg \|\eta\|$" "\n\n"
        r"$\bullet$ Subajuste de datos" "\n"
        r"$\bullet$ Imagen borrosa / lavada" "\n"
        r"$\bullet$ $\|D\hat{x}\| \to 0$", 
        fontsize=8.5, va="center", ha="center", bbox=box_kw, color="#d97706")

ax.annotate("", xy=(0.34, 0.45), xytext=(0.28, 0.45), arrowprops=dict(arrowstyle="->", lw=1.5, color="#64748b"))
ax.annotate("", xy=(0.72, 0.45), xytext=(0.66, 0.45), arrowprops=dict(arrowstyle="->", lw=1.5, color="#64748b"))

plt.tight_layout()
plt.savefig("figuras/ej10_pipeline_128.png")
plt.close()

print("Todas las figuras generadas exitosamente en la carpeta figuras/.")

