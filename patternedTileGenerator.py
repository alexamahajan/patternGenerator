# patternedTileGenerator.py

import maya.cmds as cmds
import functools
import random
import math

# Initialize random seed with current time
from datetime import datetime
random.seed( datetime.now() )

# Tile pattern function
def createTilePattern(patternType, patternWidth, patternDepth, tileWidth, tileHeight, tileDepth, tileSpacingAmount, heightVariationIntensity):
    
    # Variables
    rowOffset = tileWidth / 2
    currRowPosition = 0
    
    tileSpacingAmount = float(tileSpacingAmount)
    tileSpacingEquation = tileWidth / tileSpacingAmount
    
    heightVariationIntensity *= 0.1
    
    # Delete old tiles
    def deleteOldTiles():
        tileList = cmds.ls( patternType + '_patternGroup*' )
        if len( tileList ) > 0:
            cmds.delete( tileList )
            
    deleteOldTiles()
    
    # Hide previous tile groups
    def hidePreviousPatterns():
        patternTypes = ['Basketweave', 'Chevron', 'Herringbone', 'Brick', 'Panels']
        for i in range(0, len(patternTypes)):
            patternGroup = cmds.ls( patternTypes[i] + '_patternGroup*' )
            cmds.hide( patternGroup )
            
    hidePreviousPatterns()
    
    # Brick Pattern
    if patternType == 'Brick':
        
        # Variables
        numTilesPerRow = int( math.ceil( patternWidth / ( tileWidth + tileSpacingEquation ) ) )
        numRows = int( math.ceil( patternDepth / ( tileDepth + tileSpacingEquation ) ) )
        
        # Create parent tile
        parentTile = cmds.polyCube( w=tileWidth, h=tileHeight, d=tileDepth, name='tile' )
        tileInstanceName = parentTile[0]
        tileGroup = cmds.group( empty=True, name=patternType + '_patternGroup#' )
        
        for i in range ( 0, numRows ):
            
            currTilePosition = 0
            currRowGroup = cmds.group( empty=True, name=patternType + '_row#' )
            cmds.parent( currRowGroup, tileGroup )
            
            # Rows
            for j in range ( 0, numTilesPerRow ):
                
                # Create tile instance & add to group
                currTile = cmds.instance( tileInstanceName, name=patternType + '_tile#' )
                cmds.parent( currTile, currRowGroup )
                
                # Randomization used for variations in tile textures and heights
                if heightVariationIntensity != 0:
                    cmds.move( currTilePosition + tileWidth + tileSpacingEquation, random.uniform(0.0, heightVariationIntensity), 0, currTile )
                else:
                    cmds.move( currTilePosition + tileWidth + tileSpacingEquation, 0, 0, currTile )
                
                # Update next tile placement position    
                currTilePosition += ( tileWidth + tileSpacingEquation )
            
            cmds.xform( currRowGroup, centerPivots=True )
            
            # Alternating row offset
            if ( i % 2 ) == 0:
                cmds.move( 0, 0, currRowPosition, currRowGroup )
            else:
                cmds.move( rowOffset, 0, currRowPosition, currRowGroup )
            
            # Update next row placement position    
            currRowPosition += ( tileDepth + tileSpacingEquation )
            
        # Center pivot & center pattern at origin
        cmds.xform( tileGroup, centerPivots=True )
        cmds.move( 0, 0, 0, tileGroup, rpr=True )
    # Basketweave Pattern
    elif patternType == 'Basketweave':
        
        # Variables
        numRows = int( math.ceil( patternDepth / ( tileWidth + tileSpacingEquation ) ) )
        
        # Create parent tile
        tileWidth = (tileDepth * 2) + tileSpacingEquation
        parentTile = cmds.polyCube( w=tileWidth, h=tileHeight, d=tileDepth, name='tile' )
        tileInstanceName = parentTile[0]
        tileGroup = cmds.group( empty=True, name=patternType + '_patternGroup#' )
        
        def verticalBasketweaveBlock():
            # Create vertical block
            currTilePosition = 0
            verticalBlock = cmds.group( empty=True, name=patternType + '_block#' )
            cmds.parent( verticalBlock, tileGroup )
            
            for i in range ( 0, 2 ):
                # Create tile instance & add to group
                currTile = cmds.instance( tileInstanceName, name=patternType + '_tile#' )
                cmds.parent( currTile, verticalBlock )
                cmds.rotate( 0, 90, 0, currTile )
                # Randomization used for variations in tile textures and heights
                if heightVariationIntensity != 0:
                    cmds.move( 0, random.uniform(0.0, heightVariationIntensity), 0, currTile )
                
                if i == 1:
                    cmds.move( tileDepth + tileSpacingEquation, 0, 0, currTile )
                    
            cmds.xform( verticalBlock, centerPivots=True )
                    
            return verticalBlock
                    
        def horizontalBasketweaveBlock():
            # Create horizontal block
            horizontalBlock = verticalBasketweaveBlock()
            cmds.rotate( 0, 90, 0, horizontalBlock )
                    
            return horizontalBlock
 
        verticalBlockWidth = (tileDepth * 2) + tileSpacingEquation
        hortizontalBlockWidth = tileWidth
        
        # Odd rows
        def oddRowBasketweave():
            lengthOfRow = 0
            currBlockPosition = 0
            index = 0
            
            currRowGroup = cmds.group( empty=True, name=patternType + '_row#' )
            cmds.parent( currRowGroup, tileGroup )
            # While length of row is less than desired pattern width, add another block
            while lengthOfRow < patternWidth:
                if (index % 2) == 0:
                    currBlock = verticalBasketweaveBlock()
                    cmds.parent( currBlock, currRowGroup )
                    cmds.move( currBlockPosition + hortizontalBlockWidth, 0, 0, currBlock )
                    lengthOfRow += verticalBlockWidth
                    currBlockPosition += (verticalBlockWidth + tileSpacingEquation)
                    index += 1    
                else:
                    currBlock = horizontalBasketweaveBlock()
                    cmds.parent( currBlock, currRowGroup )
                    cmds.move( currBlockPosition + verticalBlockWidth, 0, 0, currBlock ) 
                    lengthOfRow += hortizontalBlockWidth
                    currBlockPosition += (hortizontalBlockWidth + tileSpacingEquation)
                    index += 1
                    
            cmds.xform( currRowGroup, centerPivots=True )
            
            return currRowGroup
        # Even rows
        def evenRowBasketweave():
            lengthOfRow = 0
            currBlockPosition = 0
            index = 0
            
            currRowGroup = cmds.group( empty=True, name=patternType + '_row#' )
            cmds.parent( currRowGroup, tileGroup )
            # While length of row is less than desired pattern width, add another block
            while lengthOfRow < patternWidth:
                if (index % 2) == 1:
                    currBlock = verticalBasketweaveBlock()
                    cmds.parent( currBlock, currRowGroup )
                    cmds.move( currBlockPosition + hortizontalBlockWidth, 0, 0, currBlock )
                    lengthOfRow += verticalBlockWidth
                    currBlockPosition += (verticalBlockWidth + tileSpacingEquation)
                    index += 1    
                else:
                    currBlock = horizontalBasketweaveBlock()
                    cmds.parent( currBlock, currRowGroup )
                    cmds.move( currBlockPosition + verticalBlockWidth, 0, 0, currBlock ) 
                    lengthOfRow += hortizontalBlockWidth
                    currBlockPosition += (hortizontalBlockWidth + tileSpacingEquation)
                    index += 1
                    
            cmds.xform( currRowGroup, centerPivots=True )
            
            return currRowGroup, lengthOfRow
        currRowPosition = 0
        for i in range ( 0, numRows ): 
            if (i % 2) == 0:           
                currRow = oddRowBasketweave()
            else:
                currRow, rowLength = evenRowBasketweave()
            cmds.move( 0, 0, currRowPosition + verticalBlockWidth + tileSpacingEquation, currRow )  
            currRowPosition += ( verticalBlockWidth + tileSpacingEquation )
            
        # Center pivot & center pattern at origin
        cmds.xform( tileGroup, centerPivots=True )
        cmds.move( 0, 0, 0, tileGroup, rpr=True )
    else:
        print('Pattern choice not available')
    
    # Delete parent tile    
    cmds.delete( tileInstanceName )
    
    # Deselect all tiles
    cmds.select( clear=True )

