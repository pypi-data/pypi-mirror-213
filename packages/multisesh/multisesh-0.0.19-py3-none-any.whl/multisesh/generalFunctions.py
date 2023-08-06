import re
import os
import math
import csv
import numpy as np
import tifffile
from datetime import datetime
from datetime import timedelta

# this makes the import work when this file is being imported as part 
# of a package or by itself
if __package__ == '':
    from exceptions import UnknownTifMeta
    import findMeta as fMeta
    import errorMessages as EM
else:
    from .exceptions import UnknownTifMeta
    from . import findMeta as fMeta
    from . import errorMessages as EM
    
    
from skimage import measure
from scipy.ndimage import binary_fill_holes


def groupSessionFiles(fpaths):
    """ Takes a list of file paths and groups into sessions. Gives metadata, 
    image files and what software made it for each session. Returned sessions 
    are sorted according to the time their imaging protocol was run.
    
    Parameters
    ----------
    fpaths : list
        A list of filepaths that you want to sort into sessions.
    
    Returns
    --------
    sesh : list
        each element represents a session, is in form [meta,filepaths,madeBy]
        where meta is path to files containing any metadata not within the 
        imaging files, filepaths are filepaths to image data and madeBy is a 
        string giving the software it was made by.
    
    Also
    -----
    It raises an exception if the txt file has an Andor like tag
    i.e if it has something t0005 at the end
    because that would confuse it...
    because these tags are removed from the tif file in order to 
    do the matching.
    
    """
    
    tps = [t for t in fpaths if '.tif' in t]
    tps2 = tps.copy()
    mps = [t for t in fpaths if '.txt' in t]
    sesh = []
    for t in tps:
        if t not in tps2:
            continue
        with tifffile.TiffFile(t) as tif:
            m = tif.micromanager_metadata
            f = tif.fluoview_metadata
            time = fMeta.startMom()
        if m:
            madeBy = 'MicroManager'
        elif f:
            madeBy = 'Andor'
        else:
            raise Exception(f'Unknown software made your session {t}')
        seshTPs = [T for T in tps2 if stripTags(T,madeBy)==stripTags(t,madeBy)]
        for T in seshTPs:
            tps2.remove(T)
        met = stripTags(t,madeBy)+'.txt'
        if met in mps:
            mps.remove(met)
        else:
            met = ''
        sesh.append[met,seshTPs,madeBy,time]
        
    return sesh
    
    # get all .txt files
    mFiles = [[file] for file in fpaths if '.txt' in file]
    tFiles = [file for file in fpaths if '.tif' in file]
    
    # now we set the order of the sessions in terms of the 
    # start time found in the metadata
    T0Reg = re.compile(r'Time=(\d\d:\d\d:\d\d)\n\[Created End\]')
    # start date regex:
    D0Reg = re.compile(r'\[Created\]\nDate=(\d\d/\d\d/\d\d\d\d)') 
    # format for datetime
    TX = '%d/%m/%Y %H:%M:%S'
    # loop over mFiles making a list with the associated start times
    mT0s = []
    for m in mFiles:
        # import metadata
        with open(m[0], 'rt') as theFile:  
            metadata = theFile.read()
        # extract start moment as datetime object
        startMom = meta2StartMom(metadata)
        mT0s.append(startMom)
    # use list of start times to sort mFiles:
    mFiles = [m for _,m in sorted(zip(mT0s,mFiles))]
    
    
    # this is the regex for detecting any tag at the end of filename: 
    tagRegex = r'_(f|m|t)\d{3,9}$'
    # error message (see assert below)
    eMess = 'metadata file {file} has a tag at the end which has the '\
            'same e.g. _t0005 format as Andor puts at the end of tif'\
            ' tif files. This makes it complex to automatically'\
            ' group metadata and tif files together and isn\'t'\
            ' handled yet. See generalFunctions.groupSessionFiles'\
            ' to make this work.'
    
    # find the tifnames for each metadata file
    for mf in mFiles:
        # metadata called e.g. data_t0002.txt aren't handled
        assert not re.search(tagRegex,mf[0][:-4]), eMess.format(file=mf)
        
        # strip tags off tiff files names and see if they match metafile name
        mf.append([tf for tf in tFiles if stripTags(tf)==mf[0][:-4]])
        
    return mFiles



def getSessionPaths(xPath,filters):
    """ This is similar to the method of XFold called getSessions().
    It produces Session-like data, but not real Sessions.
    In fact it returns the [meta,[tif,tif...]] structure lists of file 
    paths that are produced by groupSessionFiles().
    This was motivated by wanting to get some session data during XFold 
    initialisation but not wanting to go round in cricles by using a method 
    of the class you were trying to set up an instance of. 
    It gets all the sessions found in the xPath
    It of course applies the filters, to filter out unwanted files
    """   
    # make a flat list of all the filepaths in XFold:
    walk = [x for x in os.walk(xPath)]
    fps = [os.path.join(x[0],fn) for x in walk for fn in x[2]]
    # filter out paths which have any terms included in filts
    fps = [fp for fp in fps if not any(fl in fp for fl in filters)]
    # pass fps->groupSessionFiles to organise into session structure:
    seshPaths = groupSessionFiles(fps)
    
    return seshPaths



