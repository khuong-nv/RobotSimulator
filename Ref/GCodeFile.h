#pragma once
#include <vector>
#include <string>
#include <fstream>
#include <iostream>
#include "glut.h"
using namespace std;

const float XMIN = 0;
const float XMAX = 40;
const float YMIN = 0;
const float YMAX = 40;
const float ZMIN = 0;
const float ZMAX = 1;



class GCodeFile
{
private:
	Pt CurrentPoint;
	Pt_t AllPoint;
	vtstr_t vtStr;
	string_t filename;
	ifstream inf;
public:
	void SetFile(string_t par_filename);
	bool LoadFile();
	void ReadFile();
	vtstr_t GetData();
	Pt_t GetAllPoint();
	void OutputData();
	void ProcessGCode(float offsetx, float offsety);
	void Draw();
	GCodeFile();
	~GCodeFile();
};

string_t split(const string_t &text, char sep);
vtstr_t split_t(string_t data, string_t token);
void RemoveCommand(vtstr_t& str);

