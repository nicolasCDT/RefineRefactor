// Search :
		bool			DoRefine(LPITEM item, bool bMoneyOnly = false);
		bool			DoRefineWithScroll(LPITEM item);
// Replace :
#ifdef MULTIPLE_REFINE
		bool			DoRefine(LPITEM item, BYTE index, bool bMoneyOnly = false);
		bool			DoRefineWithScroll(LPITEM item, BYTE index);
#else
		bool			DoRefine(LPITEM item, bool bMoneyOnly = false);
		bool			DoRefineWithScroll(LPITEM item);
#endif