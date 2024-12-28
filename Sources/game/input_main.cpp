// Search :
	if (p->type == REFINE_TYPE_NORMAL)
	{
		sys_log (0, "refine_type_noraml");
		ch->DoRefine(item);
	}
// Replace:
	if (p->type == REFINE_TYPE_NORMAL)
	{
		sys_log (0, "refine_type_noraml");
#ifdef MULTIPLE_REFINE
		ch->DoRefine(item, p->index);
#else
		ch->DoRefine(item);
#endif
	}


// Search :
	else if (p->type == REFINE_TYPE_SCROLL || p->type == REFINE_TYPE_HYUNIRON || p->type == REFINE_TYPE_MUSIN || p->type == REFINE_TYPE_BDRAGON)
	{
		sys_log (0, "refine_type_scroll, ...");
		ch->DoRefineWithScroll(item);
	}
// Replace:
	else if (p->type == REFINE_TYPE_SCROLL || p->type == REFINE_TYPE_HYUNIRON || p->type == REFINE_TYPE_MUSIN || p->type == REFINE_TYPE_BDRAGON)
	{
		sys_log (0, "refine_type_scroll, ...");
		
#ifdef MULTIPLE_REFINE
		ch->DoRefineWithScroll(item, p->index);
#else
		ch->DoRefineWithScroll(item);
#endif
	}


// Search :
			if (ch->GetQuestFlag("deviltower_zone.can_refine"))
				{
					ch->DoRefine(item, true);
					ch->SetQuestFlag("deviltower_zone.can_refine", 0);
				}
// Replace :
			if (ch->GetQuestFlag("deviltower_zone.can_refine"))
				{
#ifdef MULTIPLE_REFINE
					ch->DoRefine(item,p->index, true);
#else
					ch->DoRefine(item, true);
#endif
					ch->SetQuestFlag("deviltower_zone.can_refine", 0);
				}