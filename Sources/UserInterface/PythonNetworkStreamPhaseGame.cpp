// Search :
bool CPythonNetworkStream::SendRefinePacket(BYTE byPos, BYTE byType)
{
	// [...]
}
// Replace :
#ifdef MULTIPLE_REFINE
bool CPythonNetworkStream::SendRefinePacket(BYTE byPos, BYTE byType, BYTE byIndex)
{
	TPacketCGRefine kRefinePacket;
	kRefinePacket.header = HEADER_CG_REFINE;
	kRefinePacket.pos = byPos;
	kRefinePacket.type = byType;
	kRefinePacket.index = byIndex;

	if (!Send(sizeof(kRefinePacket), &kRefinePacket))
		return false;

	return SendSequence();
}
#else
bool CPythonNetworkStream::SendRefinePacket(BYTE byPos, BYTE byType)
{
	TPacketCGRefine kRefinePacket;
	kRefinePacket.header = HEADER_CG_REFINE;
	kRefinePacket.pos = byPos;
	kRefinePacket.type = byType;

	if (!Send(sizeof(kRefinePacket), &kRefinePacket))
		return false;

	return SendSequence();
}
#endif


// Search :
bool CPythonNetworkStream::RecvRefineInformationPacketNew()
{
	// [...]
}
// Replace:
#ifdef MULTIPLE_REFINE
bool CPythonNetworkStream::RecvRefineInformationPacketNew()
{
	TPacketGCRefinesInformation kRefineInfoPacket;
	if (!Recv(sizeof(kRefineInfoPacket), &kRefineInfoPacket))
		return false;

	// Make results list
	PyObject* results = Py_BuildValue("[]"); 
	for (int i = 0; i < kRefineInfoPacket.refine_count; i++)
	{
		PyObject* materials = Py_BuildValue("[]");
		for (int j = 0; j < kRefineInfoPacket.refine[i].material_count; j++)
		{
			PyList_Append(
				materials, 
				Py_BuildValue(
					"{s:i,s:i}",
					"vnum", kRefineInfoPacket.refine[i].materials[j].vnum,
					"count", kRefineInfoPacket.refine[i].materials[j].count
					)
			);
		}

		PyList_Append(
			results,
			Py_BuildValue(
				"{s:i,s:i,s:i,s:i,s:O}",
				"index", kRefineInfoPacket.refine[i].index,
				"price", kRefineInfoPacket.refine[i].cost,
				"prob", kRefineInfoPacket.refine[i].prob,
				"result_vnum", kRefineInfoPacket.refine[i].result_vnum,
				"materials", materials
			)
		);
	}

	// Send to Python
	PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME],"OpenRefineDialog", Py_BuildValue("(iiO)", kRefineInfoPacket.pos, kRefineInfoPacket.type, results));

	return true;
}
#else
bool CPythonNetworkStream::RecvRefineInformationPacketNew()
{
	TPacketGCRefineInformationNew kRefineInfoPacket;
	if (!Recv(sizeof(kRefineInfoPacket), &kRefineInfoPacket))
		return false;

	TRefineTable & rkRefineTable = kRefineInfoPacket.refine_table;
	PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME],
		"OpenRefineDialog",
		Py_BuildValue("(iiiii)",
			kRefineInfoPacket.pos,
			kRefineInfoPacket.refine_table.result_vnum,
			rkRefineTable.cost,
			rkRefineTable.prob,
			kRefineInfoPacket.type)
		);

	for (int i = 0; i < rkRefineTable.material_count; ++i)
	{
		PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "AppendMaterialToRefineDialog", Py_BuildValue("(ii)", rkRefineTable.materials[i].vnum, rkRefineTable.materials[i].count));
	}

#ifdef _DEBUG
	Tracef(" >> RecvRefineInformationPacketNew(pos=%d, result_vnum=%d, cost=%d, prob=%d, type=%d)\n",
														kRefineInfoPacket.pos,
														kRefineInfoPacket.refine_table.result_vnum,
														rkRefineTable.cost,
														rkRefineTable.prob,
														kRefineInfoPacket.type);
#endif

	return true;
}
#endif