# UI Window
class PatternGeneratorUI():
    
    # Constructor
    def __init__(self):
        
        self.windowID = 'patternedTileGeneratorWindow'
    
        # Check if window already open & close it
        if cmds.window( self.windowID, exists=True ):
            cmds.deleteUI( self.windowID )
        
        # Create new window
        self.window = cmds.window( self.windowID, title='Patterned Tile Generator', resizeToFitChildren=True)
        cmds.rowColumnLayout( numberOfColumns=3, columnWidth=[ (1,125), (2,115), (3,50) ], columnOffset=[ (1,'right',3) ] )
        
        # Formatting - Blank row
        cmds.separator( h=15, style='none' )
        cmds.separator( h=15, style='none' )
        cmds.separator( h=15, style='none' )
        
        # Pattern type
        cmds.text( label='Pattern Type' )
        self.patternTypeOptionMenu = cmds.optionMenu( 'patternTypeOptionMenu', changeCommand=self.tilePattern )
        basketweave = cmds.menuItem( label='Basketweave' )
        cmds.menuItem( label='Chevron' )
        cmds.menuItem( label='Herringbone' )
        cmds.menuItem( label='Brick' )
        cmds.menuItem( label='Panels' )
        cmds.separator( h=10, style='none' )
            
        # Formatting - Blank row
        cmds.separator( h=10, style='none' )
        cmds.separator( h=10, style='none' )
        cmds.separator( h=10, style='none' )
        
        # Pattern dimensions
        cmds.text( label='Pattern Width' )
        self.patternWidth = cmds.intField( minValue=0, maxValue=100, value=25, changeCommand=self.tilePattern )
        cmds.separator( h=10, style='none' )
        
        cmds.text( label='Pattern Height' )
        self.patternHeight = cmds.intField( minValue=0, maxValue=100, value=15, changeCommand=self.tilePattern )
        cmds.separator( h=10, style='none' )
        
        # Formatting - Blank row
        cmds.separator( h=10, style='none' )
        cmds.separator( h=10, style='none' )
        cmds.separator( h=10, style='none' )
        
        # Tile dimensions
        cmds.text( label='Tile Width' )
        self.tileWidth = cmds.intField( minValue=1, maxValue=10, value=4, changeCommand=self.tilePattern )
        cmds.separator( h=10, style='none' )
        
        cmds.text( label='Tile Height' )
        self.tileHeight = cmds.intField( minValue=1, maxValue=10, value=1, changeCommand=self.tilePattern )
        cmds.separator( h=10, style='none' )
        
        cmds.text( label='Tile Depth' )
        self.tileDepth = cmds.intField( minValue=1, maxValue=10, value=2, changeCommand=self.tilePattern )
        cmds.separator( h=10, style='none' )
        
        # Formatting - Blank row
        cmds.separator( h=10, style='none' )
        cmds.separator( h=10, style='none' )
        cmds.separator( h=10, style='none' )
        
        # Tile spacing
        cmds.text( label='Tile Spacing' )
        self.tileSpacing = cmds.intSlider( minValue=1, maxValue=100, value=25, step=2, dragCommand=self.tilePattern )
        cmds.separator( h=10, style='none' )
        
        # Formatting - Blank row
        cmds.separator( h=10, style='none' )
        cmds.separator( h=10, style='none' )
        cmds.separator( h=10, style='none' )
        
        # Tile height variation
        cmds.text( label='Height Variation' )
        self.tileHeightVariation = cmds.intSlider( minValue=0, maxValue=20, value=0, step=1, dragCommand=self.tilePattern )
        cmds.separator( h=10, style='none' )
        
        # Formatting - Blank row
        cmds.separator( h=15, style='none' )
        cmds.separator( h=15, style='none' )
        cmds.separator( h=15, style='none' )
        
        # Display window   
        cmds.showWindow()
        
    def tilePattern(self, *args):
        
        # Pattern type
        patternType = cmds.optionMenu( self.patternTypeOptionMenu, query=True, value=True )
        print(patternType)
        
        # Pattern dimensions
        patternWidth = cmds.intField( self.patternWidth, query=True, value=True)
        patternHeight = cmds.intField( self.patternHeight, query=True, value=True)
        print(patternWidth, patternHeight)
        
        # Tile dimensions
        tileWidth = cmds.intField( self.tileWidth, query=True, value=True)
        tileHeight = cmds.intField( self.tileHeight, query=True, value=True)
        tileDepth = cmds.intField( self.tileDepth, query=True, value=True)
        print(tileWidth, tileHeight, tileDepth)
        
        #Tile positioning
        tileSpacing = cmds.intSlider( self.tileSpacing, query=True, value=True )
        tileHeightVariation = cmds.intSlider( self.tileHeightVariation, query=True, value=True )
        print(tileSpacing, tileHeightVariation)
        
        '''
        if patternType == 'Basketweave':
            cmds.intField( self.tileWidth, value=5)
        '''
        # Function call
        createTilePattern(patternType, patternWidth, patternHeight, tileWidth, tileHeight, tileDepth, tileSpacing, tileHeightVariation)
    
# UI call    
window = PatternGeneratorUI()