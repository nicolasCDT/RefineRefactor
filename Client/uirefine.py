#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Replace RefineDialog class with your class (in case where you delete #define)

import app
import net
import player
import item
import ui
import uiToolTip
import localeInfo
import uiCommon
import constInfo


class RefineDialog(ui.ScriptWindow):

	makeSocketSuccessPercentage = ( 100, 33, 20, 15, 10, 5, 0 )
	upgradeStoneSuccessPercentage = ( 30, 29, 28, 27, 26, 25, 24, 23, 22 )
	upgradeArmorSuccessPercentage = ( 99, 66, 33, 33, 33, 33, 33, 33, 33 )
	upgradeAccessorySuccessPercentage = ( 99, 88, 77, 66, 33, 33, 33, 33, 33 )
	upgradeSuccessPercentage = ( 99, 66, 33, 33, 33, 33, 33, 33, 33 )

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__LoadScript()

		self.scrollItemPos = 0
		self.targetItemPos = 0

	def __LoadScript(self):

		self.__LoadQuestionDialog()

		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "refinedialog.py")

		except:
			import exception
			exception.abort("RefineDialog.__LoadScript.LoadObject")

		try:
			self.board = self.GetChild("Board")
			self.titleBar = self.GetChild("TitleBar")
			self.successPercentage = self.GetChild("SuccessPercentage")
			self.GetChild("AcceptButton").SetEvent(self.OpenQuestionDialog)
			self.GetChild("CancelButton").SetEvent(self.Close)
		except:
			import exception
			exception.abort("RefineDialog.__LoadScript.BindObject")
		if constInfo.ENABLE_REFINE_PCT:
			self.successPercentage.Show()
		else:
			self.successPercentage.Hide()

		toolTip = uiToolTip.ItemToolTip()
		toolTip.SetParent(self)
		toolTip.SetPosition(15, 38)
		toolTip.SetFollow(False)
		toolTip.Show()
		self.toolTip = toolTip

		self.titleBar.SetCloseEvent(ui.__mem_func__(self.Close))

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __LoadQuestionDialog(self):
		self.dlgQuestion = ui.ScriptWindow()

		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self.dlgQuestion, "questiondialog2.py")
		except:
			import exception
			exception.abort("RefineDialog.__LoadQuestionDialog.LoadScript")

		try:
			GetObject=self.dlgQuestion.GetChild
			GetObject("message1").SetText(localeInfo.REFINE_DESTROY_WARNING)
			GetObject("message2").SetText(localeInfo.REFINE_WARNING2)
			GetObject("accept").SetEvent(ui.__mem_func__(self.Accept))
			GetObject("cancel").SetEvent(ui.__mem_func__(self.dlgQuestion.Hide))
		except:
			import exception
			exception.abort("SelectCharacterWindow.__LoadQuestionDialog.BindObject")

	def Destroy(self):
		self.ClearDictionary()
		self.board = 0
		self.successPercentage = 0
		self.titleBar = 0
		self.toolTip = 0
		self.dlgQuestion = 0

	def GetRefineSuccessPercentage(self, scrollSlotIndex, itemSlotIndex):

		if -1 != scrollSlotIndex:
			if player.IsRefineGradeScroll(scrollSlotIndex):
				curGrade = player.GetItemGrade(itemSlotIndex)
				itemIndex = player.GetItemIndex(itemSlotIndex)

				item.SelectItem(itemIndex)
				itemType = item.GetItemType()
				itemSubType = item.GetItemSubType()

				if item.ITEM_TYPE_METIN == itemType:

					if curGrade >= len(self.upgradeStoneSuccessPercentage):
						return 0
					return self.upgradeStoneSuccessPercentage[curGrade]

				elif item.ITEM_TYPE_ARMOR == itemType:

					if item.ARMOR_BODY == itemSubType:
						if curGrade >= len(self.upgradeArmorSuccessPercentage):
							return 0
						return self.upgradeArmorSuccessPercentage[curGrade]
					else:
						if curGrade >= len(self.upgradeAccessorySuccessPercentage):
							return 0
						return self.upgradeAccessorySuccessPercentage[curGrade]

				else:

					if curGrade >= len(self.upgradeSuccessPercentage):
						return 0
					return self.upgradeSuccessPercentage[curGrade]

		for i in xrange(player.METIN_SOCKET_MAX_NUM+1):
			if 0 == player.GetItemMetinSocket(itemSlotIndex, i):
				break

		return self.makeSocketSuccessPercentage[i]

	def Open(self, scrollItemPos, targetItemPos):
		self.scrollItemPos = scrollItemPos
		self.targetItemPos = targetItemPos

		percentage = self.GetRefineSuccessPercentage(scrollItemPos, targetItemPos)
		if 0 == percentage:
			return
		self.successPercentage.SetText(localeInfo.REFINE_SUCCESS_PROBALITY % (percentage))

		itemIndex = player.GetItemIndex(targetItemPos)
		self.toolTip.ClearToolTip()
		metinSlot = []
		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			metinSlot.append(player.GetItemMetinSocket(targetItemPos, i))
		self.toolTip.AddItemData(itemIndex, metinSlot)

		self.UpdateDialog()
		self.SetTop()
		self.Show()

	def UpdateDialog(self):
		newWidth = self.toolTip.GetWidth() + 30
		newHeight = self.toolTip.GetHeight() + 98
		self.board.SetSize(newWidth, newHeight)
		self.titleBar.SetWidth(newWidth-15)
		self.SetSize(newWidth, newHeight)

		(x, y) = self.GetLocalPosition()
		self.SetPosition(x, y)

	def OpenQuestionDialog(self):
		percentage = self.GetRefineSuccessPercentage(-1, self.targetItemPos)
		if 100 == percentage:
			self.Accept()
			return

		self.dlgQuestion.SetTop()
		self.dlgQuestion.Show()

	def Accept(self):
		net.SendItemUseToItemPacket(self.scrollItemPos, self.targetItemPos)
		self.Close()

	def Close(self):
		self.dlgQuestion.Hide()
		self.Hide()

	def OnPressEscapeKey(self):
		self.Close()
		return True

