// Search:
	typedef std::map<DWORD, TRefineTable> TRefineRecipeMap;
// Add :
#ifdef MULTIPLE_REFINE
	typedef std::map<DWORD, TRefine> TRefineMap; // <id, table> -> easier to find vnum in map
#endif


// Search :
TRefineRecipeMap    m_map_RefineRecipe;
// Add :
#ifdef MULTIPLE_REFINE
		TRefineMap			m_map_Refine;
#endif


// Search : 
		bool Initialize(TRefineTable * table, int size);
// Add :
#ifdef MULTIPLE_REFINE
		bool InitializeTable(TRefine * table, int size);
		const TRefine* GetRefine(DWORD vnum);
		const TRefineTable* GetRefineRecipeByIndex(DWORD vnum, DWORD id);
		const DWORD GetUpgradedVnumByIndex(DWORD vnum, DWORD id);
#endif
