from typing import Any, Dict, Iterable, Optional, Tuple

from pp.cell import cell
from pp.component import Component
from pp.components.compass import compass
from pp.layers import LAYER
from pp.types import ComponentOrFactory, Layer


@cell
def pad(
    width: float = 100.0, height: float = 100.0, layer: Layer = LAYER.M3
) -> Component:
    """rectangular pad with 4 ports (N, S, E, W)

    Args:
        width: pad width
        height: pad height
        layer: pad layer

    """
    c = Component()
    _c = compass(size=(width, height), layer=layer).ref()
    c.add(_c)
    c.absorb(_c)
    c.ports = _c.ports
    return c


@cell
def pad_array(
    pad: ComponentOrFactory = pad,
    pitch: float = 150.0,
    n: int = 6,
    port_list: Iterable[str] = ("N",),
    pad_settings: Optional[Dict[str, Any]] = None,
    **port_settings,
) -> Component:
    """Returns 1D array of rectangular pads

    Args:
        pad: pad element
        pitch: x spacing
        n: number of pads
        port_list: list of port orientations (N, S, W, E) per pad
        pad_settings: settings for pad if pad is callable
        **port_settings
    """
    c = Component()
    pad_settings = pad_settings or {}
    pad = pad(**pad_settings) if callable(pad) else pad

    for i in range(n):
        p = c << pad
        p.x = i * pitch
        for port_name in port_list:
            port_name_new = f"{port_name}{i}"
            c.add_port(port=p.ports[port_name], name=port_name_new, **port_settings)

    return c


@cell
def pad_array_2d(
    pad: ComponentOrFactory = pad,
    pitchx: float = 150.0,
    pitchy: float = 150.0,
    ncols: int = 3,
    nrows: int = 3,
    port_list: Tuple[str, ...] = ("N",),
    pad_settings: Optional[Dict[str, Any]] = None,
    **port_settings,
) -> Component:
    """Returns 2D array of rectangular pads

    Args:
        pad: pad element
        pitchx: x spacing
        pitchy: x spacing
        ncols: number of cols
        nrows: number of rows
        port_list: list of port orientations (N, S, W, E) per pad
        pad_settings: settings for pad if pad is callable
        **port_settings
    """
    c = Component()
    pad_settings = pad_settings or {}
    pad = pad(**pad_settings) if callable(pad) else pad

    for j in range(nrows):
        for i in range(ncols):
            p = c << pad
            p.x = i * pitchx
            p.y = j * pitchy
            for port_name in port_list:
                port_name_new = f"{port_name}_{j}_{i}"
                c.add_port(port=p.ports[port_name], name=port_name_new, **port_settings)

    return c


if __name__ == "__main__":

    # c = pad()
    # print(c.ports)
    # c = pad(width=10, height=10)
    # print(c.ports.keys())
    # print(c.settings['spacing'])
    # c = pad_array()
    c = pad_array_2d(ncols=2, nrows=3, port_list=("E",), pad_settings=dict(width=80))
    c.show(show_ports=True)
