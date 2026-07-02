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
from GlyphsApp import Glyphs, GSLayer
from GlyphsApp.plugins import FilterWithDialog
from AppKit import NSPoint


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

		# Set value of text field
		self.italicAngleField.setStringValue_(Glyphs.defaults['com.mekkablue.MagicItalic.italicAngle'])
		self.correctContrastField.setStringValue_(Glyphs.defaults['com.mekkablue.MagicItalic.correctContrast'])
		self.correctShapeField.setStringValue_(Glyphs.defaults['com.mekkablue.MagicItalic.correctShape'])
		self.correctThicknessField.setStringValue_(Glyphs.defaults['com.mekkablue.MagicItalic.correctThickness'])
		self.hStemField.setStringValue_(Glyphs.defaults['com.mekkablue.MagicItalic.hStem'])
		self.vStemField.setStringValue_(Glyphs.defaults['com.mekkablue.MagicItalic.vStem'])

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

	@objc.python_method
	def generateCustomParameter(self):
		return f"{self.__class__.__name__}; italicAngle: {Glyphs.defaults['com.mekkablue.MagicItalic.italicAngle']}; correctContrast: {Glyphs.defaults['com.mekkablue.MagicItalic.correctContrast']}; correctShape: {Glyphs.defaults['com.mekkablue.MagicItalic.correctShape']}; correctThickness: {Glyphs.defaults['com.mekkablue.MagicItalic.correctThickness']}; hStem: {Glyphs.defaults['com.mekkablue.MagicItalic.hStem']}; vStem: {Glyphs.defaults['com.mekkablue.MagicItalic.vStem']};"

	@objc.python_method
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__
