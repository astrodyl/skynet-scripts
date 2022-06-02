import pyfits as py
import numpy as np

"""
Convert Skynet's radio mapping algorithm's
output from txt to fits. Add wcs coordinates
so ra/dec info is available as well.

Skynet ouputs: main.txt, coordinateInfo.txt
"""

TXTFILES = ['main']
FITFILES = ['hdul']
PARAMFILE = 'CoordinateInfo'

class wcsValues:
    centerDec = 0.0
    centerRA = 0.0
    centerXPixel = 0.0
    centerYPixel = 0.0
    pixelSizeDeg = 0.0


def processCoordinateFile():
    coordinateFile = open(PARAMFILE + ".txt")
    s = coordinateFile.read()
    s = s.split('\n')
    wcs = wcsValues()

    for line in s:
        #non wcs members
        if ("beam (deg):" in line):
            splitLine = line.split(':')
            beamDeg = float(splitLine[1])
        if ("pixel size (beams):" in line):
            splitLine = line.split(':')
            pixelSizeBeam = float(splitLine[1])

        #wcs members
        if ("center dec (deg):" in line):
            splitLine = line.split(':')
            wcs.centerDec = float(splitLine[1])
        if ("center ra (deg):" in line):
            splitLine = line.split(':')
            wcs.centerRA = float(splitLine[1])
        if ("center pixel (x):" in line):
            splitLine = line.split(':')
            wcs.centerXPixel = float(splitLine[1])
        if ("center pixel (y):" in line):
            splitLine = line.split(':')
            wcs.centerYPixel = float(splitLine[1])
    
    wcs.pixelSizeDeg = pixelSizeBeam * beamDeg
    return wcs


def convertTXTtoFITS(filename):
    imageData = np.genfromtxt(filename+".txt", delimiter='\t')
    py.writeto(filename+".fits", imageData, clobber=True)


def addCoordinates(wcs, filename):
    f = py.open(filename + ".fits", 'update')
	
    for i in range(0, len(f)):
        f[i].header['CTYPE1'] = 'RA---SIN'
        f[i].header['CTYPE2'] = 'DEC--SIN'
        f[i].header['CUNIT1'] = 'deg     '
        f[i].header['CUNIT2'] = 'deg     '
        f[i].header['CRVAL1'] = wcs.centerRA
        f[i].header['CRVAL2'] = wcs.centerDec
        f[i].header['CDELT1'] = -1 * wcs.pixelSizeDeg
        f[i].header['CDELT2'] = wcs.pixelSizeDeg
        f[i].header['CRPIX1'] = wcs.centerXPixel
        f[i].header['CRPIX2'] = wcs.centerYPixel
    
    f.flush()
    f.close()

# convert output from Skynet radio mapping algorithm to fits file
def makeFiles():
    for ft in TXTFILES:
        try:
            convertTXTtoFITS(ft)
        except IOError:
            print("File type {0} not found! Continuing...").format(ft)
            
    print("FITS file creation complete.")

# add wcs to fits file (coordinate info when hovering over pixel)
def coordinateAdditionHandler():
    try:
        wcs = processCoordinateFile()
        if wcs is None:
            return
    except IOError:
        print("Coordinate file not found! Coordinate addition failed. Exiting.")
        return
    
    for ft in FITFILES:
        try:
            addCoordinates(wcs, ft)
        except IOError:
            print("File type {0} not found! Continuing...").format(ft)
        
    print("Coordinate addition complete")

def main():
    makeFiles()
    coordinateAdditionHandler()

main()