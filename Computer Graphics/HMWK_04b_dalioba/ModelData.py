# Adem, Said
# saa3053
# 2019-25-04

#---------#---------#---------#---------#---------#--------#
import sys
import math

#----------------------------------------------------------------------
class ModelData() :
  def __init__( self, inputFile = None ) :
    self.m_Vertices = []
    self.m_Faces    = []
    self.m_Window   = []
    self.m_Viewport = []
    self.m_Patches  = []

    self.m_minX     = float( '+inf' )
    self.m_maxX     = float( '-inf' )
    self.m_minY     = float( '+inf' )
    self.m_maxY     = float( '-inf' )
    self.m_minZ     = float( '+inf' )
    self.m_maxZ     = float( '-inf' )

    self.m_sx       = 1.0
    self.m_ax       = 0.0
    self.m_sy       = 1.0
    self.m_ay       = 0.0
    self.distance   = 0.0

    self.r00        = 0.0
    self.r01        = 0.0
    self.r02        = 0.0
    
    self.r10        = 0.0
    self.r11        = 0.0
    self.r12        = 0.0

    self.r20        = 0.0
    self.r21        = 0.0
    self.r22        = 0.0

    self.ex        = 0.0
    self.ey        = 0.0
    self.ez        = 0.0


    if inputFile is not None :
      # File name was given.  Read the data from the file.
      self.loadFile( inputFile )

  def loadFile( self, inputFile ) :
    with open( inputFile, 'r' ) as fp :
      lines = fp.read().replace('\r', '' ).split( '\n' )

    for ( index, line ) in enumerate( lines, start = 1 ) :
      line = line.strip()
      if ( line == '' or line[ 0 ] == '#' ) :
        continue

      if ( line[ 0 ] == 'v' ) :
        try :
          ( _, x, y, z ) = line.split()
          x = float( x )
          y = float( y )
          z = float( z )

          self.m_minX = min( self.m_minX, x )
          self.m_maxX = max( self.m_maxX, x )
          self.m_minY = min( self.m_minY, y )
          self.m_maxY = max( self.m_maxY, y )
          self.m_minZ = min( self.m_minZ, z )
          self.m_maxZ = max( self.m_maxZ, z )

          self.m_Vertices.append( ( x, y, z ) )

        except :
          print( 'Line %d is a malformed vertex spec.' % index )

      elif ( line[ 0 ] == 'f' ) :
        try :
          ( _, v1, v2, v3 ) = line.split()
          v1 = int( v1 )-1
          v2 = int( v2 )-1
          v3 = int( v3 )-1
          self.m_Faces.append( ( v1, v2, v3 ) )

        except :
          print( 'Line %d is a malformed face spec.' % index )

      elif ( line[ 0 ] == 'p' ) :
        try :
          ( _, p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13, p14, p15, p16 ) = line.split()
          p1 = int( p1 )-1
          p2 = int( p2 )-1
          p3 = int( p3 )-1
          p4 = int( p4 )-1
          p5 = int( p5 )-1
          p6 = int( p6 )-1
          p7 = int( p7 )-1
          p8 = int( p8 )-1
          p9 = int( p9 )-1
          p10 = int( p10 )-1
          p11 = int( p11 )-1
          p12 = int( p12 )-1
          p13 = int( p13 )-1
          p14 = int( p14 )-1
          p15 = int( p15 )-1
          p16 = int( p16 )-1
          self.m_Patches.append( ( p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13, p14, p15, p16  ) )

        except :
          print( 'Line %d is a malformed face spec.' % index )

      elif ( line[ 0 ] == 'w' ) :
        if ( not self.m_Window == [] ) :
          print( 'Line %d is a duplicate window spec.' % index )

        try :
          ( _, xmin, ymin, xmax, ymax ) = line.split()
          xmin = float( xmin )
          ymin = float( ymin )
          xmax = float( xmax )
          ymax = float( ymax )
          self.m_Window = ( xmin, ymin, xmax, ymax )

        except :
          print( 'Line %d is a malformed window spec.' % index )

      elif ( line[ 0 ] == 's' ) :
        if ( not self.m_Viewport == [] ) :
          print( 'Line %d is a duplicate viewport spec.' % index )

        try :
          ( _, xmin, ymin, xmax, ymax ) = line.split()
          xmin = float( xmin )
          ymin = float( ymin )
          xmax = float( xmax )
          ymax = float( ymax )
          self.m_Viewport = ( xmin, ymin, xmax, ymax )

        except :
          print( 'Line %d is a malformed viewport spec.' % index )

      else :
          print( 'Line %d \'%s\' is unrecognized.' % ( index, line ) )

  def getBoundingBox( self ) :
    return (
      self.m_minX, self.m_maxX,
      self.m_minY, self.m_maxY,
      self.m_minZ, self.m_maxZ )

  def specifyTransform( self, ax, ay, sx, sy, distance ) :
    self.m_ax = ax
    self.m_sx = sx
    self.m_ay = ay
    self.m_sy = sy
    self.distance = distance

  def specifyEuler( self, phi, theta, psi ) :
    cosPhi,   sinPhi  = math.cos( phi ),     math.sin( phi )
    cosTheta, sinTheta = math.cos( theta ), math.sin( theta )
    cosPsi,   sinPsi  = math.cos( psi ),     math.sin( psi )

    cosPhiCosPsi =  cosPhi * cosPsi
    cosPhiSinPsi =  cosPhi * sinPsi
    sinPhiCosPsi =  sinPhi * cosPsi
    sinPhiSinPsi =  sinPhi * sinPsi

    self.r00 = cosPsi * cosTheta
    self.r01 = -cosTheta * sinPsi
    self.r02 = sinTheta
    
    self.r10 = cosPhiSinPsi + cosPhiSinPsi*sinTheta
    self.r11 = cosPhiCosPsi - sinPhiSinPsi*sinTheta
    self.r12 = -cosTheta*sinPhi
    
    self.r20 = -cosPhiCosPsi * sinTheta + sinPhiSinPsi
    self.r21 = cosPhiSinPsi * sinTheta + sinPhiCosPsi
    self.r22 = cosPhi * cosTheta

    tx, ty, tz = self.getCenter()

    self.ex = -self.r00*tx - self.r01*ty - self.r02*tz + tx
    self.ey = -self.r10*tx - self.r11*ty - self.r12*tz + ty
    self.ez = -self.r20*tx - self.r21*ty - self.r22*tz + tz

  def getTransformedVertex( self, vNum, doPerspective, doEuler ) :
    ( x, y, z ) = self.m_Vertices[ vNum ]
    if doEuler == True:
      xprime = self.r00*x + self.r01*y + self.r02*z + ( self.ex )
      yprime = self.r10*x + self.r11*y + self.r12*z + ( self.ey )
      zprime = self.r20*x + self.r21*y + self.r22*z + ( self.ez )
      x, y, z = xprime, yprime, zprime
    if doPerspective == True:    
      if self.distance == 0 or self.distance <= z:
        x = 0.0
        y = 0.0
        z = 0.0
      else:
        x,y = x/(1-(z/self.distance)), y/(1-(z/self.distance))
    return ( self.m_sx*x + self.m_ax, self.m_sy*y + self.m_ay, 0.0 )
      

  def getCenter( self ) :
    return (
      ( self.m_minX + self.m_maxX ) / 2.0,
      ( self.m_minY + self.m_maxY ) / 2.0,
      ( self.m_minZ + self.m_maxZ ) / 2.0 )

  def getFaces( self )    : return self.m_Faces
  def getPatches( self )  : return self.m_Patches
  def getVertices( self ) : return self.m_Vertices
  def getViewport( self ) : return self.m_Viewport
  def getWindow( self )   : return self.m_Window

#---------#---------#---------#---------#---------#--------#
def _main() :
  # Get the file name to load.
  fName = sys.argv[1]

  # Create a ModelData object to hold the model data from
  # the supplied file name.
  model = ModelData( fName )

  # Now that it's loaded, print out a few statistics about
  # the model data that we just loaded.
  print( f'{fName}: {len( model.getVertices() )} vert%s, {len( model.getFaces() )} face%s' % (
    'ex' if len( model.getVertices() ) == 1 else 'ices',
    '' if len( model.getFaces() ) == 1 else 's' ))

  print( 'First 3 vertices:' )
  for v in model.getVertices()[0:3] :
    print( f'     {v}' )

  print( 'First 3 faces:' )
  for f in model.getFaces()[0:3] :
    print( f'     {f}' )

  print( f'Window line    : {model.getWindow()}' )
  print( f'Viewport line  : {model.getViewport()}' )

  print( f'Center         : {model.getCenter()}' )

#---------#
if __name__ == '__main__' :
  _main()

#---------#---------#---------#---------#---------#--------#
