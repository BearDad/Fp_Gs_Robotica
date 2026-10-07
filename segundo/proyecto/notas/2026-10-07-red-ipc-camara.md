# 2026-10-07 — Red del portátil, IPC Robot Pick AI y cámara Femto Mega

Sesión de diagnóstico de la instalación PickAI desde el portátil (Arch, systemd-networkd).

## 1. Ethernet solo para LAN, internet por WiFi

El router de la instalación (192.168.1.1) no tiene internet. Con la config por defecto de
systemd-networkd la ethernet (métrica 100) le quitaba la ruta por defecto al WiFi (métrica 600).

Drop-in `/etc/systemd/network/20-ethernet.network.d/50-lan-only.conf`:

```ini
[DHCPv4]
UseGateway=no
UseRoutes=no
UseDNS=no

[IPv6AcceptRA]
UseGateway=no
UseDNS=no
```

Así la ethernet coge IP por DHCP pero ignora gateway y DNS: la LAN va por cable y todo lo
demás por WiFi. No afecta al WiFi. Pega: con esto activo, el cable nunca da internet.

Función de fish `ethlan` (`~/dotfiles/fish/.config/fish/functions/ethlan.fish`):

```fish
ethlan on      # crea el drop-in (solo LAN)
ethlan off     # lo borra (ethernet normal)
ethlan         # estado
```

Para hablar con la red de la instalación (192.168.15.x) hace falta una IP extra temporal:

```fish
sudo ip addr add 192.168.15.50/24 dev enp2s0
sudo ip addr del 192.168.15.50/24 dev enp2s0   # quitarla
```

## 2. Equipos encontrados

Red del router (192.168.1.0/24):

| IP | MAC | Equipo |
|---|---|---|
| 192.168.1.1 | d0:0e:d9:44:d0:d6 | router (SSH, Telnet, HTTP/S abiertos) |
| 192.168.1.33 | 40:c2:ba:5d:8e:81 | portátil (DHCP) |
| 192.168.1.34 | 30:2f:1e:78:81:44 | IPC SIMATIC BX-59A, web "SIMATIC Robot Pick AI" (22, 80) |

Red de la instalación según los apuntes (`RobotPick_Ai_Apuntes_CC_Zigiluak_2_MarcaAgua.pdf`, apdo. 2):

| Equipo | IP |
|---|---|
| Cámara Orbbec Femto Mega | 192.168.15.41 |
| IPC SIMATIC BX-59A | 192.168.15.19 |
| PLC 1516-3 PN/DP V2.9 | 192.168.15.10 |
| UR3e | 192.168.15.20 |

Las credenciales del IPC están en los apuntes (no las pongo aquí, repo público).
**No valen para SSH** (`Permission denied`); serán las de la sesión local del IPC.
La web de Robot Pick AI no tiene login.

Método de búsqueda: barrido de ping por la subred (fuerza ARP, así salen también los equipos
que bloquean ICMP) y `ping -6 ff02::1%enp2s0` para ver cualquier equipo del segmento
independientemente de su IPv4.

## 3. API de Robot Pick AI

La web (React) habla con un backend en el puerto **9080**. Endpoints útiles sin auth:

```fish
curl http://192.168.1.34:9080/api/v1/status
curl http://192.168.1.34:9080/api/v1/camera/info
curl http://192.168.1.34:9080/api/v1/version-info
```

- `status` → `cameraStatus: 1` (desconectada), `plcStatus: 0`, `licenseStatus: 2`.
- Mapeo de la UI: `0 = connected`, `1 = disconnected`. El PLC aparece como *connected* aunque
  no está conectado a nada: no fiarse de ese indicador.
- `camera/info` → `Camera initialization failed` (init_failure, user_resolvable).
- Versiones: computationalNn 0.7.3, fgBackend 2.0.0-Sprint87-rc3.
- `licenseStatus: 2` sin investigar.

## 4. Cámara Orbbec Femto Mega

- Serie **CL2H8410049**, MAC Ethernet **48:B0:2D:9B:3D:1D**, firmware 1.2.9.
- Conectada por USB al portátil sale como **USB 2.1** (cable/puerto): ancho de banda limitado.
- El cable Ethernet de la cámara funciona; no salía en los barridos porque estaba en otra subred.

**Problema encontrado:** la cámara tenía IP fija **192.168.15.20**, la misma que el UR3e
(conflicto) y distinta de la .41 que espera el IPC.

**Cambio hecho** (por USB con pyorbbecsdk, `Device.set_ip_config` + `reboot`):

```
192.168.15.20 → 192.168.15.41 / 255.255.255.0, gw 192.168.15.1, DHCP off
```

Verificado después del reinicio: responde a ping en 192.168.15.41.

Pendiente: los apuntes tienen más parámetros de la cámara que espera el IPC (en una captura
del OrbbecViewer); no están comprobados.

## 5. Estado del IPC y puertos

- El cable del IPC se movió de puerto: en el nuevo **no hay link** (sin luces en el router) y
  el IPC deja de verse en 192.168.1.34 y tampoco aparece en 192.168.15.19 ni por IPv6.
- El puerto **X4** tenía luces sin cable: probablemente es la interfaz activa/configurada.
- Siguiente paso: pantalla y teclado en el IPC, entrar con el usuario de los apuntes y:

```bash
ip -br addr                     # qué puerto tiene 192.168.15.19
ip -br link                     # UP/DOWN/NO-CARRIER
sudo ethtool -p <interfaz> 10   # parpadea el LED del puerto
sudo ip link set <interfaz> up  # si está desactivada
sudo docker ps                  # contenedores de Robot Pick AI
```

Objetivo: cámara (.41), IPC (.19), PLC (.10) y UR (.20) en el mismo switch de la 192.168.15.x.

## 6. Visor de la cámara en el portátil

SDK: `pyorbbecsdk2` 2.1.2 (wheel Linux de GitHub, el de PyPI solo trae macOS) en un venv de
Python 3.11 (no hay wheel para 3.14):

```fish
python3.11 -m venv /tmp/obenv/.venv
gh release download v2.1.2 -R orbbec/pyorbbecsdk -p 'pyorbbecsdk2-2.1.2-cp311-cp311-manylinux_2_27_x86_64.whl' -D /tmp/obenv/dl
/tmp/obenv/.venv/bin/pip install /tmp/obenv/dl/*.whl opencv-python numpy
```

Visor: `femto_view.py` (en esta carpeta). Color, profundidad, IR y alineado depth→color.

```fish
set py /tmp/obenv/.venv/bin/python
$py -I femto_view.py --list
$py -I femto_view.py --color 1280x720@15 --depth 640x576@15 --ir
$py -I femto_view.py --align --max-mm 1500
$py -I femto_view.py --net          # por Ethernet (necesita IP 192.168.15.x)
```

Teclas: `a` alinear, `i` IR, `+`/`-` escala de profundidad, `s` captura, `q`/`Esc` salir.
Profundidad: 640x576 = NFOV, 512x512 / 1024x1024 = WFOV. En Hyprland lanzar con
`QT_QPA_PLATFORM=xcb`.

Prueba: color, depth, IR y alineado llegan bien a 1280x720@15 + 640x576@15 (~972 mm al centro).

Nota: `/tmp/obenv` se borra al reiniciar; hay que reinstalarlo con los comandos de arriba.
