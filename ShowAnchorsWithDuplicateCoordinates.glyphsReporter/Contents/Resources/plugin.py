# encoding: utf-8
from __future__ import division, print_function, unicode_literals

###########################################################################################################
#
#
#	Reporter Plugin
#
#	Read the docs:
#	https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates/Reporter
#
#
###########################################################################################################

import objc
from GlyphsApp import Glyphs, distance
from GlyphsApp.plugins import ReporterPlugin
from Cocoa import NSBezierPath, NSColor, NSClassFromString, NSRect, NSPoint, NSSize


class ShowAnchorsWithDuplicateCoordinates(ReporterPlugin):

	@objc.python_method
	def settings(self):
		self.menuName = Glyphs.localize({
			'en': 'Anchors with Duplicate Coordinates',
			'de': 'Anker mit selben Koordinaten',
			'es': 'anclas con mismas coordenadas',
			'fr': 'ancres avec mêmes coordonnées',
			'pt': 'âncoras com as mesmas coordenadas',
		})

	@objc.python_method
	def conditionsAreMetForDrawing(self):
		"""
		Don't activate if text or pan (hand) tool are active.
		"""
		currentController = self.controller.windowController()
		if currentController:
			tool = currentController.toolDrawDelegate()
			textToolIsActive = tool.isKindOfClass_(NSClassFromString("GlyphsToolText"))
			handToolIsActive = tool.isKindOfClass_(NSClassFromString("GlyphsToolHand"))
			if not textToolIsActive and not handToolIsActive:
				return True
		return False

	@objc.python_method
	def background(self, layer):
		if self.conditionsAreMetForDrawing():
			self.drawCirclesAroundDoubleAnchors(layer)

	@objc.python_method
	def handleSize(self):
		# calculate handle size:
		handleSizes = (5, 8, 12) # possible user settings
		handleSizeIndex = Glyphs.handleSize # user choice in Glyphs > Preferences > User Preferences > Handle Size
		handleSize = handleSizes[handleSizeIndex] * self.getScale()**-0.9 # scaled diameter
		return handleSize

	@objc.python_method
	def drawCirclesAroundDoubleAnchors(self, layer):
		collectedCoords = []

		anchorCoordinates = [a.position for a in layer.anchors]
		for i, pos in enumerate(anchorCoordinates):
			for otherPos in anchorCoordinates[i + 1:]:
				if distance(pos, otherPos) < 1.0:
					collectedCoords.append(pos)

		if collectedCoords:
			circleSize = self.handleSize() * 2
			for position in collectedCoords:
				# # selected handles are a little bigger:
				# if node.selected:
				# 	circleSize *= 1.45
				rect = NSRect()
				rect.origin = NSPoint(position.x - circleSize / 2, position.y - circleSize / 2)
				rect.size = NSSize(circleSize, circleSize)
				circle = NSBezierPath.bezierPathWithOvalInRect_(rect)
				circle.setLineWidth_(6.0 / self.getScale())
				NSColor.redColor().set()
				circle.stroke()
				circle.setLineWidth_(2.0 / self.getScale())
				NSColor.yellowColor().set()
				circle.stroke()

	@objc.python_method
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__
