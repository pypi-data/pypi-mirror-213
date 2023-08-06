from typing import Optional, Union

import numpy as np
import cv2

from dna import Box, Point, BGR, Image
from dna.color import WHITE, RED


def draw_line(convas:Image, from_pt:Point, to_pt:Point, color:BGR,
                line_thickness: int=2) -> Image:
    return draw_line_raw(convas, from_pt.xy.astype(int), to_pt.xy.astype(int), color, line_thickness)

def draw_line_raw(convas:Image, from_pt, to_pt, color:BGR, line_thickness: int=2) -> Image:
    return cv2.line(convas, from_pt, to_pt, color, line_thickness, lineType=cv2.LINE_AA)

def draw_line_string_raw(convas:Image, pts:list[list[int]], color: BGR,
                            line_thickness: int=2) -> Image:
    for pt1, pt2 in zip(pts, pts[1:]):
        convas = draw_line_raw(convas, pt1, pt2, color, line_thickness)
    return convas

def draw_line_string(convas:Image, pts: list[Point], color:BGR, line_thickness: int=2) -> Image:
    return draw_line_string_raw(convas, [pt.xy.astype(int) for pt in pts], color, line_thickness)

def draw_label(convas:Image, label:str, tl:Point, color: BGR=WHITE, fill_color:BGR=RED,
                thickness: int=2, font_scale=0.4) -> Image:
    txt_thickness = max(thickness - 1, 1)
    # font_scale = thickness / 4

    txt_size = cv2.getTextSize(label, 0, fontScale=font_scale, thickness=thickness)[0]
    br = (tl.x + txt_size[0], tl.y - txt_size[1] - 3)
    convas = cv2.rectangle(convas, tuple(tl.xy), br, color=fill_color, thickness=-1, lineType=cv2.LINE_AA)  # filled
    return cv2.putText(convas, label, (tl.x, tl.y - 2), 0, font_scale, color, thickness=txt_thickness,
                        lineType=cv2.LINE_AA)
    
def draw_polygon(convas:Image, coords:list[Union[tuple[float,float],list[float]]], color, line_thickness) -> Image:
    if len(coords) > 2:
        coords = np.array(coords).astype(int)
        return cv2.polylines(convas, [coords], True, color, line_thickness, lineType=cv2.LINE_AA)
    elif len(coords) == 2:
        return cv2.line(convas, coords[0], coords[1], color, line_thickness, lineType=cv2.LINE_AA)
    else:
        return convas