def stripTags(filename,madeBy='Andor'):
    """ this removes from a filename the file extension and the tags (which 
    are software specific) which are added when a session is divided up into 
    different files.
    
    madeBy dependent behaviour
    -------------------------
    Andor : removes tags like _qnnnn from the end. Removes any number from the 
            end but not ever from the middle of the filename.
    MicroManager : removes .ome from end, then _MMStack_n, then Pos_nnn_nnn. 
            Haven't tested this on many variants.
    """ 
    # first get rid of extension
    filename = filename.split('.')[0]
    if madeBy=='Andor':
        tagRegex = re.compile(r'(_(t|f|m|z|w|s)\d{3,9})+$')
        return tagRegex.sub('',filename)
    elif madeBy=='MicroManager':
        return filename.split('_MMStack_')[0]
        # old way:
        #regPos = re.compile(r'(-?Pos_\d\d\d_\d\d\d$)')
        #regOME = re.compile(r'(.ome$)')
        #regF = re.compile(r'(_MMStack_\d-?$)')
        #return regF.sub('',regPos.sub('',regOME.sub('',filename)))
    else:
        raise Exception(f'Unknown sotware {madeBy}')
                      
    
    
def tagIntFromTifName(name,findTag,stripTags=['t','f','m','s'],returnList=False):
    """This returns a list of ints taken from the tag that Andor puts on the 
        end of names of tif files when it splits data into different files. 
        The andor tag has a letter at the beginning, e.g. _t0005, here you 
        provide a list (stripTags) of which letters you want it to consider
        as counting as a tag. 
        It progressively strips these tags from the end of the filename 
        (after first having removed the .tif if it exists) and keeps each tag
        that has the letter that matches the letter provided in findTag.
        It returns the list of these tags converted to ints.
        I.e. name_m0004_name_m0001_t0005_m0109.tif will return
        [1,109] if you give it ['m'].
        """
    
    # take .tif off
    if name[-4:]=='.tif':
        fn = name[:-4]
    else:
        fn = name
    
    # make the regexes:
    findReg = r'_'+findTag+r'(\d{3,9})'
    stripEndReg = r'(_('+'|'.join(stripTags)+r')\d{3,9})$'
    
    # now keep stripping until non left but save findTags that crop up
    foundInts = []
    while re.search(stripEndReg,fn):
        foundTag = re.search(stripEndReg,fn).group(1)
        if re.search(findReg,foundTag):
            foundInts.append(int(re.search(findReg,foundTag).group(1)))  
        fn = re.sub(stripEndReg,'',fn)
    
    if returnList:
        return foundInts
    else:
        if len(foundInts)>0:
            return foundInts[0]
        else:
            return
    

def regexFromfilePath(reg,fPath,findAll=False,g=1,chars=10000,isFloat=False):
    """ this return regexes from fPath
        if the thing found is a digit char it always converts it to an int
        you can access other groups with g but default is g=1
        only loads no. 'chars' of characters from file in case too big
        for findAll = False you can use a compiled regex or a raw string
    """
    # loads data from fPath
    with open(fPath, 'rt') as theFile:  
        fileData = theFile.read(chars)            
    if findAll:
        N = re.findall(reg,fileData)
    else:
        if type(reg)==str:
            reg = re.compile(reg)
        N = reg.search(fileData)
        if N and type(N)!=list:
            N = N.group(g)
            if N.isdigit():
                N = int(N)
            if isFloat:
                N = float(N)
    return N

    
def chanDic(channel):
    """ This converts the channel's actual protocol 
    name to it's 'general name'.
    """
    channelDic = {'BF':'BF',
            'GFP':'GFP',
            'YFP':'YFP',
            'RFP':'RFP',
            'CFP':'CFP',
            'DAPI':'DAPI',
            'FR':'FR',
            'Unknown_Gray':'Unknown_Gray',
            'Unknown_Green':'Unknown_Green',
            'Unknown_Blue':'Unknown_Blue',
            'Unknown_Red':'Unknown_Red',
            'Tom_BF':'BF',
            'Tom_YFP':'YFP',
            'Tom_GFP':'GFP',                  
            'Tom_CFP':'CFP',
            'Tom_RFP':'RFP',
            'Tom_FR':'FR',
            'Far_Red':'FR',
            'FarRed':'FR',
            'Tom_DAPI':'DAPI',
            'RFP_Wide':'RFP',
            'rhodamine':'RFP',
            'Label':'Label',
            None:None
                 }
    
    assert channel in channelDic.keys(),EM.ch1 + 'Channel: '+channel
    
    return channelDic[channel]



