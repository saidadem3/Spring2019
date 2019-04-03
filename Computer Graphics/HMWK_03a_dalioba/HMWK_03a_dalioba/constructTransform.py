# Adem, Said A.
# saa3053
# 2019-03-04

#---------#---------#---------#---------#---------#--------#
def constructTransform( w, v, width, height ) :
    ##################################################
    # Put your Python code for computing fx, fy, gx, gy, sx, sy,
    # ax, and ay here.
    #
    # Return ax, ay, sx, and sy as a tuple.
    ##################################################
    wxmin,wymin,wxmax,wymax = w
    vxmin,vymin,vxmax,vymax = v

    fx = -wxmin
    fy = -wymin
    gx,gy = width*vxmin, height*vymin

    sx = (width*(vxmax - vxmin))/(wxmax - wxmin)
    sy = (height*(vymax - vymin))/(wymax - wymin)

    ax = fx*sx + gx
    ay = fy*sy + gy

    return(ax, ay, sx, sy)




#---------#---------#---------#---------#---------#--------#
def _main() :
  w      = ( -1.0, -2.0, 4.0, 5.0 )
  v      = ( 0.15, 0.15, 0.85, 0.85 )
  width  = 500
  height = 400

  values = constructTransform( w, v, width, height )
  ax, ay, sx, sy = values

  print( f'Values          : {values}' )
  print( f'Test transform  : ax {ax}, ay {ay}, sx {sx}, sy {sy}' )

#---------#
if __name__ == '__main__' :
  _main()

#---------#---------#---------#---------#---------#--------#
