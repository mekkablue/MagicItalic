# encoding: utf-8

###########################################################################################################
#
#
# Filter with dialog Plugin
#
# Read the docs:
# https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates/Filter%20with%20Dialog
#
# For help on the use of Xcode:
# https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates
#
#
###########################################################################################################

from __future__ import division, print_function, unicode_literals
import objc
from GlyphsApp import Glyphs, GSLayer, GSSMOOTH, GSOFFCURVE
from GlyphsApp.plugins import FilterWithDialog
from AppKit import NSPoint


def straightenBCPs(layer):
	# ported from mekkablue’s RealignHandles filter plug-in

	def triplet(n1, n2, n3):
		return (*n1.position, *n2.position, *n3.position)

	def closestPointOnLine(P, A, B):
		# vector of line AB
		AB = NSPoint(B.x - A.x, B.y - A.y)
		# vector from point A to point P
		AP = NSPoint(P.x - A.x, P.y - A.y)
		# dot product of AB and AP
		dotProduct = AB.x * AP.x + AB.y * AP.y
		ABsquared = AB.x**2 + AB.y**2
		t = dotProduct / ABsquared
		x = A.x + t * AB.x
		y = A.y + t * AB.y
		return NSPoint(x, y)

	def ortho(n1, n2):
		xDiff = n1.x - n2.x
		yDiff = n1.y - n2.y
		# must not have the same coordinates,
		# and either vertical or horizontal:
		if xDiff != yDiff and xDiff * yDiff == 0.0:
			return True
		return False

	handleCount = 0
	for p in layer.paths:
		for n in p.nodes:
			if n.connection != GSSMOOTH:
				continue
			nn, pn = n.nextNode, n.prevNode
			if all((nn.type == GSOFFCURVE, pn.type == GSOFFCURVE)):
				# surrounding points are BCPs
				smoothen, center, opposite = None, None, None
				for handle in (nn, pn):
					if ortho(handle, n):
						center = n
						opposite = handle
						smoothen = nn if nn != handle else pn
						oldPos = triplet(smoothen, center, opposite)
						p.setSmooth_withCenterNode_oppositeNode_(smoothen, center, opposite)
						if oldPos != triplet(smoothen, center, opposite):
							handleCount += 1
						break
				if smoothen == center == opposite is None:
					oldPos = triplet(n, nn, pn)
					n.position = closestPointOnLine(n.position, nn, pn)
					if oldPos != triplet(n, nn, pn):
						handleCount += 1
			elif n.type != GSOFFCURVE and (nn.type, pn.type).count(GSOFFCURVE) == 1:
				# only one of the surrounding points is a BCP
				center = n
				if nn.type == GSOFFCURVE:
					smoothen = nn
					opposite = pn
				elif pn.type == GSOFFCURVE:
					smoothen = pn
					opposite = nn
				else:
					continue  # should never occur
				oldPos = triplet(smoothen, center, opposite)
				p.setSmooth_withCenterNode_oppositeNode_(smoothen, center, opposite)
				if oldPos != triplet(smoothen, center, opposite):
					handleCount += 1
	return handleCount


