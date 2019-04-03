# Adem, Said A.
# saa3053
# 2019-02-06

import sys

class ModelData() :
  def __init__( self, inputFile = None ) :
    self.m_Vertices = []
    self.m_Faces    = []
    self.minX = 0
    self.minY = 0
    self.minZ = 0
    self.maxX = 0
    self.maxY = 0
    self.maxZ = 0

    if inputFile is not None :
      # File name was given.  Read the data from the file.
      self.loadFile( inputFile )

  def loadFile( self, inputFile ) :
    ##################################################
    # Put your Python code for reading and processing the lines
    # from the source file in the place of the comments below.
    # (The comments give all the direction you should need to
    #  write the code.  It's not all that difficult.)
    ##################################################

    # Read each line of the file.

    # Ignore any blank line (or line that's only whitespace characters).

    # Ignore any line that starts with a #.

    # For the remaining lines, if the line starts with:
    #  f -- Append the three integers as a tuple to self.m_Faces.
    #  v -- Append the three floats as a tuple to self.m_Vertices.

    # Note that the above comments mention integers and floats.
    # You must convert the string representation of the integers
    # and floats into actual numbers.  There may be formatting
    # errors in the file, so ensure you catch (and report)
    # conversion errors.

    # It is an error if a line starts with any other character.
    # Print an error message for that line, but keep going and look
    # at the rest of the lines.

    # A model file may have any number of f and v lines.  In fact,
    # some model files we will use will have thousands of v and f
    # lines.

    with open( inputFile, 'r' ) as fp :
          lines = fp.read().replace('\r', '' ).split( '\n' )

    for ( index, line ) in enumerate( lines, start = 1 ) :
          line = line.strip()

          if len(line) == 0 or line[0] == '#':
            continue
          elif line[0] == 'v':
            tokens = line.split()
            if len(tokens) != 4:
              print ("Line %d is a malformed vertex spec." % index)
              continue
            tokens.pop(0)
            tokens = list(map(float, tokens))
            self.minMax(tokens)
            self.m_Vertices.append( ( tokens[0], tokens[1], tokens[2] ) )         
          elif line[0] == 'f':
            tokens = line.split()
            if len(tokens) != 4:
              print ("Line %d is a malformed face spec." % index)
              continue
            tokens.pop(0)
            try:
              tokens = list(map(int, tokens))
            except:
              print("Line %d is a malformed face spec." % index)
              continue
                        
            tokens[:] = [x - 1 for x in tokens]
            self.m_Faces.append( tuple(tokens) )
          else:
               print( f'Line {index} \'{line}\' is unrecognized.' )

    print("THIS IS THE CENTER: ")
    print(self.getCenter())


    ##################################################
    # All the code you have to write should go above here in the
    # body of the loadFile() routine.
    ##################################################

  def getFaces( self )    : return self.m_Faces
  def getVertices( self ) : return self.m_Vertices
  def minMax( self, tokens):
    if tokens[0] < self.minX:
      self.minX = tokens[0]
    if tokens[1] < self.minY:
      self.minY = tokens[1]
    if tokens[2] < self.minZ:
      self.minZ = tokens[2]
    if tokens[0] > self.maxX:
      self.maxX = tokens[0]
    if tokens[1] > self.maxY:
      self.maxY = tokens[1]
    if tokens[2] > self.maxZ:
      self.maxZ = tokens[2]
  def getCenter( self ) :
    return ((self.maxX+self.minX)/2,(self.maxY+self.minY)/2,(self.maxZ+self.minZ)/2)


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

#---------#
if __name__ == '__main__' :
  _main()

#---------#---------#---------#---------#---------#--------#
