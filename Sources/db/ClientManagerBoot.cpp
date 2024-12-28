// Search :
	if (!InitializeRefineTable())
	{
		sys_err("InitializeRefineTable FAILED");
		return false;
	}
// Add : 
#ifdef MULTIPLE_REFINE
bool CClientManager::InitializeRefine()
{
	char query[1024];
	// Load other table
	snprintf(query, sizeof(query),
		"SELECT id, src_vnum,"
		"dest_vnum_0, refine_set_0, "
		"dest_vnum_1, refine_set_1, "
		"dest_vnum_2, refine_set_2, "
		"dest_vnum_3, refine_set_3, "
		"dest_vnum_4, refine_set_4 "
		"FROM refine_table%s",
		GetTablePostfix());
	
	std::auto_ptr<SQLMsg> pkMsg(CDBManager::instance().DirectQuery(query));
	SQLResult * pRes = pkMsg->Get();

	m_iRefineSize = pRes->uiNumRows; // Size

	if (m_pRefine)
	{
		sys_log(0, "RELOAD: refine_table");
		delete [] m_pRefine;
		m_pRefine = NULL;
	}

	sys_log(0, "Founded %d line in refine_table", m_iRefineSize);
	
	// Register :
	m_pRefine	= new TRefine[m_iRefineSize]; // Make new table 
	memset(m_pRefine, 0, sizeof(TRefine) * m_iRefineSize); // Put 0 

	TRefine* ptr = m_pRefine; // On current table
	MYSQL_ROW data;

	while ((data = mysql_fetch_row(pRes->pSQLResult))) // for all line
	{
		int col = 1; // current col 1 to ignore id
		int dest = 0; // possibilites
		str_to_number(ptr->vnum, data[col++]);
		for (; dest < 5; dest++) // {0, 1, 2, 3, 4}
		{
			str_to_number(ptr->possibilities[dest].vnum, data[col++]);
			str_to_number(ptr->possibilities[dest].recipe_id, data[col++]);
			if (ptr->possibilities[dest].vnum == 0)
				break;
		}
		ptr->possibilities_count = dest;
		ptr++;
	}
	return true;
}
#endif