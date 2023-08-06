def extractRegion(im7D,ang,shift,ysizeT,xsizeT,ysizeOut=None,xsizeOut=None):
    """ This function extracts a region from a 7D image.
        You tell it the size, location and rotation of the region to extract.
        I.e. it is made to work with findSelection() below.
        im7D must be in our starndard form, i.e. with dimensions:
        (times,regions,montages,zslices,channels,ysize,xsize)
        You just pass it the angle and shift from findYourSection().
        You can pad the output to make it a certain size if you want, using 
        ysizeOut and xsizeOut.
        If you give it an image with 5D it assumes you want to add time and 
        field dimensions. I.e. it assumes you have done something likes 
        extractRegion(im7D[t,f]) and lost the first 2 dimensions.
        
        How it works:
        to extract template from image given ang and shift is easy:
        rotate point [0,0] in template by ang
        (remember how this requires ysizeT,xsizeT b/c it takes resizing of 
        the template during rotation into account)
        (and it was this resized rotated template that was matched to an 
        image region)
        then shift that rotated [0,0] point (it will now match the top left 
        corner of the template but in the image coordinates)
        then rotate both the image and point by -ang (now taking into 
        account the resizing of the image)
        (now the template will be sat squarely in the rotated image)
        now just add ysizeT,xsizeT to the point to find the limits
    """
    # package template shape to stop code bloating
    shapeT = (ysizeT,xsizeT)
    
    # add axes if needed
    if len(im7D.shape)==5:
        im7D = im7D[np.newaxis,np.newaxis]
    if len(im7D.shape)==6:
        im7D = im7D[np.newaxis]
    
    times,regions,montages,zslices,channels,ysizeI,xsizeI = im7D.shape
    # package these to stop code bloating
    shapeI = (ysizeI,xsizeI)
    
    # the top left corner of the template, in the template coord system:
    corner = [0,0]
    
    # now rotated as template rotates and shift added 
    # so it is aligned into the image coordinate system:
    corner = [sum(x) for x in zip(rotCoord_NoCrop(corner,*shapeT,ang),shift)]
    
    # and now rotated as image rotates so it is square:
    corner = [int(pos) for pos in rotCoord_NoCrop(corner,*shapeI,-ang)]
    
    # now arrange the im7D so it can apply all rotations at once:
    prod5D = times*regions*montages*zslices*channels
    im7D = np.swapaxes(np.swapaxes(np.reshape(im7D,(prod5D,*shapeI)),0,1),1,2)

    # rotate the image so template can be extracted as a square
    im7D = rotate_image(im7D,-ang)
    
    # do extraction:
    im7D = im7D[corner[0]:corner[0] + ysizeT,corner[1]:corner[1] + xsizeT]
    
    # put it back in the original shape:
    # package first 5 dimensions to stop code bloating
    shape5D = (times,regions,montages,zslices,channels)
    im7D = np.swapaxes(np.swapaxes(im7D,1,2),0,1).reshape(*shape5D,*shapeT)
    
    if ysizeOut:
        pY = ysizeOut - ysizeT
        pad = ((0,0),(0,0),(0,0),(0,0),(0,0),(pY//2,math.ceil(pY/2)),(0,0))
        im7D = np.pad(im7D,pad)
    if xsizeOut:
        pX = xsizeOut - xsizeT
        pad = ((0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(pX//2,math.ceil(pX/2)))
        im7D = np.pad(im7D,pad)
    
    # now return the extraction:
    return im7D