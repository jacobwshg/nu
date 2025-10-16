/* main.cpp */

//
// Parallelizes a generic "work graph" where work is randomly
// distributed across the vertices in the graph. Naive 
// parallelization works, but doesn't scale. A much more 
// dynamic solution is needed.
// 
// Usage:
//   work [-?] [-t NumThreads]
//
// Author:
//   Jacob Wang
//   Northwestern University
// 
// Initial template:
//   Prof. Joe Hummel
//   Northwestern University
//

#include <iostream>
#include <string>
#include <cstring>
#include <vector>
#include <chrono>
#include <random>
#include <sys/sysinfo.h>
#include <omp.h>

#include <unordered_set>

#include "workgraph.h"

using namespace std;


//
// Globals:
//
static int _numThreads = 1;  // default to sequential execution

//
// Function prototypes:
//
static void ProcessCmdLineArgs(int argc, char* argv[]);


//
// main:
//
int main(int argc, char *argv[])
{
	cout << "** Work Graph Application **" << endl;
	cout << endl;

	//
	// Set defaults, process environment & cmd-line args:
	//
	ProcessCmdLineArgs(argc, argv);

	WorkGraph wg;  // NOTE: wg MUST be created in sequential code

	cout << "Graph size:   " << wg.num_vertices() << " vertices" << endl;
	cout << "Start vertex: " << wg.start_vertex() << endl;
	cout << "# of threads: " << _numThreads << endl;
	cout << endl;

	cout << "working";
	cout.flush();

	/* Neighbors to visit next */
	std::vector<int> fringe {}, fringe_tmp {};

	/* Visited nodes */
	std::unordered_set<int> v_set {};

	std::size_t node_cnt { 0 };

	auto start = chrono::high_resolution_clock::now();

/*
	//
	// TODO: solve all the vertices in the graph. This code just
	// solves the start vertex.
	//
	int start_vertex = wg.start_vertex();

	vector<int> neighbors = wg.do_work(start_vertex);

	//
*/
	int v_start { wg.start_vertex() };
	fringe.emplace_back( v_start );
	v_set.emplace ( v_start );

	while ( !fringe.empty() ) 
	{ 
		#pragma omp parallel for num_threads(_numThreads) schedule(dynamic) 
		for (const int &node : fringe) 
		{
			/* Let threads respectively expand nodes in current fringe
			 */
			std::vector<int> neis {};
			neis = wg.do_work(node);
			#pragma omp critical 
			{
				/* Buffer neighbors for next fringe */
				for (const int &nei : neis)
				{
					if (v_set.find(nei) == v_set.end())
					{
						/* New neighbor;
							push to shared buffer and visited set */
						fringe_tmp.emplace_back(nei);
						v_set.emplace(nei);
					}

					/* Show progress */
					if (++node_cnt % 500 == 0)
					{
						std::cout<<"."<<std::flush;
					}
				}
			}
		}
		/* Replace fringe with buffered new fringe */
		fringe = std::move(fringe_tmp);
	}

	auto stop = chrono::high_resolution_clock::now();
	auto diff = stop - start;
	auto duration = chrono::duration_cast<chrono::milliseconds>(diff);

	cout << endl;
	cout << endl;

	cout << endl;
	cout << "** Done!  Time: " << duration.count() / 1000.0 << " secs" << endl;
	cout << "** Execution complete **" << endl;
	cout << endl;

	return 0;
}


//
// processCmdLineArgs:
//
static void ProcessCmdLineArgs(int argc, char* argv[])
{
	for (int i = 1; i < argc; i++)
	{

		if (strcmp(argv[i], "-?") == 0)  // help:
		{
			cout << "**Usage: work [-?] [-t NumThreads]" << endl << endl;
			exit(0);
		}
		else if ((strcmp(argv[i], "-t") == 0) && (i+1 < argc))  // # of threads:
		{
			i++;
			_numThreads = atoi(argv[i]);
		}
		else  // error: unknown arg
		{
			cout << "**Unknown argument: '" << argv[i] << "'" << endl;
			cout << "**Usage: work [-?] [-t NumThreads]" << endl << endl;
			exit(0);
		}

	}//for
}

