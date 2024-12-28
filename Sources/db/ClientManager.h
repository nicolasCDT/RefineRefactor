// Search :
bool		InitializeRefineTable();
// Add :
#ifdef MULTIPLE_REFINE
	bool 		InitializeRefine();
#endif


// Search : 
	int				m_iRefineTableSize;
	TRefineTable*	m_pRefineTable;
// Add :
#ifdef MULTIPLE_REFINE
	int			m_iRefineSize;
	TRefine*	m_pRefine;
#endif