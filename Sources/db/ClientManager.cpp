// Search in class constructor (CClientManager::CClientManager()) this:
	m_iRefineTableSize(0),
	m_pRefineTable(NULL),
// And add :
#ifdef MULTIPLE_REFINE
	m_iRefineSize(0),
	m_pRefine(NULL),
#endif


// Search :
		sizeof(WORD) + sizeof(WORD) + sizeof(TSkillTable) * m_vec_skillTable.size() +
// Add :
#ifdef MULTIPLE_REFINE
		sizeof(WORD) + sizeof(WORD) + sizeof(TRefine) * m_iRefineSize +
#endif


// Search :
	sys_log(0, "sizeof(TSkillTable) = %d", sizeof(TSkillTable));
// Add :
#ifdef MULTIPLE_REFINE
	sys_log(0, "sizeof(TRefine) = %d", sizeof(TRefine));
#endif


// Search :
	peer->EncodeWORD(sizeof(TSkillTable));
	peer->EncodeWORD(m_vec_skillTable.size());
	peer->Encode(&m_vec_skillTable[0], sizeof(TSkillTable) * m_vec_skillTable.size());
// Add : 
#ifdef MULTIPLE_REFINE
	peer->EncodeWORD(sizeof(TRefine));
	peer->EncodeWORD(m_iRefineSize);
	peer->Encode(m_pRefine, sizeof(TRefine) * m_iRefineSize);
#endif