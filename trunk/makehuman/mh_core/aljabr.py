#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Common 3D Algebric functions.

**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Manuel Bastioni, Marc Flerackers

**Copyright(c):**      MakeHuman Team 2001-2010

**Licensing:**         GPL3 (see also http://sites.google.com/site/makehumandocs/licensing)

**Coding Standards:**  See http://sites.google.com/site/makehumandocs/developers-guide

Abstract
--------

This module contains the most common 3D algebraic operations used in MakeHuman.
These are mostly the vector and matrix operations core to any 3D application.

The name is a tribute to \"Al-jabr wa'l muqabalah\" the most important paper of Mohammed ibn-Musa al-Khuwarizmi (VII - VIII sec d.C.)
The paper was so important that Al-jabr is the root of modern word I{algebra} and al-Khuwarizmi is the root of word I{algorithm}.

"""

__docformat__ = 'restructuredtext'

from math import sqrt, cos, sin, tan, atan2

machine_epsilon = 1.0e-16

def vsub(vect1, vect2):
    """

    This function returns the difference between two 3D vectors (vect1-vect2).
    The input parameters to this function can be 4D vectors, but only
    the first 3 dimensions are used and only a 3D vector is returned.
    This effectively returns the vector required to get from the coordinates of
    vect2 to the coordinates of vect1.

    Parameters
    ----------

    vect1:
        *float list*. The first vector - in the format [x,y,z]
        (or [x,y,z,0] for affine transformations in an homogeneous space).

    vect2:
        *float list*. The second vector [x,y,z]
        (or [x,y,z,0] for affine transformations in an homogeneous space).

    """

    return [vect1[0] - vect2[0], vect1[1] - vect2[1], vect1[2] - vect2[2]]


def vdot(vect1, vect2):
    """

    This function returns the dot (scalar) product between two 3D vectors (vect1.vect2)
    The input parameters to this function can be 4D vectors, but only
    the first 3 dimensions are used and only a 3D vector is returned.

    Parameters
    ----------

    vect1:
        *float list*. The first vector - in the format[x,y,z]
        (or [x,y,z,0] for affine transformations in an homogeneous space).

    vect2:
        *float list*. The second vector - in the format [x,y,z]
        (or [x,y,z,0] for affine transformations in an homogeneous space).
    """

    return vect1[0] * vect2[0] + vect1[1] * vect2[1] + vect1[2] * vect2[2]


def vlen(vect):
    """
    This function returns the length of a vector [x,y,z] (as a float).

    Parameters
    ----------

    vect:
        *float list*. The vector - in the format [x,y,z]
        (or [x,y,z,0] for affine transformations in an homogeneous space).

    """

    return sqrt(vect[0] * vect[0] + vect[1] * vect[1] + vect[2] * vect[2])


def vnorm(vect):
    """
    This function returns a normalized vector [x,y,z] ie a unit length
    vector pointing in the same direction as the input vector. This performs
    essentially the same function as vunit(vect) except that this function
    handles potential zero length vectors.

    Parameters
    ----------

    vect:
        *float list*. The vector - in the format [x,y,z]
        (or [x,y,z,0] for affine transformations in an homogeneous space).
    """

    length = sqrt(vect[0] * vect[0] + vect[1] * vect[1] + vect[2] * vect[2])

    # Keep the program from blowing up by providing an acceptable
    # value for vectors whose length may be calculated too close to zero.

    if length == 0.0:
        return [0.0, 0.0, 0.0]

    # Dividing each element by the length will result in a
    # unit normal vector.

    return [vect[0] / length, vect[1] / length, vect[2] / length]


def vdist(vect1, vect2):
    """
    This function returns the euclidean distance (the straight-line distance)
    between two vector coordinates.
    The distance between two points is the length of the vector joining them.

    Parameters
    ----------

    vect1:
        *float list*. The first vector - in the format[x,y,z]
        (or [x,y,z,0] for affine transformations in an homogeneous space).

    vect2:
        *float list*. The second vector - in the format [x,y,z]
        (or [x,y,z,0] for affine transformations in an homogeneous space).
    """

    joiningVect = [vect1[0] - vect2[0], vect1[1] - vect2[1], vect1[2] - vect2[2]]
    return sqrt(joiningVect[0] * joiningVect[0] + joiningVect[1] * joiningVect[1] + joiningVect[2] * joiningVect[2])


def vcross(vect1, vect2):
    """
    This function returns the cross product of two vectors.

    Parameters
    ----------

    vect1:
        *float list*. The first vector - in the format[x,y,z]
        (or [x,y,z,0] for affine transformations in an homogeneous space).

    vect2:
        *float list*. The second vector - in the format [x,y,z]
        (or [x,y,z,0] for affine transformations in an homogeneous space).
    """

    return [vect1[1] * vect2[2] - vect1[2] * vect2[1], vect1[2] * vect2[0] - vect1[0] * vect2[2], vect1[0] * vect2[1] - vect1[1] * vect2[0]]


def centroid(vertsList):
    """
    This function returns the baricenter of a set of coordinate vectors
    [[x1,y1,z1],[x2,y2,z2],...,[xn,yn,zn]], returning a coordinate vector
    formatted as a float list [float X,float Y, float Z].
    This is the sum of all of the vectors divided by the number of vectors.

    Parameters
    ----------

    vertsList:
        *float list*. List of list. Each vector is in the format [x,y,z]
        (or [x,y,z,0] for affine transformations in an homogeneous space).
    """

    nVerts = len(vertsList)
    xTot = 0.0
    yTot = 0.0
    zTot = 0.0
    for v in vertsList:
        xTot += v[0]
        yTot += v[1]
        zTot += v[2]
    if nVerts != 0:
        centrX = xTot / nVerts
        centrY = yTot / nVerts
        centrZ = zTot / nVerts
    else:
        print 'Warning: no verts to calc centroid'
        return 0
    return [centrX, centrY, centrZ]


def vadd(vect1, vect2):
    """
    This function returns the sum of two vectors as a vector.

    Parameters
    ----------

    vect1:
        *float list*. The first vector - in the format[x,y,z]
        (or [x,y,z,0] for affine transformations in an homogeneous space).

    vect2:
        *float list*. The second vector - in the format [x,y,z]
        (or [x,y,z,0] for affine transformations in an homogeneous space).
    """

    return [vect1[0] + vect2[0], vect1[1] + vect2[1], vect1[2] + vect2[2]]


def vmul(vect, s):
    """
    This function returns the result of multiplying a vector by a scalar (a float).

    Parameters
    ----------

    vect:
        *float list*. The vector - in the format[x,y,z]
        (or [x,y,z,0] for affine transformations in an homogeneous space).

    s:
        *float*. The scalar value.
    """

    return [vect[0] * s, vect[1] * s, vect[2] * s]


def vunit(vect):
    """
    This function returns a normalized vector [x,y,z] ie a unit length
    vector pointing in the same direction as the input vector. This performs
    essentially the same function as vnorm(vect) except that vnorm handles
    potential zero length vectors.

    Parameters
    ----------

    vect:
        *float list*. The vector - in the format[x,y,z]
        (or [x,y,z,0] for affine transformations in an homogeneous space).
    """

    length = sqrt(vect[0] * vect[0] + vect[1] * vect[1] + vect[2] * vect[2])
    return [vect[0] / length, vect[1] / length, vect[2] / length]


def mulmatvec3x3(m, vect):
    """
    This function returns a 3D vector which consists of the 3D input
    vector multiplied by a 3x3 matrix.

    Parameters
    ----------

    m:
        *float list*. List of list. The 3x3 matrix.

    vect:
        *float list*. The vector - in the format[x,y,z]
        (or [x,y,z,0] for affine transformations in an homogeneous space).
    """

    r = [0.0, 0.0, 0.0]
    r[0] = vect[0] * m[0][0] + vect[1] * m[1][0] + vect[2] * m[2][0]
    r[1] = vect[0] * m[0][1] + vect[1] * m[1][1] + vect[2] * m[2][1]
    r[2] = vect[0] * m[0][2] + vect[1] * m[1][2] + vect[2] * m[2][2]
    return r


def makeRotEulerMtx3D(rx, ry, rz):
    """
    This function returns a 3x3 euler rotation matrix based on the 3 angles
    rx, ry and rz.

    Parameters
    ----------

    rx:
        *float*. The angle of rotation (in radians) around the x-axis

    ry:
        *float*. The angle of rotation (in radians) around the y-axis

    rz:
        *float*. The angle of rotation (in radians) around the z-axis
    """

    SRX = sin(rx)
    SRY = sin(ry)
    SRZ = sin(rz)
    CRX = cos(rx)
    CRY = cos(ry)
    CRZ = cos(rz)

    return [[CRY * CRZ, CRY * SRZ, -SRY], [(CRZ * SRX) * SRY - CRX * SRZ, CRX * CRZ + (SRX * SRY) * SRZ, CRY * SRX], [SRX * SRZ + (CRX * CRZ) * SRY, (CRX * SRY) * SRZ
             - CRZ * SRX, CRX * CRY]]


def makeRotEulerMtx2D(theta, rotAxe):
    """
    This function returns a 3x3 euler matrix that rotates a point on
    a plane perpendicular to a specified rotational axis.

    Parameters
    ----------

    theta:
        *float*. The angle of rotation (in radians).

    rotAxe:
        *string*. The axis of rotation, which can be \"X\", \"Y\" or \"Z\".
    """

    if rotAxe == 'X':
        Rmtx = makeRotEulerMtx3D(theta, 0, 0)
    elif rotAxe == 'Y':
        Rmtx = makeRotEulerMtx3D(0, theta, 0)
    elif rotAxe == 'Z':
        Rmtx = makeRotEulerMtx3D(0, 0, theta)
    return Rmtx


def makeRotMatrix(angle, axis):
    """
    This function returns a 3x3 transformation matrix that represents a
    rotation through the specified angle around the specified axis.
    This matrix is presented in Graphics Gems (Glassner, Academic Press, 1990),
    and discussed here: http://www.gamedev.net/reference/programming/features/whyquats/

    Parameters
    ----------

    angle:
        *float*. The angle of rotation (rad) around the specified axis

    axis:
        *float list*. A 3d vector [x,y,z] defining the axis of rotation
        (this should already be normalized to avoid strange results).
    """

    a = angle
    x = axis[0]
    y = axis[1]
    z = axis[2]
    t = 1 - cos(a)
    c = cos(a)
    s = sin(a)
    M11 = (t * x) * x + c
    M12 = (t * x) * y + s * z
    M13 = (t * x) * z - s * y
    M21 = (t * x) * y - s * z
    M22 = (t * y) * y + c
    M23 = (t * y) * z + s * x
    M31 = (t * x) * z + s * y
    M32 = (t * y) * z - s * x
    M33 = (t * z) * z + c
    return [[M11, M12, M13], [M21, M22, M23], [M31, M32, M33]]


def rotatePoint(center, vect, rotMatrix):
    """
    This function returns the 3D vector coordinates of a
    vector rotated around a specified centre point using a
    3x3 rotation matrix.

    Parameters
    ----------

    center:
        *float list*. A 3D vector - in the format[x,y,z] containing the
        coordinates of the center of rotation.

    vect:
        *float list*. A 3D vector - in the format[x,y,z] containing the
        coordinates of the point to be rotated.

    rotMatrix:
        *float list of lists*. A 3x3 rotation matrix.
    """

    # subtract rotation point

    tv = vsub(vect, center)

    # rotate

    nv = mulmatvec3x3(rotMatrix, tv)

    # add the rotation point back again

    nv = vadd(nv, center)
    return nv


def scalePoint(center, vect, scale, axis=None):
    """
    This function returns the 3D vector coordinates of a
    coordinate vector scaled relative to a specified centre point using a
    scalar value.

    Parameters
    ----------

    center:
        *float list*. A 3D vector - in the format[x,y,z] containing the
        coordinates of the center point.

    vect:
        *float list*. A 3D vector - in the format[x,y,z] containing the
        coordinates of the point to be scaled.

    scale:
        *float*. Scale factor.

    axis:
        *string*. An optional axis to constrain scaling (\"X\", \"Y\", \"Z\" or None).
        If an axis is specified then no scaling takes place along that axis.
    """

    # subtract centre point

    tv = vsub(vect, center)

    # scale

    if axis == 'X':
        nv = [tv[0], tv[1] * scale, tv[2] * scale]
    elif axis == 'Y':
        nv = [tv[0] * scale, tv[1], tv[2] * scale]
    elif axis == 'Z':
        nv = [tv[0] * scale, tv[1] * scale, tv[2]]
    else:
        nv = [tv[0] * scale, tv[1] * scale, tv[2] * scale]

    # add the centre point back again

    nv = vadd(nv, center)
    return nv


def planeNorm(vect1, vect2, vect3):
    """
    This function returns the vector of the normal to a plane, where the
    plane is defined by the vector coordinates of 3 points on that plane.
    This function calculates two direction vectors eminating from
    vect2, and calculates the normalized cross product to derive
    a vector at right angles to both direction vectors.
    This function assumes that the input coordinate vectors
    do not all lie on the same straight line.

    Parameters
    ----------

    vect1:
        *float list*. A 3D vector - in the format[x,y,z] containing the
        coordinates of the first point.
        (or [x,y,z,0] for affine transformations in an homogeneous space).

    vect2:
        *float list*. A 3D vector - in the format[x,y,z] containing the
        coordinates of the second point.
        (or [x,y,z,0] for affine transformations in an homogeneous space).

    vect3:
        *float list*. A 3D vector - in the format[x,y,z] containing the
        coordinates of the third point.
        (or [x,y,z,0] for affine transformations in an homogeneous space).
    """

    # Calculate two vectors from the three points

    v1 = [vect1[0] - vect2[0], vect1[1] - vect2[1], vect1[2] - vect2[2]]
    v2 = [vect2[0] - vect3[0], vect2[1] - vect3[1], vect2[2] - vect3[2]]

    # Take the cross product

    normal = [v1[1] * v2[2] - v1[2] * v2[1], v1[2] * v2[0] - v1[0] * v2[2], v1[0] * v2[1] - v1[1] * v2[0]]

    # Normalize

    length = sqrt(normal[0] * normal[0] + normal[1] * normal[1] + normal[2] * normal[2])
    return [normal[0] / length, normal[1] / length, normal[2] / length]


def focalToFov(dimension, focal):
    if focal == 0:
        return 0
    else:
        return 2 * atan2(dimension * 0.5, focal)


def fovToFocal(dimension, fov):
    return dimension / (2 * tan(fov / 2))


def in2pts(point1, point2, t):
    """
    This function returns a vector that lies on the directed line between points, given
    a parameter t. The paraemeter t is between 0 and 1 and it parametrizes our directed line
    between point1 and point2
    

    Parameters
    ----------

    point1:
        *float list*. A 3D vector - in the format[x,y,z] containing the
        coordinates of the first point (i.e. starting point) of a directed line.

    point2:
        *float list*. A 3D vector - in the format[x,y,z] containing the
        coordinates of the second point (i.e. endpoint) of a directed line.

    t:
        *float*. A real number between 0 and 1, that linearly parametrizes
        the directed line between point1 and point2. In other words, when t is 0 the 
        return value for this function is point1 and when t is 1 the return value
        for this function is point2.
    """

    return vadd(vmul(point1, 1 - t), vmul(point2, t))

# u and m must be float 0<=m<=1
# returns : sn,cn,dn,phi
#TODO : Add reference: Louis V. King; Hofsommer; Salzer (after reading it yourself :P)
#pg. 9 eq'n 35 of Louis V. King for m within 1.0e-9 range
def jacobianEllipticFunction(u,m):
    """
    This function returns a triple consisting of the Jacobian elliptic functions, namely the
    Jacobian sine (sn), Jacobian cosine (cn), Jacobian *TODO.. dn*, angle (in radians)      

    Parameters
    ----------

    u:
        *float*. A 3D vector - in the format[x,y,z] containing the
        coordinates of the first point (i.e. starting point) of a directed line.

    k:
        *float* a value between 0 and 1 which represent the modulus of the Jacobian elliptic function

    """
    if (m< 0) or (m >1):
        print "Coefficient for Elliptic Integral should be between 1 and 0"
        return  #error-code!
    a=[0]*9
    c=[0]*9
    if m < 1.0e-9:
        t = sin(u)
        b = cos(u)
        ai = 0.25*m*(u-t*b)
        sn = t-ai*b
        cn = b+ai*t
        ph = u-ai
        dn = 1.0 - 0.5*m*t*t
        return sn,cn,dn,ph
    if m>=1.0 - 1.0e-9:
        ai = 0.25*(1.0-m)
        b = math.cosh(u)
        t= math.tanh(u)
        phi = 1.0/b
        twon = b*math.sinh(u)
        sn = t+a*(twon-u)/(b*b)
        ph = 2.0*math.atan(math.exp(u))-math.pi/2+ai*(twon-u)/b
        ai=ai*t*phi
        cn = phi - ai*(twon-u)
        dn=phi+ai*(twon+u)
        return sn,cn,dn,ph
        
    a[0] = 1.0;
    b=math.sqrt(1.0-m)
    c[0]=math.sqrt(m)
    twon=1.0
    i=0
    
    while math.fabs(c[i]/a[i])>machine_epsilon:
        if i>7:
            print "Overflow in the calculation of Jacobian elliptic functions"
            break
        ai = a[i]
        i=i+1
        c[i]=0.5*(ai-b)
        t=sqrt(ai*b)
        a[i]=0.5*(ai+b)
        b=t
        twon=twon*2.0

    phi=twon*a[i]*u
    while i!=0:
        t=c[i]*sin(phi)/a[i]
        b=phi
        phi=(math.asin(t)+phi)/2.0
        i=i-1            
    return sin(phi),cn,cn/cos(phi-b),phi

def axisAngleToQuaternion(axis, angle):
    s = sin(angle/2.0)
    qx = axis[0] * s
    qy = axis[1] * s
    qz = axis[2] * s
    qw = cos(angle/2.0)
    return (qx, qy, qz, qw)