class MagicItalic(FilterWithDialog):
	# Definitions of IBOutlets

	# The NSView object from the User Interface. Keep this here!
	dialog = objc.IBOutlet()

	# Text field in dialog
	italicAngleField = objc.IBOutlet()
	correctContrastField = objc.IBOutlet()
	correctShapeField = objc.IBOutlet()
	correctThicknessField = objc.IBOutlet()
	hStemField = objc.IBOutlet()
	vStemField = objc.IBOutlet()
	realignHandlesCheckbox = objc.IBOutlet()

	@objc.python_method
	def settings(self):
		self.menuName = Glyphs.localize({
			'en': 'Magic Italic',
		})

		# Word on Run Button (default: Apply)
		self.actionButtonLabel = Glyphs.localize({
			'en': 'Italify',
		})

		# Load dialog from .nib (without .extension)
		self.loadNib('IBdialog', __file__)

	# On dialog show
	@objc.python_method
	def start(self):

		# Set default value
		Glyphs.registerDefault('com.mekkablue.MagicItalic.italicAngle', 10.0)
		Glyphs.registerDefault('com.mekkablue.MagicItalic.correctContrast', 20)
		Glyphs.registerDefault('com.mekkablue.MagicItalic.correctShape', 30)
		Glyphs.registerDefault('com.mekkablue.MagicItalic.correctThickness', 100)
		Glyphs.registerDefault('com.mekkablue.MagicItalic.hStem', "*")
		Glyphs.registerDefault('com.mekkablue.MagicItalic.vStem', "*")
		Glyphs.registerDefault('com.mekkablue.MagicItalic.realignHandles', True)

		# Set value of text field
		self.italicAngleField.setStringValue_(Glyphs.defaults['com.mekkablue.MagicItalic.italicAngle'])
		self.correctContrastField.setStringValue_(Glyphs.defaults['com.mekkablue.MagicItalic.correctContrast'])
		self.correctShapeField.setStringValue_(Glyphs.defaults['com.mekkablue.MagicItalic.correctShape'])
		self.correctThicknessField.setStringValue_(Glyphs.defaults['com.mekkablue.MagicItalic.correctThickness'])
		self.hStemField.setStringValue_(Glyphs.defaults['com.mekkablue.MagicItalic.hStem'])
		self.vStemField.setStringValue_(Glyphs.defaults['com.mekkablue.MagicItalic.vStem'])
		self.realignHandlesCheckbox.setState_(Glyphs.defaults['com.mekkablue.MagicItalic.realignHandles'])

		# Set focus to text field
		self.italicAngleField.becomeFirstResponder()

	# Actions triggered by UI
	@objc.IBAction
	def setItalicAngle_(self, sender):
		Glyphs.defaults['com.mekkablue.MagicItalic.italicAngle'] = sender.floatValue()
		self.update()

	@objc.IBAction
	def setCorrectContrast_(self, sender):
		Glyphs.defaults['com.mekkablue.MagicItalic.correctContrast'] = sender.floatValue()
		self.update()

	@objc.IBAction
	def setCorrectShape_(self, sender):
		Glyphs.defaults['com.mekkablue.MagicItalic.correctShape'] = sender.floatValue()
		self.update()

	@objc.IBAction
	def setCorrectThickness_(self, sender):
		Glyphs.defaults['com.mekkablue.MagicItalic.correctThickness'] = sender.floatValue()
		self.update()

	@objc.IBAction
	def setHStem_(self, sender):
		Glyphs.defaults['com.mekkablue.MagicItalic.hStem'] = sender.stringValue()
		self.update()

	@objc.IBAction
	def setVStem_(self, sender):
		Glyphs.defaults['com.mekkablue.MagicItalic.vStem'] = sender.stringValue()
		self.update()

	@objc.IBAction
	def setRealignHandles_(self, sender):
		Glyphs.defaults['com.mekkablue.MagicItalic.realignHandles'] = bool(sender.state())
		self.update()

	# Actual filter
	@objc.python_method
	def filter(self, layer, inEditView, customParameters):
		if not isinstance(layer, GSLayer):
			return

		if not layer.shapes:
			return

		if "italicAngle" in customParameters:
			italicAngle = customParameters['italicAngle']
		else:
			italicAngle = float(Glyphs.defaults['com.mekkablue.MagicItalic.italicAngle'])
		if "correctContrast" in customParameters:
			correctContrast = customParameters['correctContrast']
		else:
			correctContrast = float(Glyphs.defaults['com.mekkablue.MagicItalic.correctContrast'])
		if "correctShape" in customParameters:
			correctShape = customParameters['correctShape']
		else:
			correctShape = float(Glyphs.defaults['com.mekkablue.MagicItalic.correctShape'])
		if "correctThickness" in customParameters:
			correctThickness = customParameters['correctThickness']
		else:
			correctThickness = float(Glyphs.defaults['com.mekkablue.MagicItalic.correctThickness'])
		if "hStem" in customParameters:
			hStem = customParameters['hStem']
		else:
			hStem = Glyphs.defaults['com.mekkablue.MagicItalic.hStem']
		if "vStem" in customParameters:
			vStem = customParameters['vStem']
		else:
			vStem = Glyphs.defaults['com.mekkablue.MagicItalic.vStem']
		if "realignHandles" in customParameters:
			realignHandles = customParameters['realignHandles']
		else:
			realignHandles = Glyphs.defaults['com.mekkablue.MagicItalic.realignHandles']

		# secret italification
		def firstStem(font, h=True):
			for i in range(len(font.stems)):
				if font.stems[i].horizontal == h:
					return font.selectedFontMaster.stems[i]
			return 90 # fallback
		
		font = layer.parent.parent
		halfXHeight = layer.master.xHeight / 2
		
		override = False
		if override:
			italicAngle = font.selectedFontMaster.italicAngle
			hStem = firstStem(font)
			vStem = firstStem(font, h=False)
		
		if hStem == "*":
			hStem = firstStem(font)
		else:
			hStem = float(hStem)
		
		if vStem == "*":
			vStem = firstStem(font, h=False)
		else:
			vStem = float(vStem)
			
		layer.doSlantingCorrectionWithAngle_checkSelection_correctContrast_correctShape_correctThickness_horizontalStem_verticalStem_center_(
			italicAngle,  # angle
			False, # for selection only?
			correctContrast / 100.0,   # correct contrast  0...1
			correctShape / 100.0,      # correct shape     0...1
			correctThickness / 100.0,  # correct thickness 0...1
			hStem, # H stem
			vStem, # V stem
			(layer.bounds.origin.x + layer.bounds.size.width/2, halfXHeight),   # center
		)

		layer.slantX_origin_doCorrection_checkSelection_(
			italicAngle,
			halfXHeight,
			False,
			False,
			)

		if realignHandles:
			straightenBCPs(layer)

	@objc.python_method
	def generateCustomParameter(self):
		return f"{self.__class__.__name__}; italicAngle: {Glyphs.defaults['com.mekkablue.MagicItalic.italicAngle']}; correctContrast: {Glyphs.defaults['com.mekkablue.MagicItalic.correctContrast']}; correctShape: {Glyphs.defaults['com.mekkablue.MagicItalic.correctShape']}; correctThickness: {Glyphs.defaults['com.mekkablue.MagicItalic.correctThickness']}; hStem: {Glyphs.defaults['com.mekkablue.MagicItalic.hStem']}; vStem: {Glyphs.defaults['com.mekkablue.MagicItalic.vStem']}; realignHandles: {Glyphs.defaults['com.mekkablue.MagicItalic.realignHandles']};"

	@objc.python_method
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__
