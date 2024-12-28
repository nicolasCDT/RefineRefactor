// Add after the structure :
typedef struct SRefineTable
{
	DWORD id;
	BYTE material_count;
	int cost;
	int prob;&
	TRefineMaterial materials[REFINE_MATERIAL_MAX_NUM];
} TRefineTable;

// this : 
#ifdef MULTIPLE_REFINE
typedef struct SRefinePossibilities
{
	DWORD vnum; // result vnum
	DWORD recipe_id; // result recipe set id (TRefineTable)
} TRefinePossibilities;

typedef struct SRefine
{
	DWORD vnum; // Source Vnum
	BYTE possibilities_count; // Number of possibilities
	TRefinePossibilities possibilities[5]; //5 : {0, 1, 2, 3, 4}
} TRefine;
#endif