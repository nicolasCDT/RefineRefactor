// Search :
	/*
	 * SKILL
	 */

	if (decode_2bytes(data) != sizeof(TSkillTable))
	{
		sys_err("skill table size error");
		thecore_shutdown();
		return;
	}
	data += 2;

	size = decode_2bytes(data);
	data += 2;
	sys_log(0, "BOOT: SKILL: %d", size);

	if (size)
	{
		if (!CSkillManager::instance().Initialize((TSkillTable *) data, size))
		{
			sys_err("cannot initialize skill table");
			thecore_shutdown();
			return;
		}

		data += size * sizeof(TSkillTable);
	}
// Add after:
#ifdef MULTIPLE_REFINE
	/*
	 * REFINE TABLE
	 */
	if (decode_2bytes(data) != sizeof(TRefine))
	{
		sys_err("refine size error");
		thecore_shutdown();
		return;
	}
	data += 2;

	size = decode_2bytes(data);
	data += 2;
	sys_log(0, "BOOT: MULTIPLE REFINE: %d", size);

	if (size)
	{
		CRefineManager::instance().InitializeTable((TRefine*) data, size);
		data += size * sizeof(TRefine);
	}
#endif