class RefineDialogNew(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__Initialize()
		self.isLoaded = False

	def __Initialize(self):
		self.dlgQuestion = None
		self.children = []
		self.vnum = 0
		self.targetItemPos = 0
		self.dialogHeight = 0
		self.cost = 0
		self.percentage = 0
		self.type = 0
		self.previousButton = None
		self.nextButton = None
		self.index = 0
		self.recipeCount = 0
		self.recipe_index = 0
		self.refines = None

	def __Reset(self):
		self.children = []
		self.vnum = 0
		self.targetItemPos = 0
		self.dialogHeight = 0
		self.cost = 0
		self.percentage = 0
		self.type = 0
		self.xRefineStart = 0
		self.yRefineStart = 0
		self.index = 0
		self.recipeCount = 0
		self.recipe_index = 0
		self.refines = None

	def __LoadScript(self):

		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "refinedialog.py")

		except:
			import exception
			exception.abort("RefineDialog.__LoadScript.LoadObject")

		try:
			self.board = self.GetChild("Board")
			self.titleBar = self.GetChild("TitleBar")
			self.probText = self.GetChild("SuccessPercentage")

			self.probIncreaseText = self.GetChild("SuccessPercentageIncreased")
			self.costText = self.GetChild("Cost")
			self.designMode = self.GetChild("DesignIncrease")

			self.button_accept = self.GetChild("AcceptButton")
			self.button_cancel = self.GetChild("CancelButton")
			self.previousButton = self.GetChild("PreviousButton")
			self.previousButton.SetEvent(lambda x = -1: self.ChangePage(x))
			self.nextButton = self.GetChild("NextButton")
			self.nextButton.SetEvent(lambda x = 1: self.ChangePage(x))
			self.refineNumberText = self.GetChild("refineIndexText")

			self.button_accept.SetEvent(self.OpenQuestionDialog)
			self.button_cancel.SetEvent(self.CancelRefine)
		except:
			import exception
			exception.abort("RefineDialog.__LoadScript.BindObject")

		self.toolTipNext = uiToolTip.ItemToolTip()
		self.toolTipNext.HideToolTip()

		self.toolTipCur = uiToolTip.ItemToolTip()
		self.toolTipCur.HideToolTip()

		self.tooltipMode = uiToolTip.ItemToolTip()
		self.tooltipMode.HideToolTip()

		self.toolTipMaterial = uiToolTip.ItemToolTip()
		self.toolTipMaterial.HideToolTip()

		self.slotCurrent, self.slotAfter, self.numberSlotImage, self.imgPotion = {}, {}, {}, {}
		posY = 61
		for i in xrange(3):
			self.slotCurrent[i] = ui.make_image_box(self, "d:/ymir work/ui/public/Slot_Base.sub", 41, posY) # 60
			self.slotAfter[i] = ui.make_image_box(self, "d:/ymir work/ui/public/Slot_Base.sub", 105*2-32, posY)
			posY += 32

		self.itemImageCur = ui.make_image_box(self, "d:/ymir work/ui/public/Slot_Base.sub", 42, 60)
		self.itemImageNext = ui.make_image_box(self, "d:/ymir work/ui/public/Slot_Base.sub", 105*2-31, 60)
		
		self.materialList = []

		self.checkBox = ui.CheckBox()
		self.checkBox.SetParent(self)
		self.checkBox.SetPosition(-170, 45)
		self.checkBox.SetWindowHorizontalAlignCenter()
		self.checkBox.SetWindowVerticalAlignBottom()
		self.checkBox.SetEvent(ui.__mem_func__(self.AutoRefine), "ON_CHECK", True)
		self.checkBox.SetEvent(ui.__mem_func__(self.AutoRefine), "ON_UNCKECK", False)
		self.checkBox.SetCheckStatus(constInfo.IS_AUTO_REFINE)
		self.checkBox.SetTextInfo(localeInfo.REFINE_CHECKBOX)
		self.checkBox.Show()

		self.titleBar.SetCloseEvent(ui.__mem_func__(self.CancelRefine))
		self.isLoaded = True

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __make_thin_board(self):
		thinBoard = ui.ThinBoard()
		thinBoard.SetParent(self)
		thinBoard.Show()
		self.children.append(thinBoard)
		return thinBoard

	def Destroy(self):
		self.ClearDictionary()
		self.dlgQuestion = None
		self.board = 0
		self.probText = 0
		self.costText = 0
		self.titleBar = 0
		self.toolTip = 0
		self.successPercentage = None
		self.slotList = []
		self.children = []

	def Open(self, targetItemPos, type, data):

		if not self.isLoaded:
			self.__LoadScript()

		self.__Reset()

		self.refines = data
		self.targetItemPos = targetItemPos
		self.recipeCount = len(data)
		self.type = type
		self.targetItemPos = targetItemPos

		self.dialogHeight = 62
		self.UpdateDialog()

		self.SetTop()
		self.Show()
		self.UpdateRefine()

	def UpdateRefine(self):
		self.vnum = self.refines[self.index]["result_vnum"]
		self.cost = self.refines[self.index]["price"]
		self.percentage = self.refines[self.index]["prob"]

		self.probText.SetText(localeInfo.REFINE_SUCCESS_PROBALITY % (self.percentage))
		self.costText.SetText("%s" % localeInfo.number_to_money_string(self.cost))
		
		self.toolTipNext.ClearToolTip()
		self.toolTipCur.ClearToolTip()

		metinSlot = []
		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			metinSlot.append(player.GetItemMetinSocket(self.targetItemPos, i))

		attrSlot = []
		for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
		 	attrSlot.append(player.GetItemAttribute(self.targetItemPos, i))
		
		self.toolTipCur.SetInventoryItem(self.targetItemPos)
		self.toolTipNext.AddRefineItemData(self.vnum, metinSlot, attrSlot)

		curItemIndex = player.GetItemIndex(self.targetItemPos)
		
		if curItemIndex != 0:
			item.SelectItem(curItemIndex)

		 	try:
		 		self.itemImageCur.LoadImage(item.GetIconImageFileName())
		 	except:
		 		dbg.TraceError("Refine.CurrentItem.LoadImage - Failed to find item data")

		item.SelectItem(self.refines[self.index]["result_vnum"])
		self.itemImageNext.LoadImage(item.GetIconImageFileName())

		self.ShowMaterials()
		self.refineNumberText.SetText("[{}/{}]".format(self.index+1, self.recipeCount))
		if self.index == 0:
			self.previousButton.Hide()
		else:
			self.previousButton.Show()
		if self.index+1 == self.recipeCount:
			self.nextButton.Hide()
		else:
			self.nextButton.Show()


	def Close(self):
		self.dlgQuestion = None
		self.Hide()

	def OverInItem(self, slot):
		if self.toolTipMaterial:
			self.toolTipMaterial.SetItemToolTip(self.materialList[slot])

	def OverOutItem(self):
		if self.toolTipMaterial:
			self.toolTipMaterial.HideToolTip()

	def OnUpdate(self):
		if self.itemImageCur:
			if self.itemImageCur.IsIn():
				self.toolTipCur.ShowToolTip()
			else:
				self.toolTipCur.HideToolTip()

		if self.itemImageNext:
			if self.itemImageNext.IsIn():
				self.toolTipNext.ShowToolTip()
			else:
				self.toolTipNext.HideToolTip()

	def __MakeItemSlot(self,c):
		itemslot = ui.SlotWindow()
		itemslot.SetParent(self)
		itemslot.SetSize(32, 32)
		itemslot.SetSlotBaseImage("d:/ymir work/ui/public/Slot_Base.sub", 1.0, 1.0, 1.0, 1.0)
		itemslot.AppendSlot(c, 0, 0, 32, 32)
		itemslot.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
		itemslot.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
		itemslot.RefreshSlot()
		itemslot.Show()
		self.children.append(itemslot)
		return itemslot


	# -1 -> Previous
	# 1 -> Next 
	def ChangePage(self, action):
		if self.index == 0 and action == -1:
			return
		if self.index+1 == self.recipeCount and action == 1:
			return
		self.index += action
		self.recipe_index = self.refines[self.index]["index"]
		self.UpdateRefine()

	def ShowMaterials(self):
		self.materialList = []
		self.children = []
		self.dialogHeight = 62
		for item in self.refines[self.index]["materials"]:
			self.AppendMaterial(item["vnum"], item["count"])

	def AppendMaterial(self, vnum, count):
		grid = self.__MakeItemSlot(len(self.materialList))
		grid.SetPosition(293-35, self.dialogHeight)
		grid.SetItemSlot(len(self.materialList), vnum, 0)

		self.materialList.append(vnum)

		thinBoard = self.__make_thin_board()
		thinBoard.SetPosition(293, self.dialogHeight)
		thinBoard.SetSize(191, 20)

		textLine = ui.TextLine()
		textLine.SetParent(thinBoard)
		textLine.SetFontName(localeInfo.UI_DEF_FONT)

		if player.GetItemCountByVnum(vnum) < count:
			textLine.SetPackedFontColor(0xffFF0033)
		else:
			textLine.SetPackedFontColor(0xffdddddd)

		textLine.SetText("%s x%d  |cFFffce00(%d)" % (item.GetItemName(), count, player.GetItemCountByVnum(vnum)))
		textLine.SetOutline()
		textLine.SetFeather(False)
		textLine.SetWindowVerticalAlignCenter()
		textLine.SetVerticalAlignCenter()

		textLine.SetPosition(15, 0)

		textLine.Show()
		self.children.append(textLine)

		self.dialogHeight += 34
		self.UpdateDialog()

	def UpdateDialog(self):
		self.board.SetSize(500, 250)
		self.titleBar.SetWidth(500-15)
		self.SetSize(500, 250)

		(x, y) = self.GetLocalPosition()
		self.SetPosition(x, y)

	def OpenQuestionDialog(self):

		if 100 == self.percentage:
			self.Accept()
			return

		if 5 == self.type: ## ??????????
			self.Accept()
			return

		dlgQuestion = uiCommon.QuestionDialog2()
		dlgQuestion.SetText2(localeInfo.REFINE_WARNING2)
		dlgQuestion.SetAcceptEvent(ui.__mem_func__(self.Accept))
		dlgQuestion.SetCancelEvent(ui.__mem_func__(dlgQuestion.Close))

		if 3 == self.type: ## ?ö
			dlgQuestion.SetText1(localeInfo.REFINE_DESTROY_WARNING_WITH_BONUS_PERCENT_1)
			dlgQuestion.SetText2(localeInfo.REFINE_DESTROY_WARNING_WITH_BONUS_PERCENT_2)
		elif 2 == self.type: ## ?????
			dlgQuestion.SetText1(localeInfo.REFINE_DOWN_GRADE_WARNING)
		else:
			dlgQuestion.SetText1(localeInfo.REFINE_DESTROY_WARNING)

		dlgQuestion.Open()
		self.dlgQuestion = dlgQuestion

	def Accept(self):
		net.SendRefinePacket(self.targetItemPos, self.type, self.recipe_index)
		# self.Close()

	def AutoRefine(self, checkType, autoFlag):
		constInfo.IS_AUTO_REFINE = autoFlag
	
	def CheckRefine(self, isFail):
		if constInfo.IS_AUTO_REFINE:
			if constInfo.AUTO_REFINE_TYPE == 1:
				if constInfo.AUTO_REFINE_DATA["ITEM"][0] != -1 and constInfo.AUTO_REFINE_DATA["ITEM"][1] != -1:
					scrollIndex = player.GetItemIndex(constInfo.AUTO_REFINE_DATA["ITEM"][0])
					itemIndex = player.GetItemIndex(constInfo.AUTO_REFINE_DATA["ITEM"][1])
					if scrollIndex == 0 or (itemIndex % 10 == 8 and not isFail):
						self.Close()
					else:
						net.SendItemUseToItemPacket(constInfo.AUTO_REFINE_DATA["ITEM"][0], constInfo.AUTO_REFINE_DATA["ITEM"][1])
			elif constInfo.AUTO_REFINE_TYPE == 2:
				npcData = constInfo.AUTO_REFINE_DATA["NPC"]
				if npcData[0] != 0 and npcData[1] != -1 and npcData[2] != -1 and npcData[3] != 0:
					itemIndex = player.GetItemIndex(npcData[1], npcData[2])
					if (itemIndex % 10 == 8 and not isFail) or isFail:
						self.Close()
					else:
						net.SendGiveItemPacket(npcData[0], npcData[1], npcData[2], npcData[3])
			else:
				self.Close()
		else:
			self.Close()

	def CancelRefine(self):
		net.SendRefinePacket(255, 255)
		self.Close()
		constInfo.AUTO_REFINE_TYPE = 0
		constInfo.AUTO_REFINE_DATA = {
			"ITEM" : [-1, -1],
			"NPC" : [0, -1, -1, 0]
		}

	def OnPressEscapeKey(self):
		self.CancelRefine()
		return True
