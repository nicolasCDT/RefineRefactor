// Search :
bool CHARACTER::DoRefine(LPITEM item, bool bMoneyOnly)
// Replace :
#ifdef MULTIPLE_REFINE
bool CHARACTER::DoRefine(LPITEM item, BYTE index, bool bMoneyOnly)
#else
bool CHARACTER::DoRefine(LPITEM item, bool bMoneyOnly)
#endif


// In DoRefine function, search : 
	const TRefineTable * prt = CRefineManager::instance().GetRefineRecipe(item->GetRefineSet());
// Replace :
#ifdef MULTIPLE_REFINE
	const TRefineTable * prt = CRefineManager::instance().GetRefineRecipeByIndex(item->GetVnum(), index);
	DWORD result_vnum = CRefineManager::instance().GetUpgradedVnumByIndex(item->GetVnum(), index);
#else
	const TRefineTable * prt = CRefineManager::instance().GetRefineRecipe(item->GetRefineSet());
	DWORD result_vnum = item->GetRefinedVnum();
#endif


// Again in DoRefine, search DWORD result_vnum = .. and delete this line.



// Search :
bool CHARACTER::DoRefineWithScroll(LPITEM item)
// Replace :
#ifdef MULTIPLE_REFINE
bool CHARACTER::DoRefineWithScroll(LPITEM item, BYTE index)
#else
bool CHARACTER::DoRefineWithScroll(LPITEM item)
#endif


// In DoRefineWithScroll method, Search :
	const TRefineTable * prt = CRefineManager::instance().GetRefineRecipe(item->GetRefineSet());
// Replace :
#ifdef MULTIPLE_REFINE
	const TRefineTable * prt = CRefineManager::instance().GetRefineRecipeByIndex(item->GetVnum(), index);
	DWORD result_vnum = CRefineManager::instance().GetUpgradedVnumByIndex(item->GetVnum(), index);
#else
	const TRefineTable * prt = CRefineManager::instance().GetRefineRecipe(item->GetRefineSet());
#endif


// Again in DoRefineWithScroll, search DWORD result_vnum = .. and delete this line.