def LUTDic(channel):
    """
    This takes a channel's 'general name' (see channelDic) and assigns 
    an LUT mix rule (see LUTMixer()).
    You might want to change this around or add new channels etc.
    """
    
    theLUTDic = {'BF':[True,True,True],
                 'DAPI':[False,False,True],
                 'GFP':[False,True,False],
                 'YFP':[False,True,False],
                 'CFP':[False,False,True],
                 'RFP':[True,False,False],
                 'FR':[True,True,False], # = yellow!
                 'Label':[True,True,True],
                 'Unknown_Grey':[True,True,True],
                 'Unknown_Green':[False,True,False],
                 'Unknown_Blue':[False,False,True],
                 'Unknown_Red':[True,False,False],
                 'Chan_unknown':[True,True,True]
                }
    
    assert channel in theLUTDic.keys(),EM.ch2
    
    return theLUTDic[channel]



def LUTMixer(mixVector):
    """
    This makes an LUT in image j format from a boolean vector.
    I.e. you give it a vector like [True, False, True] to say which 
    RGB channels to put in the LUT.
    """
    val_range = np.arange(256, dtype=np.uint8)
    LUT = np.zeros((3, 256), dtype=np.uint8)
    LUT[mixVector] = val_range
    return LUT


def LUTInterpreter(LUT):
    """
    You give a list of LUTs and it return the channel names.
    i.e. you can put imagej_metadata LUTs in and it tells you what colour 
    it is so that you can rebuild the LUTs when you resave for imagej. 
    Works alongside LUTDic.
    """

    assert LUT.shape[1]==3 and LUT.shape[2]==256,EM.LT1
    
    boolDic = {[True,True,True]:'Unknown_Grey',
               [False,False,True]:'Unknown_Green',
               [False,False,True]:'Unknown_Blue',
               [True,False,False]:'Unknown_Red',
              }
    
    boolVec = [[L[0].sum()==0,L[1].sum()==0,L[2].sum()==0] for L in LUT]
    boolVec = [[not BV[0],not BV[1],not BV[2]] for BV in boolVec]
    return [boolDic[bv] for bv in boolVec]


def getProcessedDataDs(xPath,xSig):
    """
    This function looks in the parent directory of the path given for any
    directories containing the signature xSig in their name.
    It returns a set of paths to those directories.
    """
    
    # get parent directory path
    parPath = os.path.split(xPath)[0]
    # get the names of all objects in that directory
    listDir = os.listdir(parPath)
    # filter to get just the directories
    allDirs = [d for d in listDir if os.path.isdir(os.path.join(parPath,d))]
    # filter for directories must contain the signature xSig
    allDirs = [os.path.join(parPath,d) for d in allDirs if xSig in d]
    
    return set(allDirs)



def listStr2List(listString,convertNumeric=True):
    """
    This converts a string of a python list to a list.
    Only currently works for elements that are ints or 'None'
    """
    reg = r'\[(.*)\]'
    list1 = re.search(reg,listString).group(1)
    list1 = list1.split(',')
    
    list2 = []
    for l in list1:
        if l=='None':
            list2.append(None)
        elif l.replace(' ','').isdecimal() and convertNumeric:
            list2.append(int(l.replace(' ','')))
        elif l.replace('.','',1).isdecimal() and convertNumeric:
            list2.append(float(l))
        else:
            list2.append(l.replace('\'','').replace(' ',''))
    
    return list2



def maskFromOutlinePath(outLinePath):
    """ 
    This takes the path of an image outline you have drawn and returns
    a binary mask with all values within the outline set to 
    1 and 0 elsewhere.
    The only requirement is that your outline has the pixel value that 
    is the highest in the image.
    """
    # import image
    with tifffile.TiffFile(outLinePath) as tif:
        outLine = tif.asarray()
    # normalise it
    outLine = outLine/np.max(outLine)
    # set non-maximum pixels to zero so we have a binary image
    outLine[outLine!=1.0] = 0
    # find connected components
    labels = measure.label(outLine)
    # find the connected component with the most pixels
    # we assume this is your outline
    biggestComponent = np.bincount(labels.flatten())[1:].argmax()+1
    # set everything to zero except your outline
    labels[labels != biggestComponent] = 0
    labels[labels == biggestComponent] = 1
    # fill in the outline
    mask = binary_fill_holes(labels)
    # return your mask
    return mask



def shapeFromFluoviewMeta(meta):
    """ 
    This gets the 7D dimensions from fluoview metadata. 
    In some fluoview versions it doesn't include the dimension 
    name if the dimension size is 1 so we have to add it.
    """
    dims = meta['Dimensions']
    dimsDic = {l[0]:l[1] for l in dims}
    shapeKeys = ['Time','XY','Montage','Z','Wavelength','y','x']
    dims = []
    for k in shapeKeys:
        if k in dimsDic.keys():
            dims.append(dimsDic[k])
        else:
            dims.append(1)
    return dims



