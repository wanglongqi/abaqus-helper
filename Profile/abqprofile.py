# -*- coding: utf-8 -*-
"""
Created on Thu Sep 29 19:34:05 2016

@author: Longqi
"""
from sympy import Polygon, Point
import sympy


def second_moments(self):
    """The second moments of area of the polygon.

    Returns
    =======

    Ix, Iy, Ixy : Second moments of area

    Examples
    ========

    >>> from sympy import Point, Polygon, S
    >>> from numpy import arange
    >>> p=[(cos(i),sin(i)) for i in arange(6)/S.One/3*pi]
    >>> poly = Polygon(*p)
    >>> second_moments(poly)
        (5*sqrt(3)/16, 5*sqrt(3)/16, 0)

    """
    xc, yc = self.centroid.args
    Ix, Iy, Ixy = 0, 0, 0
    args = self.args
    for i in xrange(len(args)):
        x1, y1 = args[i - 1].args
        x2, y2 = args[i].args
        x1 -= xc
        x2 -= xc
        y1 -= yc
        y2 -= yc
        v = x1 * y2 - x2 * y1
        Ix += v * (y1 * y1 + y1 * y2 + y2 * y2)
        Iy += v * (x1 * x1 + x1 * x2 + x2 * x2)
        Ixy += v * (x1 * y2 + 2 * x1 * y1 + 2 * x2 * y2 + x2 * y1)
    Ix /= 12
    Iy /= 12
    Ixy /= 24
    return sympy.Point(Ix, Iy, Ixy)


class Profile(object):
    """Summary
    Base class for profile calculation.
    """

    def __init__(self):
        """Summary
        Dummy constructor
        """
        pass

    @property
    def area(self):
        """Summary

        Returns
        -------
        Rational
            area of the profile
        """
        if isinstance(self.inner, type(None)):
            return self.outter.area
        else:
            return self.outter.area - self.inner.area

    @property
    def centroid(self):
        """Summary

        Returns
        -------
        Point2D
            Centroid of the profile
        """
        if isinstance(self.inner, type(None)):
            return self.outter.centroid
        else:
            return (self.outter.area * self.outter.centroid - self.inner.area * self.inner.centroid) /\
                (self.outter.area - self.inner.area)

    @property
    def second_moments(self):
        """Summary

        Returns
        -------
        Point
            second moments of area of the profile
        """
        if isinstance(self.inner, type(None)):
            return second_moments(self.outter)
        else:
            return second_moments(self.outter) - second_moments(self.inner) +\
                self.outter.area * self.outter.centroid.distance(self.centroid)**2 -\
                self.inner.area * \
                self.inner.centroid.distance(self.centroid)**2

    def farea(self, prec=16):
        """Summary

        Parameters
        ----------
        prec : int, optional
            required precision to obtain

        Returns
        -------
        TYPE
            area in floating number
        """
        return sympy.Rational.evalf(self.area, prec)

    def fcentroid(self, prec=16):
        """Summary

        Parameters
        ----------
        prec : int, optional
            required precision to obtain

        Returns
        -------
        TYPE
            centroid in floating number
        """
        return map(lambda x: sympy.Rational.evalf(x, prec), self.centroid)

    def fsecond_moments(self, prec=16):
        """Summary

        Parameters
        ----------
        prec : int, optional
            required precision to obtain

        Returns
        -------
        TYPE
            second moments of area in floating number
        """
        return map(lambda x: sympy.Rational.evalf(x, prec), self.second_moments)


class BoxProfile(Profile):
    """Summary
    ------------
    Contructed using the same dimensions as in Abaqus BoxProfile

    `BoxProfile(a, b, t1, t2, t3, t4)`

    """

    def __init__(self, a, b, t1, t2, t3, t4):
        self.outter = Polygon(*map(Point, ((0, 0), (a, 0), (a, b), (0, b))))
        self.inner = Polygon(
            *map(Point, ((t3, t4), (a - t1, t4), (a - t1, b - t2), (t3, b - t2))))