// Replace RefineInformation method with : 
#ifdef MULTIPLE_REFINE
bool CHARACTER::RefineInformation(BYTE bCell, BYTE bType, int iAdditionalCell)
{
	if (bCell > INVENTORY_MAX_NUM)
		return false;

	LPITEM item = GetInventoryItem(bCell);

	if (!item)
		return false;

	// REFINE_COST
	if (bType == REFINE_TYPE_MONEY_ONLY && !GetQuestFlag("deviltower_zone.can_refine"))
	{
		ChatPacket(CHAT_TYPE_INFO, LC_TEXT("You can only be rewarded once for the Demon Tower Quest."));
		return false;
	}
	// END_OF_REFINE_COST

	TPacketGCRefinesInformation packet;
	const TRefine* refines = CRefineManager::Instance().GetRefine(item->GetVnum());

	if(!refines)
		return false;

	packet.header = HEADER_GC_REFINE_INFORMATION;
	packet.type = bType;
	packet.pos = bCell;
	packet.src_vnum = item->GetVnum();
	packet.refine_count = refines->possibilities_count;

	for(int i = 0; i < refines->possibilities_count; i++)
	{
		packet.refine[i].index = i;
		packet.refine[i].result_vnum = refines->possibilities[i].vnum;
		if (packet.refine[i].result_vnum == 0)
		{
			sys_err("RefineInformation packet.refine[i].result_vnum == 0");
			ChatPacket(CHAT_TYPE_INFO, LC_TEXT("This Item can't be made better."));
			return false;
		}

		if (item->GetType() == ITEM_USE && item->GetSubType() == USE_TUNING)
		{
			if (bType == 0)
			{
				ChatPacket(CHAT_TYPE_INFO, LC_TEXT("This Item can't be advanced this way."));
				return false;
			}
			else
			{
				LPITEM itemScroll = GetInventoryItem(iAdditionalCell);
				if (!itemScroll || item->GetVnum() == itemScroll->GetVnum())
				{
					ChatPacket(CHAT_TYPE_INFO, LC_TEXT("You can't combine identical Advancement Scrolls."));
					ChatPacket(CHAT_TYPE_INFO, LC_TEXT("The Blessing Scroll and Magic Metal can be combined"));
					return false;
				}
			}
		}

		// Get refine set
		const TRefineTable* ptr = CRefineManager::instance().GetRefineRecipe(refines->possibilities[i].recipe_id);

		if (!ptr)
		{
			sys_err("RefineInformation NOT GET REFINE SET %d", refines->possibilities[i].recipe_id);
			ChatPacket(CHAT_TYPE_INFO, LC_TEXT("This Item can't be made better."));
			return false;
		}

		//MAIN_QUEST_LV7
		if (GetQuestFlag("main_quest_lv7.refine_chance") > 0)
		{

			if (!item->CheckItemUseLevel(20) || item->GetType() != ITEM_WEAPON)
			{
				ChatPacket(CHAT_TYPE_INFO, LC_TEXT("Free advancement is only for weapons up to level 20."));
				return false;
			}
			packet.refine[i].cost = 0;
		}
		else
			packet.refine[i].cost = ComputeRefineFee(ptr->cost);
		//END_MAIN_QUEST_LV7

		packet.refine[i].prob = ptr->prob;
		if (bType == REFINE_TYPE_MONEY_ONLY)
		{
			packet.refine[i].material_count = 0;
			memset(packet.refine[i].materials, 0, sizeof(packet.refine[i].materials));
		}
		else
		{
			packet.refine[i].material_count = ptr->material_count;
			thecore_memcpy(&packet.refine[i].materials, ptr->materials, sizeof(ptr->materials));
		}
		// END_OF_REFINE_COST
	}

	GetDesc()->Packet(&packet, sizeof(TPacketGCRefinesInformation));

	SetRefineMode(iAdditionalCell);
	return true;
}
#else
bool CHARACTER::RefineInformation(BYTE bCell, BYTE bType, int iAdditionalCell)
{
	if (bCell > INVENTORY_MAX_NUM)
		return false;

	LPITEM item = GetInventoryItem(bCell);

	if (!item)
		return false;

	// REFINE_COST
	if (bType == REFINE_TYPE_MONEY_ONLY && !GetQuestFlag("deviltower_zone.can_refine"))
	{
		ChatPacket(CHAT_TYPE_INFO, LC_TEXT("You can only be rewarded once for the Demon Tower Quest."));
		return false;
	}
	// END_OF_REFINE_COST

	TPacketGCRefineInformation p;

	p.header = HEADER_GC_REFINE_INFORMATION;
	p.pos = bCell;
	p.src_vnum = item->GetVnum();
	p.result_vnum = item->GetRefinedVnum();
	p.type = bType;

	if (p.result_vnum == 0)
	{
		sys_err("RefineInformation p.result_vnum == 0");
		ChatPacket(CHAT_TYPE_INFO, LC_TEXT("This Item can't be made better."));
		return false;
	}

	if (item->GetType() == ITEM_USE && item->GetSubType() == USE_TUNING)
	{
		if (bType == 0)
		{
			ChatPacket(CHAT_TYPE_INFO, LC_TEXT("This Item can't be advanced this way."));
			return false;
		}
		else
		{
			LPITEM itemScroll = GetInventoryItem(iAdditionalCell);
			if (!itemScroll || item->GetVnum() == itemScroll->GetVnum())
			{
				ChatPacket(CHAT_TYPE_INFO, LC_TEXT("You can't combine identical Advancement Scrolls."));
				ChatPacket(CHAT_TYPE_INFO, LC_TEXT("The Blessing Scroll and Magic Metal can be combined"));
				return false;
			}
		}
	}

	CRefineManager & rm = CRefineManager::instance();

	const TRefineTable* prt = rm.GetRefineRecipe(item->GetRefineSet());

	if (!prt)
	{
		sys_err("RefineInformation NOT GET REFINE SET %d", item->GetRefineSet());
		ChatPacket(CHAT_TYPE_INFO, LC_TEXT("This Item can't be made better."));
		return false;
	}

	// REFINE_COST

	//MAIN_QUEST_LV7
	if (GetQuestFlag("main_quest_lv7.refine_chance") > 0)
	{

		if (!item->CheckItemUseLevel(20) || item->GetType() != ITEM_WEAPON)
		{
			ChatPacket(CHAT_TYPE_INFO, LC_TEXT("Free advancement is only for weapons up to level 20."));
			return false;
		}
		p.cost = 0;
	}
	else
		p.cost = ComputeRefineFee(prt->cost);

	//END_MAIN_QUEST_LV7
	p.prob = prt->prob;
	if (bType == REFINE_TYPE_MONEY_ONLY)
	{
		p.material_count = 0;
		memset(p.materials, 0, sizeof(p.materials));
	}
	else
	{
		p.material_count = prt->material_count;
		thecore_memcpy(&p.materials, prt->materials, sizeof(prt->materials));
	}
	// END_OF_REFINE_COST

	GetDesc()->Packet(&p, sizeof(TPacketGCRefineInformation));

	SetRefineMode(iAdditionalCell);
	return true;
}
#endif