def tif2Dims(tif):
    """ This takes a tifffile.TiffFile object and returns dimensions 
        of the associated tifffile in the 7D format that we use. Currently
        works for fluoview and files we use in image j but we want to do 
        it for as many file types as possible.
        
        It returns an error if the data is not in one of these forms unless 
        there is only one image in which case it knows T,F,M,Z,C dims are 1. 
        This is useful because we use images of one frame to do things like 
        draw the masks but when you save them image j will erase all metadata.
    """
    fluo = 'fluoview_metadata'
    d = dir(tif)
    # for fluoview files:
    if fluo in d and tif.fluoview_metadata != None:
        meta = tif.fluoview_metadata
        dims = shapeFromFluoviewMeta(meta)                    
    # for image j ready files that we saved:
    elif ('imagej_metadata' in d and 
            tif.imagej_metadata != None and 
            'tw_nt' in tif.imagej_metadata.keys()):
        meta = tif.imagej_metadata
        baseString = 'tw_n'
        dimStrings = ['t','f','m','z','c','y','x']
        dims = [meta[baseString+L] for L in dimStrings]
    elif len(tif.asarray().shape)==2:
        dims = [1 for i in range(5)] + list(tif.asarray().shape)
    else:
        raise UnknownTifMeta()
    return dims



def meta2StartMom(meta):
    """ 
    This takes a session's metadata file and returns a datetime object 
    of the moment when the file was started.
    """
    # the format of the datatime string we give it
    TX = '%d/%m/%Y %H:%M:%S'
    startTimeReg = re.compile(r'Time=(\d\d:\d\d:\d\d)\n\[Created End\]')
    # start date regex:
    startDateReg = re.compile(r'\[Created\]\nDate=(\d\d/\d\d/\d\d\d\d)')
    # delay reg, i.e. time between session starting and imaging starting
    delayReg = re.compile(r'Delay - (\d+) (\w+)')
    # take start moment from the vth metadata
    startT = re.search(startTimeReg,meta).group(1)
    startDate = re.search(startDateReg,meta).group(1)
    startMom = startDate + ' ' + startT
    startMom = datetime.strptime(startMom,TX)
    
    # add the delay time if necessary
    if re.search(startTimeReg,meta):
        delayT = int(re.search(delayReg,meta).group(1))
        if re.search(delayReg,meta).group(2)=='min':
            delayT = timedelta(minutes=delayT)
            startMom += delayT
        elif re.search(delayReg,meta).group(2)=='hr':
            delayT = timedelta(hours=delayT)
            startMom += delayT
        else:
            raise Exception(EM.sm1)
             
    return startMom



def meta2TStep(meta):
    """ 
    This takes a session's metadata file and returns a timedelta object
    of the time between time points.
    """
    # time interval group(1), units group(2)
    DTReg = re.compile(r'Repeat T - \d+ times? \((\d+) (\w+)\)')
    
    # find the time between time-points of this TData (from its 
    # parent session metadata)
    seshTStep = int(re.search(DTReg,meta).group(1))
    
    if re.search(DTReg,meta).group(2) == 'hr':
        seshTStep = timedelta(hours=seshTStep)
    elif re.search(DTReg,meta).group(2) == 'min':
        seshTStep = timedelta(minutes=seshTStep)
    elif re.search(DTReg,meta).group(2) == 'sec':
        seshTStep = timedelta(seconds=seshTStep)
    else:
        raise Exception(EM.sm2)

    return seshTStep



def onlyKeepChanges(theList):
    """ 
    This makes a list from theList in which only elements which are 
    different from the previous are kept.
    """
    
    if len(theList)==0:
        return theList
    
    newList = []
    newList.append(theList[0])
    
    for l in theList[1:]:
        if l != newList[-1]:
            newList.append(l)
    
    return newList


def savedByXFoldQ(filepath):
    """ 
    Returns True if the files was saved by this package, False otherwise
    Tests this by looking at metadata.
    """
    with tifffile.TiffFile(filepath) as tif:
        d = dir(tif)
        if ('imagej_metadata' in d and 
            tif.imagej_metadata != None and 
            'tw_nt' in tif.imagej_metadata.keys()):
            return True
        else:
            return False
        
        
