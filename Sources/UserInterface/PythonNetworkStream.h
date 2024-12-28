// Search :
bool SendRefinePacket(BYTE byPos, BYTE byType);
// Replace :
#ifdef MULTIPLE_REFINE
		bool SendRefinePacket(BYTE byPos, BYTE byType, BYTE ByIndex);
#else
		bool SendRefinePacket(BYTE byPos, BYTE byType);
#endif