"""Visor Femto Mega: color, profundidad, IR y alineado.

Uso:
  view.py [--color 1920x1080@30] [--depth 640x576@30] [--ir] [--align]
          [--max-mm 3000] [--net] [--list]

Teclas: q/Esc salir, a alinear on/off, i IR on/off (si se arrancó con --ir),
        +/- rango de profundidad, s guardar captura en /tmp/obview/.
"""
import argparse
import time

import cv2
import numpy as np
import pyorbbecsdk as ob

SENSORS = {
    "color": ob.OBSensorType.COLOR_SENSOR,
    "depth": ob.OBSensorType.DEPTH_SENSOR,
    "ir": ob.OBSensorType.IR_SENSOR,
}


def parse_mode(s):
    res, fps = s.split("@") if "@" in s else (s, "30")
    w, h = res.lower().split("x")
    return int(w), int(h), int(fps)


def pick_profile(pipe, sensor, mode, fmt):
    pl = pipe.get_stream_profile_list(sensor)
    if mode is None:
        return pl.get_default_video_stream_profile()
    w, h, fps = mode
    return pl.get_video_stream_profile(w, h, fmt, fps)


def list_profiles(pipe):
    for name, sensor in SENSORS.items():
        pl = pipe.get_stream_profile_list(sensor)
        modes = set()
        for i in range(pl.get_count()):
            v = pl.get_stream_profile_by_index(i).as_video_stream_profile()
            if name == "color" and v.get_format() != ob.OBFormat.MJPG:
                continue
            modes.add((v.get_width(), v.get_height(), v.get_fps()))
        print(f"{name}:", ", ".join(f"{w}x{h}@{f}" for w, h, f in sorted(modes)))


def color_img(f):
    data = np.asanyarray(f.get_data())
    w, h, fmt = f.get_width(), f.get_height(), f.get_format()
    if fmt == ob.OBFormat.MJPG:
        return cv2.imdecode(data, cv2.IMREAD_COLOR)
    if fmt == ob.OBFormat.RGB:
        return cv2.cvtColor(data.reshape(h, w, 3), cv2.COLOR_RGB2BGR)
    if fmt == ob.OBFormat.BGR:
        return data.reshape(h, w, 3)
    if fmt == ob.OBFormat.YUYV:
        return cv2.cvtColor(data.reshape(h, w, 2), cv2.COLOR_YUV2BGR_YUYV)
    return None


def depth_mm(f):
    d = np.frombuffer(f.get_data(), dtype=np.uint16).reshape(f.get_height(), f.get_width())
    return d.astype(np.float32) * f.get_depth_scale()


def depth_colormap(mm, max_mm):
    d8 = (np.clip(mm, 0, max_mm) / max_mm * 255).astype(np.uint8)
    img = cv2.applyColorMap(d8, cv2.COLORMAP_JET)
    img[mm == 0] = 0
    return img


def ir_img(f):
    ir = np.frombuffer(f.get_data(), dtype=np.uint16).reshape(f.get_height(), f.get_width())
    return cv2.normalize(ir, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)