def saveTiffForIJ(
    outPath,
    data,
    chan=False,
    seshDs=False,
    autoscale=True,
    minP=2,
    maxP=98,
    overwrite=False):
    """
    Uses tifffile package to save 7D data in way that is good for imagej.
    Also saves metadata inside the tif that xfold will recognise.
    
    Parameters
    ----------
    outPath : str
        File path to save to.
    data : numpy.array
        Image array. Must have 7 dimensions as in standard TData structure.
    chan : list of str
        The channel names. Used to set LUT. If not provide it will try to set 
        default channels but currently this only works if the number of 
        channels can be read from provided seshDs or the data shape. It only 
        knows how to read from the data shape if the shape has 2,3 or 7 axes.
    seshDs : list of lists
        Used to save as metadata, should be: [seshT,seshF,seshM,seshZ,seshC]. 
        Also used to try and reshape data to 7D if it is not 7D and set 
        default channels if they're not provided. If seshDs not provided then 
        it can continue only if the data shape has 2,3 or 7 axes.
    autoscale : bool
        Whether to autoscale or not. This doesn't change the data, it just 
        sets the metadata for imagej.
    minP : int [0-100]
        The percentile to set the min pixel value to during autoscaling.
    maxP : int [0-100]
        The percentile to set the max pixel value to during autoscaling.
    overwrite : bool
        Whether to allow overwriting of data with the same filename.
        
    Notes
    -----
    It will try to reshape the data if it isn't 7D - it will work if 
    images are properly ordered and you give the correct seshDs. It will also 
    work if the data is 3D - it will assume the first axis is channels.
    """
    
    dims = data.shape
    assert len(dims)<8 and len(dims)>1,'data must be maximum 7D and minimum 2D'
    
    defaultChans = ['BF','GFP','RFP','CFF','FR']
    if not chan:
        if seshDs:
            assert len(seshDs[4])<6,EM.sv4
            chan = defaultChans[:len(seshDs[4])]
        elif len(dims)==7:
            assert dims[-3]<6,EM.sv5
            chan = defaultChans[:dims[-3]]
        elif len(dims)==3:
            assert dims[0]<6,EM.sv5
            chan = defaultChans[:dims[0]]
        elif len(dims)==2:
            chan = ['BF']          
        else:
            raise Exception(EM.sv3)
    
    # reshape data according to seshDs if data is not 7D and seshDs provided
    if len(dims)!=7 and seshDs:
        seshDL = [len(s) for s in seshDs]
        nImMeta = np.product(seshDL)*dims[-1]*dims[-2]
        assert np.product(dims)==nImMeta,EM.sv2
        dims = seshDL + [dims[-2]] + [dims[-1]]
        data = data.reshape(dims)
    # reshape data if data has 3 axes and seshD not provided 
    # also set seshDs from dims
    elif len(dims)==3 and not seshDs:
        dims = [1,1,1,1]+[dims[-3]]+[dims[-2]]+[dims[-1]]
        data = data.reshape(dims)
        seshDs = [['None']*dims[0],
                  ['None']*dims[1],
                  ['None']*dims[2],
                  ['None']*dims[3],
                  ['None']*dims[4]]  
    # reshape data if data has 2 axes and seshD not provide    
    # also set seshDs from dims
    elif len(dims)==2 and not seshDs:
        dims = [1,1,1,1,1]+[dims[-2]]+[dims[-1]]
        data = data.reshape(dims)
        seshDs = [['None']*dims[0],
                  ['None']*dims[1],
                  ['None']*dims[2],
                  ['None']*dims[3],
                  ['None']*dims[4]]          
    # set seshDs if data has 7 axes and seshDs not provided
    elif len(dims)==7 and not seshDs:
        seshDs = [['None']*dims[0],
                  ['None']*dims[1],
                  ['None']*dims[2],
                  ['None']*dims[3],
                  ['None']*dims[4]] 
    elif len(dims)!=7 and not seshDs:
        raise Exception(EM.sv6)
        
    assert not (os.path.exists(outPath) and not overwrite),EM.sv1
    
    # this is the metadata to add:
    singleImQ = all([d==1 for d in dims[0:5]])
    meta = {'hyperstack':'true','mode':'composite','unit':'um',
            'spacing':'2.56','loop':'false','min':'0.0','max':'256',
            'tw_NT':dims[0],'tw_NF':dims[1],'tw_NM':dims[2],
            'tw_NZ':dims[3],'tw_NC':dims[4],'tw_NY':dims[5],
            'tw_NX':dims[6],'tw_SeshT':str(seshDs[0]),
            'tw_SeshF':str(seshDs[1]),'tw_SeshM':str(seshDs[2]),
            'tw_SeshZ':str(seshDs[3]),'tw_SeshC':str(seshDs[4]),
            'tw_chan':str(chan)}
    if singleImQ:
        minV = np.percentile(np.ravel(data),minP)
        maxV = np.percentile(np.ravel(data),maxP)
        meta['min'] = str(minV)
        meta['max'] = str(maxV)
    
    # tifffile requires a dictionary ijmeta which it converts to binary for ij
    # set ranges for each channel:
    if autoscale:
        ranges = []
        for c,ch in enumerate(chan):
            minV = np.percentile(np.ravel(data[:,:,:,:,c]),minP)
            ranges.append(minV)
            maxV = np.percentile(np.ravel(data[:,:,:,:,c]),maxP)
            ranges.append(maxV)
    else:
        ranges = [x for i in range(dims[4]) for x in [0.0,65535.0]]
    # make the LUTs
    LUTs = [LUTMixer(LUTDic(c)) for c in chan]
    # package ranges and LUTs into imagej metadata dictionary 
    ijmeta = {'Ranges':tuple(ranges),'LUTs':LUTs}
    # do the save, reshaping the array for image j at the last moment
    dims = (dims[0]*dims[1]*dims[2],dims[3],dims[4],dims[5],dims[6])
    tifffile.imsave(outPath,data.reshape(dims),imagej=True,metadata=meta,
                    ijmetadata=ijmeta)
    
    
