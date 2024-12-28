# Search OpenRefineDialog method and change it like that : 
# Don't forget to put your current method after else
	if app.MULTIPLE_REFINE:
		def OpenRefineDialog(self, targetItemPos, type, data):
			self.interface.OpenRefineDialog(targetItemPos, type, data)
	else:
		def OpenRefineDialog(self, targetItemPos, nextGradeItemVnum, cost, prob, type=0):
			self.interface.OpenRefineDialog(targetItemPos, nextGradeItemVnum, cost, prob, type)


# Search :
	def RefineSuceededMessage(self):
		snd.PlaySound("sound/ui/make_soket.wav")
		self.PopupMessage(localeInfo.REFINE_SUCCESS)

	def RefineFailedMessage(self):
		snd.PlaySound("sound/ui/jaeryun_fail.wav")
		self.PopupMessage(localeInfo.REFINE_FAILURE)
# Replace:
	def RefineSuceededMessage(self):
		snd.PlaySound("sound/ui/make_soket.wav")
		self.PopupMessage(localeInfo.REFINE_SUCCESS)
		if app.MULTIPLE_REFINE:
			self.interface.CheckRefineDialog(False)

	def RefineFailedMessage(self):
		snd.PlaySound("sound/ui/jaeryun_fail.wav")
		self.PopupMessage(localeInfo.REFINE_FAILURE)
		if app.MULTIPLE_REFINE:
			self.interface.CheckRefineDialog(True)

# Last step will be a litle bit difficult.
# Change your function to have constInfo.AUTO_REFINE_TYPE... in the same case of me :
# (Ask me if you want)
	def __PutItem(self, attachedType, attachedItemIndex, attachedItemSlotPos, attachedItemCount, dstChrID):
		if player.SLOT_TYPE_INVENTORY == attachedType or player.SLOT_TYPE_DRAGON_SOUL_INVENTORY == attachedType \
			or (app.ENABLE_SPECIAL_STORAGE and ( player.SLOT_TYPE_UPGRADE_INVENTORY == attachedType or\
				player.SLOT_TYPE_BOOK_INVENTORY == attachedType or\
				player.SLOT_TYPE_STONE_INVENTORY == attachedType)):
			attachedInvenType = player.SlotTypeToInvenType(attachedType)
			if 	chr.HasInstance(self.PickingCharacterIndex) and player.GetMainCharacterIndex() != dstChrID:
				if player.IsEquipmentSlot(attachedItemSlotPos) and player.SLOT_TYPE_DRAGON_SOUL_INVENTORY != attachedType and \
					(app.ENABLE_SPECIAL_STORAGE and player.SLOT_TYPE_UPGRADE_INVENTORY != attachedType and\
						player.SLOT_TYPE_BOOK_INVENTORY != attachedType and\
						player.SLOT_TYPE_STONE_INVENTORY != attachedType):
					self.stream.popupWindow.Close()
					self.stream.popupWindow.Open(localeInfo.EXCHANGE_FAILURE_EQUIP_ITEM, 0, localeInfo.UI_OK)
				else:
					if chr.IsNPC(dstChrID):
						constInfo.AUTO_REFINE_TYPE = 2								# <-----
						constInfo.AUTO_REFINE_DATA["NPC"][0] = dstChrID				# <-----
						constInfo.AUTO_REFINE_DATA["NPC"][1] = attachedInvenType	# <----- Important code
						constInfo.AUTO_REFINE_DATA["NPC"][2] = attachedItemSlotPos	# <-----
						constInfo.AUTO_REFINE_DATA["NPC"][3] = attachedItemCount	# <-----
						net.SendGiveItemPacket(dstChrID, attachedInvenType, attachedItemSlotPos, attachedItemCount)
					else:
						net.SendExchangeStartPacket(dstChrID)
						net.SendExchangeItemAddPacket(attachedInvenType, attachedItemSlotPos, 0)
			else:
				self.__DropItem(attachedType, attachedItemIndex, attachedItemSlotPos, attachedItemCount)
