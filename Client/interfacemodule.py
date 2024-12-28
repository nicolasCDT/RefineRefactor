# In this file carefull : your files can be not like mine.
# Don't forget to copy/paste you current code in else case.

# In __MakeDialogs method, change dlgRefine initialization like that:
		if app.MULTIPLE_REFINE:
			self.dlgRefineNew = uiRefine.RefineDialogNew()
			self.dlgRefineNew.Hide()
		else:
			self.dlgRefine = uiRefine.RefineDialog()
			self.dlgRefine.Hide()


# In Close method, change like that :
		if app.MULTIPLE_REFINE:
			if self.dlgRefineNew:
				self.dlgRefineNew.Destroy()
		else:
			if self.dlgRefine:
				self.dlgRefine.Destroy()
# And :

		if app.MULTIPLE_REFINE:
			del self.dlgRefineNew
		else:
			del self.dlgRefine
		del self.wndGuildBuilding


# Add: 
	def CheckRefineDialog(self, isFail):
		self.dlgRefineNew.CheckRefine(isFail)


# Change OpenRefineDialog like that:
	if app.MULTIPLE_REFINE:
		def OpenRefineDialog(self, targetItemPos, type, data):
			self.dlgRefineNew.Open(targetItemPos, type, data)
	else:
		def OpenRefineDialog(self, targetItemPos, nextGradeItemVnum, cost, prob, type):
			self.dlgRefine.Open(targetItemPos, nextGradeItemVnum, cost, prob, type)