// Add at the end :
#ifdef MULTIPLE_REFINE
/**
 * Initializes m_map_Refine with all refines
 * 
 * @param table pointer on first recipe
 * @param size Number of refine
 * 
 * @return Always true... (I'm following ymir)
 */
bool CRefineManager::InitializeTable(TRefine * table, int size)
{
	for(int i = 0; i < size; i++, ++table)
		m_map_Refine.insert(std::make_pair(table->vnum, *table));

	sys_log(0, "Received %d refine from db", size);
	return true;
}

/**
 * Returns refine table with a vnum
 * 
 * @param vnum Item's vnumm
 * 
 * @return Pointer on vnum's upgrade table (null if doesn't exist)
 */
const TRefine* CRefineManager::GetRefine(DWORD vnum)
{
	if(vnum == 0)
		return NULL;
	
	itertype(m_map_Refine) it = m_map_Refine.find(vnum);

	if (it == m_map_Refine.end()) // cant find vnum
		return NULL;
	return &it->second; // Return the tab
}

/**
 * Returns TRefineTable (set) with a vnum and possibilites'index
 * 
 * @param vnum item's vnum
 * @param id recipe's id
 * 
 * @return Pointer on TRefineTable set (null if doesn't exist)
 */
const TRefineTable* CRefineManager::GetRefineRecipeByIndex(DWORD vnum, DWORD id)
{
	if(vnum == 0)
		return NULL;
	itertype(m_map_Refine) it = m_map_Refine.find(vnum);

	if (it == m_map_Refine.end()) // cant find vnum
		return NULL;
	TRefine* table = &it->second;

	if(id < table->possibilities_count)
		return GetRefineRecipe(table->possibilities[id].recipe_id);
	return NULL;
}

/**
 * Returns upgraded item's vnum with source vnum and possiblitess' index
 * 
 * @param vnum item's vnum
 * @param id recipe's id
 * 
 * @return Vnum (0 if doesn't exist)
 */
const DWORD CRefineManager::GetUpgradedVnumByIndex(DWORD vnum, DWORD id)
{
	if(vnum == 0)
		return 0;
	itertype(m_map_Refine) it = m_map_Refine.find(vnum);

	if (it == m_map_Refine.end()) // cant find vnum
		return 0;
	TRefine* table = &it->second;

	if(id < table->possibilities_count)
		return table->possibilities[id].vnum;
	return 0;
}

#endif