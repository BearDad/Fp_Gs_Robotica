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
        "grid.alpha": 0.3,  # Transparencia del grid
    }
)
# Data from the PT100 table (temperature, resistance pairs)
temperatures = np.array(
    [
        -100,
        -90,
        -80,
        -70,
        -60,
        -50,
        -40,
        -30,
        -20,
        -10,
        0,
        10,
        20,
        30,
        40,
        50,
        60,
        70,
        80,
        90,
        100,
        110,
        120,
        130,
        140,
        150,
        160,
        170,
        180,
        190,
        200,
        210,
        220,
        230,
        240,
        250,
        260,
        270,
        280,
        290,
        300,
        310,
        320,
        330,
        340,
        350,
        360,
        370,
        380,
        390,
        400,
        410,
        420,
        430,
        440,
        450,
        460,
        470,
        480,
        490,
        500,
        510,
        520,
        530,
        540,
        550,
        560,
        570,
        580,
        590,
        600,
        610,
        620,
        630,
        640,
        650,
        660,
        670,
        680,
        690,
        700,
        710,
        720,
        730,
        740,
        750,
        760,
        770,
        780,
        790,
        800,
    ]
)
resistances = np.array(
    [
        60.26,
        64.30,
        68.33,
        72.33,
        76.33,
        80.31,
        84.27,
        88.22,
        92.16,
        96.09,
        100.00,
        103.90,
        107.79,
        111.67,
        115.54,
        119.40,
        123.24,
        127.08,
        130.90,
        134.71,
        138.51,
        142.29,
        146.07,
        149.83,
        153.58,
        157.33,
        161.05,
        164.77,
        168.48,
        172.17,
        175.86,
        179.53,
        183.19,
        186.84,
        190.47,
        194.10,
        197.71,
        201.31,
        204.90,
        208.48,
        212.05,
        215.61,
        219.15,
        222.68,
        226.21,
        229.72,
        233.21,
        236.70,
        240.18,
        243.64,
        247.09,
        250.53,
        253.96,
        257.38,
        260.78,
        264.18,
        267.56,
        270.93,
        274.29,
        277.64,
        280.98,
        284.30,
        287.62,
        290.92,
        294.21,
        297.49,
        300.75,
        304.01,
        307.25,
        310.49,
        313.71,
        316.92,
        320.12,
        323.30,
        326.48,
        329.64,
        332.79,
        335.93,
        339.06,
        342.18,
        345.28,
        348.38,
        351.46,
        354.53,
        357.59,
        360.64,
        363.67,
        366.70,
        369.71,
        372.71,
        375.70,
    ]
)
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(
    temperatures,
    resistances,
    color=kanagawa_colors["waveBlue2"],  # Línea en azul Kanagawa
    linewidth=2.5,
    label="Curva PT100",
)
ax.set_xlabel("Temperatura (°C)")
ax.set_ylabel("Resistencia (Ω)")
ax.set_title("Resistencia PT100 vs. Temperatura")
ax.grid(True, alpha=0.3)
ax.legend()

# === CUSTOM AXIS TICKS HERE ===
# X-axis: Ticks every 100°C
ax.set_xticks(
    [
        -100,
        -50,
        0,
        50,
        100,
        150,
        200,
        250,
        300,
        350,
        400,
        450,
        500,
        550,
        600,
        650,
        700,
        750,
        800,
    ]
)
ax.set_xticklabels(
    [
        f"{t}°C"
        for t in [
            -100,
            -50,
            0,
            50,
            100,
            150,
            200,
            250,
            300,
            350,
            400,
            450,
            500,
            550,
            600,
            650,
            700,
            750,
            800,
        ]
    ]
)  # Custom labels with °C

# Y-axis: Ticks every 50 Ω
ax.set_yticks([50, 75, 100, 125, 150, 175, 200, 225, 250, 275, 300, 325, 350, 375, 400])
ax.set_yticklabels(
    [
        f"{r} Ω"
        for r in [
            50,
            75,
            100,
            125,
            150,
            175,
            200,
            225,
            250,
            275,
            300,
            325,
            350,
            375,
            400,
        ]
    ]
)  # Custom labels with Ω

# Optional: Set axis limits if you want to zoom (e.g., focus on 0-400°C)
ax.set_xlim(-100, 800)
ax.set_ylim(50, 400)
# Crear el plot

# Ajustes finales para bordes suaves
for spine in ax.spines.values():
    spine.set_color(kanagawa_colors["sumiInk3"])
    spine.set_linewidth(1.5)

plt.tight_layout()

# Exportar como PDF para LaTeX
plt.savefig("pt100_plot_kanagawa.pdf", format="pdf", bbox_inches="tight", dpi=300)
# O para EPS: plt.savefig('pt100_plot_kanagawa.eps', format='eps', bbox_inches='tight')

plt.show()  # Muestra el plot localmente
