# Adem, Said
# saa3053
# 2019-11-04

#----------------------------------------------------------------------
# This code was originally created by Prof. Farhad Kamangar.
# It has been significantly modified and updated by Brian A. Dalio for
# use in CSE 4303 / CSE 5365 in the 2018 Fall semester.

#----------------------------------------------------------------------
from CohenSutherland import clipLine

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

  def create_graphic_objects( self, canvas, modelData, doClip, doPerspective) :
    ax, ay, sx, sy = modelData.getViewport()
    width  = int( canvas.cget( "width" ) )
    height = int( canvas.cget( "height" ) )
    portal = (width*ax, height*ay, width*sx, height*sy)
    
    if doClip == False:
      for v1Num, v2Num, v3Num in modelData.getFaces() :
        x1, y1, _ = modelData.getTransformedVertex( v1Num, doPerspective )
        x2, y2, _ = modelData.getTransformedVertex( v2Num, doPerspective )
        x3, y3, _ = modelData.getTransformedVertex( v3Num, doPerspective )

        canvas.create_line( x1, y1, x2, y2, x3, y3, x1, y1 )
    else:
      for v1Num, v2Num, v3Num in modelData.getFaces() :
        x1, y1, _ = modelData.getTransformedVertex( v1Num, doPerspective )
        x2, y2, _ = modelData.getTransformedVertex( v2Num, doPerspective )
        x3, y3, _ = modelData.getTransformedVertex( v3Num, doPerspective )

        draw, p1x, p1y, p2x, p2y = clipLine(x1, y1, x2, y2, portal)
        if draw == True:
          canvas.create_line(p1x, p1y, p2x, p2y)
        draw, p1x, p1y, p2x, p2y = clipLine(x2, y2, x3, y3, portal)
        if draw == True:
          canvas.create_line(p1x, p1y, p2x, p2y)
        draw, p1x, p1y, p2x, p2y = clipLine(x3, y3, x1, y1, portal)
        if draw == True:
          canvas.create_line(p1x, p1y, p2x, p2y)

  def redisplay( self, canvas, event ) :
    pass

#----------------------------------------------------------------------