def trap2rect(points):
    ymin = min([p[0] for p in points])
    ymax = max([p[0] for p in points])
    xmin = min([p[1] for p in points])
    xmax = max([p[1] for p in points])
    return [[ymin,xmin],[ymin,xmax],[ymax,xmax],[ymax,xmin]]    

    
def getTagDic(fp,madeBy):
    """
    When the data along a certain dimension Q is split between different files 
    the file name is given a tag. This function returns that tag in a 
    dictionary. The keys of the dictionary are the 'Q' of any found tags and 
    the values are the tags. 
    
    Our code in general is going to assume that all files with the same tag 
    contain equivalent Q-points. That is, all files with time tag '_t0004' 
    have the same set of time points even if they contain different subsets 
    of other dimensions, e.g. you could have _t0004_m0000 and _t0004_m0001 
    but both contain time points e.g. t=6,7,8.
    
    Parameters
    -----------
    fp : str
        The filepath.
    madeBy : {'Andor','MicroManager'}
        The software that made the image.
    
    Returns
    ----------
    tagDic : dict
        Keys can be any of ('T','F','M','Z','C')
        Values are the found tags.
    """
    tagDic = {}
    if madeBy=='Andor':
        fp = fp[:-4]
        endTagReg = r'(_(t|f|m|z|w)\d{3,9})$'
        # takes tags off end one by one
        tag = re.search(endTagReg,fp)
        foundTags = []
        while tag:
            foundTags.append(tag.group(1))
            fp = fp[:-len(tag.group(1))]
            tag = re.search(endTagReg,fp)
        for t in foundTags:
            if t[1]=='w':
                tagDic.update({'C':t})
            else:
                tagDic.update({t[1].upper():t})
    
    elif madeBy=='MicroManager':
        fTag = fp.split('MMStack_')[1][:-4]
        fTag = re.sub('.ome','',fTag)
        fTag = re.sub('_\d\d\d_\d\d\d','',fTag)
        #fTag = re.search(r'(MMStack_\d)',fp) # old way
        if fTag:
            tagDic.update({'F':fTag})
        mTag = re.search(r'(Pos_\d\d\d_\d\d\d)',fp)
        if mTag:
            tagDic.update({'M':mTag.group(1)})
    else:
        raise Exception(EM.md1)
    
    return tagDic



def unravel(T,F,M,Z,C,NT,NF,NM,NZ,NC):
    """
    this function converts 7D indices to their flat equivalent index
    given the shapes of those dimensions of course
    actually it only does 5D of the 7D, XY ignored here    
    """
    return T*NF*NM*NZ*NC + F*NM*NZ*NC + M*NZ*NC + Z*NC + C



