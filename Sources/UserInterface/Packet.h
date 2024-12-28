// Search :
typedef struct SPacketCGRefine
{
	// [...]
} TPacketCGRefine;
// Change :
typedef struct SPacketCGRefine
{
	BYTE		header;
	BYTE		pos;
	BYTE		type;
#ifdef MULTIPLE_REFINE
	BYTE		index;
#endif
} TPacketCGRefine;


// Add :
#ifdef MULTIPLE_REFINE
typedef struct SPacketGCRefineInfo
{
	DWORD 	index;
	DWORD	result_vnum;
	BYTE	material_count;
	int		cost; 
	int		prob; 
	TMaterial materials[REFINE_MATERIAL_MAX_NUM];
}	TPacketGCRefineInfo;

typedef struct SPacketGCRefinesInformation
{
	BYTE	header;
	BYTE	type;
	BYTE	pos;
	DWORD	src_vnum;
	BYTE refine_count;
	TPacketGCRefineInfo refine[5];
} TPacketGCRefinesInformation;
#endif