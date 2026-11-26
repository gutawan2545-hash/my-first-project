"""One-point perspective camera for Odd Hours scenes (540x960 frame).

World units are metres: X right, Y up, Z away from the camera. Everything in a scene goes
through the same camera, so objects sit on the ground, shrink with distance and share one
horizon. Faces parallel to the frame (front faces) are plain rectangles on screen, so signs,
shelves and windows on them can be drawn flat with face() and stay correct.
"""


class Cam:
    def __init__(self, horizon=380, f=560, h=1.6, cx=270, ox=0.0):
        self.hz, self.f, self.h, self.cx, self.ox = horizon, f, h, cx, ox

    def p(self, X, Y, Z):
        return (self.cx + self.f * (X - self.ox) / Z, self.hz - self.f * (Y - self.h) / Z)

    def ppm(self, Z):
        """pixels per metre at depth Z"""
        return self.f / Z

    def path(self, pts):
        return 'M ' + ' L '.join(f'{x:.1f},{y:.1f}' for x, y in (self.p(*q) for q in pts)) + ' Z'

    def poly(self, pts, fill, extra=''):
        return f'<path d="{self.path(pts)}" fill="{fill}" {extra}/>'

    def line(self, a, b, stroke, w=1.0, extra=''):
        (x0, y0), (x1, y1) = self.p(*a), self.p(*b)
        return f'<path d="M {x0:.1f},{y0:.1f} L {x1:.1f},{y1:.1f}" stroke="{stroke}" stroke-width="{w}" {extra}/>'

    def box(self, x0, x1, y0, y1, z0, z1, front, side, top, side_dark=None):
        """Cuboid with block shading. Draws only the faces the camera can see."""
        out = ''
        if y1 < self.h:                                   # top visible from above
            out += self.poly([(x0, y1, z0), (x1, y1, z0), (x1, y1, z1), (x0, y1, z1)], top)
        elif y0 > self.h:                                 # underside visible from below
            out += self.poly([(x0, y0, z0), (x1, y0, z0), (x1, y0, z1), (x0, y0, z1)], side_dark or side)
        if x0 > self.ox:                                        # left side faces the camera
            out += self.poly([(x0, y0, z0), (x0, y0, z1), (x0, y1, z1), (x0, y1, z0)], side)
        if x1 < self.ox:                                        # right side faces the camera
            out += self.poly([(x1, y0, z0), (x1, y0, z1), (x1, y1, z1), (x1, y1, z0)], side_dark or side)
        out += self.poly([(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0)], front)
        return out

    def face(self, x0, y1, z, content):
        """Draw content on a front face. Content is in centimetres, origin at the face's top-left, y down."""
        sx, sy = self.p(x0, y1, z)
        return f'<g transform="translate({sx:.1f},{sy:.1f}) scale({self.ppm(z) / 100:.4f})">{content}</g>'

    def sprite(self, X, Y, Z, content, units_per_m):
        """Place a 2D prop drawn around its base point (0,0) at world position, scaled by distance."""
        sx, sy = self.p(X, Y, Z)
        return f'<g transform="translate({sx:.1f},{sy:.1f}) scale({self.ppm(Z) / units_per_m:.4f})">{content}</g>'

    def char_transform(self, X, Z, Y=0.0, height_m=1.75, body_units=560, feet_units=490):
        """translate/scale for an Odd Hours character (head origin, feet at y=490, ~560 units tall)."""
        s = self.ppm(Z) * height_m / body_units
        x, y = self.p(X, Y, Z)
        return x, y - feet_units * s, s
