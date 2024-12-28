// Search :
PyModule_AddIntConstant(poModule, "USE_OPENID",	0);
// Add before  :
#ifdef MULTIPLE_REFINE
	PyModule_AddIntConstant(poModule, "MULTIPLE_REFINE", 1);
#else
	PyModule_AddIntConstant(poModule, "MULTIPLE_REFINE", 0);
#endif