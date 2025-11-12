import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl

print([key for key in mpl.rcParams if "legend" in key.lower()])
# Paleta de colores Kanagawa (extraída del tema 'wave')
kanagawa_colors = {
    "fujiWhite": "#DCD7BA",
    "oldWhite": "#C8C093",
    "sumiInk0": "#16161D",
    "sumiInk1": "#1F1F28",
    "sumiInk2": "#2A2A37",
    "sumiInk3": "#363646",
    "sumiInk4": "#54546D",
    "waveBlue1": "#223249",
    "waveBlue2": "#2D4F67",
    "winterGreen": "#2B3328",
    "winterYellow": "#49443C",
    "winterRed": "#43242B",
    "winterBlue": "#252535",
    "autumnGreen": "#76946A",
    "autumnRed": "#C34043",
    "autumnYellow": "#DCA561",
    "samuraiRed": "#E82424",
    "roninYellow": "#FF9E3B",
    "waveAqua1": "#6A9589",
    "dragonBlue": "#658594",
    "fujiGray": "#727169",
    "springViolet1": "#938AA9",
    "oniViolet": "#957FB8",
    "crystalBlue": "#7E9CD8",
    "springViolet2": "#9CABCA",
    "springBlue": "#7FB4CA",
    "lightBlue": "#A3D4D5",
    "waveAqua2": "#7AA89F",
    "springGreen": "#98BB6C",
    "boatYellow1": "#938056",
    "boatYellow2": "#C0A36E",
    "carpYellow": "#E6C384",
    "sakuraPink": "#D27E99",
    "waveRed": "#E46876",
    "peachRed": "#FF5D62",
    "surimiOrange": "#FFA066",
    "katanaGray": "#717C7C",
}

# Configuración de estilo Matplotlib inspirada en Kanagawa
plt.style.use("dark_background")  # Base oscura, como Kanagawa
plt.rcParams.update(
    {
        "figure.facecolor": kanagawa_colors["sumiInk1"],  # Fondo del plot
        "axes.facecolor": kanagawa_colors["sumiInk1"],  # Fondo de ejes
        "axes.edgecolor": kanagawa_colors["sumiInk3"],  # Bordes de ejes
        "xtick.color": kanagawa_colors["fujiGray"],  # Ticks X
        "ytick.color": kanagawa_colors["fujiGray"],  # Ticks Y
        "text.color": kanagawa_colors["fujiWhite"],  # Texto general
        "axes.labelcolor": kanagawa_colors["fujiWhite"],  # Etiquetas de ejes
        "axes.titlecolor": kanagawa_colors["oniViolet"],  # Título
        "legend.facecolor": kanagawa_colors["sumiInk2"],  # Fondo de leyenda
        "legend.edgecolor": kanagawa_colors["sumiInk3"],  # Borde de leyenda
        "legend.labelcolor": kanagawa_colors["oldWhite"],  # Texto de leyenda
        "grid.color": kanagawa_colors["fujiGray"],  # Grid
        "grid.alpha": 0.5,  # Transparencia del grid
    }
)
# Data from the PT100 table (temperature, resistance pairs)
temperatures = np.array([-20, 0, 20, 60, 70])
amperes = np.array([4.00, 7.56, 11.11, 18.22, 20.00])
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(
    temperatures,
    amperes,
    color=kanagawa_colors["waveBlue2"],  # Línea en azul Kanagawa
    linewidth=2.5,
    label="Curva PT100",
)
ax.set_xlabel("Temperatura (°C)")
ax.set_ylabel("Amperaje (A)")
ax.set_title("Cambio de amperaje PT100 acondicionada vs. Temperatura")
ax.grid(True, alpha=0.3)
ax.legend()

# === CUSTOM AXIS TICKS HERE ===
# X-axis: Ticks every 100°C
ax.set_xticks([-20, -10, 0, 10, 20, 30, 40, 50, 60, 70])
ax.set_xticklabels(
    [f"{t}°C" for t in [-20, -10, 0, 10, 20, 30, 40, 50, 60, 70]]
)  # Custom labels with °C

# Y-axis: Ticks every 50 Ω
ax.set_yticks(
    [
        0,
        5,
        10,
        15,
        20,
        25,
    ]
)
ax.set_yticklabels(
    [
        f"{r} A"
        for r in [
            0,
            5,
            10,
            15,
            20,
            25,
        ]
    ]
)  # Custom labels with Ω

# Optional: Set axis limits if you want to zoom (e.g., focus on 0-400°C)
ax.set_xlim(-20, 70)
ax.set_ylim(0, 25)
# Crear el plot

# Ajustes finales para bordes suaves
for spine in ax.spines.values():
    spine.set_color(kanagawa_colors["sumiInk3"])
    spine.set_linewidth(1.5)

plt.tight_layout()

# Exportar como PDF para LaTeX
plt.savefig("pt100_plot.pdf", format="pdf", bbox_inches="tight", dpi=300)
# O para EPS: plt.savefig('pt100_plot_kanagawa.eps', format='eps', bbox_inches='tight')

plt.show()  # Muestra el plot localmente
