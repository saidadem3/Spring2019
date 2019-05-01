# Adem, Said
# saa3053
# 2019-16-04

#----------------------------------------------------------------------
# This code was originally created by Prof. Farhad Kamangar.
# It has been significantly modified and updated by Brian A. Dalio for
# use in CSE 4303 / CSE 5365 in the 2018 Fall semester.

#----------------------------------------------------------------------
from CohenSutherland import clipLine
import numpy

def drawTriangle (self, canvas, v1, v2, v3, portal, doClip):
    if doClip:
      for  ( vax, vay, _ ), (vbx, vby, _ ) in [ ( v1, v2 ), ( v2, v3 ), ( v3, v1) ] :
        doDraw, vax, vay, vbx, vby = clipLine( vax, vay, vbx, vby, portal )

        if doDraw:
          canvas.create_line( vax, vay, vbx, vby )

    else:
      canvas.create_line( *v1[:-1], *v2[:-1], *v3[:-1], *v1[:-1] )

def resolveBezierPatch( self, resolution, controlPoints ):
  # pointList = []
  # for u in numpy.linspace( 0.0, 1.0, resolution ):
  #   for v in numpy.linspace( 0.0, 1.0, resolution ):
  #     point = ( 0.0, 0.0, 0.0 )
  #     for i in 0 .. 3
  #       for j in 0 .. 3
  #         compute c[i,j]
  #         point = point + c[i,j] * P[i,j]
  #       end
  #     end
      
  #     pointList.append( point )
  #   end
  # end
  
  pointList = []
  for u in numpy.linspace( 0.0, 1.0, resolution ):
    for v in numpy.linspace( 0.0, 1.0, resolution ):
      c = [
        (-u + 1)**3 * (-v + 1)**3,          3*v(-u + 1)**3 * (-v + 1)**2,
        3*(v**2)(-u + 1)**3 * (-v + 1),     v**3 * (-u + 1)**3,

        3*u(-u + 1)**2 * (-v + 1)**3,       9*u*v(-u + 1)**2 * (-v + 1)**2,
        9*u*(v**2)(-u + 1)**2 * (-v + 1),   3*u*(v**3) * (-u + 1)**2,

        3*(u**2)*(-u + 1) * (-v + 1)**3,    9*(u**2)*v*(-u + 1) * (-v + 1)**2,
        9*(u**2)*(v**2)(-u + 1) * (-v + 1), 3*(u**2)(v**3) * (-u + 1)

        (u**3) * (-v + 1)**3,               3*(u**3)*v * (-v + 1)**2,
        3*(u**3)*(v**2) * (-v + 1),         (u**3) * (v**3)
      ]
      point = [ 0.0, 0.0, 0.0 ]
      for i in range(4):
        for j in range(4):
              point = [x + c[i*4+j] * controlPoints[i*4+j] for x in point]        
      pointList.append( point )
  return pointList

class cl_world :
  def __init__( self, objects = [], canvases = [] ) :
    self.objects = objects
    self.canvases = canvases

  def add_canvas( self, canvas ) :
    self.canvases.append( canvas )
    canvas.world = self

  def reset( self ) :
    self.objects = []
    for canvas in self.canvases :
      canvas.delete( 'all' )

  def create_graphic_objects( self, canvas, modelData, doClip, doPerspective, doEuler, resolution ) :
    ax, ay, sx, sy = modelData.getViewport()
    width  = int( canvas.cget( "width" ) )
    height = int( canvas.cget( "height" ) )
    portal = (width*ax, height*ay, width*sx, height*sy)
    pointList = []
    
    if doClip == False:
      for v1Num, v2Num, v3Num in modelData.getFaces() :
        x2, y2, _ = modelData.getTransformedVertex( v2Num, doPerspective, doEuler )
        x1, y1, _ = modelData.getTransformedVertex( v1Num, doPerspective, doEuler )
        x3, y3, _ = modelData.getTransformedVertex( v3Num, doPerspective, doEuler )

        canvas.create_line( x1, y1, x2, y2, x3, y3, x1, y1 )
    else:
      for v1Num, v2Num, v3Num in modelData.getFaces() :
        x1, y1, _ = modelData.getTransformedVertex( v1Num, doPerspective, doEuler )
        x2, y2, _ = modelData.getTransformedVertex( v2Num, doPerspective, doEuler )
        x3, y3, _ = modelData.getTransformedVertex( v3Num, doPerspective, doEuler )

        draw, p1x, p1y, p2x, p2y = clipLine(x1, y1, x2, y2, portal)
        if draw == True:
          canvas.create_line(p1x, p1y, p2x, p2y)
        draw, p1x, p1y, p2x, p2y = clipLine(x2, y2, x3, y3, portal)
        if draw == True:
          canvas.create_line(p1x, p1y, p2x, p2y)
        draw, p1x, p1y, p2x, p2y = clipLine(x3, y3, x1, y1, portal)
        if draw == True:
          canvas.create_line(p1x, p1y, p2x, p2y)

    for p in modelData.getPatches() :
        tCpts = [ modelData.getTransformedVertex(vNum, doPerspective, doEuler) for vNum in p]
        bpts  = resolveBezierPatch(self, resolution, tCpts )
        pointList.append(bpts)

    # tCpts = []
    # for p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11,p12,p13,p14,p15,p16 in modelData.getPatches() :
    #     x1, y1, _ = modelData.getTransformedVertex( p1, doPerspective, doEuler )
    #     x2, y2, _ = modelData.getTransformedVertex( p2, doPerspective, doEuler )
    #     x3, y3, _ = modelData.getTransformedVertex( p3, doPerspective, doEuler )
    #     x4, y4, _ = modelData.getTransformedVertex( p4, doPerspective, doEuler )
    #     x5, y5, _ = modelData.getTransformedVertex( p5, doPerspective, doEuler )
    #     x6, y6, _ = modelData.getTransformedVertex( p6, doPerspective, doEuler )
    #     x7, y7, _ = modelData.getTransformedVertex( p7, doPerspective, doEuler )
    #     x8, y8, _ = modelData.getTransformedVertex( p8, doPerspective, doEuler )
    #     x9, y9, _ = modelData.getTransformedVertex( p9, doPerspective, doEuler )
    #     x10, y10, _  = modelData.getTransformedVertex( p10, doPerspective, doEuler )
    #     x11, y11, _  = modelData.getTransformedVertex( p11, doPerspective, doEuler )
    #     xp12, y12, _ = modelData.getTransformedVertex( p12, doPerspective, doEuler )
    #     x13, y13, _ = modelData.getTransformedVertex( p13, doPerspective, doEuler )
    #     x14, y14, _ = modelData.getTransformedVertex( p14, doPerspective, doEuler )
    #     x15, y15, _ = modelData.getTransformedVertex( p15, doPerspective, doEuler )
    #     x16, y16, _ = modelData.getTransformedVertex( p16, doPerspective, doEuler )


    for row in range(resolution-1):
      rowStart = row * resolution
      
      for col in range(resolution-1):
        here = rowStart + col
        there = here + resolution
        triangleA = ( pointList[here], pointList[there], pointList[there+1] )
        triangleB = ( pointList[there+1], pointList[here+1], pointList[here] )
        
        drawTriangle( self, canvas, triangleA[0], triangleA[1], triangleA[2], portal, doClip )
        drawTriangle( self, canvas, triangleB[0], triangleB[1], triangleB[2], portal, doClip )

    


  def redisplay( self, canvas, event ) :
    pass

#----------------------------------------------------------------------