class IProfile(Profile):
    """Summary
    ------------
    Contructed using the same dimensions as in Abaqus IProfile

    `IProfile(l, h, b1, b2, t1, t2, t3)`

    """

    def __init__(self, l, h, b1, b2, t1, t2, t3):

        self.outter = Polygon(*map(Point, ((0, 0), (b1, 0), (b1, t1), (b1 / 2 + t3 / 2, t1), (b1 / 2 + t3 / 2, h - t2),
                                           (b1 / 2 + b2 / 2, h - t2), (b1 / 2 + b2 / 2,
                                                                       h), (b1 / 2 - b2 / 2, h), (b1 / 2 - b2 / 2, h - t2),
                                           (b1 / 2 - t3 / 2, h - t2), (b1 / 2 - t3 / 2, t1), (0, t1))))
        self.inner = None


class CircularProfile(Profile):
    """Summary
    ------------
    Contructed using the same dimensions as in Abaqus CircularProfile

    `CircularProfile(r)`

    """

    def __init__(self, r):
        self.outter = r
        self.inner = None
        self.area = sympy.pi * r * r
        self.centroid = Point((r, r))
        self.second_moments = Point(
            sympy.pi * r**4 / 4, sympy.pi * r**4 / 4, 0)


class PipeProfile(Profile):
    """Summary
    ------------
    Contructed using the same dimensions as in Abaqus PipeProfile

    `PipeProfile(r, t)`

    """

    def __init__(self, r, t):
        self.outter = r
        self.inner = t
        self.area = sympy.pi * (r * r - (r - t)**2)
        self.centroid = Point((r, r))
        self.second_moments = Point(
            sympy.pi * (r**4 - (r - t)**4) / 4, sympy.pi * (r**4 - (r - t)**4) / 4, 0)


class HexagonalProflie(Profile):
    """Summary
    ------------
    Contructed using the same dimensions as in Abaqus HexagonalProfile

    `HexagonalProfile(d, t)`

    """

    def __init__(self, d, t):
        sqrt3 = sympy.sqrt(3)
        lp = (-d, -sqrt3 * d / 2)
        self.outter = Polygon(*map(Point, ((-d, 0), (-d / 2, -sqrt3 * d / 2), (d / 2, -sqrt3 * d / 2),
                                           (d / 2, sqrt3 * d / 2), (d, 0), (-d / 2, sqrt3 * d / 2)))).translate(
            x=-lp[0], y=-lp[1])
        d -= t * 2 / sqrt3
        self.inner = Polygon(*map(Point, ((-d, 0), (-d / 2, -sqrt3 * d / 2), (d / 2, -sqrt3 * d / 2),
                                          (d / 2, sqrt3 * d / 2), (d, 0), (-d / 2, sqrt3 * d / 2)))).translate(
            x=-lp[0], y=-lp[1])


class LProfile(Profile):
    """Summary
    ------------
    Contructed using the same dimensions as in Abaqus LProfile

    `LProfile(a, b, t1, t2)`

    """

    def __init__(self, a, b, t1, t2):
        self.outter = Polygon(
            *map(Point, ((0, 0), (a, 0), (a, t1), (t2, t1), (t2, b), (0, b))))
        self.inner = None


class RectangleProfile(Profile):
    """Summary
    ------------
    Contructed using the same dimensions as in Abaqus RectangleProfile

    `RectangleProfile(a, b)`

    """

    def __init__(self, a, b):

        self.outter = Polygon(*map(Point, ((0, 0), (a, 0), (a, b), (0, b))))
        self.inner = None


class TrapezoidalProfile(Profile):
    """Summary
    ------------
    Contructed using the same dimensions as in Abaqus TrapezoidalProfile

    `TrapezoidalProfile(a, b, c, d)`

    """

    def __init__(self, a, b, c, d):

        self.outter = Polygon(
            *map(Point, ((0, 0), (a, 0), (a / 2 + c / 2, b), (a / 2 - c / 2, b))))
        self.inner = None


class CProfile(Profile):
    """Summary
    ------------
    Contructed using the dimensions as in the profile defination drawing in the project

    `CProfile(h, b1, b2, t1, t2, t3)`

    """

    def __init__(self, h, b1, b2, t1, t2, t3):
        self.outter = Polygon(*map(Point, ((0, 0), (b1, 0), (b1, h), (b1 - b2, h),
                                           (b1 - b2, h - t2), (b1 - t3, h - t2), (b1 - t3, t1), (0, t1))))
        self.inner = None