def fit(img, max_w=1280):
    h, w = img.shape[:2]
    return img if w <= max_w else cv2.resize(img, (max_w, int(h * max_w / w)))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--color", type=parse_mode, help="WxH@fps (MJPG)")
    ap.add_argument("--depth", type=parse_mode, help="WxH@fps (640x576 = NFOV, 512x512/1024x1024 = WFOV)")
    ap.add_argument("--ir", action="store_true", help="mostrar infrarrojos")
    ap.add_argument("--align", action="store_true", help="arrancar con la profundidad alineada sobre el color")
    ap.add_argument("--max-mm", type=int, default=3000, help="fondo de escala de la profundidad")
    ap.add_argument("--net", action="store_true", help="usar la cámara por Ethernet en vez de USB")
    ap.add_argument("--list", action="store_true", help="listar modos disponibles y salir")
    args = ap.parse_args()

    ctx = ob.Context()
    dl = ctx.query_devices()
    want = "Ethernet" if args.net else "USB"
    idx = [k for k in range(dl.get_count()) if dl.get_device_connection_type_by_index(k).startswith(want)]
    if not idx:
        raise SystemExit(f"No hay ninguna Femto Mega por {want}")
    dev = dl.get_device_by_index(idx[0])
    info = dev.get_device_info()
    print(f"{info.get_name()} {info.get_serial_number()} ({info.get_connection_type()})")

    pipe = ob.Pipeline(dev)
    if args.list:
        list_profiles(pipe)
        return

    cfg = ob.Config()
    cfg.enable_stream(pick_profile(pipe, SENSORS["color"], args.color, ob.OBFormat.MJPG))
    cfg.enable_stream(pick_profile(pipe, SENSORS["depth"], args.depth, ob.OBFormat.Y16))
    if args.ir:
        cfg.enable_stream(pick_profile(pipe, SENSORS["ir"], args.depth, ob.OBFormat.Y16))
    pipe.enable_frame_sync()
    pipe.start(cfg)

    align = ob.AlignFilter(align_to_stream=ob.OBStreamType.COLOR_STREAM)
    aligned, show_ir, max_mm = args.align, args.ir, args.max_mm
    last = {}
    t0, n, fps = time.time(), 0, 0.0

    try:
        while True:
            fs = pipe.wait_for_frames(200)
            if fs is None:
                if cv2.waitKey(1) & 0xFF in (ord("q"), 27):
                    break
                continue

            n += 1
            if time.time() - t0 >= 1:
                fps, n, t0 = n / (time.time() - t0), 0, time.time()

            c = fs.get_color_frame()
            color = color_img(c) if c is not None else None

            if aligned and color is not None:
                af = align.process(fs)
                d = af.as_frame_set().get_depth_frame() if af is not None else None
            else:
                d = fs.get_depth_frame()

            if color is not None:
                if aligned and d is not None:
                    dm = depth_colormap(depth_mm(d), max_mm)
                    if dm.shape[:2] == color.shape[:2]:
                        color = cv2.addWeighted(color, 0.6, dm, 0.4, 0)
                cv2.putText(color, f"{fps:.1f} fps  align={'on' if aligned else 'off'}",
                            (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
                last["color"] = color
                cv2.imshow("Femto Mega - color", fit(color))

            if d is not None and not aligned:
                mm = depth_mm(d)
                dm = depth_colormap(mm, max_mm)
                h, w = mm.shape
                center = mm[h // 2, w // 2]
                cv2.drawMarker(dm, (w // 2, h // 2), (255, 255, 255), cv2.MARKER_CROSS, 20, 2)
                cv2.putText(dm, f"centro: {center:.0f} mm  escala: 0-{max_mm} mm",
                            (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                last["depth"] = dm
                cv2.imshow("Femto Mega - depth", fit(dm))

            if show_ir:
                irf = fs.get_ir_frame()
                if irf is not None:
                    last["ir"] = ir_img(irf)
                    cv2.imshow("Femto Mega - IR", fit(last["ir"]))

            k = cv2.waitKey(1) & 0xFF
            if k in (ord("q"), 27):
                break
            if k == ord("a"):
                aligned = not aligned
                if aligned:
                    cv2.destroyWindow("Femto Mega - depth")
            elif k == ord("i") and args.ir:
                show_ir = not show_ir
                if not show_ir:
                    cv2.destroyWindow("Femto Mega - IR")
            elif k in (ord("+"), ord("=")):
                max_mm += 500
            elif k == ord("-"):
                max_mm = max(500, max_mm - 500)
            elif k == ord("s"):
                ts = time.strftime("%Y%m%d-%H%M%S")
                for name, img in last.items():
                    path = f"/tmp/obview/{ts}-{name}.png"
                    cv2.imwrite(path, img)
                    print("guardado", path)
    finally:
        pipe.stop()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
