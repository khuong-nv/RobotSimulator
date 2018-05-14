#include "stdafx.h"
#include "GCodeFile.h"
#include <Windows.h>
void GCodeFile::SetFile(string_t par_filename)
{
	filename = par_filename;
	//LoadFile();
}

bool GCodeFile::LoadFile()
{
	inf.open(filename, std::ifstream::in);
	if (!inf)
	{
		// khong the mo file
		return false;
	}
	else
		return true;
}

void GCodeFile::ReadFile()
{
	vtStr.clear();
	string_t strtmp;
	while (inf)
	{
		getline(inf, strtmp);
		vtStr.push_back(strtmp);
	}
	inf.close();
	RemoveCommand(vtStr);
}

vtstr_t GCodeFile::GetData()
{
	return vtStr;
}

Pt_t GCodeFile::GetAllPoint()
{
	return AllPoint;
}

void GCodeFile::OutputData()
{
	for (int i = 0; i < vtStr.size(); i++)
	{
		cout << vtStr.at(i) << endl;
	}
}

void GCodeFile::ProcessGCode(float offsetx, float offsety)
{
	AllPoint.clear();
	string_t strFind1("G1"), strFind2("G4"), strFind3("M300"), strFind4("M18");
	for (int i = 0; i < vtStr.size(); i++)
	{
		std::size_t found1 = vtStr.at(i).find(strFind1);
		std::size_t found2 = vtStr.at(i).find(strFind2);
		std::size_t found3 = vtStr.at(i).find(strFind3);
		std::size_t found4 = vtStr.at(i).find(strFind4);

		vtstr_t spline;
		Pt point;
		if (found1 != string_t::npos)
		{
			spline = split_t(vtStr.at(i), " ");
			if (spline[1][0] == 'X' || spline[2][0] == 'Y')
			{
				spline[1].erase(0, 1);
				spline[2].erase(0, 1);
				point.x = offsetx + std::stod(spline[1]);
				point.y = offsety + std::stof(spline[2]);
				point.z = 0;
				AllPoint.push_back(point);
			}
		}
		if (found2 != string_t::npos)
		{
			int a;
			a = 0;
			//wait ...ms
		}
		if (found3 != string_t::npos)
		{
			//up down
			int a;
			a = 0;
		}
		if (found4 != string_t::npos)
		{
			//turn off
			int a;
			a = 0;
		}
	}
}

void GCodeFile::Draw()
{
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
	glPushMatrix();
		//ve khung chu nhat
		/*glPushMatrix();
		glBegin(GL_LINE_LOOP);
			glVertex2f(XMIN, YMIN);
			glVertex2f(XMAX, YMIN);
			glVertex2f(XMAX, YMAX);
			glVertex2f(XMIN, YMAX);
		glEnd();
		glPopMatrix();*/

		glPushMatrix();
		glTranslated(0, 0, 0);
		glBegin(GL_LINE_STRIP);
		for (int i = 0; i < AllPoint.size(); i++)
		{
			glVertex2f(AllPoint.at(i).x, AllPoint.at(i).y);
			//Sleep(200);
		}
		glEnd();
		glPopMatrix();
	glPopMatrix();
	glutSwapBuffers();
}

GCodeFile::GCodeFile()
{
}


GCodeFile::~GCodeFile()
{
}



string_t split(const string_t &text, char sep) {
	vtstr_t result;
	std::size_t start = 0, end = 0;
	while ((end = text.find(sep, start)) != string_t::npos) {
		result.push_back(text.substr(start, end - start));
		start = end + 1;
	}
	result.push_back(text.substr(start));
	return result.at(0);
}

void RemoveCommand(vtstr_t& str)
{
	//char firstline;
	//string_t strFind1("G1"), strFind2("G4"), strFind3("M");
	//for (int i = 0; i < str.size(); i++)
	//{
	//	std::size_t found1 = str.at(i).find(strFind1);
	//	std::size_t found2 = str.at(i).find(strFind2);
	//	std::size_t found3 = str.at(i).find(strFind3);
	//	if (found1 == string_t::npos && found2 == string_t::npos && found3 == string_t::npos)
	//	{
	//		str.erase(str.begin() + i);
	//		i--;
	//	}
	//}

	//for (int i = 0; i < str.size(); i++)
	//	str.at(i) = split(str.at(i), '(');

	char firstline;
	string_t strFind1("G1");
	for (int i = 0; i < str.size(); i++)
	{
		std::size_t found1 = str.at(i).find(strFind1);

		if (found1 == string_t::npos)
		{
			str.erase(str.begin() + i);
			i--;
		}
	}

	for (int i = 0; i < str.size(); i++)
		str.at(i) = split(str.at(i), '(');
}

vtstr_t split_t(string_t data, string_t token)
{
	vtstr_t output;
	size_t pos = string_t::npos; // size_t to avoid improbable overflow
	do
	{
		pos = data.find(token);
		output.push_back(data.substr(0, pos));
		if (string_t::npos != pos)
			data = data.substr(pos + token.size());
	} while (string_t::npos != pos);
	return output;
}