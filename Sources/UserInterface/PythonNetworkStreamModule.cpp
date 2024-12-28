// Search :
PyObject* netSendRefinePacket(PyObject* poSelf, PyObject* poArgs)
{
	// [...]
}
// Change :
PyObject* netSendRefinePacket(PyObject* poSelf, PyObject* poArgs)
{
	int iSlotIndex;
	if (!PyTuple_GetInteger(poArgs, 0, &iSlotIndex))
		return Py_BuildException();
	int iType;
	if (!PyTuple_GetInteger(poArgs, 1, &iType))
		return Py_BuildException();
#ifdef MULTIPLE_REFINE
	int iIndex;
	if (!PyTuple_GetInteger(poArgs, 2, &iIndex))
		return Py_BuildException();
#endif

	CPythonNetworkStream& rns=CPythonNetworkStream::Instance();

#ifdef MULTIPLE_REFINE
	rns.SendRefinePacket(iSlotIndex, iType, iIndex);
#else
	rns.SendRefinePacket(iSlotIndex, iType);
#endif

	return Py_BuildNone();
}