def UDRL2LRUD(I,NY,NX):
    """
    Give this a list of indices for tiles in left-right-up-down ordering and 
    it returns the list of where you find those tiles in a up-down-right-left 
    ordered list of tiles. Hence it helps to convert UDLR -> LRUD.
    
    Parameters
    -----------
    I : 1d list
        the list of indices in LRUD for which you would like to find the 
        corresponding UDRL indices.
    NY,NX : int
        The sizes of the full montages.
    
    Returns
    -------
    I2 : 1d list
        Each element of the original list I converted to UDRL indices.
    """
    
    R = [i//NX for i in I]
    C = [i%NX for i in I]
    
    return [(NX-1-c)*NY + r for i,r,c in zip(I,R,C)]


def removePads(im,pads=None,retPad=False):
    """
    Removes padding from a 2D image by either detecting the blank (0) edges 
    or according to user provided padding. Padding is defined as 
    rows/columns of 0. It returns the image without padding and (optionally) 
    the padding that was removed so you can add it back later if you like.
    
    Parameters
    ----------
    im : 2D numpy.array
        The image.
    pads : None or [int,int]
        If None then it will find the padding by detecting blank rows/columns 
        at edges. Otherwise it gives the total number of blank pixels that are 
        to be removed from the [y,x]-axes. See code for how this total number 
        is divided between the two sides.
    retPad : bool
        Whether to return the pad along with cropped image.
    
    Returns
    -------
    im : 2D numpy.array
        The image without padding.
    pad : tuple of tuple of ints
        If returnPad then how many pixels were removed is returned in: 
        (top,bottom,left,right). In this case im and pad are a tuple.
    """
    ny,nx =im.shape
    if pads is None:
        for t in range(ny):
            if any(im[t,:]):
                break
        for b in reversed(range(ny)):
            if any(im[b,:]):
                break
        for l in range(nx):
            if any(im[:,l]):
                break
        for r in reversed(range(nx)):
            if any(im[:,r]):
                break
    else:
        t,b = [pads[0]//2,ny-math.ceil(pads[0]/2)-1]
        l,r = [pads[1]//2,nx-math.ceil(pads[1]/2)-1]
    if retPad:
        return (im[t:b+1,l:r+1],(t,ny-b-1,l,nx-r-1))
    else:
        return im[t:b+1,l:r+1]
    
    
def pad2Size(im,sizes):
    """
    Pads the image to the specified size, using the convention of 
    sessionStitcher to decide where to put extra pixels.
    
    Parameters
    ----------
    im : array-like
        The image you want to pad. Can be any dimension, always the last two 
        axes are the ones that will be padded.
    sizes : tuple
        The (ysize,xsize) that you pad to.
    
    Returns
    -------
    im : array like
        The padded image.
    """
    pY = sizes[0] - im.shape[-2]
    pX = sizes[1] - im.shape[-1]
    pY = ((pY//2,math.ceil(pY/2)),)
    pX = ((pX//2,math.ceil(pX/2)),)
    pad = ((0,0),)*(im.ndim - len(sizes)) + pY + pX
    return np.pad(im,pad)  


def takeWindow(im,win):
    """
    Extracts window from an image when window is given in format of 
    XFold.WindowDic, which is [[y,x],[y,x],[y,x],[y,x]]. Image is assumed to 
    be size of the template that the window was drawn on, no padding 
    considered.
    
    Parameters
    ----------
    im : numpy.array
        2D image that will be cropped.
    win : list of lists of ints
        The window in XFold.WindowDic format.
    """
    return im[win[0][0]:win[2][0],win[0][1]:win[2][1]]


def makeuint8(img,quantH=0.9,quantL=False):
    """
    Converts uint16 to uint8 with re-scaling to the max value. Can also do 
    clipping (max or max and min) to stop detail loss from anomalous high 
    values.
    """
    maxV = np.quantile(img,quantH)
    img[img>maxV] = maxV
    if quantL:
        minV = np.quantile(img,quantL)
        img[img<minV] = minV
    if quantL:
        return (255*((img-minV)/(maxV-minV))).astype('uint8')
    else:
        return (255*(img/maxV)).astype('uint8')
    
    
def ExtractProfileRectangle(data,outDir,outName=False,masks=None,
                            NXSegs=10,downsizeY=2,overwrite=False):
    """
    This saves csvs containing averaged pixel values taken from the image 
    data. NXSegs and downsizeY define a grid in which the mean of each 
    square is returned.

    Parameters
    ----------
    data : array-like, shape (NIm,sizeY,sizeX)
        The image data. One csv will be saved for each image along axis 0.
    outDir : str
        Path of directory to save csvs too. This directory will be created if 
        needed.
    outName : str or list of str
        The name of the csv(s). If False then it will create a name and number 
        according NIm. If you provide a list then the names correspond to the 
        images along axis 0 of the data.
    masks : array-like, shape (NIm,sizeY,sizeX) or (sizeY,sizeX)
        Image(s) which define(s) a region of arbitrary shape to decide which 
        pixels to include. This image should be binary with included regions 
        as white.
    NXSegs : int
        The number of segments to return along the x-axis. All pixel
        values are averaged within each segment. The X position in pixels
        of the middle of each segment will be given in the CSV row heading
        (measured relative to the window).
    downsizeY : int
        Factor to downsize y-axis length by. Pixels are averaged. Position
        put in CSV headings too.
    overwrite : bool
        Whether to allow csvs to be overwritten.

    Returns
    -------
    Nothing returned but csvs are saved. The csvs have NSegs+1 columns and
    1+NY//downsizeY rows. One separate csv for each image along data axis 0.
    """
    if len(data.shape)==2:
        data = data[np.newaxis]
    NIm,sizeY,sizeX = data.shape
    for i in range(NIm):
        # initiate np array and steps for collecting data
        dy = downsizeY
        NY = int(sizeY/dy)
        dx = int(sizeX/NXSegs)
        _csv = np.zeros((NY,NXSegs))
        for y in range(NY):
            for x in range(NXSegs):
                # input the data
                blockD = data[i,y*dy:(y+1)*dy,x*dx:(x+1)*dx].copy()
                if len(masks.shape)==3:
                    blockM = masks[i,y*dy:(y+1)*dy,x*dx:(x+1)*dx].copy()
                else:
                    assert len(masks.shape)==2,'masks not of shape we can handle'
                    blockM = masks[y*dy:(y+1)*dy,x*dx:(x+1)*dx].copy()
                result = blockD[blockM==1]
                if result.size==0:
                    _csv[y,x] = 'NaN'
                else:
                    _csv[y,x] = np.mean(result)
                del blockD
                del blockM
        del data
    
        # add x-slice and y-distance headings
        xlab = [str(dx*x+dx//2) for x in range(NXSegs)]
        xlab = np.array(['x='+x+' pixels' for x in xlab])
        ylab = ['y='+str(dy*y+dy//2)+'pixels' for y in range(NY)]
        ylab = np.array(['Y distance']+ylab)
        _csv = np.vstack((xlab,_csv))
        _csv = np.hstack((ylab.reshape((NY+1,1)),_csv))
    
        if not outName:
            outName1 = 'ExtractedValues_Image_'+str(i).zfill(4)+'.csv'
        else:
            if isinstance(outName,list):
                assert len(outName)==NIm,EM.ae9
                outName1 = outName[i]
            else:
                outName1 = outName
        if not os.path.exists(outDir):
            os.makedirs(outDir)
        outPath = os.path.join(outDir,outName1)
        if not overwrite:
            assert not os.path.exists(outPath),EM.ae5
    
        with open(outPath,'w',newline='') as file:
            writer = csv.writer(file)
            writer.writerows(_csv)

            
            
def adjustFilterEdges(filt,DF,tileA,tileB,molap):
    """
    This improves the homogenisation filter using the knowledge that the 
    bottom fraction of tileA overlaps with the top section of tileB, with a 
    fractional overlap size of molap.
    
    Parameters
    ----------
    filt : array-like shape (NY,NX)
        The original filter, e.g. calculated by BaSiC.
    DF : array-like shape (NY,NX)
        The original dar-fileld filter, e.g. calculated by BaSiC.        
    tileA : array-like shape (NY,NX)
        A tile in the montage where there is good signal all at the bottom.
    tileB : array-like shape (NY,NX)
        The tile in the montage directly below tileA.
    molap : float
        The decimal fraction of tile A and tileB that overlap.
    """
    
    # extract section of tiles and filter that should overlap
    ny,nx = tileA.shape
    segA_B = (tileA-DF)[ny-math.floor(ny*molap)-1:-1]
    segB_T = (tileB-DF)[:math.floor(ny*molap)]
    segF_B = filt[ny-math.floor(ny*molap)-1:-1]
    segF_T = filt[:math.floor(ny*molap)]
    
    ny_seg = segA_B.shape[0]
    
    # y is essentially the equation that says that the corrected image sections 
    # should be the same... solve that equation with best fit straight line
    # that gives you the factor to correct the filter with
    x = np.array(range(ny_seg))
    y = np.mean((segA_B/segB_T)/(segF_B/segF_T),axis=1)
    a,b = np.polyfit(x,y,1)
    
    A = np.ones((ny))
    for i in range(ny):
        if i > ny - ny_seg:
            A[i] = math.sqrt(a*(i - (ny - ny_seg)) + b)
        elif i < ny_seg:
            A[i] = 1/math.sqrt(a*i + b)            
    
    start_T = int(3*ny_seg/4)
    end_T = int(5*ny_seg/4)
    max_T = A[start_T]
    for i in range(start_T,end_T):
        A[i] = max_T + (i-start_T)*((1-max_T)/(ny_seg/2))
        
    start_B = int(ny-ny_seg-(ny_seg/4))
    end_B = int(ny-ny_seg+(ny_seg/4))
    max_B = A[end_B]
    for i in range(start_B,end_B):
        A[i] = 1 + (i-start_B)*((max_B-1)/(ny_seg/2))        
        
    A = A[:,np.newaxis]
    A = np.tile(A,(1,nx))
    
    filt = filt*A
    filt = filt/np.mean(filt)
    
    return (A,filt)



def signalNoiseMasks(mask,mask2=None):
    """
    You provide a mask and it returns two masks, one of definite signal 
    and one of definite noise. I.e. it erodes/dilates/inverts the provided 
    mask of signal to be sure.
    
    mask : array-like
        The mask of a segmentation of signal.
    mask2 : False or array-like or str
        A further mask to restrict the region from which signal is taken.
    
    Returns
    -------
    sig : array-like
        The mask of where signal definitely is.
    noise : array-like
        The mask of where noise definitely is.
    """
    # nuclei and noise masks
    kernel = np.ones((3,3),np.uint8)
    sig = cv.erode(mask,kernel)
    mask2 = cv.erode(mask.astype('uint16'),kernel)
    nucleiMask = np.logical_and(nucleiMask,mask2)
    noise = 1-cv.dilate(mask,kernel)
    noise = np.logical_and(noise,mask2)
    
    return sig,noise